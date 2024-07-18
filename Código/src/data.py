import hashlib

def generarHashEdicionDisco(agno, paisEdicionDisco, edicion, tituloTratado):
    infoHash = f"{agno}{paisEdicionDisco}{edicion}{tituloTratado}"
    infoHash = infoHash.encode("utf-8")
    hash = hashlib.sha256(infoHash)
    return hash.hexdigest()

def generarHashCanciones(idArtista, idDisco, canciones): 
        try:
            hashCanciones=[]
            for cancionTratada in canciones:
                infoHash = f"{idArtista}{idDisco}{cancionTratada}"   
                infoHash = infoHash.encode('utf-8')
                hash = hashlib.sha256(infoHash)
                hashCanciones.append(hash.hexdigest())               
            return hashCanciones
        except TypeError:
            print("Error: se esta introduciendo por los parámetros otros tipos de datos diferentes a los esperados") 