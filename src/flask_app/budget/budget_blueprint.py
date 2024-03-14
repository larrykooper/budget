from flask import (
    Blueprint, jsonify, render_template, request
)

from src.adapters.repositories.category_repository import CategoryRepository

bp = Blueprint('budget', __name__, url_prefix='/budget')

@bp.route('/', methods=['GET'])
def budget_home():
    """
    Lists all the categories
    """
    category_repo = CategoryRepository()
    categories = category_repo.get_all_categories()
    total_budget = category_repo.get_total_budget()
    return render_template('budget/home.html',
        total_budget=total_budget,
        categories=categories
    )


# Used for in-place editing -- called via AJAX
@bp.route('/_updatebudget', methods=['POST'])
def update():
    category_repo = CategoryRepository()
    form = request.form
    if form['action'] == 'edit':
        if 'budget_per_month' in form:
            category_repo.update_budget_per_month(form['budget_per_month'], form['id'])
            total_budget = category_repo.get_total_budget()
        if 'money_saving_steps' in form:
            category_repo.update_money_saving_steps(form['money_saving_steps'], form['id'])
    return jsonify(total_budget)

