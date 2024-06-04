from flask import flash
from config import config as p
from sqlalchemy import create_engine, text
from models import *
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

# Creamos el motor sobre el que se conectará
database_url = (
    "postgresql://"
    + p.DB_USER
    + ":"
    + p.DB_PASS
    + "@"
    + p.DB_HOST
    + ":"
    + p.DB_PORT
    + "/"
    + p.DB_NAME
)
engine = create_engine(database_url)
connection = engine.connect()
Base.metadata.create_all(engine)

# Creamos la sesión a través de la cual haremos las consultas
Session = sessionmaker(bind=engine)
session = Session()


# Comprobar datos para iniciar sesión como usuario
def db_login(inUsername, inPassword):
    try:
        dbUser = find_username(inUsername)
        if dbUser:
            dbUser.correctPassword = check_password_hash(dbUser.contrasena, inPassword)
            dbUser.admin = dbUser.role == "ADMIN"
            return dbUser
        else:
            return None
    except Exception as ex:
        raise Exception(ex)


# Buscar usuario por username
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


def find_userid(id):
    try:
        return session.query(User).where(User.id_usuario == id).first()
    except Exception as ex:
        raise Exception(ex)


# Crear nuevo usuario
def db_signup(inUsername, inName, inPassword, inEmail):
    try:
        if find_username(inUsername):
            flash("El nombre de usuario ya está en uso")
            return False
        elif find_email(inEmail):
            flash("Ya existe una cuenta con ese correo electrónico")
            return False
        else:
            inPassword = generate_password_hash(inPassword)
            inId = generate_password_hash(inUsername)
            user = User(
                id_usuario=inId,
                username=inUsername,
                nombre=inName,
                email=inEmail,
                contrasena=inPassword,
                role="USER",
            )
            session.add(user)
            session.commit()
            return True
    except Exception as ex:
        raise Exception(ex)


def change_password(user, password):
    hash = generate_password_hash(password)
    session.query(User).filter(User.username == user.username).update(
        {"contrasena": hash}
    )
    session.commit
    return True


def db_insert_disk(
    artista,
    titulo,
    canciones,
    edicion,
    agno,
    hashEdicionesDisco,
    hashCanciones,
    pais,
    idDisco,
    idArtista,
    caratula,
    duracionCanciones,
    usuario,
):

    inserted = False
    # Comprobamos si existe el artista
    artista = modString(artista)
    query = f"SELECT * FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO WHERE A.ID_ARTISTA='{idArtista}'"
    result = connection.execute(text(query))
    row = result.fetchone()
    if row is None:  # El artista no está en la base de datos
        query = f"INSERT INTO ARTISTAS (id_artista, artista) VALUES ('{idArtista}','{artista}')"
        connection.execute(text(query))
        inserted = True

    titulo = modString(titulo)
    query = f"SELECT * FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO WHERE A.ID_ARTISTA='{idArtista}' AND D.ID_DISCO='{idDisco}'"
    result = connection.execute(text(query))
    row = result.fetchone()
    if row is None:  # El disco no está en la base de datos
        query = f"INSERT INTO DISCOS (id_disco, titulo, id_artista) VALUES ('{idDisco}','{titulo}','{idArtista}')"
        connection.execute(text(query))
        inserted = True

    # Comprobamos si este usuario ya tiene esta edición
    query = f"SELECT * FROM EDICIONES_DISCO WHERE id_edicion='{hashEdicionesDisco}'"
    result = connection.execute(text(query))
    row = result.fetchone()
    if row is None:
        edicion = modString(edicion)
        pais = modString(pais)
        query = f"INSERT INTO EDICIONES_DISCO (id_edicion, id_disco, edicion, agno, pais, caratula) VALUES ('{hashEdicionesDisco}','{idDisco}','{edicion}','{agno}','{pais}','{caratula}')"
        connection.execute(text(query))
        inserted = True

    query = f"SELECT * FROM EDICIONES_USUARIO WHERE id_edicion='{hashEdicionesDisco}' AND id_usuario='{usuario}'"
    result = connection.execute(text(query))
    row = result.fetchone()
    if row is None:
        query = f"INSERT INTO EDICIONES_USUARIO(id_edicion, id_usuario) VALUES ('{hashEdicionesDisco}','{usuario}')"
        connection.execute(text(query))
        inserted = True

    # Insercion de canciones
    contador = 0
    for cancion in canciones:
        # Comprobar si ya existe la canción
        cancion = modString(cancion)
        query = f"SELECT * FROM CANCIONES WHERE ID_CANCION='{hashCanciones[contador]}'"
        connection.execute(text(query))
        result = connection.execute(text(query))
        row = result.fetchone()
        if row is None:  # La canción no está en la base de datos
            query = f"INSERT INTO CANCIONES (id_cancion, cancion, duracion) VALUES ('{hashCanciones[contador]}','{cancion}','{duracionCanciones[contador]}')"
            connection.execute(text(query))
            query = f"INSERT INTO ARTISTAS_CANCIONES (id_artista, id_cancion) VALUES ('{idArtista}','{hashCanciones[contador]}')"
            connection.execute(text(query))
            query = f"INSERT INTO DISCOS_CANCIONES (id_disco, id_cancion) VALUES ('{idDisco}','{hashCanciones[contador]}')"
            connection.execute(text(query))
            inserted = True
        contador += 1

    connection.commit()
    return inserted


def get_collection(usuario):
    query = f"""SELECT A.ID_ARTISTA, A.ARTISTA, D.ID_DISCO, D.TITULO, ED.ID_EDICION, ED.EDICION, ED.AGNO, ED.PAIS, EU.ID_USUARIO, ED.CARATULA FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
        INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
        WHERE EU.ID_USUARIO='{usuario}' ORDER BY D.TITULO ASC"""
    result = connection.execute(text(query))
    rows = result.fetchall()
    collection = []
    for row in rows:
        item = {
            "title": row.titulo,
            "artists": row.artista,
            "tracklist": 0,  # Para acceder a la tracklist se utilizará la función get_tracklist(idDisco)
            "format": row.edicion,
            "year": row.agno,
            "country": row.pais,
            "idDisco": row.id_disco,
            "idArtista": row.id_artista,
            "imageUrl": row.caratula,
        }
        collection.append(item)
    return collection


def get_tracklist(idDisco):
    query = f"""SELECT CA.id_cancion, CA.cancion, CA.duracion, DC.id_disco
        FROM CANCIONES CA INNER JOIN DISCOS_CANCIONES DC ON CA.ID_CANCION=DC.ID_CANCION
        WHERE DC.ID_DISCO='{idDisco}'"""
    result = connection.execute(text(query))
    rows = result.fetchall()
    tracklist = []
    for row in rows:
        song = {
            "idCancion": row.id_cancion,
            "songTitle": row.cancion,
            "songDuration": row.duracion,
            "idDisco": row.id_disco,
        }
        tracklist.append(song)
    query = f"SELECT titulo FROM DISCOS WHERE ID_DISCO='{idDisco}'"
    result = connection.execute(text(query))
    titulo = result.fetchone()[0]
    return tracklist


def get_disk(idDisco):
    query = f"SELECT * FROM ediciones_disco WHERE id_disco='{idDisco}'"
    edition = connection.execute(text(query)).fetchone()
    query = f"SELECT * FROM discos WHERE id_disco='{idDisco}'"
    disk = connection.execute(text(query)).fetchone()
    idArtista = disk.id_artista
    query = f"SELECT * FROM artistas WHERE id_artista='{idArtista}'"
    artist = connection.execute(text(query)).fetchone()
    info = {
        "title": disk.titulo,
        "artists": artist.artista,
        "tracklist": get_tracklist(idDisco),
        "format": edition.edicion,
        "year": edition.agno,
        "country": edition.pais,
        "idDisco": idDisco,
        "idArtista": idArtista,
        "idEdicion": edition.id_edicion,
        "imageUrl": edition.caratula,
    }
    return info


def db_delete_user_disk(idDisco, usuario):
    # Buscamos el id_edicion
    query = f"""SELECT EU.id_edicion FROM ediciones_usuario EU INNER JOIN ediciones_disco ED ON EU.id_edicion=ED.id_edicion
        WHERE ED.id_disco='{idDisco}' AND EU.id_usuario='{usuario}'"""
    result = session.execute(text(query))
    rows = result.fetchall()
    idEdicion = rows[0].id_edicion

    query = f"SELECT titulo FROM discos WHERE id_disco='{idDisco}'"
    result = session.execute(text(query))
    title = result.fetchall()[0].titulo

    query = f"SELECT caratula FROM ediciones_disco WHERE id_disco='{idDisco}'"
    result = session.execute(text(query))
    image = result.fetchall()[0].caratula

    query = f"DELETE FROM ediciones_usuario WHERE id_edicion='{idEdicion}' AND id_usuario='{usuario}'"
    result = session.execute(text(query))
    session.commit()

    return title, image


def modString(string):
    return string.replace("'", "''")


def get_six(user):
    query = f"""SELECT A.ID_ARTISTA, A.ARTISTA, D.ID_DISCO, D.TITULO, ED.ID_EDICION, ED.EDICION, ED.AGNO, ED.PAIS, EU.ID_USUARIO, ED.CARATULA FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
        INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
        WHERE EU.ID_USUARIO='{user}' ORDER BY RANDOM() LIMIT 6"""
    result = connection.execute(text(query))
    rows = result.fetchall()
    collection = []
    for row in rows:
        item = {
            "title": row.titulo,
            "artists": row.artista,
            "format": row.edicion,
            "year": row.agno,
            "country": row.pais,
            "idDisco": row.id_disco,
            "imageUrl": row.caratula,
        }
        collection.append(item)
    return collection


def get_users():
    query = f"""SELECT * FROM usuarios"""
    result = connection.execute(text(query))
    rows = result.fetchall()
    collection = []
    for row in rows:
        item = {
            "idUsuario": row.id_usuario,
            "username": row.username,
            "name": row.nombre,
            "email": row.email,
            "role": row.role,
        }
        collection.append(item)
    return collection


def db_delete_user(idUsuario):
    try:
        query = f"DELETE FROM ediciones_usuario WHERE id_usuario='{idUsuario}'"
        result = session.execute(text(query))
        query = f"SELECT * FROM usuarios WHERE id_usuario='{idUsuario}'"
        username = session.execute(text(query)).fetchone().username
        query = f"DELETE FROM usuarios WHERE id_usuario='{idUsuario}'"
        result = session.execute(text(query))
        session.commit()
        return username
    except Exception as e:
        session.rollback()
        flash(f"Error al modificar el usuario: {str(e)}")

def db_delete_user(isUsuario):
    try:
        query = f"DELETE FROM ediciones_usuario WHERE id_usuario='{isUsuario}'"
        result = session.execute(text(query))
        query = f"SELECT * FROM usuarios WHERE id_usuario='{isUsuario}'"
        username = session.execute(text(query)).fetchone().username
        query = f"DELETE FROM usuarios WHERE id_usuario='{isUsuario}'"
        result = session.execute(text(query))
        session.commit()
        return username
    except Exception as e:
        session.rollback()
        flash(f"Error al modificar el usuario: {str(e)}")


def db_modify_user(user):
    try:
        query = text(
            """UPDATE usuarios
            SET username=:username, nombre=:nombre, email=:email, role=:role
            WHERE id_usuario=:id_usuario"""
        )
        session.execute(
            query,
            {
                "username": user["username"],
                "nombre": user["name"],
                "email": user["email"],
                "role": user["role"],
                "id_usuario": user["id"],
            },
        )
        session.commit()
    except Exception as e:
        session.rollback()
        flash(f"Error al modificar el usuario: {str(e)}")
