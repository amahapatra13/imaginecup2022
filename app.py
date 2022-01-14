import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024 * 1024

# @app.route("/", methods=["GET","POST"])
# def home():
#     if request.method == "POST":
#         print(request.form)
#     return render_template("index.html")


@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_video():
    print(request.files)
    if 'rfile' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    rfile = request.files['rfile']
    yfile = request.files['yfile']
    print(rfile,yfile)
    
    if rfile.filename == '' and yfile.filename == '':
        flash('upload both the files')
        return redirect(request.url)
    else:
        rfilename = secure_filename(rfile.filename)
        yfilename = secure_filename(yfile.filename)
        rfile.save(os.path.join(app.config['UPLOAD_FOLDER'], rfilename))
        yfile.save(os.path.join(app.config['UPLOAD_FOLDER'], yfilename))
        filename = [rfilename,yfilename]
        flash('Videos judged succesfully and results are displayed below')
        return render_template('upload.html', filename=filename)

@app.route('/display/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
    rfile = 'uploads/' + filename[0]
    yfile = 'uploads/' + filename[1]
    filenames = {'1':rfile,'2':yfile}
    return redirect(url_for('static', filename=filenames), code=301)

if __name__ == "__main__":
    app.run()