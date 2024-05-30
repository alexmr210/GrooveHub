from flask import Blueprint, abort, flash, render_template, redirect, request, session, url_for
from flask_login import login_required, current_user
from extraccionDatos import *
from data import *
from db import get_users, db_delete_user, find_userid, db_modify_user

main = Blueprint("admin", __name__)


@main.route("/admin")
def auth():
    return redirect(url_for("admin.view_users"))


@main.route("/users")
@login_required
def view_users():
    check_admin()
    userData = get_users()
    return render_template("admin/users.html", userData=userData)

@main.route("/modify-user/<idUsuario>", methods=["GET", "POST"])
@login_required
def modify_user(idUsuario):
    check_admin()
    if request.method == "POST":
        user = {
            "id": idUsuario,
            "username": request.form["username"],
            "name": request.form["name"],
            "email": request.form["email"],
            "role": request.form["role"],
        }
        db_modify_user(user)
        print(user)
        flash("En desarrollo")
        return redirect(url_for("admin.view_users"))
    else:
        userData = find_userid(idUsuario)
        user = {
            "id": userData.id_usuario,
            "username": userData.username,
            "name": userData.nombre,
            "email": userData.email,
            "role": userData.role,
        }
        return render_template("admin/modify-user.html", user=user)

@main.route("/delete-user/<idUsuario>")
@login_required
def delete_user(idUsuario):
    username = db_delete_user(idUsuario)
    flash("Se ha eliminado el usuario " + username + ".")
    return redirect(url_for("admin.view_users"))


def check_admin():
    if not current_user.admin:
        abort(403)
