from flask import Blueprint, url_for, session, redirect, render_template, flash

user = Blueprint('user', __name__)


@user.route('/')
def dashboard():
    if 'email' and 'username' and 'type' in session:
        # Assings session data to variables
        return render_template('public/admin.html', email=session['email'], username=session['username'], type=session['type'])
    else:
        flash('you need to be logged in.')
        return redirect(url_for('login'))
