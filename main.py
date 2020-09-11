from flask import Flask, render_template, request, redirect, url_for, session, flash
from skgen import SkGen
from datetime import timedelta

# Generates a unique secret key
sk = SkGen(64)

app = Flask(__name__)
app.secret_key = sk.gen()
app.permanent_session_lifetime = timedelta(days=31)


@app.route('/', methods=["GET", "POST"])
def login():
    # Current page
    log_current = True
    # Debugging login
    email1 = 'admin@localhost.com'
    password1 = 'admin'
    # Checks request method
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
        # Adds email and password to a session

        # Checking the debug login and if False sends an error
        if email1 == email and password1 == password:
            session.permanent = True
            session['email'] = email
            session['password'] = password
            flash('you successfully logged in.')
            return redirect(url_for('dashboard'))
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
        return render_template('public/dashboard.html', email=email, password=password, db_current=db_current)
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
    app.run(debug=True, host='192.168.1.9', port=80)
