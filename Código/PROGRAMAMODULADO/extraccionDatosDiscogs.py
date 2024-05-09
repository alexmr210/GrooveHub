import discogs_client

class extraccionDatosDiscogs:
    def deteccionCodigoBarrasLista(listaCodigoBarras):
        if isinstance(listaCodigoBarras, list):
            arrayTitulo=[]
            arrayArtista=[]
            arrayCanciones=[]
            arrayEdicion=[]
            arrayAgno=[]
            arrayPaisEdicionDisco=[]
            arrayidDisco=[]   
            arrayidArtista=[]
            for codigo_barras in listaCodigoBarras:
                titulo, artista, canciones, edicion, agno, paisEdicionDisco, idDisco, idArtista=extraccionDatosDiscogs.extraer_discogs(codigo_barras)
                arrayTitulo.append(titulo)
                arrayArtista.append(artista)
                arrayCanciones.append(canciones)
                arrayEdicion.append(edicion)
                arrayAgno.append(agno)
                arrayPaisEdicionDisco.append(paisEdicionDisco)
                arrayidDisco.append(idDisco)
                arrayidArtista.append(idArtista)
            return arrayTitulo, arrayArtista, arrayCanciones, arrayEdicion, arrayAgno, arrayPaisEdicionDisco, arrayidDisco, arrayidArtista
        else:
            titulo, artista, canciones, edicion, agno, paisEdicionDisco, idDisco, idArtista=extraccionDatosDiscogs.extraer_discogs(listaCodigoBarras)  
            return titulo, artista, canciones, edicion, agno, paisEdicionDisco, idDisco, idArtista       
               

    def extraer_discogs(codigo_barras):
        """Extrae toda la información a partir del código de barras

        >>> extraccionDatosDiscogs.extraer_discogs("314 526 013-2")
        ('Bon Jovi - Cross Road', [<Artist 124541 'Bon Jovi'>], [<Track '1' "Livin' On A Prayer">, <Track '2' 'Keep The Faith'>, <Track '3' "Someday I'll Be Saturday Night">, <Track '4' 'Always'>, <Track '5' 'Wanted Dead Or Alive'>, <Track '6' 'Lay Your Hands On Me'>, <Track '7' 'You Give Love A Bad Name'>, <Track '8' 'Bed Of Roses'>, <Track '9' 'Blaze Of Glory'>, <Track '10' "Prayer '94">, <Track '11' 'Bad Medicine'>, <Track '12' "I'll Be There For You">, <Track '13' 'In & Out Of Love'>, <Track '14' 'Runaway'>], 'CD', 1994, 'US', 96114, 124541)
        >>> extraccionDatosDiscogs.extraer_discogs("uhdsiu")
        Error: se ha introducido un código de barras que no existe
        >>> extraccionDatosDiscogs.extraer_discogs(2376484736-98)
        Error de tipo de dato introducido por el parámetro de la función
        """
        try:
            #Se introduce el id y token de la API para conectarnos para conectarnos con la base de datos de discogs
            d = discogs_client.Client('TFG_discos', user_token="dmAPijsocOyiHNAfggGWoixCsBibEOfwlaiPQrEa")  
            #una vez conectados, hacemos una busqueda en la base de datos de discogs con el codigo de barras que pasamos a esta función como parámetro
            #el cual es obtenido o de introducir el codigo de barras previamente por teclado o de obtenerlo a través de la webcam
            
            
            resultados = d.search(codigo_barras, type='release')
            #print("results "+str(results))  #<discogs_client.models.MixedPaginatedList object at 0x103125130>
            #print("results[0] "+str(results[0]))    #<Release 3092528 'Bon Jovi - Cross Road'>
            #de los resultados de la busqueda
            #Mostramos todos los resultados con ese código de barras de artista y titulo
            i=0
            #if resultados:
            if resultados:  #Solo si hay resultados ponemos valor a todas las variables que devuelve la funcion 
                for resultado in resultados:    #Recorremos el array resultados
                    print(f"Opción {i}: {resultado.title}")    #Para mostrar todos los resultados con ese código de barras 
                    i+=1
                numeroOpcionElegido=input("Introduce el número de opción que deseas: ")
                titulo = resultados[int(numeroOpcionElegido)].title    #cogemos el titulo
                #print("titulo "+str(titulo))    #Bon Jovi - Cross Road
                artista = resultados[int(numeroOpcionElegido)].artists    #cogemos el artista    
                #print("artista "+str(artista))  #[<Artist 124541 'Bon Jovi'>]
                canciones = resultados[int(numeroOpcionElegido)].tracklist    #cogemos las canciones
                #print("canciones "+str(canciones))  
                #[<Track '1' "Livin' On A Prayer">, <Track '2' 'Keep The Faith'>, <Track '3' "Someday I'll Be Saturday Night">, <Track '4' 'Always'>, <Track '5' 'Wanted Dead Or Alive'>, 
                #<Track '6' 'Lay Your Hands On Me'>, <Track '7' 'You Give Love A Bad Name'>, <Track '8' 'Bed Of Roses'>, <Track '9' 'Blaze Of Glory'>, <Track '10' "Prayer '94">, 
                #<Track '11' 'Bad Medicine'>, <Track '12' "I'll Be There For You">, <Track '13' 'In & Out Of Love'>, <Track '14' 'Runaway'>]
                edicion = resultados[int(numeroOpcionElegido)].formats[0]['name'] #cogemos la primera columna de la clave name de la primera columna de formats
                #print("results[0].formats "+str(results[0].formats))    #[{'name': 'CD', 'qty': '1', 'descriptions': ['Compilation']}]
                #print("results[0].formats[0] "+str(results[0].formats[0]))  #{'name': 'CD', 'qty': '1', 'descriptions': ['Compilation']}
                #print("edicion "+str(edicion))  #CD
                agno = resultados[int(numeroOpcionElegido)].year  #Cogemos el año
                #print("agno "+str(agno))    #1994
                paisEdicionDisco= resultados[int(numeroOpcionElegido)].country    #Cogemos el pais de edicion del disco
                #print("paisEdicionDisco "+str(paisEdicionDisco))    #US
                #id discos e id artistas como hash
                idDisco = resultados[int(numeroOpcionElegido)].master.id  #Cogemos el id del disco
                #print("results[0].master "+str(results[0].master))  #<Master 96114 'Cross Road (The Best Of Bon Jovi)'>
                #print("idDisco "+str(idDisco))  #96114
                idArtista = resultados[int(numeroOpcionElegido)].artists[0].id    #Cogemos el id del artista   
                #print("results[0].artists "+str(results[0].artists))    #[<Artist 124541 'Bon Jovi'>]
                #print("results[0].artists[0] "+str(results[0].artists[0]))  #<Artist 124541 'Bon Jovi'>
                #print("idArtista "+str(idArtista))  #124541

                for cancion in canciones:   #Recorremos las filas de canciones           
                    duracion=cancion.duration   #de cada fila cogemos la duracion de la cancion y la almacenamos en la variable
                    #print("cancion "+str(cancion))  #<Track '1' "Livin' On A Prayer">
                    #print("duracion "+str(duracion))    #4:11   
                #else:
                #    print("No se encuentran resultados para ese código de barras")
            else:   #Por que si no por el return pone que se referencian variables antes de asignarlas valor
                titulo=None
                artista=None
                canciones=None
                edicion=None
                agno=None
                paisEdicionDisco=None
                idDisco=None
                idArtista=None
            return titulo, artista, canciones, edicion, agno, paisEdicionDisco, idDisco, idArtista

        except IndexError:
            print("Error: se ha introducido un código de barras que no existe")
        except TypeError:
            print("Error de tipo de dato introducido por el parámetro de la función")