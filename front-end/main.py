from flask import Flask,render_template,request,redirect,session,flash,url_for
import mysql.connector
from flask_mysqldb import MySQL
import os
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key=os.urandom(24)

#config db
#db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
conn = MySQL(app)

@app.route('/')
def First_home():
    return render_template('First_home.html')

@app.route('/home')
def home():
        # Check if user is loggedin
        if 'loggedin' in session:
            # User is loggedin show them the home page
            return render_template('home.html', email=session['email'])
        # User is not loggedin redirect to login page
        return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
