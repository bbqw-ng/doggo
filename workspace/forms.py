from re import L
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm(FlaskForm):
    firstName = StringField(label='First Name')
    lastName = StringField(label='Last Name')
    username = StringField(label='Username')
    password = PasswordField(label='Password')
    passwordConfirm = PasswordField(label='Confirm Password')
    email = StringField(label='Email Address')
    age = StringField(label='Age')
    postalCode = StringField(label='Zip Code')
    submit = SubmitField(label='Create Account!')

class LoginForm(FlaskForm):
    username = StringField(label='Username')
    email = StringField(label="Email")
    password = PasswordField(label='Password')

class PostForm(FlaskForm):
    title = StringField(label='Title')
    description = StringField(label='Description')
    schedule = StringField(label='Schedule')
    #automate date instead, would provide user authenticity, differentiate date posted, and schedule, maybe popout menu for the date


class RateForm(FlaskForm):
    comment = StringField(label='Comment')

class ProfileDescription(FlaskForm):
    profileDescription = StringField(label='ProfileDescription')