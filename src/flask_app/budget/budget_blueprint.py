from flask import (
    Blueprint, render_template
)

from src.adapters.repositories.category_repository import CategoryRepository

bp = Blueprint('budget', __name__, url_prefix='/budget')

@bp.route('/', methods=['GET'])
def budget_home():
    category_repo = CategoryRepository()
    categories = category_repo.get_all_categories()
    return render_template('budget/home.html', categories=categories)
