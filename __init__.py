from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from datetime import datetime
from skgen import SkGen


app = Flask(__name__)
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
