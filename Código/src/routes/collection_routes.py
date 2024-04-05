from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

main = Blueprint("collection", __name__)


@main.route("/")
def auth():
    return redirect(url_for("collection.view"))


@main.route("/general-view")
@login_required
def view():
    return render_template("collection/general_view.html")

@main.route("/new-register")
@login_required
def insert():
    return render_template("collection/new_register.html")

@main.route("/search-register")
@login_required
def search():
    return render_template("collection/search_register.html")

@main.route("/modify-register")
@login_required
def modify():
    return render_template("collection/modify_register.html")

@main.route("/delete-register")
@login_required
def delete():
    return render_template("collection/delete_register.html")