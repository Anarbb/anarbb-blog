from flask import Blueprint, url_for, session, redirect, render_template, flash, request
from sqlalchemy import desc
from project import db
from project.models import posts, users
from project.cryptpw import Crypt

user_blueprint = Blueprint('user', __name__, template_folder='templates')


@user_blueprint.route('/', methods=["GET", "POST"])
def index():
    # Checks if logged in
    if 'email' and 'username' and 'type' in session:
        if request.method == "POST":
            # Getting request form data
            req = request.form
            email = req.get('email')
            password = req.get('password')
            dlt_post = req.get('posts')
            # Querying email, username and posted_by for checks
            email_found = users.query.filter_by(email=email).first()
            username_found = users.query.filter_by(
                username=session['username']).first()
            posted_by_found = posts.query.filter_by(
                posted_by=session['username'])
            if email:
                # Checks if the email already exists in the database
                if email_found:
                    flash('That email is already in use')
                # Changes the email in the database to the desired one then prompts the user to login again
                username_found.email = email
                db.session.commit()
                flash('you just updated your email login again.')
                session.pop("email", None)
                session.pop("username", None)
                session.pop("type", None)
                return redirect(url_for('login'))
            if password:
                # Changes the password to the desired one with encrypting it then prompts the user to login again
                username_found.password = Crypt.encrypt_password(password)
                db.session.commit()
                flash('you just updated your password login again.')
                session.pop("email", None)
                session.pop("username", None)
                session.pop("type", None)
                return redirect(url_for('login'))
            if dlt_post:
                if posted_by_found:
                    # Queries the post using the title and deletes it while checking who is doing the action for security
                    posts.query.filter_by(title=dlt_post).delete()
                    db.session.commit()
                    flash(f"you just deleted '{dlt_post}'")
                else:
                    flash('sneaky one ay')

        return render_template('user/index.html', posts=posts.query.filter_by(posted_by=session['username']).order_by(desc(posts._id)).all(), email=session['email'], username=session['username'])
    else:
        flash('you need to be logged in.')
        return redirect(url_for('login'))
