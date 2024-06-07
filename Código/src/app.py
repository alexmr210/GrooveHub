from flask import redirect, render_template, url_for, session
from flask_login import LoginManager, login_required, current_user
from flask_wtf import CSRFProtect
from config import config as p
import config
from routes import (
    admin_routes,
    auth_routes,
    collection_routes,
    error_routes,
    user_routes,
)
from db import *
from models import *

# Accedemos a la configuración global e inicializamos la gestión de usuarios
config.init()
login_manager_app = LoginManager()
csrf = CSRFProtect()


@login_manager_app.user_loader
def load_user(id):
    return session.query(User).where(User.id_usuario == id).first()


@config.app.route("/")
def index():
    return redirect(url_for("auth.login"))


@config.app.route("/home")
@login_required
def home():
    if current_user.admin:
        return redirect(url_for("admin.home"))
    else:
        collectionData = get_six(current_user.id_usuario)
        return render_template("home.html", collectionData=collectionData)


# PRUEBAS
@config.app.route("/test/<idDisco>")
def test(idDisco):
    disco = db_get_disk(idDisco)
    canciones = disco.canciones
    cancion = canciones[0].cancion
    titulo = cancion.cancion
    return render_template("test.html", info=disco)


if __name__ == "__main__":
    # Configuration
    config.app.config.from_object(p)

    # Blueprints
    config.app.register_blueprint(auth_routes.main, url_prefix="/auth")
    config.app.register_blueprint(user_routes.main, url_prefix="/user")
    config.app.register_blueprint(admin_routes.main, url_prefix="/admin")
    config.app.register_blueprint(collection_routes.main, url_prefix="/")

    # Error handling
    config.app.register_error_handler(401, error_routes.status_401)
    config.app.register_error_handler(403, error_routes.status_403)
    config.app.register_error_handler(404, error_routes.status_404)
    config.app.register_error_handler(429, error_routes.status_429)

    # Start
    csrf.init_app(config.app)
    login_manager_app.init_app(config.app)
    config.app.run()
    # app.run(host="0.0.0.0")
