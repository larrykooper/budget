import calendar
import datetime
from decimal import Decimal
from flask import (
    Blueprint, render_template, request
)

from src.adapters.repositories.authority_repository import AuthorityRepository
from src.adapters.repositories.category_repository import CategoryRepository
from src.adapters.repositories.line_item.line_item_select import LineItemSelect
from src.adapters.repositories.line_item.line_item_write import LineItemWrite
from src.flask_app.utils.utils import Utils
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
        line_item_select = LineItemSelect()
        # Query the database for what we need to report
        line_items = line_item_select.get_for_spending_report(start_date, end_date, sort_column, sort_direction, sort_table)
        line_items_translated = translate_line_items(line_items)
        categories = Category.categories_for_select()
        total = line_item_select.total_spending_per_month(start_date, end_date)
        lm_year, lm_month, nm_year, nm_month = get_months_nav(month, year)
        return render_template('report/spending.html',
            line_items=line_items_translated,
            categories=categories,
            year=year,
            month=month,
            sortkey=sortkey,
            sort_direction=sort_direction,
            month_name = month_name,
            total=total,
            lm_year=lm_year,
            lm_month=lm_month,
            nm_year=nm_year,
            nm_month=nm_month
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
        start_of_year, end_of_year = Utils.get_year_start_end(year)
        denominator = get_budyear_denominator(year)
        end_of_spend_period = get_end_of_spend_period(denominator, year)
        category_repo = CategoryRepository()
        line_item_select = LineItemSelect()
        if 'sortkey' in request.args:
            sortkey = request.args.get('sortkey')
        else:
            sortkey = "name"
        if 'direction' in request.args:
            sort_direction = request.args.get('direction')
        else:
            sort_direction  = "asc"
        sort_column = sortkey
        categories = category_repo.get_for_budyear(
            start_of_year,
            end_of_year,
            end_of_spend_period,
            sort_column,
            sort_direction)
        # Do business logic per category
        for category in categories:
            if category['budget_per_year'] is None:
                category['budget_per_year'] = 0
            if category['tot_spend_year'] is None:
                category['tot_spend_year'] = 0
            category['left_per_year'] = category['budget_per_year'] - category['tot_spend_year']
            category['av_spend_per_month'] = category['tot_spend_year'] / denominator
        # total_budget is the sum of budgeted over all categories
        total_budget = category_repo.get_total_budget()
        budget_per_year = 12 * total_budget['sum']
        totals = line_item_select.total_spending_per_month_for_year(start_of_year, end_of_year)
        avg_spend_per_month, left_for_year = get_total_line_data(totals, denominator, budget_per_year)
        totals_zero_padded = zero_pad(totals, denominator)
        return render_template('report/budyear.html',
            categories=categories,
            year=year,
            totals=totals_zero_padded,
            total_budget=total_budget,
            av_per_month=avg_spend_per_month,
            sortkey=sortkey,
            sort_direction=sort_direction,
            budget_per_year=budget_per_year,
            left_for_year=left_for_year
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
        line_item_select = LineItemSelect()
        categories = line_item_select.get_for_spending_by_cat(start_date, end_date, sortkey, sort_direction)
        total = line_item_select.total_spending_per_month(start_date, end_date)
        return render_template('report/spendingcat.html',
            categories = categories,
            year=year,
            month=month,
            sortkey=sortkey,
            sort_direction = sort_direction,
            month_name=month_name,
            total=total
        )

# spending for a given category for the entire year
@bp.route('/spending_cat_year', methods=['GET'])
def spending_cat_year():
    line_item_select = LineItemSelect()
    year = int(request.args.get('year'))
    category = request.args.get('category')
    start_of_year, end_of_year = Utils.get_year_start_end(year)
    line_items = line_item_select.get_spending_cat_year(category, start_of_year, end_of_year)
    total = line_item_select.total_spending_cat_per_year(category, start_of_year, end_of_year)
    return render_template('report/spending_cat_year.html',
        line_items=line_items,
        total=total,
        year=year
    )

# Used for in-place editing -- called via AJAX
#  form['category'] is the category ID number
@bp.route('/_update', methods=['POST'])
def update():
    line_item_write = LineItemWrite()
    form = request.form
    if form['action'] == 'delete':
        line_item_write.delete_line_item(form['id'])
    elif form['action'] == 'edit':
        if 'comment' in form:
            line_item_write.update_comment(form['comment'], form['id'])
        if 'category' in form:
            line_item_write.update_category(form['category'], form['id'])
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

def get_total_line_data(totals: list, denominator: int, budget_per_year: Decimal) -> tuple[Decimal, Decimal]:
    sum = 0
    for total in totals[:denominator]:
        sum += total['sum']
    avg_spend_per_month = sum/denominator
    left_for_year = budget_per_year - sum
    return avg_spend_per_month, left_for_year

def zero_pad(totals: list, denominator: int) -> list:
    """
    Add zeros for all future months so the display puts things in the right columns
    Denominator should be equal to length of list
    """
    for i in range(denominator+1, 12):
        totals.append({'sum': Decimal(0.00)})
    return totals


def get_budyear_denominator(year: int) -> int:
    """
    If the year is a prior year return 12
    If the year is current year, return the number of the current month minus 1
    We exclude the current month from the average because its spending number is not
    comparable to other months
    """
    today = datetime.date.today()
    current_month = today.month
    current_year = today.year
    if year < current_year:
        return 12
    else:
        deno = current_month - 1
        return 1 if deno == 0 else deno


def get_end_of_spend_period(denominator: int, year_requested: int) -> datetime.date:
    """
    For the average spending to be meaningful, we
    want the numerator of it to end at the end of last month
    """
    days_in_month = calendar.monthrange(year_requested, denominator)[1]
    return datetime.date(year_requested, denominator, days_in_month)


def get_months_nav(month: int, year: int) -> tuple[int, int, int, int]:
    """
    Return last month and next month
    """
    if month == 1:
        lm_month = 12
        lm_year = year - 1
        nm_month = 2
        nm_year = year
    elif month == 12:
        lm_month = 11
        lm_year = year
        nm_month = 1
        nm_year = year + 1
    else:
        lm_month = month - 1
        lm_year = year
        nm_month = month + 1
        nm_year = year
    return lm_year, lm_month, nm_year, nm_month
