""" Author: Paul Buckley
Purpose: Flask App to Convert Bank of Ireland and AIB Statments to YNAB Format. """

import csv
import os

from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory)
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['csv'])

APP = Flask("Bank Statement Converter")
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
OUTPUT_FILE = UPLOAD_FOLDER+'/converted.csv'


def convert(file_uploaded):
    """ Convert the Uploaded File to YNAB Format"""

    # Open Input CSV File
    input_file = open(file_uploaded, mode='r')
    csv_file = csv.DictReader(input_file)

    # Remove Existing File
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    # Open Output file
    output = open(OUTPUT_FILE, 'w')

    # Write Header
    output.write("date;paymode;info;payee;memo;amount;category;tags\n")

    # Parse out the Bank Statment
    for row in csv_file:
        # Detect Bank
        if csv_file.fieldnames[0] != "Posted Account":
            boi_line_parser(row, output)
        else:
            aib_line_parser(row, output)

    # Clean Up
    output.close()
    input_file.close()


def boi_line_parser(row, output):
    """ Parse Bank of Ireland Statment Lines to YNAB Format"""

    # Description of the transaction
    description = ""

    # Was it Point of Sale?
    pos = 0

    # Amount of transaction
    amount = 0

    # Ignore invalid lines
    if not row["Date"]:
        return

    # Parse out the POS details
    if str(row["Details"]).startswith("POS"):
        subs = str(row["Details"]).split(" ", 1)
        pos = 6
        description = subs[1].lstrip()
    else:
        description = row["Details"].lstrip()


    # Convert from Debit/Credit to abs amount
    if not row["Credit"]:
        amount = 0 - float(row["Debit"])
    else:
        amount = row["Credit"]

    # Print to YNAB format
    output.write(row["Date"]+";"+str(pos)+";;"+ description+";;"+str(amount)+";;\n")

def aib_line_parser(row, output):
    """ Convert the BOI Input Row Values to YNAB Format"""

    # Ignore invalid lines
    if not row[" Posted Transactions Date"]:
        return

    # Description of the transaction
    description = row[" Description"].lstrip()

    # Was it Point of Sale?
    pos = 0

    # Amount of transaction
    amount = 0

    # Convert from Debit/Credit to abs amount
    if not row[" Credit Amount"]:
        if not row[" Debit Amount"]:
            return
        amount = 0 - float(row[" Debit Amount"])
    else:
        amount = row[" Credit Amount"]

    # Print to YNAB format
    output.write(row[" Posted Transactions Date"].replace("/", "-") \
        +";"+str(pos)+";;"+ description+";;"+str(amount)+";;\n")


def allowed_file(filename):
    """ Determine the Allowed File Uploads """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@APP.route('/', methods=['GET', 'POST'])
def upload_file():
    """ Flask App to Take Uploaded File and Push Converted File """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        input_file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if input_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if input_file and allowed_file(input_file.filename):
            filename = secure_filename(input_file.filename)
            input_file.save(os.path.join(UPLOAD_FOLDER, filename))
            convert(os.path.join(UPLOAD_FOLDER, filename))
            return send_from_directory(directory=UPLOAD_FOLDER, \
                filename='converted.csv', as_attachment=True)

    return render_template('index.html')

if __name__ == "__main__":
    APP.run(host='0.0.0.0')
