from flask import Flask, render_template, url_for, request, redirect
import csv
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name, favicon=url_for('static', filename='favicon.ico'))

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        user = data["user"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{user},{email}, {subject}, {message}')
        
def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2: 
        current_time = datetime.now()
        time_stamp = current_time.timestamp()
        date_time = datetime.fromtimestamp(time_stamp)
        str_date_time = date_time.strftime("%A, %B %d, %Y, %-I:%M:%S %p")
        
        user = data["user"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([user, email, subject, message,str_date_time])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return 'did not save to database'
    else:
        return 'something went wrong'
