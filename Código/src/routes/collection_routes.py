import math
from flask import Blueprint, flash, render_template, redirect, request, session, url_for
from flask_login import login_required, current_user
from extraccionDatos import *
from data import *
from db import (
    get_artists_amount,
    get_collection,
    get_collection_page,
    get_collection_page_filter,
    get_disk,
    db_delete_user_disk,
    db_insert_disk,
    get_disks_amount,
    get_disks_amount_filter,
    get_favourite_format,
)
from utils import not_empty, send_modification_email

main = Blueprint("collection", __name__)


@main.route("/")
def auth():
    return redirect(url_for("collection.disks"))


@main.route("/disks", methods=["GET", "POST"])
@login_required
def disks():
    print(request.args.get("page"))
    page = max(1, request.args.get("page", type=int, default=1))
    if request.method == "POST":
        search = request.form["search"]
        filterBy = request.form["filter-by"]
        if filterBy != 'None':
            collectionData = get_collection_page_filter(
                current_user.id_usuario, page, filterBy, search
            )
            disksAmount = get_disks_amount_filter(current_user.id_usuario, filterBy, search)
        else:
            collectionData = get_collection_page(current_user.id_usuario, page)
            disksAmount = get_disks_amount(current_user.id_usuario)
    else:
        collectionData = get_collection_page(current_user.id_usuario, page)
        disksAmount = get_disks_amount(current_user.id_usuario)
        filterBy, search = None, None
    artistsAmount = get_artists_amount(current_user.id_usuario)
    pagesAmount = (disksAmount + 9) // 10
    favouriteFormat = get_favourite_format(current_user.id_usuario)
    if pagesAmount <= 0:
        pagesAmount = 1
    return render_template(
        "collection/disks.html",
        collectionData=collectionData,
        artists=artistsAmount,
        disks=disksAmount,
        page=page,
        pagesAmount=pagesAmount,
        favouriteFormat=favouriteFormat,
        filterBy=filterBy,
        search=search,
    )


@main.route("/details/<idEdicion>")
@login_required
def details(idEdicion):
    collectionData = get_disk(idEdicion)
    return render_template("collection/details.html", collectionData=collectionData)


@main.route("/insert", methods=["GET", "POST"])
@login_required
def insert():
    if request.method == "POST":
        scanned = False
        advanced = False
        if "search" in request.form:
            search = request.form["search"]
        elif (
            "title" in request.form
            or "artist" in request.form
            or "year" in request.form
            or "format" in request.form
            or "country" in request.form
            or "barcode" in request.form
        ):
            advanced = True
            title = request.form["title"]
            artist = request.form["artist"]
            year = request.form["year"]
            format = request.form["format"]
            country = request.form["country"]
            barcode = request.form["barcode"]
            search = [title, artist, year, format, country, barcode]
        elif "search" in request.json:
            scanned = True
            search = request.json["search"]
        else:
            flash("No se ha proporcionado un término de búsqueda válido.")
            return redirect(url_for("main.insert"))
        if search != None and search != "" and search != []:
            session["firstSelectOption"] = False
            if type(search) == str:
                options = [searchDiscogs(search)]
                auxSearch = []
                auxSearch.append(search)
            elif advanced:
                if not_empty(search):
                    options = [searchDiscogsAdvanced(search)]
                    auxSearch = []
                    auxSearch.append(search)
                else:
                    flash(
                        "No se ha introducido ningún valor. Por favor, inténtalo de nuevo."
                    )
                    return render_template("collection/insert.html")
            elif scanned:
                options = searchDiscogsList(search)
                auxSearch = search
                session["firstSelectOption"] = True
            if options:
                session["optionsList"] = options
                session["codesList"] = auxSearch
                return redirect(url_for("collection.select"))
            else:
                flash("No se han encontrado resultados para esta búsqueda.")
                return render_template("collection/insert.html")
        else:
            flash("No se ha introducido ningún valor. Por favor, inténtalo de nuevo.")
        return render_template("collection/insert.html")
    else:
        if "pendingMessage" in session:
            flash(session["pendingMessage"])
            del session["pendingMessage"]
        return render_template("collection/insert.html")


@main.route("/select")
@login_required
def select():
    if "pendingMessage" in session:
        flash(session["pendingMessage"])
        del session["pendingMessage"]
    if session.get("firstSelectOption"):
        session["firstSelectOption"] = False
        return render_template("collection/insert_select.html", options=[], code="0")
    else:
        try:
            session["firstSelectOption"] = False
            optionsList = session.get("optionsList")  # Objeto list
            options = optionsList.pop(0)
            session["optionsList"] = optionsList
            codesList = session.get("codesList")
            code = codesList.pop(0)
            session["codesList"] = codesList
            session["lastSearch"] = len(optionsList) == 0
            if options:
                session["options"] = options
                session["code"] = code
                options = json.loads(options)
                return render_template(
                    "collection/insert_select.html", options=options, code=code
                )
            else:
                flash("No se han encontrado resultados.")
                return render_template(
                    "collection/insert_select.html", options=options, code=code
                )
        except IndexError:
            flash("¡Vaya! Algo no ha ido como debería.")
            return redirect(url_for("collection.insert"))


@main.route("/selected")
@login_required
def selected():
    if "optionSelected" in request.args:
        numero = int(request.args.get("optionSelected")) - 1
        options = json.loads(session.get("options"))
        option = options[numero]
        tracklist = []
        duracionCanciones = []
        for song in option["tracklist"]:
            tracklist.append(song["songTitle"])
            duracionCanciones.append(song["songDuration"])
        hashEdicionDisco = generarHashEdicionDisco(
            option["year"], option["country"], option["format"], option["title"]
        )
        hashCanciones = generarHashCanciones(
            option["idArtista"], option["idDisco"], tracklist
        )
        idUsuario = current_user.id_usuario
        inserted = db_insert_disk(
            option["artists"],
            option["title"],
            tracklist,
            option["format"],
            option["year"],
            hashEdicionDisco,
            hashCanciones,
            option["country"],
            option["idDisco"],
            option["idArtista"],
            option["imageUrl"],
            duracionCanciones,
            idUsuario,
        )

        if inserted:
            pendingMessage = "Se ha añadido el disco seleccionado a tu colección."
        else:
            pendingMessage = (
                "Ya tienes ese disco en tu colección. No se han realizado cambios."
            )
        # session["pendingMessage"] = pendingMessage
        flash(pendingMessage)
    if session.get("lastSearch"):
        return redirect(url_for("collection.disks"))
    else:
        return redirect(url_for("collection.select"))


@main.route("/modify/<idEdicion>", methods=["GET", "POST"])
@login_required
def modify(idEdicion):
    if request.method == "POST":
        tracklist = []
        index = 0
        while True:
            original_song_title = request.form.get(
                f"tracklist[{index}][originalSongTitle]"
            )
            song_title = request.form.get(f"tracklist[{index}][songTitle]")
            original_song_duration = request.form.get(
                f"tracklist[{index}][originalSongDuration]"
            )
            song_duration = request.form.get(f"tracklist[{index}][songDuration]")

            # Si no se encuentra una canción en el índice actual, terminamos el bucle
            if not song_title:
                break

            tracklist.append(
                {
                    "originalSongTitle": original_song_title,
                    "songTitle": song_title,
                    "originalSongDuration": original_song_duration,
                    "songDuration": song_duration,
                }
            )
            index += 1
        disk = {
            "title": request.form["title"],
            "artists": request.form["artists"],
            "tracklist": tracklist,
            "format": request.form["format"],
            "year": request.form["year"],
            "country": request.form["country"],
            "idDisco": request.form["idDisco"],
            "idArtista": request.form["idArtista"],
            "idEdicion": request.form["idEdicion"],
            "observations": request.form["observations"],
        }
        send_modification_email(disk)
        flash(
            "Gracias por tu ayuda. Hemos notificado al administrador para que revise los cambios necesarios."
        )
        return redirect(url_for("collection.disks"))
    else:
        diskData = get_disk(idEdicion)
        return render_template("collection/modify_register.html", diskData=diskData)


@main.route("/delete/<idEdicion>")
@login_required
def delete(idEdicion):
    db_delete_user_disk(idEdicion, current_user.id_usuario)
    flash("Se ha eliminado el disco seleccionado.")
    return redirect(url_for("collection.disks"))
