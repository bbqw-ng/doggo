from argparse import _MutuallyExclusiveGroup
from flask import render_template, request, session, redirect, flash
from workspace import app
from workspace.forms import RegisterForm, LoginForm
from workspace.emails import validate
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
    return render_template('home.html', username= session['userName'])

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    db = sqlhost.db
    mycursor = db.cursor()

    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form["lastName"]
        age = request.form["age"]
        postalCode = request.form["postalCode"]


        if len(userName) < 3:
            flash("Username must be at least 3 characters in length")
            return redirect('/register')
        elif len(password) < 8:
            flash("Password must be at least 8 characters in length")
            return redirect('/register')
        elif password != passwordConfirm:
            flash("Passwords do not match. Please retry again.")
            return redirect('/register')
        elif validate(email) == 0:
            flash("Please enter a valid e-mail")
            return redirect('/register')
        elif len(firstName) < 1:
            flash("Please enter a valid name.")
            return redirect('/register')
        elif len(lastName) < 1:
            flash("Please enter a valid last name.")
            return redirect('/register')
        elif int(age) < 16:
            flash("Please enter a valid age.")
            return redirect('/register')
        elif len(postalCode) < 5:
            flash("Please enter a valid postal code.")
            return redirect('/register')

        
        mycursor.execute('INSERT INTO LoginInfo(email, password, firstName, lastName, userName, age, postalCode) VALUES (%s, %s, %s, %s, %s, %s, %s)', [email, password, firstName, lastName, userName, age, postalCode])

        db.commit()
        flash("Account created!")
        return redirect('/register')
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    db = sqlhost.db
    mycursor = db.cursor()
    if request.method == 'POST' and 'userName' in request.form and 'password' in request.form:
        userName = request.form['userName']
        password = request.form['password']
        mycursor.execute('SELECT * FROM LoginInfo WHERE userName = %s and password = %s', [userName, password])
        account = mycursor.fetchone()
        if account:
            session['loggedin'] = True
            session['userName'] = account[1]
            flash("Logged in!")
            return redirect('/login')
        else:
            flash("Incorrect username or password. Please retry.")
            return redirect('/login')

    return render_template('login.html', form=form)

@app.route("/logout")
def logout_btn():
    session.pop('loggedin', None)
    session.pop('userName', None)
    return redirect('/login')