from flask import Flask, Blueprint, redirect, url_for, session, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dummy.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
cookie_life_time_days = 31
app.secret_key = "secret key here"
app.permanent_session_lifetime = timedelta(days=cookie_life_time_days)
db = SQLAlchemy(app)

from project.home.views import home_blueprint
from project.auth.views import auth_blueprint
from project.post.views import post_blueprint
from project.user.views import user_blueprint
from project.admin.views import admin_blueprint

app.register_blueprint(home_blueprint, url_prefix="/home")
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(post_blueprint, url_prefix="/post")
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(admin_blueprint, url_prefix="/admin")


@app.route("/")
def root():
    return redirect(url_for("home.index"))


@app.errorhandler(404)
def error404(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def error404(error):
    return render_template("500.html"), 500