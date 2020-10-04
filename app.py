from flask import render_template, request, redirect, url_for, session, flash
from __init__ import app, db, posts, users
from cryptpw import Crypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import timedelta
from datetime import datetime
from admin import admin
from user import user

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')
cookie_life_time_days = 31
app.secret_key = 'bruh'
app.permanent_session_lifetime = timedelta(days=cookie_life_time_days)


@app.route('/')
def index():
    # Renders all the posts in the database
    return render_template('public/index.html', blogs=posts.query.order_by(desc(posts._id)).all())


@app.route('/login', methods=["GET", "POST"])
def login():
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
                return redirect(url_for('index'))
            else:
                feedback = 'Wrong password or email'
                return render_template("public/login.html", feedback=feedback)
        else:
            feedback = 'Wrong password or email'
            return render_template("public/login.html", feedback=feedback)
    # Simple page render
    if 'email' and 'username' and 'type' in session:
        flash('you are already logged in.')
        return redirect(url_for('index'))
    else:
        return render_template('public/login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
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
            return render_template("public/register.html", feedback=feedback)
        elif email_found:
            feedback = f"{email} already exists."
            return render_template("public/register.html", feedback=feedback)
        else:
            data = users(username, email,
                         Crypt.encrypt_password(password), 'reader')
            db.session.add(data)
            db.session.commit()
        flash("you have been registered login now.")
        return redirect(url_for('login'))
    # Checks if the user is already logged in if so redirects them to the index page
    if 'email' and 'username' and 'type' in session:
        flash('you are already logged in.')
        return redirect(url_for('index'))
    return render_template('public/register.html')


@app.route('/post', methods=["GET", "POST"])
def post():
    if request.method == "POST":
        # Getting request form data and getting the username from the cookie instead of a form
        req = request.form
        title = req.get('title')
        post = req.get('post')
        username = session['username']
        data = posts(title=title, post=post, posted_by=username, views=0)
        db.session.add(data)
        db.session.commit()
        flash('Your thread has been posted.')
    if 'email' and 'username' and 'type' in session:
        # Disallows users with type 'reader' from accessing the page.
        if session['type'] == 'reader':
            flash('you are not allowed to be on this page.')
            return redirect(url_for('index'))
        return render_template('public/post.html')
    else:
        flash('you need to be logged in.')
        return redirect(url_for('login'))


@app.route('/read/<id>')
def read(id):
    # Getting the ID of the thread from the link and passing it as a parameter to the query function and for checks
    post = posts.query.filter_by(_id=id).first()
    if post:
        if id in session:
            pass
        else:
            views = int(post.views)
            views += 1
            post.views = views
            session[id] = id
            db.session.commit()
        return render_template('public/read.html', post=posts.query.filter_by(_id=id).first())
    else:
        flash("this post doesn't exist.")
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    # Pops all the session data of the user and redirects them to the index page
    session.pop("email", None)
    session.pop("username", None)
    session.pop("type", None)
    flash('you have been logged off.')
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
