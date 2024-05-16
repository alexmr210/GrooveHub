from flask import Blueprint, flash, render_template, redirect, request, session, url_for
from flask_login import login_required, current_user
from extraccionDatos import *
from data import *
from db import db_insert_disk, get_collection, get_tracklist, db_delete_disk

# from PROGRAMAMODULADO import extraccionDatosDiscogs as edd

main = Blueprint("collection", __name__)


@main.route("/")
def auth():
    return redirect(url_for("collection.view"))


@main.route("/general-view")
@login_required
def view():
    collectionData = get_collection(current_user.id_usuario)
    return render_template(
        "collection/general_view.html", collectionData=collectionData
    )


@main.route("/tracklist/<idDisco>")
@login_required
def tracklist(idDisco):
    collectionData = get_tracklist(idDisco)
    return render_template("collection/tracklist.html", collectionData=collectionData)


@main.route("/insert", methods=["GET", "POST"])
@login_required
def insert():
    if request.method == "POST":
        if "search" in request.form:
            search = request.form["search"]
        elif "search" in request.json:
            search = request.json["search"]
        else:
            flash("No se ha proporcionado un término de búsqueda válido.")
            return redirect(url_for("main.insert"))
        if search != None:
            opciones = searchDiscogs(search)
            if opciones:
                session["opciones"] = opciones
                return redirect(url_for("collection.select"))
            else:
                flash("No hay coincidencias. Por favor, intenta de nuevo.")
                return render_template("collection/insert.html")
        else:
            flash("Error al realizar la búsqueda. Por favor, inténtalo de nuevo.")
        return render_template("collection/insert.html")
    else:

        if "pendingMessage" in session:
            flash(session["pendingMessage"])
            del session["pendingMessage"]
        return render_template("collection/insert.html")


@main.route("/select")
@login_required
def select():
    opciones = json.loads(session.get("opciones"))
    if opciones:
        return render_template("collection/insert_select.html", opciones=opciones)
    else:
        flash("Ha habido un error. Por favor, intenta buscar de nuevo.")
        return render_template("collection/insert.html")


@main.route("/selected")
@login_required
def selected():
    numero = int(request.args.get("option")) - 1
    opciones = json.loads(session.get("opciones"))
    opcion = opciones[numero]
    tracklist = []
    duracionCanciones = []
    for song in opcion["tracklist"]:
        tracklist.append(song["songTitle"])
        duracionCanciones.append(song["songDuration"])
    hashEdicionDisco = generarHashEdicionDisco(
        opcion["year"], opcion["country"], opcion["format"], opcion["title"]
    )
    hashCanciones = generarHashCanciones(
        opcion["idArtista"], opcion["idDisco"], tracklist
    )
    idUsuario = current_user.id_usuario
    inserted = db_insert_disk(
        opcion["artists"],
        opcion["title"],
        tracklist,
        opcion["format"],
        opcion["year"],
        hashEdicionDisco,
        hashCanciones,
        opcion["country"],
        opcion["idDisco"],
        opcion["idArtista"],
        opcion["imageUrl"],
        duracionCanciones,
        idUsuario,
    )

    if inserted:
        pendingMessage = "Se ha añadido el disco seleccionado a tu colección."
    else:
        pendingMessage = (
            "Ya tienes ese disco en tu colección. No se han realizado cambios."
        )
    session["pendingMessage"] = pendingMessage
    return redirect(url_for("collection.insert"))


@main.route("/search-register")
@login_required
def search():
    return render_template("collection/search_register.html")


@main.route("/modify-register")
@login_required
def modify():
    return render_template("collection/modify_register.html")


@main.route("/delete/<idDisco>")
@login_required
def delete(idDisco):
    title, image = db_delete_disk(idDisco, current_user.id_usuario)
    # collectionData = get_tracklist(idDisco)
    return render_template("collection/delete_register.html", title=title, image=image)
