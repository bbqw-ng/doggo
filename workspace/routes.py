from flask import render_template, request, session, redirect, flash
from workspace import app
from workspace.forms import RegisterForm, LoginForm, PostForm
from workspace.validators import validate
from datetime import date
import mysql.connector

class sqlhost():
    db = mysql.connector.connect(
    host = 'realdoggydata.ct9fxw3xymn0.us-east-2.rds.amazonaws.com',
    port = '3306',
    user = 'admin',
    passwd = 'doggowalk',
    database = 'UserInfo'
    )

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    db = sqlhost.db
    db.reconnect()
    mycursor = db.cursor()


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form["lastName"]
        age = request.form["age"]
        postalCode = request.form["postalCode"]


        if len(username) < 3:
            flash("Username must be at least 3 characters in length")
            return render_template('register.html', form=form)
        elif len(password) < 8:
            flash("Password must be at least 8 characters in length")
            return render_template('register.html', form=form)
        elif password != passwordConfirm:
            flash("Passwords do not match. Please retry again.")
            return render_template('register.html', form=form)
        elif validate(email) == 0:
            flash("Please enter a valid e-mail")
            return render_template('register.html', form=form)
        elif len(firstName) < 1:
            flash("Please enter a valid name.")
            return render_template('register.html', form=form)
        elif len(lastName) < 1:
            flash("Please enter a valid last name.")
            return render_template('register.html', form=form)
        elif age:
            if age.isdigit() == 0:
                flash("Please enter a valid age.")
                return render_template('register.html', form=form)
            if int(age) < 16:
                flash("You must be 16 years or older to register. (Please refer to our TOS)")
                return render_template('register.html', form=form)
        elif postalCode:
            if len(postalCode) < 5 or postalCode.isdigit() == 0:
                flash("Please enter a valid postal code.")
                return render_template('register.html', form=form)
        elif request.method == 'POST' and 'username' in request.form and 'email' in request.form:
            mycursor.execute('SELECT * FROM LoginInfo WHERE username = %s', [username])
            existingUser = mycursor.fetchall()
            if existingUser:
                flash("This username already exists. Please try again.")
                return render_template('register.html', form=form)
            mycursor.execute('SELECT * FROM LoginInfo WHERE email = %s', [email])
            existingEmail = mycursor.fetchall()
            if existingEmail:
                flash("This email has already been registered.")
                return render_template('register.html', form=form)

        mycursor.execute('INSERT INTO LoginInfo(email, password, firstName, lastName, username, age, postalCode) VALUES (%s, %s, %s, %s, %s, %s, %s)', [email, password, firstName, lastName, username, age, postalCode])
        db.commit()
        flash("Account created!")
        return redirect('/register')

    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    db = sqlhost.db
    db.reconnect()
    mycursor = db.cursor()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM LoginInfo WHERE username = %s and password = %s', [username, password])
        account = mycursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account[1]
            flash("Logged in!")
            return redirect('/login')
        else:
            flash("Incorrect username or password. Please retry.")
            return redirect('/login')

    return render_template('login.html', form=form)

@app.route("/logout")

def logout_btn():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('userID', None)
    flash("Logged out.")
    return redirect('/login')

@app.route("/listings/post", methods=['GET', 'POST'])
def posting():
    form = PostForm()
    db = sqlhost.db
    mycursor = db.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        schedule = request.form['schedule']
        timePosted = date.today()
        username = session['username']

        if len(title) < 20 or len(title) > 250:
            flash("Title must contain maximum 250 characters.")
            return render_template('user_post.html', form=form)
        elif len(description) < 30 or len(description) > 2000:
            #max and min characters
            flash("Too much/little characters. Must be at minimum 30 to 2000 characters.")
            return render_template('user_post.html', form=form)
        
        mycursor.execute('INSERT INTO PostInfo(title, description, schedule, timePosted, username)', [title, description, schedule, timePosted, username])
        db.commit()
        flash("Listing posted!")
        #DEBUG: redirect to 'listings.html' after posting
        return render_template('user_post.html', form=form)

    return render_template('user_post.html', form=form)


# Unique variable routing system, on button press (e.g. Settings, Go to Profile) this is useful
#@app.route("/user_post/<username>")
#def user_post(username):
#    username = session['username']
#    # Return a template html with placeholder variables
#    return render_template('user_post.html', username = username)

@app.route("/search")
@app.route("/listings")
def listings():

    return render_template('listings.html')

@app.route("/test")

def test():
    return render_template('briantestingyes.html')