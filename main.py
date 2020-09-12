from flask import Flask, render_template, request, redirect, url_for, session, flash
from skgen import SkGen
from cryptpw import Crypt
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# Generates a unique secret key
sk = SkGen(64)

app = Flask(__name__)
app.secret_key = sk.gen()
app.permanent_session_lifetime = timedelta(days=31)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(16))
    email = db.Column("email", db.String(320))
    password = db.Column("password", db.String(64))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@app.route('/', methods=["GET", "POST"])
def login():
    # Current page
    log_current = True
    if request.method == "POST":
        # Getting request form data
        req = request.form
        email = email = req.get('email')
        password = req.get('password')
        # Checks if the form isn't empty and if True sends an error
        missing = list()
        for k, v in req.items():
            if v == "":
                missing.append(k)
        if missing:
            feedback = f"missing input for {', '.join(missing)}"
            return render_template("public/login.html", feedback=feedback, log_current=log_current)
        # Checking the login credantials and if False sends an error
        email_found = users.query.filter_by(email=email).first()
        if email_found:
            if Crypt.verify_password(password, email_found.password):
                session.permanent = True
                session['email'] = email
                session['password'] = password
                session['username'] = email_found.username
                flash('you successfully logged in.')
                return redirect(url_for('dashboard'))
            else:
                feedback = f'Wrong password or email'
                return render_template("public/login.html", feedback=feedback, log_current=log_current)
        else:
            feedback = f'Wrong password or email'
            return render_template("public/login.html", feedback=feedback, log_current=log_current)
    # Simple page render
    if 'email' and 'password' in session:
        flash('you are already logged in.')
        return redirect(url_for('dashboard'))
    else:
        return render_template('public/login.html', log_current=log_current)


@app.route('/register', methods=["GET", "POST"])
def register():
    # Current page
    reg_current = True
    # Checks request method
    if request.method == "POST":
        # Gets POST request data
        req = request.form
        # Variables for all the data
        username = req.get('username')
        email = req.get('email')
        password = req.get('password')
        # Checks if the form isn't empty and if True sends an error
        missing = list()
        for k, v in req.items():
            if v == "":
                missing.append(k)
        if missing:
            feedback = f"missing input for {', '.join(missing)}"
            return render_template("public/register.html", feedback=feedback, reg_current=reg_current)
        else:
            # Adds the data from the form to the db and redirects to the login page
            # add SQL support here
            user_found = users.query.filter_by(username=username).first()
            email_found = users.query.filter_by(email=email).first()
            if user_found:
                feedback = f"{username} already exists."
                return render_template("public/register.html", feedback=feedback, reg_current=reg_current)
            elif email_found:
                feedback = f"{email} already exists."
                return render_template("public/register.html", feedback=feedback, reg_current=reg_current)
            else:
                usr = users(username, email, Crypt.encrypt_password(password))
                db.session.add(usr)
                db.session.commit()
            flash("you have been registered login now.")
            return redirect(url_for('login'))
    else:
        return render_template('public/register.html', reg_current=reg_current)


@app.route('/dashboard')
def dashboard():
    if 'email' and 'password' in session:
        db_current = True
        email = session['email']
        password = session['password']
        username = session['username']
        return render_template('public/dashboard.html', email=email, password=password, username=username, db_current=db_current)
    else:
        flash('you need to be logged in.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop("email", None)
    session.pop("password", None)
    flash('you have been logged off.')
    return redirect(url_for('login'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host='192.168.1.9', port=80)
