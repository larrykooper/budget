from flask import (
    Blueprint, jsonify, render_template, request
)

from src.adapters.repositories.category_repository import CategoryRepository

bp = Blueprint('budget', __name__, url_prefix='/budget')

@bp.route('/', methods=['GET'])
@bp.route('/home', methods=['GET'])
def home():
    """
    Lists all the categories, the amounts budgeted, and the money-saving steps
    """
    category_repo = CategoryRepository()
    if 'sortkey' in request.args:
            sortkey = request.args.get('sortkey')
    else:
        sortkey = "name"
    if 'direction' in request.args:
        sort_direction = request.args.get('direction')
    else:
        sort_direction  = "asc"
    sort_column = sortkey
    categories = category_repo.get_all_categories(sort_column, sort_direction)
    # total_budget is the sum over all categories of budget
    total_budget = category_repo.get_total_budget()
    return render_template('budget/home.html',
        total_budget=total_budget,
        categories=categories,
        sortkey=sortkey,
        sort_direction=sort_direction,
    )


# Used for in-place editing -- called via AJAX
@bp.route('/_updatebudget', methods=['POST'])
def update():
    category_repo = CategoryRepository()
    form = request.form
    if form['action'] == 'edit':
        if 'budget_per_month' in form:
            wanted_budget = form['budget_per_month'].strip()
            budget_no_commas = wanted_budget.replace(",", "")
            category_repo.update_budget_per_month(budget_no_commas, form['id'])
            total_budget = category_repo.get_total_budget()
        if 'money_saving_steps' in form:
            category_repo.update_money_saving_steps(form['money_saving_steps'], form['id'])
    return jsonify(total_budget)

