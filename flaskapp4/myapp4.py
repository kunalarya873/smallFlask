from flask import Flask, render_template 
from datetime import datetime
app = Flask(__name__)

@app.route('/basicloop') 
def basicloop():
    return render_template('basicloop.html')


@app.route('/listloop')
def listloop():
    x=['red', 'green', 'yellow']
    return render_template('listloop.html', my_list=x)


@app.route('/listdict')
def listdict():
    x=[{'name':'Joe', 'age':25},
    {'name':'Kathy', 'age':34},
    {'name':'John', 'age':25}]
    return render_template('listdict.html', my_list=x)

    
if __name__ == '__main__':
    app.debug = False
    app.run(port=5000)
