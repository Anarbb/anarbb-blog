from flask import render_template, Blueprint, request, flash, url_for, redirect, session
from project.cryptpw import Crypt
from project import db
from project.models import users

register_blueprint = Blueprint('register', __name__, template_folder='templates')

@register_blueprint.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Getting request form data
        req = request.form
        username = req.get('username')
        email = req.get('email')
        password = req.get('password')
        # Adds the data from the form to the db and redirects to the login page
        user_found = users.query.filter_by(username=username).first()
        email_found = users.query.filter_by(email=email).first()
        if user_found:
            feedback = f"{username} already exists."
            return render_template("register/index.html", feedback=feedback)
        elif email_found:
            feedback = f"{email} already exists."
            return render_template("register/index.html", feedback=feedback)
        else:
            data = users(username, email,
                         Crypt.encrypt_password(password), 'reader')
            db.session.add(data)
            db.session.commit()
        flash("you have been registered login now.")
        return redirect(url_for('login.index'))
    # Checks if the user is already logged in if so redirects them to the index page
    if 'email' and 'username' and 'type' in session:
        flash('you are already logged in.')
        return redirect(url_for('index'))
    return render_template('register/index.html')