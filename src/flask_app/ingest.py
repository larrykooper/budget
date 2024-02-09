from flask import (
    Blueprint, render_template
)

import src.ingest_file as ingest_file

bp = Blueprint('ingest', __name__, url_prefix='/ingest')

@bp.route('/', methods=['GET'])
def report_home():
    print("in ingest.py calling ingest_file")
    ingest_file.ingest_file()
    return render_template('ingest/home.html')