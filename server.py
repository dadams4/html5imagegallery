import os
import psycopg2
import psycopg2.extras

from flask import Flask, render_template, request, redirect, flash
from flask_uploads import UploadSet, configure_uploads
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/Uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOADS_DEFAULT_DEST = "/home/ubuntu/workspace/ImageGallery/static/Upload"

files = UploadSet('files', ("png", "jpg", "jpeg"))

app = Flask (__name__)
app.secretkey = os.urandom(24).encode('hex')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADS_DEFAULT_DEST'] = UPLOADS_DEFAULT_DEST


 
configure_uploads(app, files)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods = ['GET'])
def uploadPics():
    
    return render_template("upload.html")

@app.route('/uploadsuccess', methods = ['POST'])
def uploadSuccess():
    
    if request.method == 'POST':
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            
            flash('No file selected')
            return redirect(request.url)
            
        try: 
            
            if not allowed_file(file.filename):
                
                return redirect(request.url)
        except:
            
            flash('Wrong file type.  Only .png and .jpg are supported')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       
    pictureDictionary = os.listdir('static/Uploads/')
    pictureDictionary = ['static/Uploads/' + file for file in pictureDictionary]
            
    return render_template("index.html", pictureDictionary = pictureDictionary)
    
@app.route('/', methods = ['GET', 'POST'])
def homePage():
    
    pictureDictionary = os.listdir('static/Uploads/')
    pictureDictionary = ['static/Uploads/' + file for file in pictureDictionary]
        
    return render_template("index.html", pictureDictionary = pictureDictionary)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0',port=8080, debug = True)