from flask import Flask, jsonify, redirect, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf import CSRFProtect
from flask_mail import Mail, Message
from config import config as p
from routes import auth_routes, error_routes
from db import *
from models import *

app = Flask(__name__)
app.config.from_object(p)
login_manager_app = LoginManager()
csrf = CSRFProtect()
mail = Mail(app)


@login_manager_app.user_loader
def load_user(id):
    return session.query(User).where(User.id == id).first()


@app.route("/")
def index():
    return redirect(url_for("auth.login"))


@app.route("/home")
def home():
    return render_template("home.html")


# BORRAR v
# Ejemplo de ruta protegida (Requiere iniciar sesión)
@app.route("/protected")
@login_required
def protected():
    return "Esta es una vista protegida, solo para usuarios autenticados."


# Función de prueba para la conexión a BD
@app.route("/users")
def users():
    users = session.query(User)
    user_list = [{"username": user.username, "id": user.id} for user in users]
    return jsonify({"users": user_list})


@app.route("/hash/<password>")
def hash_password(password):
    hashed_value = generate_password_hash(password)
    return hashed_value


# BORRAR ^

if __name__ == "__main__":
    # Configuration
    app.config.from_object(p)

    # Blueprints
    app.register_blueprint(auth_routes.main, url_prefix="/auth")
    # app.register_blueprint(error_routes.main, url_prefix='/error')

    # Error handling
    app.register_error_handler(401, error_routes.status_401)
    app.register_error_handler(404, error_routes.status_404)

    # Start
    csrf.init_app(app)
    login_manager_app.init_app(app)
    app.run()
