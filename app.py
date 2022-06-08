import hashlib

from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    session,
)

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from mintz500.models.User import User

app = Flask(__name__)

app.config.update(SECRET_KEY="We mastered session")

client = MongoClient("localhost", 27017, username="root", password="password")

db = client.mintz500
users = db.Users


"""
I love ketchup
"""
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            Validator.validate_login(username, password)

            user = get_user(username)
            if user.password != hash_str(password):
                raise UserNotFoundError

            session["username"] = user.username
            return redirect(url_for("home"))
        except ValidationError as validation_error:
            return render_template("login.html", error=str(validation_error))
        except UserNotFoundError:
            return render_template("login.html", error="Invalid username or password")

    elif request.method == "GET":
        signup_successful = session.get("signup_successful")
        message = None
        if signup_successful:
            session.pop("signup_successful")
            message = "You successfully signed up!"
        return render_template("login.html", message=message)


@app.route("/home", methods=["GET"])
def home():
    if request.method == "GET":
        if session.get("username"):
            user = get_user(session["username"])
            return render_template("home.html", user=user)
        else:
            return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            Validator.validate_signup(username, password)

            create_user(username, password)

            session["signup_successful"] = True
            return redirect(url_for("login"))
        except ValidationError as validation_error:
            return render_template("signup.html", error=str(validation_error))
        except DuplicateKeyError:
            return render_template("signup.html", error="User already exists.")
    elif request.method == "GET":
        return render_template("signup.html")


def create_user(username: str, password: str) -> User:
    hashed_password = hash_str(password)
    users.insert_one(
        {"_id": username, "username": username, "password": hashed_password}
    )

    print("Successfully created user, " + username)
    return User(username, hashed_password)


def get_user(username: str) -> User:
    user_maybe = users.find_one(
        {"_id": username}
    )
    if user_maybe is None:
        raise UserNotFoundError
    return User(user_maybe["username"], user_maybe["password"])


def hash_str(password):
    hashed_password = hashlib.md5(password.encode("utf8")).hexdigest()
    return hashed_password


class Validator:
    @staticmethod
    def validate_signup(username: str, password: str):
        errors = []
        if Validator.is_none_or_empty(username):
            errors.append("username cannot be blank")
        if Validator.is_none_or_empty(password):
            errors.append("password cannot be blank")
        if len(errors):
            raise ValidationError(errors)

    @staticmethod
    def validate_login(username: str, password: str):
        errors = []
        if Validator.is_none_or_empty(username):
            errors.append("username cannot be blank")
        if Validator.is_none_or_empty(password):
            errors.append("password cannot be blank")
        if len(errors):
            raise ValidationError(errors)

    @staticmethod
    def is_none_or_empty(var):
        return var is None or not len(var)


class ValidationError(Exception):
    pass


class UserNotFoundError(Exception):
    pass
