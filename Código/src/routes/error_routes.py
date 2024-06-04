from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db_login
from flask_login import LoginManager, login_user, logout_user, login_required


def status_401(error):
    flash("Debes iniciar sesión primero para acceder a esta vista")
    return redirect(url_for("auth.login"))

def status_403(error):
    return render_template("/error/403.html")

def status_404(error):
    return render_template("/error/404.html")

def status_429(error):
    flash("Estamos teniendo problemas con tu petición. Por favor, inténtalo de nuevo en unos minutos.")
    return redirect(url_for("home"))

