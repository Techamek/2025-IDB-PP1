#! /usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import re
import config

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

db = config.dblocal

@app.route('/', methods=['GET', 'POST'])
def base():
    if 'loggedin' not in session: #if not logged in, go to login page
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))


# Login route
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']        
        cursor = db.cursor()
        #safe way to create query
        #parameterized query
        sql = "SELECT * FROM accounts WHERE username = %s"        
        cursor.execute(sql, [username])
        print("good query:", sql, [username])
        #unsafe way to create a query
        #DON'T DO IT!
        #sql = f"select * from accounts where username = " +  username
        #print(sql)
        #print("BAD QUERY = \n", sql)
        #cursor.execute(sql)        
        account = cursor.fetchone()
        cursor.close()
        print(account)

        # Check if account exists and if password is correct
        if account and check_password_hash(account[2], password):
            session['loggedin'] = True
            session['id'] = account[0] 
            session['username'] = account[1]
            session['role'] = account[4]
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    
    return render_template('index.html', msg=msg)

# Register route
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'role' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']

        print(username, password, email, role)
        cursor = db.cursor()
        sql = "SELECT * FROM accounts WHERE username = %s;"
        cursor.execute(sql, [username])
        account = cursor.fetchall()
        print(account)
        cursor.close()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not role:
            msg = 'Please fill out the form!'
        else:
            # Hash the password before storing it
            hashed_password = generate_password_hash(password)
            print("creating account")
            print(username, hashed_password, email, role)            
            cursor = db.cursor()
            sql = "insert into accounts values (%s, %s, %s, %s, %s)"            
            cursor.execute(sql, [None, username, hashed_password, email, role])
            data = cursor.fetchall()
            print(data)
            msg = 'You have successfully registered!'
            db.commit()
            cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    
    return render_template('register.html', msg=msg)

# Logout route
@app.route('/pythonlogin/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# Home route
@app.route('/pythonlogin/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'], role=session['role'])
    return redirect(url_for('login'))

# Profile route
@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

@app.route('/actions')
def actions():
    if 'loggedin' in session:
        role = session['role']
        if role is None:
            redirect(url_for("login"))
        return render_template("actions.html", role=role)
    return redirect(url_for('login'))

@app.route('/register_classes', methods=['POST', 'GET'])
def register_classes():
    return render_template("actions/student/register_classes.html")

# Search form route
@app.route('/searchform')
def searchform():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    return render_template('form.html', username=session['username'])

# Search route
@app.route('/search', methods=['POST', 'GET'])
def search():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return "Fill out the Search Form"
     
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        data = []
        if(id != '' or name != ''):
            cursor = db.cursor()        
            if name:
                cursor.execute("SELECT * from instructor where name = %s", [name])
            if id:
                cursor.execute("SELECT * from instructor where ID = %s", [id])
                    
            data = cursor.fetchall()        
            cursor.close()
            print("Found: ", data)
        return render_template('results.html', data=data)

# Run the application
app.run(host='localhost', port=4500)
