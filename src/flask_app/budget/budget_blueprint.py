from flask import (
    Blueprint, render_template, request
)

from src.adapters.repositories.category_repository import CategoryRepository

bp = Blueprint('budget', __name__, url_prefix='/budget')

@bp.route('/', methods=['GET'])
def budget_home():
    category_repo = CategoryRepository()
    categories = category_repo.get_all_categories()
    return render_template('budget/home.html', categories=categories)


# Used for in-place editing -- called via AJAX
@bp.route('/_updatebudget', methods=['POST'])
def update():
    category_repo = CategoryRepository()
    form = request.form
    if form['action'] == 'edit':
        if 'budget_per_month' in form:
            category_repo.update_budget_per_month(form['budget_per_month'], form['id'])
    return "SUCCESS"

