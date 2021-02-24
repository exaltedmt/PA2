#!/usr/bin/env python3

"""
Name: Royce Harley
ID: 811778401
Subject: CSCI4795, In Kee Kim
Title: PA2
"""

# Thanks to: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/ 
# ...and: https://docs.python.org/3/library/subprocess.html

from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
import os
import random
from werkzeug.utils import secure_filename
import shlex, subprocess

# To put us in location with the python.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'cc', 'py', 'html', 'css'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""
command_line = input()
# /bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
args = shlex.split(command_line)
print(args)
# ['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
p = subprocess.call(args, shell=True) # Success!
    """

def grader():
    subprocess.call("rm -f ./a.out", shell=True)
    retcode = subprocess.call("/usr/bin/g++ uploads/walk.cc", shell=True)
    print(retcode)

    score = None 
    if retcode:
        print("Failed to compile walk.cc!")
        exit
    else: 
        subprocess.call("rm -f ./output", shell=True)
        retcode = subprocess.call("./test.sh", shell=True)

        score = str(retcode)
        print("Score: " + str(retcode) + " out of 2 correct.")
        print("*************Original submission*************")

        with open('uploads/walk.cc','r') as fs:
            print(fs.read())
        
    return score

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # To retrieve the file uploaded.
            send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)               
           
            score = grader()
            return render_template("result.html", score=score, filename=filename)
            # return redirect(url_for('result',      filename=filename))
    
    # Display the html on homepage.
    return render_template("index.html")

"""
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
"""                       

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



