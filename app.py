# Importing libraries
from flask import Flask, flash, request, redirect, url_for
import io
import lzip
import os
import numpy as np
from PIL import Image
from flask import Flask, jsonify, request
import h5py
from py import code
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, url_for, request


UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'}

def prepare_image(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((224, 224))
    img = np.array(img)
    img = np.expand_dims(img, 0)
    return img

save_path = './numpy.hdf5' # Path to HDF5 file

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/home', methods=['GET', 'POST'])
def upload_file():
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           ##hf = h5py.File(save_path, 'a') # open a hdf5 file
           # dset = hf.create_dataset('dataset15', data=img ,compression = 'gzip',compression_opts=9 )  # write the data to hdf5 file
           # hf.close()  # close the hdf5 file
            #return jsonify("HDF5 file size in Bytes ->{}".format(os.path.getsize(save_path)))
            return jsonify("File size before compression in bytes ->{}".format(os.path.getsize(filename)),"HDF5 file size in bytes -> {}".format(os.path.getsize(save_path)))
    return render_template('home.html')
            
@app.route('/file', methods=['POST','GET']) # Endpoint for accepting a file
def infer_image():
    if 'file' not in request.files:
        return "Please try again. The file doesn't exist"
    
    file = request.files.get('file')

    if not file:
        return "No file uploaded"

    #img_bytes = file.read()
    #img = prepare_image(img_bytes)
    hf = h5py.File(save_path, 'a') # open a hdf5 file
    main_grp = hf.create_group('Base_Group5')
    sub_grp = main_grp.create_group('Sub_Group5')

    dataset1 =main_grp.create_dataset('dataset16', data=file ,compression = 'gzip',compression_opts=9 )  # write the data to hdf5 file
    dataset2 = sub_grp.create_dataset('dataset16',data=file,compression='gzip',compression_opts=9) # write the data to hdf5 file
    hf.close()  # close the hdf5 file


    return jsonify("HDF5 file size in Bytes ->{}".format(os.path.getsize(save_path)))
    


# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin': # Username and password set to default admin
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('upload_file'))
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')