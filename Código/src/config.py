### Fichero de configuración

class Config:
    SECRET_KEY = "C0ntr453ña."
    DEBUG = True
    DB_HOST = "localhost"
    DB_USER = "postgres"
    DB_PASS = "postgres"
    DB_PORT = "5432"
    DB_NAME = "prueba_usuarios"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "dummyempresa16@gmail.com"
    MAIL_PASSWORD = "fxiinnlvizvhrynq"

config = Config
