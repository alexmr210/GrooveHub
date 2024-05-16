from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db_login
from flask_login import LoginManager, login_user, logout_user, login_required


def status_401(error):
    flash("Debes iniciar sesión primero para acceder a esta vista")
    return redirect(url_for("auth.login"))


def status_404(error):
    return render_template("/error/404.html")
