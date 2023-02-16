from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm(FlaskForm):
    username = StringField(label='Username:')
    password = PasswordField(label='Password:')
    passwordConfirm = PasswordField(label='Confirm Password:')
    email = StringField(label='Email Address:')
    submit = SubmitField(label='Create Account!')