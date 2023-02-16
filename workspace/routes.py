from flask import render_template
from workspace import app
from workspace.forms import RegisterForm

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/dog")
def dog_page():
    return render_template('dog.html')

@app.route("/about")
def about_page():
    return render_template('about_us.html')

@app.route("/walker")
def walker_page():
    return render_template('walker.html')

@app.route("/register")
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)