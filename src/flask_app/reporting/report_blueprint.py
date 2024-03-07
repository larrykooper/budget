import calendar
import datetime
from flask import (
    Blueprint, jsonify, render_template, request
)

from src.adapters.larry_repository import LarryRepository
from src.authorities.authority_finder import AuthorityFinder
from src.models.persistence.category import Category

bp = Blueprint('report', __name__, url_prefix='/report')

@bp.route('/', methods=['GET'])
def report_home():
    return render_template('report/home.html')

@bp.route('/spending', methods=['GET'])
def spending():
    qs = request.query_string
    if qs.decode('ASCII') == "":
        return render_template('report/month_picker.html')
    else:
        year = int(request.args.get('year'))
        month = int(request.args.get('month'))
        start_date, end_date = get_start_end(year, month)
        repo = LarryRepository()
        # Query the database for what we need to report
        line_items = repo.get_by_date_range(start_date, end_date)
        line_items_translated = translate_line_items(line_items)
        categories = Category.categories_json()
        return render_template('report/spending.html', line_items=line_items_translated, categories=categories)

# Called via AJAX
@bp.route('/_update', methods=['POST'])
def update():
    repo = LarryRepository()
    form = request.form
    if form['action'] == 'delete':
        repo.delete_line_item(form['id'])
    elif form['action'] == 'edit':
        if 'comment' in form:
            repo.update_comment(form['comment'], form['id'])
        if 'category' in form:
            repo.update_category(form['category'], form['id'])
    return jsonify("foo")


def translate_line_items(line_items: list[dict]) -> list[dict]:
    authority_finder = AuthorityFinder()
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

