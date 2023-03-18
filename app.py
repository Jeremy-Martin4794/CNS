from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# db tables
class Users(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    year = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    major = db.Column(db.String(200), nullable=False)
    signedIn = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.email

# routes
@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/record_response.html', methods=["POST"])
def record_response():
    if request.method == "POST":
        email = request.form.get("email")
        year = request.form.get("year")
        gender = request.form.get("gender")
        major = request.form.get("major")
        blankInputError = ""

        if (email == None) or (year == None) or (gender == None) or (major == ""):
            blankInputError = "please fill in all fields"

        if blankInputError:
            return render_template("index.html", blankInputError=blankInputError)
        else:
            session["userEmail"] = email

            # add to database class
            newUser = Users(email=email, year=year, gender=gender, major=major)

            # push and commit to database
            try:
                db.session.add(newUser)
                db.session.commit()
                return redirect(url_for("response_index"))
            except:
                return "an error occurred (have you already filled out the survey?)"

@app.route('/response_index', methods=["GET"])
def response_index():
    return render_template("response-index.html")

@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html")

@app.route('/login_pass', methods=["GET", "POST"])
def login_pass():
    if request.method == "POST":
        print(request.form.get("emailInput"))
        emailInput = request.form.get("emailInput")
        session["emailInput"] = emailInput
        return render_template("login-pass.html", emailInput=emailInput)
    else:
        return render_template("login-pass.html")

@app.route('/response_login', methods=["POST"])
def response_login():
    if request.method == "POST":
        demographicEmail = session["userEmail"]
        loginInputEmail = session["emailInput"]
        if demographicEmail == loginInputEmail:
            users = Users.query.all()
            for user in users:
                if user.email == loginInputEmail:
                    user.signedIn = True
            try:
                db.session.commit()
                return render_template("response-login.html")
            except:
                return "problem occurred"
        else:
            return render_template("response-login.html")

@app.route('/survey', methods=["GET"])
def survey():
    return render_template("mySurvey.html")

@app.route('/response_survey', methods=["GET"])
def response_survey():
    return render_template("response-survey.html")

@app.route('/success', methods=["GET"])
def success():
    dataRecords = Users.query.all()
    return render_template("success.html", dataRecords=dataRecords)