from flask import Flask, render_template
from datetime import datetime
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html', curr_time= datetime.now())
@app.route('/about')
def about():
    return render_template('about.html', curr_time= datetime.now())


