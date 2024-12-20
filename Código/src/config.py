### Fichero de configuración


from datetime import timedelta
from flask import Flask
# from flask_sslify import SSLify


class Config:
    SECRET_KEY = "C0ntr453ña."
    DEBUG = True
    DB_HOST = "localhost"
    DB_USER = "postgres"
    DB_PASS = "postgres"
    DB_PORT = "5432"
    DB_NAME = "discos_2"
    # DB_NAME = "prueba_usuarios"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "dummyempresa16@gmail.com"
    MAIL_PASSWORD = "wffthsctymdqjzfk"
    MAIL_TECH = "groovehubtechnicalservice@gmail.com"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=45)


config = Config


def init():
    global app
    app = Flask(__name__)
    # SSLify(app)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
