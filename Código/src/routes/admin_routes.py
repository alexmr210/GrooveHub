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
    db_delete_lost_disks,
    get_all_disks_page,
    get_all_disks_page_filter,
    get_artists_amount_all,
    get_disks_amount_all,
    get_disks_amount_all_filter,
    get_favourite_format_all,
    get_songs_amount,
    get_users,
    db_delete_user,
    find_userid,
    db_modify_user,
    get_all_disks,
    db_delete_disk,
    get_disk,
    db_modify_disk,
    get_users_amount,
    get_users_page,
    get_users_page_filter,
)

main = Blueprint("admin", __name__)


@main.route("/admin")
def auth():
    return redirect(url_for("admin.view_users"))


@main.route("/home")
def home():
    check_admin()
    return render_template("admin/home_admin.html")


@main.route("/users", methods=["GET", "POST"])
@login_required
def view_users():
    check_admin()
    page = max(1, request.args.get("page", type=int, default=1))
    if request.method == "POST":
        search = request.form["search"]
        filterBy = request.form["filter-by"]
        if filterBy != "None":
            collectionData = get_users_page_filter(
                current_user.id_usuario, page, filterBy, search
            )
        else:
            collectionData = get_users_page(current_user.id_usuario, page)
    else:
        collectionData = get_users_page(page)
        filterBy, search = None, None
    return render_template("admin/users.html", userData=collectionData, page=page)


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


@main.route("/disks", methods=["GET", "POST"])
@login_required
def view_disks():
    check_admin()
    page = max(1, request.args.get("page", type=int, default=1))
    if request.method == "POST":
        search = request.form["search"]
        filterBy = request.form["filter-by"]
        if filterBy != "None":
            collectionData = get_all_disks_page_filter(
                page, filterBy, search
            )
            disksAmount = get_disks_amount_all_filter(filterBy, search)
        else:
            collectionData = get_all_disks_page(current_user.id_usuario, page)
            disksAmount = get_disks_amount_all(current_user.id_usuario)
    else:
        collectionData = get_all_disks_page(page)
        filterBy, search = None, None
    artistsAmount = get_artists_amount_all()
    disksAmount = get_disks_amount_all()
    pagesAmount = (disksAmount + 9) // 10
    favouriteFormat = get_favourite_format_all()
    usersAmount = get_users_amount()
    return render_template(
        "admin/disks_admin.html",
        collectionData=collectionData,
        artists=artistsAmount,
        disks=disksAmount,
        page=page,
        pagesAmount=pagesAmount,
        favouriteFormat=favouriteFormat,
        filterBy=filterBy,
        search=search,
        users=usersAmount,
    )


@main.route("/delete-disk/<idEdicion>")
@login_required
def delete_disk(idEdicion):
    check_admin()
    db_delete_disk(idEdicion)
    flash(f"Se ha eliminado el disco con ID {idEdicion}.")
    return redirect(url_for("admin.view_disks"))


@main.route("/delete-lost-disks")
@login_required
def delete_lost_disks():
    check_admin()
    db_delete_lost_disks()
    flash(f"Se han eliminado los discos sin usuarios asociados.")
    return redirect(url_for("admin.view_disks"))


@main.route("/details/<idEdicion>")
@login_required
def details(idEdicion):
    collectionData = get_disk(idEdicion)
    return render_template("admin/details_admin.html", collectionData=collectionData)


@main.route("/modify/<idEdicion>", methods=["GET", "POST"])
@login_required
def modify_disk(idEdicion):
    check_admin()
    if request.method == "POST":
        tracklist = []
        original_songs_amount = get_songs_amount(idEdicion)
        newTracklist = []
        index = 0
        while True:
            song_id = request.form.get(f"tracklist[{index}][songId]")
            song_title = request.form.get(f"tracklist[{index}][songTitle]")
            song_duration = request.form.get(f"tracklist[{index}][songDuration]")
            delete = request.form.get(f"tracklist[{index}][delete]")
            # Si no se encuentra una canción en el índice actual, terminamos el bucle
            if index >= original_songs_amount:
                break
            tracklist.append(
                {
                    "songTitle": song_title,
                    "songDuration": song_duration,
                    "songId": song_id,
                    "delete": delete,
                }
            )
            index += 1
        index = 0
        new_songs_amount = int(request.form.get("new_songs_amount"))
        while True:
            song_title = request.form.get(f"newTracklist[{index}][songTitle]")
            song_duration = request.form.get(f"newTracklist[{index}][songDuration]")
            # Si ya se han leído todas las canciones nuevas, terminamos el bucle
            if index >= new_songs_amount:
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
        }
        db_modify_disk(disk)
        flash("Se han realizado los cambios correctamente.")
        return redirect(url_for("admin.view_disks"))
    else:
        diskData = get_disk(idEdicion)
        return render_template("admin/modify_disk_admin.html", diskData=diskData)


def check_admin():
    if not current_user.admin:
        session["layout"] = "./layout.html"
        abort(403)
    else:
        session["layout"] = "./admin/layout_admin.html"
        print("ADMIN")
