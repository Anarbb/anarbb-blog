from flask import Blueprint, url_for, session, redirect, render_template, flash, request
from sqlalchemy import desc
from __init__ import users, posts, db
from cryptpw import Crypt

user = Blueprint('user', __name__)


@user.route('/', methods=["GET", "POST"])
def dashboard():
    if 'email' and 'username' and 'type' in session:
        if request.method == "POST":
            req = request.form
            email = req.get('email')
            password = req.get('password')
            dlt_post = req.get('posts')
            email_found = users.query.filter_by(email=email).first()
            username_found = users.query.filter_by(
                username=session['username']).first()
            posted_by_found = posts.query.filter_by(
                posted_by=session['username'])
            if email:
                if email_found:
                    flash('That email is already in use')
                username_found.email = email
                db.session.commit()
                flash('you just updated your email login again.')
                session.pop("email", None)
                session.pop("username", None)
                session.pop("type", None)
                return redirect(url_for('login'))
            if password:
                username_found.password = Crypt.encrypt_password(password)
                db.session.commit()
                flash('you just updated your password login again.')
                session.pop("email", None)
                session.pop("username", None)
                session.pop("type", None)
                return redirect(url_for('login'))
            if dlt_post:
                if posted_by_found:
                    posts.query.filter_by(title=dlt_post).delete()
                    db.session.commit()
                    flash(f"you just deleted '{dlt_post}'")
                else:
                    flash('sneaky one ay')

        return render_template('public/user.html', posts=posts.query.filter_by(posted_by=session['username']).order_by(desc(posts._id)).all(), email=session['email'], username=session['username'])
    else:
        flash('you need to be logged in.')
        return redirect(url_for('login'))
