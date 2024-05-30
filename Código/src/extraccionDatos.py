import json
import discogs_client


def searchDiscogs(keyword):
    try:
        inicio = 0
        fin = inicio + 6
        d = discogs_client.Client(
            "TFG_discos", user_token="dmAPijsocOyiHNAfggGWoixCsBibEOfwlaiPQrEa"
        )
        resultados = list(d.search(keyword, type="release"))
        fin = min(fin, len(resultados))
        if resultados:
            collection = []
            for resultado in resultados[inicio:fin]:
                try:
                    tracklist = []
                    for song in resultado.tracklist:
                        song = {"songTitle": song.title, "songDuration": song.duration}
                        tracklist.append(song)
                    item = {
                        "title": resultado.title,
                        "artists": resultado.artists[0].name,
                        "tracklist": tracklist,
                        "format": resultado.formats[0]["name"],
                        "year": resultado.year,
                        "country": resultado.country,
                        "idDisco": resultado.master.id,
                        "idArtista": resultado.artists[0].id,
                        "imageUrl": resultado.images[0]["resource_url"],
                    }
                    collection.append(item)
                except (AttributeError, IndexError, KeyError):
                    # Saltar el item si hay una excepción porque falten datos o alguno esté corrupto
                    continue
            resultados = json.dumps(collection)
        return resultados
    except IndexError:
        print("Error: se ha introducido un código de barras que no existe")
    except TypeError:
        print(Exception)


def searchDiscogsAdvanced(search):
    try:
        title = str(search[0])
        artist = str(search[1])
        year = str(search[2])
        format = str(search[3])
        country = str(search[4])
        barcode = str(search[5])
        inicio = 0
        fin = inicio + 6
        d = discogs_client.Client(
            "TFG_discos", user_token="dmAPijsocOyiHNAfggGWoixCsBibEOfwlaiPQrEa"
        )
        resultados = list(
            d.search(
                type="release", title=title, artist=artist, year=year, format=format, country=country, barcode=barcode
            )
        )
        fin = min(fin, len(resultados))
        if resultados:
            collection = []
            for resultado in resultados[inicio:fin]:
                try:
                    tracklist = []
                    for song in resultado.tracklist:
                        song = {"songTitle": str(song.title), "songDuration": str(song.duration)}
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
            resultados = json.dumps(collection)
        return resultados
    except IndexError:
        print("Error: se ha introducido un código de barras que no existe")
