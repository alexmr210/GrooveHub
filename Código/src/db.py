from flask import flash
from config import config as p
from sqlalchemy import create_engine
from models import *
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

# Creamos el motor sobre el que se conectará
database_url = ("postgresql://" + p.DB_USER + ":" + p.DB_PASS + "@" + p.DB_HOST + ":" + p.DB_PORT + "/" + p.DB_NAME)
engine = create_engine(database_url)
connection = engine.connect()
Base.metadata.create_all(engine)

# Creamos la sesión a través de la cual haremos las consultas
Session = sessionmaker(bind=engine)
session = Session()

#Comprobar datos para iniciar sesión como usuario
def db_login(inUsername, inPassword):
    try:
        dbUser = find_username(inUsername)
        if (dbUser):
            dbUser.correctPassword = check_password_hash(dbUser.password, inPassword)
            return dbUser
        else:
            return None
    except Exception as ex:
        raise Exception(ex)

#Buscar usuario por username
def find_username(username):
    try:
        return session.query(User).where(User.username == username).first()
    except Exception as ex:
        raise Exception(ex)
    
def find_email(email):
    try:
        return session.query(User).where(User.email == email).first()
    except Exception as ex:
        raise Exception(ex)
    
#Crear nuevo usuario
def db_signup(inUsername, inName, inPassword, inEmail):
    try:
        if (find_username(inUsername)):
            flash("El nombre de usuario ya está en uso")
            return False
        elif (find_email(inEmail)):
            flash("Ya existe una cuenta con ese correo electrónico")
            return False
        else:
            inPassword = generate_password_hash(inPassword)
            user = User(
                username=inUsername,
                name=inName,
                email=inEmail,
                password=inPassword
            )
            session.add(user)
            session.commit()
            return True
    except Exception as ex:
        raise Exception(ex)
    
def change_password(user, password):
    hash = generate_password_hash(password)
    session.query(User).filter(User.username == user.username).update({'password': hash})
    session.commit
    return True