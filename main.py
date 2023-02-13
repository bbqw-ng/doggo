from flask import Flask, render_template

app = Flask(__name__)

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