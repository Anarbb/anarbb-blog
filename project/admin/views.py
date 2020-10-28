# Still under work
from flask import Blueprint, url_for, session, redirect, render_template, flash, request
from project import db
from project.models import users, posts

admin_blueprint = Blueprint("admin", __name__, template_folder="templates")


@admin_blueprint.route("/", methods=["POST", "GET"])
def index():
    if "email" and "username" and "type" in session:
        if session["type"] == "reader":
            flash("you are not allowed to be on this page.")
            return redirect(url_for("home.index"))
        # Assings session data to variables
        if request.method == "POST":
            req = request.form
            dlt_user = req.get("dlt_user")
            edit_user = req.get("edit-user")
            edit_post = req.get("edit-post")
            if dlt_user:
                users.query.filter_by(username=dlt_user).delete()
                db.session.commit()
                flash(f"deleted user {dlt_user}")
            if edit_user:
                return redirect(f"edit/{edit_user}")
            if edit_post:
                return redirect(url_for("admin.edit_post", title=edit_post))
        return render_template(
            "admin/index.html", users=users.query.all(), posts=posts.query.all()
        )
    else:
        flash("you need to be logged in.")
        return redirect(url_for("auth.login"))


@admin_blueprint.route("/edit/<username>")
def user_edit(username):
    if "email" and "username" and "type" in session:
        if session["type"] == "reader":
            flash("you are not allowed to be on this page.")
            return redirect(url_for("home.index"))
        if users.query.filter_by(username=username).first():
            return "OK"
        flash("User not found")
        return redirect(url_for("admin.index"))


@admin_blueprint.route("/edit-post/<title>", methods=["POST", "GET"])
def edit_post(title):
    if "email" and "username" and "type" in session:
        if session["type"] == "reader":
            flash("you are not allowed to be on this page.")
            return redirect(url_for("home.index"))
        post = posts.query.filter_by(title=title).first()
        if request.method == "POST":
            req = request.form
            edited_title = req.get("edited-title")
            edited_post = req.get("edited-post")
            post.title = edited_title
            post.post = edited_post
            db.session.commit()
            flash(f"Your changes have been commited")
            return redirect(url_for("admin.index"))
        if not post:
            flash("post doesn't exist.")
            return redirect(url_for("admin.index"))
        return render_template("admin/edit-post.html", post=post)
    return redirect(url_for("home.index"))
