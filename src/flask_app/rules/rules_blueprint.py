from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from src.adapters.repositories.category_repository import CategoryRepository
from src.adapters.repositories.category_rule_repository import CategoryRuleRepository
from src.adapters.repositories.line_item_repository import LineItemRepository
from src.models.category_rule import CategoryRule
from src.models.rule_type import RuleType

bp = Blueprint('rules', __name__, url_prefix='/rules')

@bp.route('/', methods=['GET', 'POST'])
def rules_home():
    return render_template('rules/home.html')

@bp.route('/list', methods=['GET'])
def list():
    category_rule_repo = CategoryRuleRepository()
    rules = category_rule_repo.list_rules()
    return render_template('rules/list.html',
        rules=rules
    )


@bp.route('/add_rule', methods=['GET', 'POST'])
def add_rule():
    if request.method == 'GET':
        category_repo = CategoryRepository()
        categories = category_repo.get_all_categories()
        return render_template('rules/add_rule.html', categories=categories)
    if request.method == 'POST':
        category_rule_repo = CategoryRuleRepository()
        # Normalize term to lowercase
        term = request.form['term'].lower()
        category_id = request.form['category']
        rule_type_id = request.form['rule-type']
        look_back = request.form['look-back']
        rule = CategoryRule(term, category_id, rule_type_id)
        success = category_rule_repo.add_categorization_rule(rule)
        rule_type_id_num = int(rule_type_id)
        if success and (look_back == 'yes'):
            line_item_repo = LineItemRepository()
            if rule_type_id_num == RuleType.STARTS_WITH.value:
                line_item_repo.recategorize_existing_line_items_starts_with(category_id, term)
                flash("Existing line items recategorized.")
            if rule_type_id_num == RuleType.CONTAINS.value:
                line_item_repo.recategorize_existing_line_items_contains(category_id, term)
                flash("Existing line items recategorized.")
        if success:
            flash("New categorization rule saved.")
            return redirect(url_for('homepage'))
        else:
            error = "Something went wrong."
            return render_template('rules/', error=error)

