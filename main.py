from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def login():
    log_current = True
    if request.method == "POST":
        req = request.form
        email = email = req.get('email')
        password = req.get('password')
        missing = list()
        for k, v in req.items():
            if v == "":
                missing.append(k)
        if missing:
            feedback = f"Missing input for {', '.join(missing)}"
            return render_template("public/login.html", feedback=feedback, log_current=log_current)
        return "OK"
    return render_template('public/login.html', log_current=log_current)


@app.route('/register', methods=["GET", "POST"])
def register():
    reg_current = True
    if request.method == "POST":
        # Gets POST request data
        req = request.form
        # Variables for all the data
        username = req.get('username')
        email = req.get('email')
        password = req.get('password')
        # Checks if all forms are filled out and sends an error
        missing = list()
        for k, v in req.items():
            if v == "":
                missing.append(k)
        if missing:
            feedback = f"Missing input for {', '.join(missing)}"
            return render_template("public/register.html", feedback=feedback, reg_current=reg_current)
        else:
            # Adds the data from the form to the db and redirects to the login page
            # add SQL support here
            return redirect(url_for('login'))
    else:
        return render_template('public/register.html', reg_current=reg_current)


if __name__ == "__main__":
    app.run(debug=True, port=80)
