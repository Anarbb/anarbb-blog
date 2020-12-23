from flask import render_template, Blueprint, request, flash, url_for, redirect, session
from project.cryptpw import Crypt
from project import db
from project.models import posts, comments
from sqlalchemy import desc

post_blueprint = Blueprint("post", __name__, template_folder="templates")


@post_blueprint.route("/create", methods=["GET", "POST"])
def post():
    if "email" and "username" and "type" in session:
        # Disallows users with type 'reader' from accessing the page.
        if session["type"] == "reader":
            flash("you are not allowed to be on this page.")
            return redirect(url_for("home.index"))
        if request.method == "POST":
            # Getting request form data and getting the username from the cookie instead of a form
            req = request.form
            title = req.get("title")
            post = req.get("post")
            username = session["username"]
            data = posts(title=title, post=post, posted_by=username, views=0)
            db.session.add(data)
            db.session.commit()
            flash("Your thread has been posted.")
        return render_template("post/post.html")
    else:
        flash("you need to be logged in.")
        return redirect(url_for("auth.login"))


@post_blueprint.route("/read/<id>")
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
        return render_template(
            "post/read.html",
            post=posts.query.filter_by(_id=id).first(),
            comments=comments.query.filter_by(postID=id)
            .order_by(desc(comments._id))
            .all(),
        )
    else:
        flash("this post doesn't exist.")
        return redirect(url_for("home.index"))


@post_blueprint.route("/read/comment", methods=["POST"])
def comment():
    if "email" and "username" and "type" in session:
        can_comment = True
    else:
        can_comment = False
    if request.method == "GET":
        return redirect(url_for("post.read"))
    if can_comment == True:
        req = request.form
        comment = req.get("comment")
        data = comments(session["username"], comment, request.referrer[-1])
        db.session.add(data)
        db.session.commit()
        flash("Your comment have been posted!")
        return redirect(request.referrer)
    else:
        flash("You need to be logged in to comment.")
        return redirect(url_for("auth.login"))


@post_blueprint.route("/read/comment/delete/<id>", methods=["POST", "GET"])
def comment_delete(id):
    return id
