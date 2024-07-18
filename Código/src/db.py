from flask import flash
from config import config as p
from sqlalchemy import create_engine, text
from data import generarHashCanciones
from models import *
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

# Creamos el motor sobre el que se conectará
database_url = f"postgresql://{p.DB_USER}:{p.DB_PASS}@{p.DB_HOST}:{p.DB_PORT}/{p.DB_NAME}"
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

# Buscar usuarios según distintos campos
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

# Modificar contraseña de un usuario
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
    query = f"SELECT * FROM ARTISTAS WHERE ID_ARTISTA='{idArtista}'"
    result = connection.execute(text(query))
    row = result.fetchone()
    if row is None:  # El artista no está en la base de datos
        query = f"INSERT INTO ARTISTAS (id_artista, artista) VALUES ('{idArtista}','{artista}')"
        connection.execute(text(query))
        inserted = True

    titulo = modString(titulo)
    query = (
        f"SELECT * FROM DISCOS WHERE ID_ARTISTA='{idArtista}' AND ID_DISCO='{idDisco}'"
    )
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

def get_collection_page(usuario, page):
    min = (page-1) * 10
    query = f"""SELECT A.ARTISTA, D.ID_DISCO, D.TITULO, ED.ID_EDICION, ED.EDICION, ED.AGNO, ED.PAIS, ED.CARATULA
        FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA INNER JOIN EDICIONES_DISCO ED
            ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
        WHERE EU.ID_USUARIO='{usuario}'
        ORDER BY ED.ID_EDICION ASC
        LIMIT 10 OFFSET {min}"""
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
            "idEdicion": row.id_edicion,
        }
        collection.append(item)
    return collection

def get_collection_page_filter(usuario, page, filterBy, search):
    min = (page-1) * 10
    search = remove_accents(search)
    query = f"""SELECT A.ARTISTA, D.ID_DISCO, D.TITULO, ED.ID_EDICION, ED.EDICION, ED.AGNO, ED.PAIS, ED.CARATULA
        FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA INNER JOIN EDICIONES_DISCO ED
            ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
        WHERE EU.ID_USUARIO='{usuario}'
        AND UPPER ({filterBy}) LIKE UPPER('%{search}%')
        ORDER BY ED.ID_EDICION ASC
        LIMIT 10 OFFSET {min}"""
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
            "idEdicion": row.id_edicion,
        }
        collection.append(item)
    return collection

def get_favourite_format(usuario):
    query = f"""SELECT ED.edicion, COUNT(*) as count
        FROM ediciones_disco ED INNER JOIN ediciones_usuario EU ON EU.id_edicion = ED.id_edicion
        WHERE EU.id_usuario = '{usuario}'
        GROUP BY ED.edicion
        ORDER BY count DESC
        LIMIT 1"""
    result = connection.execute(text(query)).fetchall()
    if result:
        return result[0].edicion
    else:
        return "hmm... aún no lo tenemos claro"

def get_favourite_format_all():
    query = f"""SELECT ED.edicion, COUNT(*) as count
        FROM ediciones_disco ED INNER JOIN ediciones_usuario EU ON EU.id_edicion = ED.id_edicion
        GROUP BY ED.edicion
        ORDER BY count DESC
        LIMIT 1"""
    result = connection.execute(text(query))
    return result.fetchall()[0].edicion

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

def get_disk(idEdicion):
    query = f"SELECT * FROM ediciones_disco WHERE id_edicion='{idEdicion}'"
    edition = connection.execute(text(query)).fetchone()
    query = f"SELECT * FROM discos WHERE id_disco='{edition.id_disco}'"
    disk = connection.execute(text(query)).fetchone()
    idArtista = disk.id_artista
    query = f"SELECT * FROM artistas WHERE id_artista='{idArtista}'"
    artist = connection.execute(text(query)).fetchone()
    info = {
        "title": disk.titulo,
        "artists": artist.artista,
        "tracklist": get_tracklist(edition.id_disco),
        "format": edition.edicion,
        "year": edition.agno,
        "country": edition.pais,
        "idDisco": edition.id_disco,
        "idArtista": idArtista,
        "idEdicion": edition.id_edicion,
        "imageUrl": edition.caratula,
    }
    return info

def get_all_disks():
    query = f"""SELECT A.ID_ARTISTA, A.ARTISTA, D.ID_DISCO, D.TITULO, ED.ID_EDICION, ED.EDICION, ED.AGNO, ED.PAIS, ED.CARATULA
        FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
        INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO
        ORDER BY D.TITULO ASC"""
    result = connection.execute(text(query))
    rows = result.fetchall()
    collection = []
    for row in rows:
        query = f"SELECT COUNT(*) FROM ediciones_usuario WHERE id_edicion = '{row.id_edicion}'"
        amount = session.execute(text(query)).fetchone()[0]
        item = {
            "title": row.titulo,
            "artists": row.artista,
            "tracklist": 0,  # Para acceder a la tracklist se utilizará la función get_tracklist(idDisco)
            "format": row.edicion,
            "year": row.agno,
            "country": row.pais,
            "idDisco": row.id_disco,
            "idArtista": row.id_artista,
            "idEdicion": row.id_edicion,
            "imageUrl": row.caratula,
            "amount": amount,
        }
        collection.append(item)
    return collection

def get_all_disks_page(page):
    min = (page-1) * 10
    query = f"""SELECT A.ID_ARTISTA, A.ARTISTA, D.ID_DISCO, D.TITULO, ED.ID_EDICION, ED.EDICION, ED.AGNO, ED.PAIS, ED.CARATULA
        FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
        INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO
        ORDER BY ED.ID_EDICION ASC
        LIMIT 10 OFFSET {min}"""
    result = connection.execute(text(query))
    rows = result.fetchall()
    collection = []
    for row in rows:
        query = f"SELECT COUNT(*) FROM ediciones_usuario WHERE id_edicion = '{row.id_edicion}'"
        amount = session.execute(text(query)).fetchone()[0]
        item = {
            "title": row.titulo,
            "artists": row.artista,
            "format": row.edicion,
            "year": row.agno,
            "country": row.pais,
            "idDisco": row.id_disco,
            "idEdicion": row.id_edicion,
            "imageUrl": row.caratula,
            "amount": amount,
        }
        collection.append(item)
    return collection

def get_all_disks_page_filter(page, filterBy, search):
    min = (page-1) * 10
    search = remove_accents(search)
    query = f"""SELECT A.ARTISTA, D.ID_DISCO, D.TITULO, ED.ID_EDICION, ED.EDICION, ED.AGNO, ED.PAIS, ED.CARATULA
        FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA INNER JOIN EDICIONES_DISCO ED
            ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
        AND UPPER ({filterBy}) LIKE UPPER('%{search}%')
        ORDER BY ED.ID_EDICION ASC
        LIMIT 10 OFFSET {min}"""
    result = connection.execute(text(query))
    rows = result.fetchall()
    collection = []
    for row in rows:
        query = f"SELECT COUNT(*) FROM ediciones_usuario WHERE id_edicion = '{row.id_edicion}'"
        amount = session.execute(text(query)).fetchone()[0]
        item = {
            "title": row.titulo,
            "artists": row.artista,
            "format": row.edicion,
            "year": row.agno,
            "country": row.pais,
            "idDisco": row.id_disco,
            "idEdicion": row.id_edicion,
            "imageUrl": row.caratula,
            "amount": amount,
        }
        collection.append(item)
    return collection

def db_delete_user_disk(idEdicion, usuario):
    query = f"DELETE FROM ediciones_usuario WHERE id_edicion='{idEdicion}' AND id_usuario='{usuario}'"
    session.execute(text(query))
    session.commit()

def db_delete_disk(idEdicion):
    query = f"SELECT * FROM ediciones_disco WHERE id_edicion = '{idEdicion}'"
    idDisco = session.execute(text(query)).fetchone().id_disco
    query = f"DELETE FROM ediciones_usuario WHERE id_edicion = '{idEdicion}'"  # Eliminamos las ediciones de ediciones_usuario
    session.execute(text(query))
    query = f"DELETE FROM ediciones_disco WHERE id_edicion = '{idEdicion}'"  # Eliminamos las ediciones de ediciones_disco
    session.execute(text(query))
    # Comprobamos si el disco sigue teniendo alguna edicion y si no, lo eliminamos
    query = f"SELECT COUNT(*) FROM ediciones_disco WHERE id_disco = '{idDisco}'"
    result = session.execute(text(query)).fetchone()[0]
    if result > 0:
        session.commit()
    else:
        db_delete_edition(idDisco)
        db_delete_tracklist(idDisco)
        query = f"SELECT * FROM discos WHERE id_disco = '{idDisco}'"
        idArtista = session.execute(text(query)).fetchone().id_artista
        query = f"DELETE FROM discos WHERE id_disco = '{idDisco}'"  # Eliminamos el disco
        session.execute(text(query))
        db_delete_artist(idArtista)
        session.commit()

def db_modify_disk(disk):
    db_modify_tracklist(disk["tracklist"])
    db_modify_edition(disk)
    db_modify_artist(disk)
    query = f"""UPDATE discos SET
        titulo='{disk["title"]}'
        WHERE id_disco='{disk["idDisco"]}'"""
    session.execute(text(query))

    # CANCIONES
    newTracklist = []
    duracionCanciones = []
    for song in disk["newTracklist"]:
        newTracklist.append(song["songTitle"])
        duracionCanciones.append(song["songDuration"])
    hashCanciones = generarHashCanciones(
            disk["idArtista"], disk["idDisco"], newTracklist
        )
	# Insercion de canciones
    contador = 0
    for cancion in disk["newTracklist"]:
        # Comprobar si ya existe la canción
        cancion = modString(cancion["songTitle"])
        query = f"SELECT * FROM CANCIONES WHERE ID_CANCION='{hashCanciones[contador]}'"
        session.execute(text(query))
        result = session.execute(text(query))
        row = result.fetchone()
        if row is None:  # La canción no está en la base de datos
            query = f"INSERT INTO CANCIONES (id_cancion, cancion, duracion) VALUES ('{hashCanciones[contador]}','{cancion}','{duracionCanciones[contador]}')"
            session.execute(text(query))
            query = f"INSERT INTO ARTISTAS_CANCIONES (id_artista, id_cancion) VALUES ('{disk["idArtista"]}','{hashCanciones[contador]}')"
            session.execute(text(query))
            query = f"INSERT INTO DISCOS_CANCIONES (id_disco, id_cancion) VALUES ('{disk["idDisco"]}','{hashCanciones[contador]}')"
            session.execute(text(query))
            inserted = True
        contador += 1
    session.commit()

def db_modify_tracklist(tracklist):
    for song in tracklist:
        if song["delete"] == "True":
            query = f"DELETE FROM artistas_canciones WHERE id_cancion='{song["songId"]}'"
            session.execute(text(query))
            query = f"DELETE FROM discos_canciones WHERE id_cancion='{song["songId"]}'"
            session.execute(text(query))
            query = f"DELETE FROM canciones WHERE id_cancion='{song["songId"]}'"
            session.execute(text(query))
        else:
            query = f"UPDATE canciones SET cancion='{song["songTitle"]}', duracion='{song["songDuration"]}' WHERE id_cancion='{song["songId"]}'"
            session.execute(text(query))

def db_modify_edition(disk):
    query = f"""UPDATE ediciones_disco SET
        edicion='{disk["format"]}', agno='{disk["year"]}', pais='{disk["country"]}'
        WHERE id_edicion='{disk["idEdicion"]}'"""
    session.execute(text(query))

def db_modify_artist(disk):
    query = f"""UPDATE artistas SET
        artista='{disk["artists"]}'
        WHERE id_artista='{disk["idArtista"]}'"""
    session.execute(text(query))

def db_delete_artist(idArtista):
    query = f"SELECT COUNT(*) FROM discos WHERE id_artista = '{idArtista}'"  # Cuantos discos hay de este artista
    amount = session.execute(text(query)).fetchone()[0]
    if amount != 0:
        return "Hay discos asociadaos a este artista."
    query = f"SELECT COUNT(*) FROM artistas_canciones WHERE id_artista = '{idArtista}'"  # Cuantas canciones hay de este artista
    amount = session.execute(text(query)).fetchone()[0]
    if amount != 0:
        return "Hay canciones asociadas a este artista."
    query = (
        f"DELETE FROM artistas WHERE id_artista = '{idArtista}'"  # Eliminamos el disco
    )
    session.execute(text(query))
    session.commit()
    return f"Se ha eliminado el artista con ID {idArtista}."

def db_delete_tracklist(idDisco):
    query = f"SELECT id_cancion FROM discos_canciones WHERE id_disco = '{idDisco}'"
    result = session.execute(text(query)).fetchall()
    for row in result:
        songId = row[0]
        query = f"DELETE FROM discos_canciones WHERE id_cancion = '{songId}'"  # Eliminamos las canciones de discos_canciones
        result = session.execute(text(query))
        query = f"DELETE FROM artistas_canciones WHERE id_cancion = '{songId}'"  # Eliminamos las canciones de artistas_canciones
        result = session.execute(text(query))
        query = f"DELETE FROM canciones WHERE id_cancion = '{songId}'"  # Eliminamos las canciones de canciones
        result = session.execute(text(query))

def db_delete_edition(idDisco):
    query = f"SELECT id_edicion FROM ediciones_disco WHERE id_disco = '{idDisco}'"
    result = session.execute(text(query)).fetchall()
    for row in result:
        editionId = row[0]
        query = f"DELETE FROM ediciones_usuario WHERE id_edicion = '{editionId}'"  # Eliminamos las ediciones de ediciones_usuario
        result = session.execute(text(query))
        query = f"DELETE FROM ediciones_disco WHERE id_edicion = '{editionId}'"  # Eliminamos las ediciones de ediciones_disco
        result = session.execute(text(query))

def modString(string):
    return string.replace("'", "''")

def get_six(user):
    query = f"""SELECT A.ID_ARTISTA, A.ARTISTA, D.ID_DISCO, D.TITULO, ED.ID_EDICION, ED.EDICION, ED.AGNO, ED.PAIS, EU.ID_USUARIO, ED.CARATULA FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
        INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
        WHERE EU.ID_USUARIO='{user}' ORDER BY RANDOM() LIMIT 8"""
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
            "idEdicion": row.id_edicion
        }
        collection.append(item)
    return collection

def get_disks_amount(user):
    query = f"""SELECT COUNT(*) FROM ediciones_usuario WHERE id_usuario = '{user}'"""
    result = connection.execute(text(query))
    amount = result.fetchone()[0]
    return amount

def get_disks_amount_filter(usuario, filterBy, search):
    search = remove_accents(search)
    query = f"""SELECT COUNT(*)
        FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA INNER JOIN EDICIONES_DISCO ED
            ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
        WHERE EU.ID_USUARIO='{usuario}'
        AND UPPER ({filterBy}) LIKE UPPER('%{search}%')"""
    result = connection.execute(text(query))
    amount = result.fetchone()[0]
    return amount

def get_artists_amount(user):
    query = f"""SELECT COUNT(DISTINCT artista) FROM
        ediciones_usuario AS EU INNER JOIN ediciones_disco AS ED ON eu.id_edicion = ED.id_edicion
        INNER JOIN discos as DI ON ED.id_disco = DI.id_disco
        INNER JOIN artistas as AR ON DI.id_artista = AR.id_artista
        WHERE EU.id_usuario = '{user}'"""
    result = connection.execute(text(query))
    amount = result.fetchone()[0]
    return amount

def get_disks_amount_all():
    query = f"""SELECT COUNT(DISTINCT id_edicion) FROM ediciones_disco"""
    result = connection.execute(text(query))
    amount = result.fetchone()[0]
    return amount

def get_artists_amount_all():
    query = f"""SELECT COUNT(*) FROM artistas"""
    result = connection.execute(text(query))
    amount = result.fetchone()[0]
    return amount

def get_disks_amount_all_filter(filterBy, search):
    query = f"""SELECT COUNT(*)
        FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA INNER JOIN EDICIONES_DISCO ED
            ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
        AND UPPER ({filterBy}) LIKE UPPER('%{search}%')"""
    result = connection.execute(text(query))
    amount = result.fetchone()[0]
    return amount

def get_users_amount():
    query = f"""SELECT COUNT(*) FROM usuarios WHERE role != 'ADMIN'"""
    result = connection.execute(text(query))
    amount = result.fetchone()[0]
    return amount

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

def get_users_page_filter(page, filterBy, search):
    min = (page-1) * 10
    search = remove_accents(search)
    query = f"""SELECT * FROM usuarios WHERE UPPER ({filterBy}) LIKE UPPER('%{search}%') ORDER BY id_usuario ASC LIMIT 10 OFFSET {min}"""
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

def get_users_page(page):
    min = (page-1) * 10
    query = f"""SELECT * FROM usuarios ORDER BY id_usuario ASC LIMIT 10 OFFSET {min}"""
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

def db_get_disk(idDisco):
    try:
        return session.query(Disco).where(Disco.id_disco == idDisco).first()
    except Exception as ex:
        raise Exception(ex)

def db_delete_lost_disks():
    query = f"""SELECT ED.id_edicion
        FROM ediciones_disco ED
        LEFT JOIN ediciones_usuario EU
        ON EU.id_edicion = ED.id_edicion
        WHERE EU.id_edicion IS NULL"""
    result = session.execute(text(query)).fetchall()
    for row in result:
        db_delete_disk(row.id_edicion)
    session.commit()

def remove_accents(s):
    accents = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
        'À': 'A', 'È': 'E', 'Ì': 'I', 'Ò': 'O', 'Ù': 'U',
        'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o', 'ü': 'u',
        'Ä': 'A', 'Ë': 'E', 'Ï': 'I', 'Ö': 'O', 'Ü': 'U',
        'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
        'Â': 'A', 'Ê': 'E', 'Î': 'I', 'Ô': 'O', 'Û': 'U',
        'ã': 'a', 'õ': 'o', 'ñ': 'n',
        'Ã': 'A', 'Õ': 'O', 'Ñ': 'N',
        'ç': 'c', 'Ç': 'C'
    }
    
    return ''.join(accents.get(char, char) for char in s)

def get_songs_amount(idEdicion):
    query = f"SELECT * FROM ediciones_disco WHERE id_edicion = '{idEdicion}'"
    idDisco = session.execute(text(query)).fetchone().id_disco
    query = f"SELECT COUNT(*) FROM discos_canciones WHERE id_disco = '{idDisco}'"
    return session.execute(text(query)).fetchone().count