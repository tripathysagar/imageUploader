from distutils.command.config import config
from urllib import response
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from pred import predict_image_from_file
#from temp import fun
from PIL import Image


#DATABASE = 'F_images.sqlite'

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'



app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    #print('Request for index page received')
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
        filename = secure_filename(file.filename)   # get the file name 
        
        photo = Image.open(file)
        photo = photo.resize((224, 224))

        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print(photo.size)
        #print(filename)



        #flash('Image successfully uploaded and displayed below')
        #resp = predict_image_from_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = predict_image_from_file(photo)
        
        confidence = round(resp['confidence'] * 100, 3)
        
        
        flash('Prediction: ' + resp['prediction'] + ' with confidence ' + str(confidence ) + '%')
        
        #print('uploaded image')
        return render_template('index.html', filename=filename)

    else:
        #print('not able to upload image')
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    print('render image')
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)