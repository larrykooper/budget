from flask import (
    Blueprint, jsonify, render_template, request
)

from src.adapters.larry_repository import LarryRepository
from src.authorities.authority_finder import AuthorityFinder
from src.models.category import Category

bp = Blueprint('report', __name__, url_prefix='/report')

@bp.route('/', methods=['GET'])
def report_home():
    return render_template('report/home.html')

@bp.route('/spending', methods=['GET'])
def spending():
    repo = LarryRepository()
     # Query the database for what we need to report
    line_items = repo.get()
    line_items_translated = translate_line_items(line_items)
    categories = Category.categories_json()
    return render_template('report/spending.html', line_items=line_items_translated, categories=categories)

# Called via AJAX
@bp.route('/_update', methods=['POST'])
def update():
    repo = LarryRepository()
    form = request.form
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
    return line_items

def none_to_blank(field):
    if not field:
        return ''
    return field


