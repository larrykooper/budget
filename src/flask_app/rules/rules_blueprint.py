from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from src.adapters.larry_repository import LarryRepository
from src.models.category_rule import CategoryRule

bp = Blueprint('rules', __name__, url_prefix='/rules')

@bp.route('/', methods=['GET', 'POST'])
def rules_home():
    repo = LarryRepository()
    if request.method == 'GET':
        categories = repo.get_all_categories()
        return render_template('rules/home.html', categories=categories)
    if request.method == 'POST':
        term = request.form['term']
        category_id = request.form['category']
        rule_type_id = request.form['rule-type']
        look_back = request.form['look-back']
        rule = CategoryRule(term, category_id, rule_type_id)
        success = repo.add_categorization_rule(rule)
        if success:
            flash("New categorization rule saved.")
            return redirect(url_for('homepage'))
        else:
            error = "Something went wrong."
            return render_template('rules/', error=error)

