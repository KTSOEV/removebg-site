from wsgiref.util import request_uri
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image
from pathlib import Path
import time
import os
from threading import Thread

UPLOAD_FOLDER = 'C:/Users/Mernin/Desktop/PythonProjects/removeBG/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'p0o2l3kj5ndienww395'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=remove_bg(file, app.config['UPLOAD_FOLDER']+f'/{filename}')))
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return request.url + url_for('uploaded_file', filename=remove_bg(file, app.config['UPLOAD_FOLDER']+f'/{filename}'))
    return '''wrong data'''

def remove_bg(file, old_file_directory):
    output_path = f'./images/{secure_filename(file.filename)}_output.png'
    img = Image.open(file)
    output_img = remove(img)
    output_img.save(output_path)
    os.remove(old_file_directory)
    Thread(target=clear_cache, args=(output_path,)).start()
    return f'{secure_filename(file.filename)}_output.png'

def clear_cache(path):
    time.sleep(60)
    os.remove(path)

app.run(debug = True)