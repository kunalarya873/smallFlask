from flask import Flask, render_template, request
from datetime import datetime
app= Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', accesstime=datetime.now())
    else:
        celsius = float(request.form.get('celsius'))
        farenheit = celsius * 9/5 + 32.0
        return render_template('convert.html', celsius=celsius, farenheit=farenheit, curr_time=datetime.now())