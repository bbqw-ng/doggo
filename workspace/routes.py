from flask import render_template, request, session, redirect
from workspace import app
from workspace.forms import RegisterForm
import mysql.connector
import pymysql

class sqlhost():
    db = mysql.connector.connect(
    host = 'sql9.freemysqlhosting.net',
    port = '3306',
    user = 'sql9599319',
    passwd = 'doggy',
    database = 'sql9599319'
    )

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    db = sqlhost.db
    mycursor = db.cursor()
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form["lastName"]
        age = request.form["age"]
        postalCode = request.form["postalCode"]

        mycursor.execute('INSERT INTO LoginInfo(email, password, firstName, lastName, userName, age, postalCode) VALUES (%s, %s, %s, %s, %s, %s, %s)', [email, password, firstName, lastName, userName, age, postalCode])
        db.commit()
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
   db = sqlhost.db
   mycursor = db.cursor()
   error = ''
   if request.method == 'POST' and 'userName' in request.form and 'password' in request.form:
       userName = request.form['userName']
       password = request.form['password']
       mycursor.execute('SELECT * FROM accounts WHERE userName = %s and password = %s', [userName, password])
       account = mycursor.fetchone()
       if account:
           session['loggedin'] = True
           session['userName'] = account[1]
           return redirect('/home')
       else:
           error = 'The username/password was incorrect.'
   return render_template('home.html', error=error)