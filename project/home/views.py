from flask import render_template, Blueprint
from sqlalchemy import desc
from project import db
from project.models import posts


home_blueprint = Blueprint("home", __name__, template_folder="templates")


@home_blueprint.route("/")
def index():
    # Renders all the posts in the database
    return render_template(
        "home/index.html", blogs=posts.query.order_by(desc(posts._id)).all()
    )
