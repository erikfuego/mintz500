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

from mintz500.Utils import hash_str
from mintz500.Validator import Validator
from mintz500.dao.PictureDao import PictureDao
from mintz500.dao.UserDao import UserDao
from mintz500.models.exceptions.UserNotFoundException import UserNotFoundException
from mintz500.models.exceptions.ValidationException import ValidationException

app = Flask(__name__)

app.config.update(SECRET_KEY="We mastered session")

# client = MongoClient("localhost", 27017, username="root", password="password")

# db = client.mintz500
# users = db.Users
# pictures = db.Pictures
#
# user_dao = UserDao(db.Users)
# picture_dao = PictureDao(db.Pictures)


"""
I love ketchup
"""


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("Hello")
        username = request.form.get("username")
        session["username"] = username
        return redirect(url_for("home"))

        # try:
        #     username = request.form.get("username")
        #     password = request.form.get("password")
        #
        #     Validator.validate_login(username, password)
        #
        #     user = user_dao.get_user(username)
        #     if user.password != hash_str(password):
        #         raise UserNotFoundException
        #
        #     session["username"] = user.username
        #     return redirect(url_for("home"))
        # except ValidationException as validation_ex:
        #     return render_template("login.html", error=str(validation_ex))
        # except UserNotFoundException:
        #     return render_template("login.html", error="Invalid username or password")

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
            # user = user_dao.get_user(session["username"])
            user = session["username"]
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

            user_dao.create_user(username, password)

            session["signup_successful"] = True
            return redirect(url_for("login"))
        except ValidationException as validation_ex:
            return render_template("signup.html", error=str(validation_ex))
        except DuplicateKeyError:
            return render_template("signup.html", error="User already exists.")
    elif request.method == "GET":
        return render_template("signup.html")


@app.route("/my_cars", methods=["GET", "POST"])
def my_cars():
    if request.method == "GET":
        if session.get("username"):
            # user = user_dao.get_user(session["username"])
            user = session["username"]
            return render_template("my_cars.html", user=user)
        else:
            return redirect(url_for("login"))
