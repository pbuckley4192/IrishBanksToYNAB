import csv
import sys
import os
from flask import Flask, render_template, flash, request, redirect, url_for,send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['csv'])

APP = Flask("BankConverter")
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
OUTPUT_FOLDER=UPLOAD_FOLDER+'/converted.csv'

# Redirect STDOut
sys.stdout = open(OUTPUT_FOLDER, 'w')

def convert(file_uploaded):
    # Open CSV File
    file = open(file_uploaded, mode='r')
    csv_file = csv.DictReader(file)

    # Print Header
    print("date;paymode;info;payee;memo;amount;category;tags")

    # Parse out the statment
    for row in csv_file:
            
            # Description of the transaction
            description=""

            # Was it Point of Sale?
            POS = 0
        
            # Amount of transaction
            amount = 0

            # Ignore invalid lines
            if(not len(row["Date"])):
                continue
            

            # Parse out the POS details
            if str(row["Details"]).startswith("POS"):
                    subs = str(row["Details"]).split(" ", 1)
                    POS = 6
                    description = subs[1].lstrip()
            else:
                    description = row["Details"].lstrip()


            # Convert from Debit/Credit to abs amount
            if(not len(row["Credit"])):
                amount= 0 - float(row["Debit"])
            else:
                amount= row["Credit"]

            # Print to homebank format
            print(row["Date"]+";"+str(POS)+";;"+ description+";;"+str(amount)+";;")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@APP.route('/', methods=['GET', 'POST'])
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
            file.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
            convert(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
            return send_from_directory(directory=APP.config['UPLOAD_FOLDER'], filename='converted.csv', as_attachment=True)

    return render_template('index.html')


APP.run()