from flask import Flask, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fac185e9ce86fc2162b0285e'

from workspace import routes
