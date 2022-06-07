import hashlib
import os

from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    make_response,
    session,
)

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from mintz500.models.User import User

app = Flask(__name__)

app.config.update(SECRET_KEY=os.urandom(24))

client = MongoClient("localhost", 27017, username="root", password="password")

db = client.mintz500
users = db.Users

"""
I love ketchup
"""
# Route for handling the login page logic
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        login_error = "Invalid Username or Password."
        if not username or not password:
            error = login_error
            return render_template("index.html", error=error)

        hashed_password = hashlib.md5(
            request.form.get("password").encode("utf8")
        ).hexdigest()
        user = db.Users.find_one({"username": username})
        if not user['username'] or (hashed_password != user['password']):
            error = login_error
            return render_template("index.html", error=error)

        session["username"] = user['username']
        return redirect(url_for("home"))
    elif request.method == "GET":
        signup_successful = session.get("signup_successful")
        message = None
        if signup_successful:
            message = "You successfully signed up!"
        return render_template("index.html", message=message)


@app.route("/home", methods=["GET"])
def home():
    if request.method == "GET":
        if session["username"]:
            user = db.Users.find_one({"username": session["username"]})
            return render_template("home.html", user=user)
        else:
            return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            user = User(username, password)

            Validator.validate_signup(user)

            create_user(user)
            session["signup_successful"] = True
            return redirect(url_for("login"))
        except ValidationError as validation_error:
            return render_template("signup.html", error=str(validation_error))
        except DuplicateKeyError:
            return render_template("signup.html", error="User already exists.")
    elif request.method == "GET":
        return render_template("signup.html", error=error)


def create_user(user):
    user.password = hashlib.md5(user.password.encode("utf8")).hexdigest()
    users.insert_one(
        {"_id": user.username, "username": user.username, "password": user.password}
    )

    print("Successfully created user, " + user.username)
    return user


class Validator:
    @staticmethod
    def validate_signup(user):
        errors = []
        if Validator.is_none_or_empty(user.username):
            errors.append("username cannot be blank")
        if Validator.is_none_or_empty(user.password):
            errors.append("password cannot be blank")
        if len(errors):
            raise ValidationError(errors)

    @staticmethod
    def is_none_or_empty(var):
        return var is None or not len(var)


class ValidationError(Exception):
    pass
