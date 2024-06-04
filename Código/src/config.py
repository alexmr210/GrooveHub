### Fichero de configuración


from flask import Flask


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
    MAIL_PASSWORD = "fxiinnlvizvhrynq"
    MAIL_TECH = "groovehubtechnicalservice@gmail.com"


config = Config


def init():
    global app
    app = Flask(__name__)
    app.config.from_object(Config)
