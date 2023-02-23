from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm(FlaskForm):
    firstName = StringField(label='First Name:')
    lastName = StringField(label='Last Name:')
    userName = StringField(label='Username:')
    password = PasswordField(label='Password:')
    passwordConfirm = PasswordField(label='Confirm Password:')
    email = StringField(label='Email Address:')
    age = StringField(label='Age')
    postalCode = StringField(label='Zip Code')
    submit = SubmitField(label='Create Account!')

class LoginForm(FlaskForm):
    userName = StringField(label='Username:')
    password = PasswordField(label='Password:')