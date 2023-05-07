from flask import render_template, flash, request
import mysql.connector

def validate(email):
    checker = [str(i) for i in email if (i == '.') or (i == '@')]
    if '@' in checker and '.' in checker:
        return 1
    else:
        return 0


def registerHandling(form = '',
                     mycursor = '',
                     username = '', 
                     password = 0, 
                     passwordConfirm = 1,
                     email = '', 
                     firstName = '', 
                     lastName = '', 
                     age = 0, 
                     postalCode = 0):

    if len(username) < 3:
        flash("Username must be at least 3 characters in length")
        return False
    
    if len(password) < 8:
        flash("Password must be at least 8 characters in length")
        return False
    
    if password != passwordConfirm:
        flash("Passwords do not match. Please retry again.")
        return False
    
    if validate(email) == 0:
        flash("Please enter a valid e-mail")
        return False
    
    if len(firstName) < 1:
        flash("Please enter a valid name.")
        return False
    
    if len(lastName) < 1:
        flash("Please enter a valid last name.")
        return False
    
    if age.isdigit() == 0:
        flash("Please enter a valid age.")
        return False
    
    if int(age) < 16:
        flash("You must be 16 years or older to register. (Please refer to our TOS)")
        return False

    if len(postalCode) < 5 or postalCode.isdigit() == 0:
        flash("Please enter a valid postal code.")
        return False
    
    #CHECK EXISTING USERNAMES/EMAIL
    try:
        mycursor.execute('SELECT * FROM LoginInfo WHERE username = %s', [username])
        existingUser = mycursor.fetchall()

        if existingUser[0][5] == username:
            flash("This username already exists. Please try again.")
            return False

    except:
        mycursor.execute('SELECT * FROM LoginInfo WHERE email = %s', [email])
        existingEmail = mycursor.fetchall()

        try:
            if existingEmail[0][1] == email:
                flash("This email has already been registered.")
                return False
        except:
            return True


        