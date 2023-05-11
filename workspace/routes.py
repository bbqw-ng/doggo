from flask import render_template, request, session, redirect, flash, Flask, url_for
from workspace import app
from workspace.forms import RegisterForm, LoginForm, PostForm
from workspace.validators import registerHandling
from datetime import datetime
from workspace.databaseinfo import Sqlconnector
import mysql.connector
from workspace.session import UserMixin
from flask_login import LoginManager, UserMixin
import pyrebase
import tempfile

from api_photos_testing.image_test import storage

#TODO
# Add URL_FOR LINKS
# GET G.SESSION TO WORK IN JINJA

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('alantesting.html')

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    db = Sqlconnector.db
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

        #ERROR HANDLING
        result = registerHandling(form, mycursor, username, password, passwordConfirm, email, firstName, lastName, age, postalCode)
        if result == False:
            return render_template('register.html', form=form)
        #END ERROR HANDLING
        else:
            mycursor.execute('INSERT INTO LoginInfo(email, password, firstName, lastName, username, age, postalCode) VALUES (%s, %s, %s, %s, %s, %s, %s)', [email, password, firstName, lastName, username, age, postalCode])
            db.commit()
            flash("Account created!")
            return redirect('/login')

    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    db = Sqlconnector.db
    db.reconnect()
    mycursor = db.cursor(buffered=True)

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM LoginInfo WHERE username = %s and password = %s', [username, password])
        account = mycursor.fetchone()
        print(account)
        if account:
            session['username'] = account[5]
            username = session['username']
            session['userID'] = account[0]
            session['active'] = True
            session['postalCode'] = account[7]
            flash("Logged in!")

            return redirect(url_for('profile', username=username ))
        else:
            flash("Incorrect username or password. Please retry.")
            return redirect('/login')

    return render_template('login.html', form=form)

@app.route("/logout")
def logout_btn():
    #Clear user session
    session.clear()
    flash("Logged out.")
    return redirect(url_for('login_page'))
#___________________________________________________________________________________________________
@app.route("/post", methods=['GET', 'POST'])
def posting():
    form = PostForm()
    db = Sqlconnector.db
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
    db = Sqlconnector.db
    mycursor = db.cursor()
    db.reconnect()
    #takes the session username and sends it to the render_template for later use
    name = session['username']
    #takes the postalcode and sends it to the template for use on page
    postalCode = session['postalCode']
    #grabs all the sql entries that arent completed 'indicated by status = 0' and a
    #also their postnumber in descending order () from latest to oldest
    mycursor.execute("SELECT * FROM PostInfo WHERE status = 0 ORDER BY postNum DESC")

    row = mycursor.fetchall()
    return render_template('listings.html',username = name, row = row, postalCode = postalCode)

#User's Profile
@app.route("/profile/<username>", methods=['GET', 'POST'])
def profile(username):
    db = Sqlconnector.db
    mycursor = db.cursor()
    db.reconnect()
    #Find the username in database
    mycursor.execute('SELECT * FROM LoginInfo WHERE username = %s', [username])
    try:
        accountInfo = mycursor.fetchall()[0]
        # (INDEX GUIDE) 0: userID, 1: email 2: pass 3: firstName 4: lastName 5: username 6: age 7: postalCode
        #Load data into variables to put into HTML
        username = accountInfo[5]
        userID = accountInfo[0]
        

    except:
        return 'User not found', 404
    
    return render_template('user_profile.html')


#Dyamic Profiles 
#To access profiles: http://127.0.0.1:5000/profile/[username]
@app.route("/profile/<username>", methods=['GET', 'POST'])
def other_profile(username):
    db = Sqlconnector.db
    mycursor = db.cursor()
    db.reconnect()
    mycursor.execute('SELECT userID, username FROM LoginInfo') #retrieves userID and username from database
    existingUser = mycursor.fetchall()
    filtered_list = [t for t in existingUser if t[1] == username] #makes if list of userID and username iif username matches database
    print(filtered_list)
    if len(filtered_list) == 1: #if there is exactly one user associated with username
        return render_template('user_profile.html', username = filtered_list[0][1], userID = "{:03d}".format(filtered_list[0][0]))
    else: 
        return render_template("under_construction.html") #if no username exists in database takes you to invalid page

#Test Redirects
@app.route("/logintest")
def logintest():
    return render_template('logintesting.html')

@app.route("/alantest")
def alantest():
    return render_template('alantesting.html')

@app.route("/usertest")
def profile_test():
    return render_template("user_profile.html")

@app.route("/nav")
def mynavbar():
    return render_template("francisnavbar.html")

@app.route("/btest", methods=['GET', 'POST'])
def filter():
    if request.method == 'POST':
        filter_option = request.form.get('filter')
        # Process the filter_option and retrieve filtered results
        
        # For example, you can simulate filtering a list of items
        # based on the selected option
        all_results = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        filtered_results = "hi"
        #[result for result in all_results if result.endswith(filter_option)]
        
        return render_template('briantestfilter.html', filtered_results=filtered_results)
    else:
        return render_template('briantestfilter.html', filtered_results=[])
    
#photos testing

@app.route("/phototest", methods=['GET','POST'])
def phototest():
    if request.method == 'POST':
        if request.method == 'POST':
            file = request.files['image']
            temp = tempfile.NamedTemporaryFile(delete=False)
            file.save(temp.name)
            storage.child("images/" + file.filename).put(temp.name)
            return "File uploaded successfully."
    return render_template("phototest.html")
