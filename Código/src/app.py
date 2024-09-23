from flask import redirect, render_template, send_from_directory, url_for, session
from flask_login import LoginManager, login_required, current_user
from flask_wtf import CSRFProtect
from config import config as p
from pathlib import Path
import config
from routes import (
    admin_routes,
    auth_routes,
    collection_routes,
    error_routes,
)
from db import *

# from models import *

# Accedemos a la configuración global e inicializamos la gestión de usuarios
config.init()
login_manager_app = LoginManager()
csrf = CSRFProtect()


@login_manager_app.user_loader
def load_user(id):
    return session.query(User).where(User.id_usuario == id).first()

@config.app.errorhandler(SQLAlchemyError)
def handle_db_error(error):
    connection.rollback()
    flash("Ha habido un error inesperado. Por favor, intntalo de nuevo más tarde.")
    return redirect(url_for("home"))

@config.app.route("/")
def index():
    return redirect(url_for("auth.login"))

@config.app.route('/download/<filename>')
def open_pdf(filename):
    # Cambia 'static/pdfs' al directorio donde guardaste tu PDF
    return send_from_directory('static/pdf', filename, as_attachment=True)


@config.app.route("/home")
@login_required
def home():
    if current_user.admin:
        return redirect(url_for("admin.home"))
    else:
        collectionData = get_six(current_user.id_usuario)
        artists = get_artists_amount(current_user.id_usuario)
        disks = get_disks_amount(current_user.id_usuario)
        return render_template(
            "home.html", collectionData=collectionData, artists=artists, disks=disks
        )


@config.app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    # Configuration
    config.app.config.from_object(p)

    # Blueprints
    config.app.register_blueprint(auth_routes.main, url_prefix="/auth")
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
    # config.app.run()

    config.app.run(host="0.0.0.0", port=5000)

    # PROJECT_DIR = Path(__file__).parent
    # cert_path = PROJECT_DIR / 'private/cert.pem'
    # key_path = PROJECT_DIR / 'private/key.pem'
    # config.app.run(host="0.0.0.0", port=5000, ssl_context=(cert_path, key_path))
