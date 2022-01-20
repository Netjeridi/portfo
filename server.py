from flask import Flask, render_template, request, redirect
from datetime import date
import csv

app = Flask(__name__)


@app.route('/')
def my_home():
    # render templates will look in a folder called 'templates' for html files,
    # so we need to store the files there
    return render_template('index.html')


# dynamically accept new html files to create new pages
@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f"\n\nDate: {date.today()}\nEmail: {email}\nSubject: {subject}\nMessage: {message}")
    return True


def write_to_csv(data):
    with open('database.csv', newline='',  mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([date.today(), email, subject, message])
    return True


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        data = request.form.to_dict()
        success = write_to_csv(data)
        if success:
            return redirect('submitted.html')
        else:
            return "Something went wrong. Data not submitted."
