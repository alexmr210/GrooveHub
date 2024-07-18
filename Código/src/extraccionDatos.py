import json
import discogs_client
import discogs_client.exceptions
from flask import abort


def searchDiscogs(keyword):
    try:
        d = discogs_client.Client(
            "TFG_discos", user_token="dmAPijsocOyiHNAfggGWoixCsBibEOfwlaiPQrEa"
        )
        resultados = list(d.search(keyword, type="release"))
        if resultados:
            resultados = getCollection(resultados)
        return resultados
    except IndexError:
        print("Error: se ha introducido un código de barras que no existe")
    except discogs_client.exceptions.HTTPError:
        abort(429)



def searchDiscogsList(search):
    search = removeDuplicates(search)
    resultados = []
    for keyword in search:
        resultados.append(searchDiscogs(keyword))
    return resultados


def searchDiscogsAdvanced(search):
    try:
        title = str(search[0])
        artist = str(search[1])
        year = str(search[2])
        format = str(search[3])
        country = str(search[4])
        barcode = str(search[5])
        d = discogs_client.Client(
            "TFG_discos", user_token="dmAPijsocOyiHNAfggGWoixCsBibEOfwlaiPQrEa"
        )
        resultados = list(
            d.search(
                type="release",
                title=title,
                artist=artist,
                year=year,
                format=format,
                country=country,
                barcode=barcode,
            )
        )
        if resultados:
            resultados = getCollection(resultados)
        return resultados
    except IndexError:
        print("Error: se ha introducido un código de barras que no existe")


def getCollection(resultados):
    collection = []
    inicio = 0
    fin = min(inicio + 6, len(resultados))
    for resultado in resultados[inicio:fin]:
        try:
            tracklist = []
            for song in resultado.tracklist:
                song = {
                    "songTitle": str(song.title),
                    "songDuration": str(song.duration),
                }
                tracklist.append(song)
            item = {
                "title": str(resultado.title),
                "artists": str(resultado.artists[0].name),
                "tracklist": tracklist,
                "format": str(resultado.formats[0]["name"]),
                "year": str(resultado.year),
                "country": str(resultado.country),
                "idDisco": str(resultado.master.id),
                "idArtista": str(resultado.artists[0].id),
                "imageUrl": str(resultado.images[0]["resource_url"]),
            }
            collection.append(item)
        except (AttributeError, IndexError, KeyError, TypeError):
            # Saltar el item si hay una excepción porque falten datos o alguno esté corrupto
            continue
    return json.dumps(collection)


def removeDuplicates(input_list):
    seen = set()
    output_list = []
    for item in input_list:
        if item not in seen:
            seen.add(item)
            output_list.append(item)
    return output_list
