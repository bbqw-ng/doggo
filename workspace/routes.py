from flask import render_template, request, session, redirect, flash, Flask, url_for, jsonify
from workspace import app
from workspace.forms import RegisterForm, LoginForm, PostForm
from workspace.validators import registerHandling
from datetime import datetime
from workspace.databaseinfo import Sqlconnector
import mysql.connector
from workspace.session import UserMixin
from flask_login import LoginManager, UserMixin
import pyrebase

from api_photos_testing.image_test import storage
from workspace.upload import upload_image

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

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        mycursor.execute('SELECT * FROM LoginInfo WHERE email = %s and password = %s', [email, password])
        account = mycursor.fetchone()
        print(account)
        if account:
            session['username'] = account[5]
            username = session['username']
            session['userID'] = account[0]
            session['active'] = True
            session['postalCode'] = account[7]
            session['profilePic'] = account[8]
            flash("Logged in!")

            return redirect(url_for('profile'))
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
    try:
        db = Sqlconnector.db
        mycursor = db.cursor()
        db.reconnect()
        #takes the session username and sends it to the render_template for later use
        name = session['username']
        #takes the postalcode and sends it to the template for use on page
        postalCode = session['postalCode']

        mycursor.execute('SELECT * FROM LoginInfo WHERE username  = %s', [name])
        accountInfo = mycursor.fetchall()[0]
        profilePic = accountInfo[8]
        #grabs all the sql entries that arent completed 'indicated by status = 0' and a
        #also their postnumber in descending order () from latest to oldest
        mycursor.execute("SELECT * FROM PostInfo WHERE status = 0 ORDER BY postNum DESC")

        row = mycursor.fetchall()
        return render_template('listings.html',username = name, row = row, postalCode = postalCode, profilePic = profilePic)
    except: 
        return login_page()

#User's Profile
@app.route("/profile", methods=['GET', 'POST'])
def profile():
    db = Sqlconnector.db
    mycursor = db.cursor()
    db.reconnect()

    #Find the username in database
    try:
        name = session["username"]
        mycursor.execute('SELECT * FROM LoginInfo WHERE username = %s', [name])
        accountInfo = mycursor.fetchall()[0]
        print(accountInfo)
        # (INDEX GUIDE) 0: userID, 1: email 2: pass 3: firstName 4: lastName 5: username 6: age 7: postalCode
        #Load data into variables to put into HTML
        userID = accountInfo[0]
        email = accountInfo[1]
        name = accountInfo[3] + " " + accountInfo[4]
        print(name)
        username = accountInfo[5]
        age = accountInfo [6]
        postal = accountInfo[7]
        profilePic = accountInfo[8]
        gallery1 = accountInfo[9]
        gallery2 = accountInfo[10]
        gallery3 = accountInfo[11]
        gallery4 = accountInfo[12]

        averageRating = calcRating(userID, username)

        #grabs all rows from the ratinginfo table where the userID is the person that is being rated.
        mycursor.execute("SELECT * FROM ratinginfo WHERE userID = %s", [userID])
        descriptionInfo = mycursor.fetchall()
      
    except:
        return render_template('user_profile_test.html', username = username, userID = "{:03d}".format(userID), profilePic = profilePic, gallery1 = gallery1, gallery2 = gallery2, gallery3 = gallery3, gallery4 = gallery4, email = email, age = age, postal = postal, name = name, averageRating = averageRating, descriptionInfo = descriptionInfo)



    print(username, userID)
    return render_template('user_profile_test.html', username = username, userID = "{:03d}".format(userID), profilePic = profilePic, gallery1 = gallery1, gallery2 = gallery2, gallery3 = gallery3, gallery4 = gallery4, email = email, age = age, postal = postal, name = name, averageRating = averageRating, descriptionInfo = descriptionInfo)
# except:
    #     return login_page()


#Dynamic Profiles 
#To access profiles: http://127.0.0.1:5000/profile/[username]
@app.route("/profile/<username>", methods=['GET', 'POST'])
def other_profile(username):
    db = Sqlconnector.db
    mycursor = db.cursor()
    db.reconnect()
    #Find the username in database
    averageRating = 0
    mycursor.execute('SELECT * FROM LoginInfo WHERE username  = %s', [username])
    try:
        accountInfo = mycursor.fetchall()[0]
        # (INDEX GUIDE) 0: userID, 1: email 2: pass 3: firstName 4: lastName 5: username 6: age 7: postalCode
        #Load data into variables to put into HTML
        userID = accountInfo[0]
        email = accountInfo[1]
        name = accountInfo[3] + " " + accountInfo[4]
        username = accountInfo[5]
        age = accountInfo [6]
        postal = accountInfo[7]
        profilePic =  accountInfo[8]
        gallery1 = accountInfo[9]
        gallery2 = accountInfo[10]
        gallery3 = accountInfo[11]
        gallery4 = accountInfo[12]

        #grabs all rows from the ratinginfo table where the userID is the person that is being rated.
        mycursor.execute("SELECT * FROM ratinginfo WHERE userID = %s", [userID])
        descriptionInfo = mycursor.fetchall()

        averageRating = calcRating(userID, username)
        print(f"Average Rating: {averageRating}")

        if request.method == 'POST':
            try:
                profileRatings(userID, username)
                return render_template('user_profile_test.html', username = username, userID = "{:03d}".format(userID), profilePic = profilePic, gallery1 = gallery1, gallery2 = gallery2, gallery3 = gallery3, gallery4 = gallery4, email = email, age = age, postal = postal, name = name, averageRating = averageRating, descriptionInfo = descriptionInfo)

            except:
                return render_template('user_profile_test.html', username = username, userID = "{:03d}".format(userID), profilePic = profilePic, gallery1 = gallery1, gallery2 = gallery2, gallery3 = gallery3, gallery4 = gallery4, email = email, age = age, postal = postal, name = name, averageRating = averageRating, descriptionInfo = descriptionInfo)
    except:
       return 'User not found', 404
   
    return render_template('user_profile_test.html', username = username, userID = "{:03d}".format(userID), profilePic = profilePic, gallery1 = gallery1, gallery2 = gallery2, gallery3 = gallery3, gallery4 = gallery4, email = email, age = age, postal = postal, name = name, averageRating = averageRating, descriptionInfo = descriptionInfo)



#Handles ratings => database
def profileRatings(userID, username):
    db = Sqlconnector.db
    mycursor = db.cursor()
    db.reconnect()
    
    #ADD: error handling (comment & rateValue needs to be required)
    #ADD: average rating value and add to user info
    description = request.form['comment']
    

    raterUser = session['username']
    rating = session['rateValue']
        
    if rating == None or description == '':
        print("Not all requirements fufilled")
        return redirect("/profile/<username>")

    print(f"UserID: {userID}, rateUser: {raterUser}, rating: {rating}, description: {description} ")

    #'INSERT INTO PostInfo(userID, title, username, schedule, timePosted, postalCode, description, status) VALUES (%s, %s, %s, %s, %s, %s, %s, 0)', [userID, title, username, schedule, timePosted, postalCode, description]
    mycursor.execute('INSERT INTO ratinginfo(userID, raterUser, rating, description) VALUES (%s,%s,%s,%s)',[userID, raterUser, rating, description])
    db.commit()
    print("Successful!")


                
    #Once value is stored, return to default
    session.pop('rateValue', None)
            
    print(username,description,rating)
    
    return redirect("/profile/<username>")
    

@app.route('/receive_rating', methods=['POST'])
def receive_rating():
    rateValue = request.json['rating']
    session['rateValue'] = rateValue

    return jsonify({'message': 'Rating received'})


def calcRating(userID, username):
    db = Sqlconnector.db
    mycursor = db.cursor()
    db.reconnect()
    #takes all the ratings that were specific to that user.
    mycursor.execute('SELECT rating FROM ratinginfo WHERE userID = %s', [userID])

    rateList = mycursor.fetchall()
    #mycursor.fetchall() stores values as a tuple, so extracting it using list comprehension is necessary
    rateList = [i[0] for i in rateList]
    if len(rateList) != 0:
        #this would sum all the values of the list and divide it by the length of the list to calculate the average (rounded up if >=.5)
        averageRating = sum(rateList) // len(rateList)
        return averageRating
    else:
        averageRating = 0
        return averageRating

#Test Redirects
@app.route("/registertest")
def registertest():
    return render_template('registertesting.html')

@app.route("/logintest")
def logintest():
    return render_template('login.html')

@app.route("/alantest")
def alantest():
    return render_template('alantesting.html')

@app.route("/nav")
def mynavbar():
    return render_template("francisnavbar.html")

#photos testing
@app.route("/phototest", methods=['GET','POST'])
def phototest():
    db = Sqlconnector.db
    mycursor = db.cursor()
    db.reconnect()
    
    name = session["username"]
    try:
        if request.method == 'POST':
            file = request.files['image']
            if request.form['Upload'] == 'profilePic':
                upload_image(file, name, request.form['Upload'] , storage, mycursor, db)
            if request.form['Upload'] == 'gallery1':
                upload_image(file, name, request.form['Upload'] , storage, mycursor, db)
            if request.form['Upload'] == 'gallery2':
                upload_image(file, name, request.form['Upload'] , storage, mycursor, db)
            if request.form['Upload'] == 'gallery3':
                upload_image(file, name, request.form['Upload'] , storage, mycursor, db)
            if request.form['Upload'] == 'gallery4':
                upload_image(file, name, request.form['Upload'] , storage, mycursor, db)
        return redirect("/profile")
    except:
        return login_page()
    
#user profile test
@app.route("/usertest", methods=['GET','POST'])
def usertest():
    return render_template("user_profile_test.html")


