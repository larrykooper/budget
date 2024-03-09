from flask import (
    Blueprint, render_template, request
)
import src.flask_app.ingesting.upload_file as upload_file

bp = Blueprint('ingest', __name__, url_prefix='/ingest')

@bp.route('/', methods=['GET'])
def ingest_home():
    return render_template('ingest/home.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('ingest/upload.html')
    if request.method == 'POST':
        result = upload_file.upload_file(request)
    if result == "SUCCESS":
        return render_template('ingest/upload_success.html')


