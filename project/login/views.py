from flask import render_template, Blueprint, request, flash, url_for, redirect, session
from project.cryptpw import Crypt
from project.models import users

login_blueprint = Blueprint('login', __name__, template_folder='templates')

@login_blueprint.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Getting request form data
        req = request.form
        email = req.get('email')
        password = req.get('password')
        email_found = users.query.filter_by(email=email).first()
        # Checking the login credantials and if False sends an error and if the email already exists
        if email_found:
            if Crypt.verify_password(password, email_found.password):
                session.permanent = True
                session['email'] = email
                session['username'] = email_found.username
                session['type'] = email_found.type
                flash('you successfully logged in.')
                return redirect(url_for('home.index'))
            else:
                feedback = 'Wrong password or email'
                return render_template("login/index.html", feedback=feedback)
        else:
            feedback = 'Wrong password or email'
            return render_template("login/index.html", feedback=feedback)
    # Simple page render
    if 'email' and 'username' and 'type' in session:
        flash('you are already logged in.')
        return redirect(url_for('home.index'))
    else:
        return render_template('login/index.html')
