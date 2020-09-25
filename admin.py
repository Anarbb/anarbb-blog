# Still under work
from flask import Blueprint, url_for, session, redirect, render_template, flash

admin = Blueprint('admin', __name__)


@admin.route('/')
def dashboard():
    if 'email' and 'username' and 'type' in session:
        if session['type'] == 'reader':
            flash('you are not allowed to be on this page.')
            return redirect(url_for('index'))
        # Assings session data to variables
        return render_template('public/admin.html', email=session['email'], username=session['username'], type=session['type'])
    else:
        flash('you need to be logged in.')
        return redirect(url_for('login'))
