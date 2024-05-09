import hashlib      #para hash como id

import re   #para expresiones regulares

class tratamientoDatos:
    def deteccionParametrosHashCancionesLista(listaIdArtista, listaIdDisco, listaCancionesTratadas):
        if isinstance(listaIdArtista, list) or isinstance(listaIdDisco, list):   
            arrayHashHexadecimalCanciones=[]
            for idArtista, idDisco, cancionesTratadas in zip(listaIdArtista, listaIdDisco, listaCancionesTratadas):       
                hashHexadecimalCanciones= tratamientoDatos.generarHashCanciones(idArtista, idDisco, cancionesTratadas)
                arrayHashHexadecimalCanciones.append(hashHexadecimalCanciones)
            return arrayHashHexadecimalCanciones
        else:

            hashHexadecimalCanciones= tratamientoDatos.generarHashCanciones(listaIdArtista, listaIdDisco, listaCancionesTratadas)
            return hashHexadecimalCanciones

    def generarHashCanciones(idArtista, idDisco, cancionesTratadas): 
        #Se usa como id de las canciones   
        """_summary_

        >>> tratamientoDatos.generarHashCanciones(idArtista, idDisco, cancionesTratadas)
        ['3a605c554076cdca9460fb38303fbb954bd1d73ee06fd8b8ffe025c147c1ac6a', '557c8d1db9876bb6ff7ee0a08df5ab1ee4406000a03da0b98f7491b42ff93fe3', 'acc87fad4e21e44cbe8ca6cb84a29f5a85cccf84ea58d9341228db0c1431c672', 'dbe387329e429a62363d82af1aa6d89af4bb3c139e6e1777af2f8225fbb274e1', '21e4a6d2a69ceb84fa46c9cd032a9778d153f28c17e2981628deca5d88cd11da', '7dee851d776da9c18716291bde4544377fe771c7a771edfa6c69d00358ff0029', 'f686a6996c63902a3e98e024e59ae04b74541e6df1fc31f28417851cd062f43d', 'dcb39042b03dbe35f65cb540403cb6ed1a07cfc12833181230c8405255d9c623', 'c27f9fd3c9683e7eab3d1aa99b30d9224c6ca67382682cf18a88fb077926fbf6', '777756ba782df96f1943eb828346beedb5fcd8075270e2c2c0ec789daa222732', '2cd86c2e0fe726a112d62e8d9cb9815a8e5561812ad91c872e867ec40e1267c0', 'fbb3c2e30e76007ed56a3e35315e3ee101b3813603fa31b3e3355292d5c3ad0b', '167c6677b691add9811d5c9f9c9d0257f103fb922a0b8bf938fe931b01d3b410', '2bf19877981224cf0fb84e54571e4d354c41f28a74f50bd1ce04025d2031b93e']
        >>> tratamientoDatos.generarHashCanciones(idArtista, idDisco, 23432)
        Error: se esta introduciendo por los parámetros otros tipos de datos diferentes a los esperados
        """
        try:
            hashCanciones=[]    #Creo un array en el que almaceno los hash de todas las canciones
            for cancionTratada in cancionesTratadas:    #Recorro todo el array de cancionesTratadas 
                #en un texto concateno el id del artista con el id del disco y con la cancion tratada para que 
                #al convertirlo en un hash sea un hash unico
                infoHash = f"{idArtista}{idDisco}{cancionTratada}"   
                infoHash = infoHash.encode('utf-8') #Texto a bytes
                hash = hashlib.sha256(infoHash) #Calculamos hash de los datos
                hashHexadecimalCancion=hash.hexdigest() #Pasamos a hexadecimal el hash
                hashCanciones.append(hashHexadecimalCancion)    #Lo añadimos al array de hashCanciones
                #print(hashHexadecimalCancion)
                #print('hashHexadecimal: ', hashHexadecimal)                   
            return hashCanciones    #Retornamos el array hashCanciones
        except TypeError:
            print("Error: se esta introduciendo por los parámetros otros tipos de datos diferentes a los esperados") 
    
    def deteccionParametrosHashEdicionDiscoLista(listaAgno, listaPaisEdicionDisco, listaEdicion, listaTituloTratado):
        #Comprobamos si es lista listaAgno, listaPaisEdicionDisco, listaEdicion y listaTituloTratado          
        if isinstance(listaAgno, list) or isinstance(listaAgno, list) or isinstance(listaAgno, list) or isinstance(listaAgno, list):
            arrayHashHexadecimalEdicionDisco=[]
            for agno, paisEdicionDisco, edicion, tituloTratado in zip(listaAgno, listaPaisEdicionDisco, listaEdicion, listaTituloTratado):  
                hashHexadecimalEdicionesDisco = tratamientoDatos.generarHashEdicionDisco(agno, paisEdicionDisco, edicion, tituloTratado)  
                arrayHashHexadecimalEdicionDisco.append(hashHexadecimalEdicionesDisco)
            return arrayHashHexadecimalEdicionDisco
        else:
            hashHexadecimalEdicionDisco = tratamientoDatos.generarHashEdicionDisco(listaAgno, listaPaisEdicionDisco, listaEdicion, listaTituloTratado)
            return hashHexadecimalEdicionDisco    #retornamos el hash de edicion del disco
            

    def generarHashEdicionDisco(agno, paisEdicionDisco, edicion, tituloTratado): 
        #Se usa como id de las ediciones del disco 
        """_summary_

        >>> tratamientoDatos.generarHashEdicionDisco(agno, paisEdicionDisco, edicion, tituloTratado)
        '55eeb630a1d3ffb6cff8287becd9a5d62d2170c29e79816e5cf6afeaa2422278'
        """
        #En un texto concateno el agno de la edicion del disco con el pais de la edicion del disco
        #con la edicion del disco con el titulo del disco para que al convertirlo en un hash sea un hash unico
        infoHash = f"{agno}{paisEdicionDisco}{edicion}{tituloTratado}"   
        infoHash = infoHash.encode('utf-8') #Texto a bytes
        hash = hashlib.sha256(infoHash) #Calculamos hash de los datos
        hashHexadecimalEdicionDisco=hash.hexdigest()  #Pasamos a hexadecimal el hash
        #print('hashHexadecimal: ', hashHexadecimal)                   
        return hashHexadecimalEdicionDisco    #retornamos el hash de edicion del disco   
        
    def deteccionParametrosTratarDatosLista(listaArtista, listaTitulo, listaCanciones):
        #Comprobamos si es lista artistas y titulos, canciones de por si es una lista
        #En este caso comprobamos que lo sean los dos si o si ya que cuando introduces individual
        #El unico artista se guarda en lista pero titulo no
        if isinstance(listaArtista, list) and isinstance(listaTitulo, list):
            arrayArtistaTratado=[]
            arrayTituloTratado=[]
            arrayCancionesTratadas=[]
            arrayDuracionCanciones=[]
            #en canciones esta la lista de canciones de todos los artistas que haya detectado en diferentes códigos de barras
            #cancionesArtista sera lista de canciones de un unico codigo de barras
            for artista, titulo, cancionesUnCodigoBarras in zip(listaArtista, listaTitulo, listaCanciones): 
                artistaTratado, tituloTratado, cancionesTratadas, duracionCanciones= tratamientoDatos.tratarDatos(artista, titulo, cancionesUnCodigoBarras)
                arrayArtistaTratado.append(artistaTratado)
                arrayTituloTratado.append(tituloTratado)
                arrayCancionesTratadas.append(cancionesTratadas)
                arrayDuracionCanciones.append(duracionCanciones)
            return arrayArtistaTratado, arrayTituloTratado, arrayCancionesTratadas, arrayDuracionCanciones
        else:
            artistaTratado, tituloTratado, cancionesTratadas, duracionCanciones= tratamientoDatos.tratarDatos(listaArtista, listaTitulo, listaCanciones)
            return artistaTratado, tituloTratado, cancionesTratadas, duracionCanciones


             
    def tratarDatos(artista, titulo, canciones):
        """Trata los datos que es necesario tratar despues de sacarlos de discogs

        >>> tratamientoDatos.tratarDatos(artista, titulo, canciones)
        ('Bon Jovi', 'Cross Road', ['Livin', 'Keep The Faith', 'Someday Ill Be Saturday Night', 'Always', 'Wanted Dead Or Alive', 'Lay Your Hands On Me', 'You Give Love A Bad Name', 'Bed Of Roses', 'Blaze Of Glory', 'Prayer 94', 'Bad Medicine', 'Ill Be There For You', 'In & Out Of Love', 'Runaway'], ['4:11', '5:45', '4:38', '5:52', '5:07', '5:58', '3:43', '6:34', '5:40', '5:16', '5:14', '5:41', '4:23', '3:50'])
        >>> tratamientoDatos.tratarDatos("sdfuhwd", titulo, canciones)
        Error: no se consigue tratar alguno de los datos pasados por los parámetros porque no se encuentra el caracter que se quiere detectar para hacer split
        >>> tratamientoDatos.tratarDatos(798789, titulo, canciones)
        Error: se esta introduciendo por los parámetros otros tipos de datos diferentes a los esperados
        """
        try:               
            #print("artista "+str(artista))  #[<Artist 124541 'Bon Jovi'>] 
            #print("artista[0] "+str(artista[0]))    #<Artist 124541 'Bon Jovi'>
            strArtista=str(artista[0])
            artista_split=strArtista.split("'")
            artistaTratado=artista_split[1]
            #print("artistaTratado "+str(artistaTratado))    #Bon Jovi 
            #print("titulo "+str(titulo))    #Bon Jovi - Cross Road
            titulo_split=titulo.split(" - ")    #Se divide texto en antes y despues del guion
            #print("titulo_split "+str(titulo_split))    #['Bon Jovi', 'Cross Road']
            tituloTratado=titulo_split[1]   #Se coge texto de despues de guion y espacio en blanco     
            #print("tituloTratado "+str(tituloTratado))  #Cross Road


            cancionesTratadas=[]
            duracionCanciones=[]
            for cancion in canciones:   #Recorremos cada cancion que hay en canciones
                duracion=cancion.duration   #Sacamos la duracion de la cancion
                duracionCanciones.append(duracion)  #almacenamos la duracion en el array duracionCanciones

                strCancion=str(cancion) 
                cancion_split=strCancion.split("' ")    #Se divide texto en antes y despues del guion y espacio en blanco
                cancionTratada=cancion_split[1]   #Se coge texto de despues de guion y espacio en blanco
                cancionTratada2=cancionTratada.replace("'", "").replace('"', '').replace('>', '')
                #print("strCancion "+str(strCancion))    #<Track '1' "Livin' On A Prayer">
                #print("cancion_split "+str(cancion_split))  #["<Track '1", '"Livin', 'On A Prayer">']
                #print("cancionTratada "+str(cancionTratada))    #"Livin
                #print("cancionTratada2 "+str(cancionTratada2))  #Livin
                cancionesTratadas.append(cancionTratada2)   

            return artistaTratado, tituloTratado, cancionesTratadas, duracionCanciones
        except IndexError:
            print("Error: no se consigue tratar alguno de los datos pasados por los parámetros porque no se encuentra el caracter que se quiere detectar para hacer split")
        """except TypeError:
            print("Error: se esta introduciendo por los parámetros otros tipos de datos diferentes a los esperados")"""
    
    