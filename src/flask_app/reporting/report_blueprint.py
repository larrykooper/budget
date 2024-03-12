import calendar
import datetime
from flask import (
    Blueprint, jsonify, render_template, request
)

from src.adapters.repositories.authority_repository import AuthorityRepository
from src.adapters.repositories.line_item_repository import LineItemRepository
from src.models.category import Category

bp = Blueprint('report', __name__, url_prefix='/report')

@bp.route('/', methods=['GET'])
def report_home():
    return render_template('report/home.html')

# Spending details by month
@bp.route('/spending', methods=['GET'])
def spending():
    qs = request.query_string
    # If there is no querystring
    if qs.decode('ASCII') == "":
        return render_template('report/month_picker.html', path='spending')
    else:
        year = int(request.args.get('year'))
        month = int(request.args.get('month'))
        if 'sortkey' in request.args:
            sortkey = request.args.get('sortkey')
        else:
            sortkey = "li.transaction_date"
        if 'direction' in request.args:
            sort_direction = request.args.get('direction')
        else:
            sort_direction  = "asc"
        sortspec = sortkey.split(".")
        sort_table = sortspec[0]
        sort_column = sortspec[1]
        start_date, end_date = get_start_end(year, month)
        line_item_repo = LineItemRepository()
        # Query the database for what we need to report
        line_items = line_item_repo.get_for_spending_report(start_date, end_date, sort_column, sort_direction, sort_table)
        line_items_translated = translate_line_items(line_items)
        categories = Category.categories_json()
        return render_template('report/spending.html',
            line_items=line_items_translated,
            categories=categories,
            year=year,
            month=month,
            sortkey=sortkey,
            sort_direction=sort_direction
        )

# Spending by category per month
@bp.route('/spendingcat', methods=['GET'])
def spendingcat():
    qs = request.query_string
    # If there is no querystring
    if qs.decode('ASCII') == "":
        return render_template('report/month_picker.html', path='spendingcat')
    else:
        # There is a querystring
        year = int(request.args.get('year'))
        month = int(request.args.get('month'))
        month_name = calendar.month_name[month]
        start_date, end_date = get_start_end(year, month)
        line_item_repo = LineItemRepository()
        categories = line_item_repo.get_for_spending_by_cat(start_date, end_date)
        return render_template('report/spendingcat.html',
            categories = categories,
            year=year,
            month=month,
            month_name=month_name
        )

# Used for in-place editing -- called via AJAX
@bp.route('/_update', methods=['POST'])
def update():
    line_item_repo = LineItemRepository()
    form = request.form
    if form['action'] == 'delete':
        line_item_repo.delete_line_item(form['id'])
    elif form['action'] == 'edit':
        if 'comment' in form:
            line_item_repo.update_comment(form['comment'], form['id'])
        if 'category' in form:
            line_item_repo.update_category(form['category'], form['id'])
    return jsonify("foo")


def translate_line_items(line_items: list[dict]) -> list[dict]:
    """
    translate_line_items converts the IDs of dimension tables to their names,
    so they can be displayed on the front-end
    """
    authority_finder = AuthorityRepository()
    for line_item in line_items:
        line_item['check_number'] = none_to_blank(line_item['check_number'])
        line_item['type_detail_id'] = none_to_blank(line_item['type_detail_id'])
        line_item['comment'] = none_to_blank(line_item['comment'])

        # translate IDs to Names
        category_name = authority_finder.authority_display("category", line_item['category_id'])
        line_item['category_name'] = category_name
        transaction_type = authority_finder.authority_display("transaction_type", line_item['transaction_type_id'])
        line_item['transaction_type'] = transaction_type
        account_name = authority_finder.authority_display("account", line_item['account_id'])
        line_item['account_name']= account_name
        if line_item['type_detail_id']:
            type_detail_name = authority_finder.authority_display("type_detail", line_item['type_detail_id'])
        else:
            type_detail_name = ""
        line_item['type_detail_name'] = type_detail_name
    return line_items

def none_to_blank(field):
    if not field:
        return ''
    return field

def get_start_end(year: int, month: int) -> tuple[datetime.date, datetime.date]:
    days_in_month = calendar.monthrange(year, month)[1]
    start = datetime.date(year, month, 1)
    end = datetime.date(year, month, days_in_month)
    return start, end

