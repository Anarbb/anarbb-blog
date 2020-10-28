from flask import render_template, Blueprint, request, flash, url_for, redirect, session
from project.cryptpw import Crypt
from project import db
from project.models import users

auth_blueprint = Blueprint("auth", __name__, template_folder="templates")


@auth_blueprint.route("/")
def root():
    return redirect(url_for("home.index"))


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Getting request form data
        req = request.form
        username = req.get("username")
        email = req.get("email")
        password = req.get("password")
        # Adds the data from the form to the db and redirects to the login page
        user_found = users.query.filter_by(username=username).first()
        email_found = users.query.filter_by(email=email).first()
        if user_found:
            feedback = f"{username} already exists."
            return render_template("auth/register.html", feedback=feedback)
        elif email_found:
            feedback = f"{email} already exists."
            return render_template("auth/register.html", feedback=feedback)
        else:
            data = users(username, email, Crypt.encrypt_password(password), "reader")
            db.session.add(data)
            db.session.commit()
        flash("you have been registered login now.")
        return redirect(url_for("auth.login"))
    # Checks if the user is already logged in if so redirects them to the index page
    if "email" and "username" and "type" in session:
        flash("you are already logged in.")
        return redirect(url_for("home.index"))
    return render_template("auth/register.html")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Getting request form data
        req = request.form
        email = req.get("email")
        password = req.get("password")
        email_found = users.query.filter_by(email=email).first()
        # Checking the login credantials and if False sends an error and if the email already exists
        if email_found:
            if Crypt.verify_password(password, email_found.password):
                session.permanent = True
                session["email"] = email
                session["username"] = email_found.username
                session["type"] = email_found.type
                flash("you successfully logged in.")
                return redirect(url_for("home.index"))
            else:
                feedback = "Wrong password or email"
                return render_template("auth/login.html", feedback=feedback)
        else:
            feedback = "Wrong password or email"
            return render_template("auth/login.html", feedback=feedback)
    # Simple page render
    if "email" and "username" and "type" in session:
        flash("you are already logged in.")
        return redirect(url_for("home.index"))
    else:
        return render_template("auth/login.html")


@auth_blueprint.route("/logout")
def logout():
    # Pops all the session data of the user and redirects them to the index page
    session.pop("email", None)
    session.pop("username", None)
    session.pop("type", None)
    flash("you have been logged off.")
    return redirect(url_for("home.index"))
