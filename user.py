from flask import Blueprint, url_for, session, redirect, render_template, flash

user = Blueprint('user', __name__)


@user.route('/')
def dashboard():
    return render_template('public/user.html')
