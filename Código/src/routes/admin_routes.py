from flask import (
    Blueprint,
    abort,
    flash,
    render_template,
    redirect,
    request,
    session,
    url_for,
)
from flask_login import login_required, current_user
from extraccionDatos import *
from data import *
from db import (
    get_users,
    db_delete_user,
    find_userid,
    db_modify_user,
    get_all_disks,
    db_delete_disk,
    get_disk,
    db_modify_disk
)

main = Blueprint("admin", __name__)


@main.route("/admin")
def auth():
    return redirect(url_for("admin.view_users"))

@main.route("/home")
def home():
    check_admin()
    return render_template("admin/home_admin.html")

@main.route("/users")
@login_required
def view_users():
    check_admin()
    userData = get_users()
    return render_template("admin/users.html", userData=userData)


@main.route("/modify-user/<idUsuario>", methods=["GET", "POST"])
@login_required
def modify_user(idUsuario):
    check_admin()
    if request.method == "POST":
        user = {
            "id": idUsuario,
            "username": request.form["username"],
            "name": request.form["name"],
            "email": request.form["email"],
            "role": request.form["role"],
        }
        db_modify_user(user)
        print(user)
        flash("En desarrollo")
        return redirect(url_for("admin.view_users"))
    else:
        userData = find_userid(idUsuario)
        user = {
            "id": userData.id_usuario,
            "username": userData.username,
            "name": userData.nombre,
            "email": userData.email,
            "role": userData.role,
        }
        return render_template("admin/modify-user.html", user=user)


@main.route("/delete-user/<idUsuario>")
@login_required
def delete_user(idUsuario):
    username = db_delete_user(idUsuario)
    flash("Se ha eliminado el usuario " + username + ".")
    return redirect(url_for("admin.view_users"))


@main.route("/disks")
@login_required
def view_disks():
    check_admin()
    collection = get_all_disks()
    return render_template("admin/disks_admin.html", collectionData=collection)


@main.route("/delete-disk/<idDisco>")
@login_required
def delete_disk(idDisco):
    check_admin()
    db_delete_disk(idDisco)
    flash(f"Se ha eliminado el disco con ID {idDisco}.")
    return redirect(url_for("admin.view_disks"))


@main.route("/modify/<idDisco>", methods=["GET", "POST"])
@login_required
def modify_disk(idDisco):
    check_admin()
    if request.method == "POST":
        tracklist = []
        newTracklist = []
        index = 0
        while True:
            song_id = request.form.get(f"tracklist[{index}][songId]")
            song_title = request.form.get(f"tracklist[{index}][songTitle]")
            song_duration = request.form.get(f"tracklist[{index}][songDuration]")
            delete = request.form.get(f"tracklist[{index}][delete]")
            # Si no se encuentra una canción en el índice actual, terminamos el bucle
            if not song_title:
                break

            tracklist.append(
                {
                    "songTitle": song_title,
                    "songDuration": song_duration,
                    "songId": song_id,
                    "delete": delete
                }
            )
            index += 1
        index = 0
        while True:
            song_title = request.form.get(f"newTracklist[{index}][songTitle]")
            song_duration = request.form.get(f"newTracklist[{index}][songDuration]")
            # Si no se encuentra una canción en el índice actual, terminamos el bucle
            if not song_title:
                break
            newTracklist.append(
                {
                    "songTitle": song_title,
                    "songDuration": song_duration,
                }
            )
            index += 1
        disk = {
            "title": request.form["title"],
            "artists": request.form["artists"],
            "tracklist": tracklist,
            "newTracklist": newTracklist,
            "format": request.form["format"],
            "year": request.form["year"],
            "country": request.form["country"],
            "idDisco": request.form["idDisco"],
            "idArtista": request.form["idArtista"],
            "idEdicion": request.form["idEdicion"],
            "observations": request.form["observations"],
        }
        db_modify_disk(disk)
        flash("Se han realizado los cambios correctamente.")
        return redirect(url_for("admin.view_disks"))
    else:
        diskData = get_disk(idDisco)
        return render_template("admin/modify_disk_admin.html", diskData=diskData)

@main.route("/modify/<idArtista>", methods=["GET", "POST"])
@login_required
def modify_artist(idArtista):
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
        # send_modification_email(disk)
        flash(
            "Gracias por tu ayuda. Hemos notificado al administrador para que revise los cambios necesarios."
        )
        return redirect(url_for("collection.view"))
    else:
        diskData = get_disk(idDisco)
        return render_template("admin/modify_disk_admin.html", diskData=diskData)


def check_admin():
    if not current_user.admin:
        session["layout"]="./layout.html"
        abort(403)
    else:
        session["layout"]="./admin/layout_admin.html"
        print("ADMIN")