from flask import render_template, request, session, redirect, flash, Flask
from workspace import app
from workspace.forms import RegisterForm, LoginForm, PostForm
from workspace.validators import validate
from datetime import datetime
import mysql.connector
import urllib3


class sqlhost():
    db = mysql.connector.connect(
    host = 'doggoserver.mysql.database.azure.com',
    port = '3306',
    user = 'mainadmin',
    password = '9jznqua4y5T@',
    database = 'userinfo'
    )

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('alantesting.html')

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
    mycursor = db.cursor(buffered=True)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM LoginInfo WHERE username = %s and password = %s', [username, password])
        account = mycursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account[5]
            session['userID'] = account[0]
            session['postalCode'] = account[7]
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
    session.pop('postalCode', None)
    flash("Logged out.")
    return redirect('/login')

@app.route("/post", methods=['GET', 'POST'])
def posting():
    form = PostForm()
    db = sqlhost.db
    mycursor = db.cursor()
    db.reconnect()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        schedule = request.form['schedule']
        #need to turn into EST in the future, or adapt to geographical location
        defaultTime = datetime.now()
        timePosted = defaultTime.strftime("%m/%d/%Y %H:%M")
        username = session['username']
        userID = session['userID']
        postalCode = session['postalCode']

        if len(title) < 5 or len(title) > 200:
            flash("Title must contain maximum 200 characters.")
            return render_template('user_post.html', form=form)
        elif len(description) < 30 or len(description) > 2000:
            #max and min characters
            flash("Description must be at least 30 to 2000 characters.")
            return render_template('user_post.html', form=form)
        elif len(schedule) < 1:
            flash("Please insert a schedule")
            return render_template('user_post.html', form=form)
        
        mycursor.execute('INSERT INTO PostInfo(userID, title, username, schedule, timePosted, postalCode, description, status) VALUES (%s, %s, %s, %s, %s, %s, %s, 0)', [userID, title, username, schedule, timePosted, postalCode, description])
        db.commit()
        flash("Listing posted!")

        return redirect('/listings')

    return render_template('user_post.html', form=form)


# Unique variable routing system, on button press (e.g. Settings, Go to Profile) this is useful
#@app.route("/user_post/<username>")
#def user_post(username):
#    username = session['username']
#    # Return a template html with placeholder variables
#    return render_template('user_post.html', username = username)

@app.route("/listings", methods=['GET', 'POST'])
def listings():
    db = sqlhost.db
    mycursor = db.cursor()
    db.reconnect()
    mycursor.execute("SELECT * FROM PostInfo WHERE status = 0 ORDER BY postNum DESC")

    row = mycursor.fetchall()
    return render_template('listings.html', row = row)

@app.route("/users/<username>", methods=['GET', 'POST'])
def profile(username):
    db = sqlhost.db
    mycursor = db.cursor()
    db.reconnect()

    url = urllib3.PoolManager()
    r = url.request

    print(r.data)

    print(url)
    username = None

    return render_template('user_profile.html', username = username)


#Test Redirects
@app.route("/alantest")
def alantest():
    return render_template('alantesting.html')

@app.route("/usertest")
def profile_test():
    return render_template("user_profile.html")

