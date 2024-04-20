from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.datastructures import ImmutableMultiDict

from src.adapters.repositories.authority_repository import AuthorityRepository
from src.adapters.repositories.line_item.line_item_select import LineItemSelect
from src.adapters.repositories.line_item.line_item_write import LineItemWrite
from src.adapters.repositories.synthetic_line_item_repo import SyntheticLineItemRepo
from src.flask_app.utils.utils import Utils
from src.models.input_field_types.input_field import InputField
from src.models.line_item import LineItem
from src.models.synthetic_line_item import SyntheticLineItem

bp = Blueprint('medres', __name__, url_prefix='/medres')


# medres means medical reimbursement
@bp.route('/', methods=['GET'])
def medres_home():
    return render_template('medres/home.html')


@bp.route('/identify', methods=['GET', 'POST'])
def identify():
    if request.method == 'GET':
        year = int(request.args.get('year'))
        start_of_year, end_of_year = Utils.get_year_start_end(year)
        line_item_select = LineItemSelect()
        bank_deposits = line_item_select.get_bank_deposits(start_of_year, end_of_year)
        return render_template('medres/bankdeps.html',
            bank_deposits=bank_deposits
        )
    if request.method == 'POST':
        process_reimbursements(request.form)
        flash("Medical reimbursements have been processed successfully.")
        return redirect(url_for('homepage'))


def process_reimbursements(form: ImmutableMultiDict) -> None:
    deposits_to_update = []
    for key in form.keys():
        id = parse_id(key)
        deposits_to_update.append(id)
    line_item_write = LineItemWrite()

    # Mark the line_items to be is_medical_reimbursement to true
    line_item_write.update_is_medical_reimbursement(deposits_to_update)

    # For each medical reimbursement, create a synthetic transaaction
    create_synthetic_transactions(deposits_to_update)


def parse_id(key) -> str:
    # key looks like 'item20901'
    # strip out 'item'
    return key[4:]

def create_synthetic_transactions(deposits_to_update: list):
    """
    Create a new synthetic transaction for each reimbursement.
    transaction_date: Date of the deposit
    post_date: Date of the deposit
    description: "Medical Reimbursement"
    amount: The deposit amount, times -1
    category_id: Doctor
    transaction_type: credit
    account_id: id for Checking
    check_number: None
    type_detail: None
    comment: None
    show_on_spending_report: true
    is_medical_reimbursement: false (that's only for deposits)
    is_synthetic: true

    Also create a row in synthetic_line_item.
    """
    line_item_write = LineItemWrite()
    line_item_select = LineItemSelect()
    authority_repo = AuthorityRepository()
    synthetic_line_item_repo = SyntheticLineItemRepo()
    account = 'Checking'
    description_wanted = "Medical Reimbursement"
    category_wanted = "Doctor"
    transaction_type_wanted = "credit"
    category_field = InputField.instantiate_input_field("CATEGORY")
    kwargs = {'description': description_wanted}
    category_id = category_field.what_to_persist(category_wanted, **kwargs)['category_id']
    transaction_type_field = InputField.instantiate_input_field("TRANSACTION_TYPE")
    transaction_type_id = transaction_type_field.what_to_persist(transaction_type_wanted)['transaction_type_id']
    account_id = authority_repo.authority_lookup("account", account)
    for line_item_id in deposits_to_update:
        # Add a synthetic transaction to line_item
        # reimbursement is the ID of the deposit's line item (as string)
        reimbursement = line_item_select.get_for_synth_trans(line_item_id)
        line_item_dict = {}
        line_item_dict['transaction_date'] = reimbursement['transaction_date']
        line_item_dict['post_date'] = reimbursement['transaction_date']
        line_item_dict['description'] = description_wanted
        line_item_dict['amount'] = -1 * reimbursement['amount']
        line_item_dict['category_id'] = category_id
        line_item_dict['transaction_type_id'] = transaction_type_id
        line_item_dict['account_id'] = account_id
        line_item_dict['show_on_spending_report'] = 't'
        line_item_dict['is_synthetic'] = 't'
        line_item = LineItem(**line_item_dict)
        new_line_item_key = line_item_write.add_line_item(line_item)
        # Add a row to synthetic_line_item
        synthetic_line_item = SyntheticLineItem(new_line_item_key, line_item_id)
        synthetic_line_item_repo.add_synthetic_line_item(synthetic_line_item)
