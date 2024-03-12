from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

main = Blueprint("user", __name__)


@main.route("/")
def auth():
    return redirect(url_for("user.profile"))


@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("user/profile.html")