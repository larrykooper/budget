import calendar
import datetime
from decimal import Decimal
from flask import (
    Blueprint, jsonify, render_template, request
)

from src.adapters.repositories.authority_repository import AuthorityRepository
from src.adapters.repositories.category_repository import CategoryRepository
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
        month_name = calendar.month_name[month]
        if 'sortkey' in request.args:
            sortkey = request.args.get('sortkey')
        else:
            sortkey = "li.transaction_date"
        if 'direction' in request.args:
            sort_direction = request.args.get('direction')
        else:
            sort_direction  = "desc"
        sortspec = sortkey.split(".")
        sort_table = sortspec[0]
        sort_column = sortspec[1]
        start_date, end_date = get_start_end(year, month)
        line_item_repo = LineItemRepository()
        # Query the database for what we need to report
        line_items = line_item_repo.get_for_spending_report(start_date, end_date, sort_column, sort_direction, sort_table)
        line_items_translated = translate_line_items(line_items)
        categories = Category.categories_for_select()
        total = line_item_repo.total_spending_per_month(start_date, end_date)
        return render_template('report/spending.html',
            line_items=line_items_translated,
            categories=categories,
            year=year,
            month=month,
            sortkey=sortkey,
            sort_direction=sort_direction,
            month_name = month_name,
            total=total
        )

# Budget for year
@bp.route('/budyear', methods=['GET'])
def budyear():
    qs = request.query_string
    # If there is no querystring
    if qs.decode('ASCII') == "":
        return render_template('report/year_picker.html')
    else:
        year = int(request.args.get('year'))
        start_of_year, end_of_year = get_year_start_end(year)
        category_repo = CategoryRepository()
        line_item_repo = LineItemRepository()
        categories = category_repo.get_for_budyear(start_of_year, end_of_year)
        total_budget = category_repo.get_total_budget()
        totals = line_item_repo.total_spending_per_month_for_year(start_of_year, end_of_year)
        denominator = get_budyear_denominator(year)
        avg_spend_per_month = get_avg_spend_per_month(totals)
        return render_template('report/budyear.html',
            categories=categories,
            year=year,
            totals=totals,
            total_budget=total_budget,
            denominator=denominator,
            av_per_month = avg_spend_per_month
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
        if 'sortkey' in request.args:
            sortkey = request.args.get('sortkey')
        else:
            sortkey = "catname"
        if 'direction' in request.args:
            sort_direction = request.args.get('direction')
        else:
            sort_direction  = "asc"
        start_date, end_date = get_start_end(year, month)
        line_item_repo = LineItemRepository()
        categories = line_item_repo.get_for_spending_by_cat(start_date, end_date, sortkey, sort_direction)
        total = line_item_repo.total_spending_per_month(start_date, end_date)
        return render_template('report/spendingcat.html',
            categories = categories,
            year=year,
            month=month,
            sortkey=sortkey,
            sort_direction = sort_direction,
            month_name=month_name,
            total=total
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
    return "SUCCESS"


def translate_line_items(line_items: list[dict]) -> list[dict]:
    """
    translate_line_items converts the IDs of dimension tables to their names,
    so they can be displayed on the front-end
    """
    authority_repo = AuthorityRepository()
    for line_item in line_items:
        line_item['check_number'] = none_to_blank(line_item['check_number'])
        line_item['type_detail_id'] = none_to_blank(line_item['type_detail_id'])
        line_item['comment'] = none_to_blank(line_item['comment'])

        # translate IDs to Names
        transaction_type = authority_repo.authority_display("transaction_type", line_item['transaction_type_id'])
        line_item['transaction_type'] = transaction_type
        if line_item['type_detail_id']:
            type_detail_name = authority_repo.authority_display("type_detail", line_item['type_detail_id'])
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

def get_year_start_end(year: int) -> tuple[datetime.date, datetime.date]:
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    return start, end

def get_budyear_denominator(year: int) -> int:
    """
    If the year is a prior year return 12
    If the year is current year, return the number of the current month
    """
    today = datetime.date.today()
    current_month = today.month
    current_year = today.year
    if year < current_year:
        return 12
    else:
        return current_month

def get_avg_spend_per_month(totals: list) -> Decimal:
    sum = 0
    for total in totals:
        sum += total['sum']
    return sum/12
