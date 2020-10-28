from project import db
from datetime import datetime

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.Text(16))
    email = db.Column("email", db.Text(320))
    password = db.Column("password", db.Text(16383))
    type = db.Column("type", db.Text(60))

    def __init__(self, username, email, password, type):
        self.username = username
        self.email = email
        self.password = password
        self.type = type


class posts(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.Text(32))
    post = db.Column("post", db.Text(1638300))
    posted_by = db.Column("posted_by", db.Text(16))
    created_date = db.Column("created_date",
                             db.Text(32), default=datetime.utcnow, nullable=False)
    views = db.Column("views", db.Text(99999999))

    def __init__(self, title, post, posted_by, views):
        self.title = title
        self.post = post
        self.posted_by = posted_by
        self.views = views
