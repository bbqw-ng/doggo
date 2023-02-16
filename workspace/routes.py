from flask import render_template
from workspace import app
from workspace.forms import RegisterForm

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/register")
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)