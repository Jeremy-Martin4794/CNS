from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# db tables


# routes
@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/response_index', methods=["GET"])
def response_index():
    return render_template("response-index.html")

@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html")

@app.route('/login_pass', methods=["GET"])
def login_pass():
    return render_template("login-pass.html")

@app.route('/response_login', methods=["GET"])
def response_login():
    return render_template("response-login.html")

@app.route('/survey', methods=["GET"])
def survey():
    return render_template("mySurvey.html")

@app.route('/response_survey', methods=["GET"])
def response_survey():
    return render_template("response-survey.html")

@app.route('/success', methods=["GET"])
def success():
    return render_template("success.html")