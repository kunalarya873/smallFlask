from flask import Flask, render_template
from datetime import datetime
app= Flask(__name__)

@app.route('/') #decorator to define a route for the home page of our website
def index():
    return render_template('index.html', page_access_time=datetime.now())
