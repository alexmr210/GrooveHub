from flask import Flask, jsonify, redirect, render_template, url_for
from flask_login import LoginManager, login_required, current_user
from flask_wtf import CSRFProtect
from flask_mail import Mail, Message
from config import config as p
from routes import (
    auth_routes,
    error_routes,
    user_routes,
    collection_routes,
    admin_routes,
)
from db import *
from models import *

app = Flask(__name__)
app.config.from_object(p)
login_manager_app = LoginManager()
csrf = CSRFProtect()
mail = Mail(app)


@login_manager_app.user_loader
def load_user(id):
    return session.query(User).where(User.id_usuario == id).first()


@app.route("/")
def index():
    return redirect(url_for("auth.login"))


@app.route("/home")
@login_required
def home():
    if current_user.admin:
        return render_template("admin/home_admin.html")
    else:
        collectionData = get_six(current_user.id_usuario)
        return render_template("home.html", collectionData=collectionData)


if __name__ == "__main__":
    # Configuration
    app.config.from_object(p)

    # Blueprints
    app.register_blueprint(auth_routes.main, url_prefix="/auth")
    app.register_blueprint(user_routes.main, url_prefix="/user")
    app.register_blueprint(admin_routes.main, url_prefix="/admin")
    app.register_blueprint(collection_routes.main, url_prefix="/")

    # Error handling
    app.register_error_handler(401, error_routes.status_401)
    app.register_error_handler(403, error_routes.status_403)
    app.register_error_handler(404, error_routes.status_404)

    # Start
    csrf.init_app(app)
    login_manager_app.init_app(app)
    app.run()
    # app.run(host="0.0.0.0")
