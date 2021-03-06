import os
from datetime import datetime

from flask import (Flask, render_template, request, send_file,
                   send_from_directory)
from werkzeug.utils import secure_filename

from functions.main import main

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    now = datetime.now()
                    time_string = now.strftime("%d%m%Y%H%M%S%F")
                    filename = time_string + secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    main(filename)
                    return send_file(os.path.splitext(filename)[0] + '.docx')


if __name__ == "__main__":
    app.run()
