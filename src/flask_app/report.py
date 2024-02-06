

from flask import (
    Blueprint, render_template
)

from src.adapters.larry_repository import LarryRepository


bp = Blueprint('report', __name__, url_prefix='/report')

@bp.route('/', methods=['GET'])
def report_home():
    return render_template('report/home.html')



@bp.route('/spending', methods=['GET'])
def spending():
    repo = LarryRepository()
     # Query the database for what we need to report    

    line_items = repo.get()   
    #breakpoint() 

    return render_template('report/spending.html', line_items=line_items)

 