from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import sqlite3
import fastbook
fastbook.setup_book()
from fastai.vision.all import *

DATABASE = 'images.db'

app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
path = Path('static')

learn_inf = load_learner(path('static')/export.pkl)


app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        #flash(filename)
        #save in the db
        con = sqlite3.connect(DATABASE,check_same_thread=False)
        cur = con.cursor()

        cur.execute("INSERT INTO images (image_file) VALUES (?)", (str(filename),))
        con.commit()
        con.close()

        pred,pred_idx,probs = learn_inf.predict(img)
        flash(f'Prediction: {pred_word}; Probability: {probs[pred_idx]:.04f}')
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)

    else:
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

