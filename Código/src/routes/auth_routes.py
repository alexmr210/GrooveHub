from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from db import db_login, db_signup, find_email, find_username, change_password
from flask_login import login_user, logout_user
from utils import send_reset_email
from models import User

main = Blueprint("auth", __name__)


@main.route("/")
def auth():
    return redirect(url_for("auth.login"))


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        loggedUser = db_login(username, password)
        if loggedUser != None:
            if loggedUser.correctPassword:
                login_user(loggedUser)
                return redirect(url_for("home"))
            else:
                flash("Contraseña incorrecta")
        else:
            flash("Usuario incorrecto")
        return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")


@main.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        name = request.form["name"]
        created = db_signup(username, name, password, email)
        if created:
            flash("Cuenta creada, ya puedes iniciar sesión")
            return render_template("auth/login.html")
    return render_template("auth/signup.html")


@main.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form["email"]
        user = find_email(email)
        if user:
            send_reset_email(user)
            flash(
                "Te hemos enviado un correo electrónico para restablecer tu contraseña"
            )
            return render_template("auth/login.html")
        else:
            flash("No hay ningún usuario con ese correo electrónico")
            return render_template("auth/reset_password.html")
    else:
        return render_template("auth/reset_password.html")


@main.route("/password_reset_verified/<token>", methods=["GET", "POST"])
def reset_verified(token):
    username = User.verify_reset_token(token)
    user = find_username(username)
    if not user:
        flash("Enlace no válido")
        return redirect(url_for("auth.login"))
    password = request.form.get("password")
    if password:
        change_password(user, password)
        flash("Contraseña cambiada")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_verified.html")


@main.route("/logout")
def logout():
    logout_user()
    session.pop('admin', None)
    return redirect(url_for("auth.login"))
