from flask import (
    Blueprint, render_template, request
)
from werkzeug.datastructures import ImmutableMultiDict

from src.adapters.repositories.line_item.line_item_select import LineItemSelect
from src.adapters.repositories.line_item.line_item_write import LineItemWrite
from src.flask_app.utils.utils import Utils

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
        breakpoint()
        process_reimbursements(request.form)
        return render_template('medres/bankdeps.html')


def process_reimbursements(form: ImmutableMultiDict) -> None:
    deposits_to_update = []
    for key in form.keys():
        id = parse_id(key)
        deposits_to_update.append(id)
    line_item_write = LineItemWrite()
    line_item_write.update_is_medical_reimbursement(deposits_to_update)
    line_item_write.create_synthetic_transactions(deposits_to_update)


def parse_id(key) -> str:
    # key looks like 'item20901'
    # strip out 'item'
    return key[4:]




