import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import src.flask_app.ingesting.ingest_file as ingest_file

ALLOWED_EXTENSIONS = {'csv', 'CSV'}
app_root = os.environ['PYTHONPATH']
UPLOAD_FOLDER = f"{app_root}/uploaded_files"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(request):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # ingest the file
            ingest_file.ingest_file(filename)
