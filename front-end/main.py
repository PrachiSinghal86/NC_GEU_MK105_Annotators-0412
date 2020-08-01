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
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MySQL@2000'
app.config['MYSQL_DB'] = 'registration_sih'
conn = MySQL(app)

@app.route('/')
def First_home():
    return render_template('First_home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')


@app.route('/home')
def home():
        # Check if user is loggedin
        if 'loggedin' in session:
            # User is loggedin show them the home page
            return render_template('home.html', email=session['email'])
        # User is not loggedin redirect to login page
        return redirect('/login')

@app.route('/about')
def about_home():
    return render_template('about.html')


#User end
@app.route('/login_validation', methods=['GET', 'POST'])
def login_validation():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_register WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['ID'] = account['ID']
            session['email'] = account['email']
            flash('Logged in Successfully!')
            # Redirect to home page
            return redirect('/home')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password!')
            return render_template('login.html', msg=msg)
    # Show the login form with message (if any)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_register WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user_register (username, password, email) VALUES (%s, %s, %s)', (username, password, email,))
            conn.connection.commit()
            flash('You have successfully registered!')
            return render_template('login.html')

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html')

@app.route('/logout')
def logout():
# Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('ID', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
