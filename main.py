from flask import Flask, render_template, request, redirect, url_for, session, flash
from skgen import SkGen
from cryptpw import Crypt
from datetime import timedelta
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from admin import admin
from user import user

# Generates a unique secret key
sk = SkGen(64)
cookie_life_time_days = 31
app = Flask(__name__)
app.secret_key = sk.gen()
app.permanent_session_lifetime = timedelta(days=cookie_life_time_days)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dummy.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(16))
    email = db.Column("email", db.String(320))
    password = db.Column("password", db.String(32))
    type = db.Column("type", db.String(60))

    def __init__(self, username, email, password, type):
        self.username = username
        self.email = email
        self.password = password
        self.type = type


class posts(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(64))
    post = db.Column("post", db.String)
    posted_by = db.Column("posted_by", db.String)
    created_date = db.Column("created_date",
                             db.String, default=datetime.utcnow, nullable=False)
    views = db.Column("views", db.Integer)

    def __init__(self, title, post, posted_by):
        self.title = title
        self.post = post
        self.posted_by = posted_by


@app.route('/')
def index():
    return render_template('public/index.html', blogs=posts.query.order_by(desc(posts._id)).all())


@app.route('/login', methods=["GET", "POST"])
def login():
    # Current page
    if request.method == "POST":
        # Getting request form data
        req = request.form
        email = email = req.get('email')
        password = req.get('password')
        # Checking the login credantials and if False sends an error
        email_found = users.query.filter_by(email=email).first()
        if email_found:
            if Crypt.verify_password(password, email_found.password):
                session.permanent = True
                session['email'] = email
                session['username'] = email_found.username
                session['type'] = email_found.type
                flash('you successfully logged in.')
                return redirect(url_for('index'))
            else:
                feedback = f'Wrong password or email'
                return render_template("public/login.html", feedback=feedback)
        else:
            feedback = f'Wrong password or email'
            return render_template("public/login.html", feedback=feedback)
    # Simple page render
    if 'email' and 'username' and 'type' in session:
        if session['type'] == 'reader':
            flash('you are already logged in.')
            return redirect(url_for('index'))
        flash('you are already logged in.')
        return redirect(url_for('admin.dashboard'))
    else:
        return render_template('public/login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    # Checks request method
    if request.method == "POST":
        # Gets POST request data
        req = request.form
        # Variables for all the data
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
    else:
        if 'email' and 'username' in session:
            if session['type'] == 'reader':
                flash('you are already logged in.')
                return redirect(url_for('index'))
            flash('you are already logged in.')
            return redirect(url_for('admin.dashboard'))
        return render_template('public/register.html')


@app.route('/post', methods=["GET", "POST"])
def post():
    if request.method == "POST":
        req = request.form
        title = req.get('title')
        post = req.get('post')
        username = session['username']
        data = posts(title=title, post=post, posted_by=username)
        db.session.add(data)
        db.session.commit()
    if 'email' and 'username' and 'type' in session:
        if session['type'] == 'reader':
            flash('you are not allowed to be on this page.')
            return redirect(url_for('index'))
        return render_template('public/post.html')
    else:
        flash('you need to be logged in.')
        return redirect(url_for('login'))


@app.route('/read/<link>')
def read(link):
    title = link.replace('-', ' ')
    return render_template('public/read.html', title=title, post=posts.query.filter_by(title=title).first())


@app.route('/logout')
def logout():
    session.pop("email", None)
    session.pop("password", None)
    session.pop("username", None)
    session.pop("type", None)
    flash('you have been logged off.')
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host='192.168.1.9', port=80)
