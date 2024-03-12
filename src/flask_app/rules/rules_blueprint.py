from flask import (
    Blueprint, render_template
)

from src.adapters.larry_repository import LarryRepository

bp = Blueprint('rules', __name__, url_prefix='/rules')

@bp.route('/', methods=['GET'])
def rules_home():
    repo = LarryRepository()
    categories = repo.get_all_categories()
    return render_template('rules/home.html')

