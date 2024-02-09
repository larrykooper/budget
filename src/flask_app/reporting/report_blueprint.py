from flask import (
    Blueprint, render_template
)

from src.adapters.larry_repository import LarryRepository
from src.authorities.authority_finder import AuthorityFinder

bp = Blueprint('report', __name__, url_prefix='/report')

@bp.route('/', methods=['GET'])
def report_home():
    return render_template('report/home.html')



@bp.route('/spending', methods=['GET'])
def spending():
    repo = LarryRepository()
     # Query the database for what we need to report    

    line_items = repo.get()  
    line_items_translated = translate_ids_to_names(line_items)    
    

    return render_template('report/spending.html', line_items=line_items_translated)

def translate_ids_to_names(line_items: list):
    authority_finder = AuthorityFinder()
    for line_item in line_items:
        category_name = authority_finder.authority_display("category", line_item['category_id'])
        line_item['category_name'] = category_name
        transaction_type = authority_finder.authority_display("transaction_type", line_item['transaction_type_id'])
        line_item['transaction_type'] = transaction_type
        account_name = authority_finder.authority_display("account", line_item['account_id'])
        line_item['account_name']= account_name
    return line_items    


 