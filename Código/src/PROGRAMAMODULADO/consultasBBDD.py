import psycopg2

class consultasBBDD:
    def detectarParametrosInsertar_en_base_datosLista(listaArtistaTratado, listaTituloTratado, listaCancionesTratadas, listaEdicion, listaAgno, 
                               listaHashHexadecimalEdicionesDisco, listaHashHexadecimalCanciones, listaPaisEdicionDisco, listaIdDisco, listaIdArtista, listaDuracionCanciones, preguntarParametrosConexion):
        #print(f"listaArtistaTratado: {listaArtistaTratado}")
        #print(f"listaTituloTratado: {listaTituloTratado}")
        #print(f"listaEdicion: {listaEdicion}")
        #print(f"listaAgno: {listaAgno}")
        #print(f"listaHashHexadecimalEdicionesDisco: {listaHashHexadecimalEdicionesDisco}")
        #print(f"listaHashHexadecimalCanciones: {listaHashHexadecimalCanciones}")
        #print(f"listaPaisEdicionDisco: {listaPaisEdicionDisco}")
        #print(f"listaIdDisco: {listaIdDisco}")
        #print(f"listaIdArtista: {listaIdArtista}")
        #print(f"listaDuracionCanciones: {listaDuracionCanciones}")
        #No comprobamos si es lista listaCancionesTratadas, listaHashHexadecimalEdicionesDisco, listaDuracionCanciones y listaHashHexadecimalCanciones porque esos cuando se introduzca un solo disco
        #tambien seran lista siempre
        if (isinstance(listaArtistaTratado,list) or isinstance(listaTituloTratado,list) or isinstance(listaEdicion,list) or isinstance(listaAgno,list) 
            or isinstance(listaPaisEdicionDisco,list) or isinstance(listaIdDisco,list) or isinstance(listaIdArtista,list)): 
            for artistaTratado, tituloTratado, cancionesTratadas, edicion, agno, hashHexadecimalEdicionesDisco, hashHexadecimalCanciones, paisEdicionDisco, idDisco, idArtista, duracionCanciones in zip(
                listaArtistaTratado, listaTituloTratado, listaCancionesTratadas, listaEdicion, listaAgno, listaHashHexadecimalEdicionesDisco, listaHashHexadecimalCanciones, 
                listaPaisEdicionDisco, listaIdDisco, listaIdArtista, listaDuracionCanciones):
                consultasBBDD.insertar_en_base_datos(artistaTratado, tituloTratado, cancionesTratadas, edicion, agno, hashHexadecimalEdicionesDisco, 
                                                     hashHexadecimalCanciones, paisEdicionDisco, idDisco, idArtista, duracionCanciones, preguntarParametrosConexion)
        else:
            consultasBBDD.insertar_en_base_datos(listaArtistaTratado, listaTituloTratado, listaCancionesTratadas, listaEdicion, listaAgno, 
                               listaHashHexadecimalEdicionesDisco, listaHashHexadecimalCanciones, listaPaisEdicionDisco, listaIdDisco, listaIdArtista, listaDuracionCanciones, preguntarParametrosConexion)    
                
        
    def insertar_en_base_datos(artistaTratado, tituloTratado, cancionesTratadas, edicion, agno, 
                               hashHexadecimalEdicionesDisco, hashHexadecimalCanciones, paisEdicionDisco, idDisco, idArtista, duracionCanciones, preguntarParametrosConexion):
        #Se recibe por los parametros todos los datos que recibimos de discogs ya tratados, 
        #y ask_conn_parameters que contiene todos los datos para poder realizar la conexion con la base de datos en variables
        """_summary_

        Args:
            artistaTratado (_type_): _description_
            tituloTratado (_type_): _description_
            cancionesTratadas (_type_): _description_
            edicion (_type_): _description_
            agno (_type_): _description_
            hashHexadecimalEdicionesDisco (bool): _description_
            hashHexadecimalCanciones (bool): _description_
            paisEdicionDisco (_type_): _description_
            idDisco (_type_): _description_
            idArtista (_type_): _description_
            duracionCanciones (_type_): _description_
            ask_conn_parameters (_type_): _description_
        """
        # Obtener los parámetros de conexión
        (host, puerto, usuario, contrasena, baseDatos) = preguntarParametrosConexion    #se guarda en variables de la izquierda los argumentos que pasamos por terminal al ejecutar el programa

        # Se introducen los datos de la conexion
        datosConexion = f'host={host} port={puerto} user={usuario} password={contrasena} dbname={baseDatos}'

        # Nos conectamos a la base de datos introduciendo la variable datosConexion como parametro
        conexion = psycopg2.connect(datosConexion)


        # Creamos un cursor el cual usaremos despues para ejecutar las querys
        cursor = conexion.cursor()

        query=f"SELECT COUNT(*) FROM USUARIOS WHERE ID_USUARIO='{usuario}'"

        #Usamos el cursor para ejecutar la query que contiene la variable query
        cursor.execute(query)

        #Le pedimos al cursor que nos devuelva el resultado y lo guardamos en la variable results
        resultado = cursor.fetchall()

         #Recorremos las filas del resultado de la query
        for fila in resultado:
            cuentaFilasIdUsuario=fila[0]    #Cogemos la primera columna de la fila del resultado de la query
        
        if cuentaFilasIdUsuario==0:
            query=f"INSERT INTO USUARIOS (id_usuario, contrasena) VALUES ('{usuario}','{contrasena}')"

            #Usamos el cursor para ejecutar la query que contiene la variable query
            cursor.execute(query)
            
        #Query para comprobar si hay que evitar introducir artista porque ya existe pero se esta introduciendo una edicion diferente de esta
        #Si COUNT(*) es mayor que 0 significa que ya esta insertado el artista, el disco de ese artista y la edicion del disco de ese artista
        #A la query se le esta pasando para esto de condicion que el idArtista sea el que se le pasó al parámetro de la función
        query=f"SELECT COUNT(*) FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO WHERE A.ID_ARTISTA='{idArtista}'"

        #Usamos el cursor para ejecutar la query que contiene la variable query
        cursor.execute(query)

        #Le pedimos al cursor que nos devuelva el resultado y lo guardamos en la variable results
        resultado = cursor.fetchall()
        #print(resultado)    #[(0,)]
        #Recorremos las filas del resultado de la query
        for fila in resultado:  #row es un elemento de la lista resultados, recorremos todos los elementos de la lista resultados
            numeroEdicionesArtista=fila[0]   #Aseguramos coger la primera columna de la fila de la consulta, de ahi el [0]
            #print(fila) #(0,)
            #print(fila[0])  #0
        #Se introduce en SQL por orden de pk y fk, ya que la foreign key tiene que coincidir con una pk de otra tabla ya existente
        if numeroEdicionesArtista==0:   #Si el resultado de la anterior consulta es 0 significa que no hay ninguna edicion de ese artista, 
            #lo cual significa que no existe el artista en la tabla artistas
            #Por ello se introduce el id y nombre de artista en la tabla ARTISTAS
            insertarArtistaTratado=f"INSERT INTO ARTISTAS (id_artista, artista) VALUES ('{idArtista}','{artistaTratado}')"   
            cursor.execute(insertarArtistaTratado)  #y usando el cursor ejecutamos la query que contiene la variable insertarArtistaTratado
        
        #Comprobar si hay que evitar introducir disco porque ya existe ese disco de ese artista pero se esta introduciendo una edicion diferente de este disco
        query=f"SELECT COUNT(*) FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO WHERE A.ID_ARTISTA='{idArtista}' AND D.ID_DISCO='{idDisco}'"

        #Ejecuta la consulta
        cursor.execute(query)

        #Obtiene los resultados
        resultado = cursor.fetchall()

        #Recorremos las filas del resultado de la query
        for fila in resultado:
            numeroEdicionesDisco=fila[0]    #Cogemos la primera columna de la fila del resultado de la query
        
        if numeroEdicionesDisco==0: #Si la query anterior da de resultado 0 es que no hay ningun disco, y por tanto no hay ninguna edicion de disco tampoco de ese artista
            #Por tanto insertamos idDisco(PK), tituloTratado, e idArtista(FK)
            insertarDiscoTratado=f"INSERT INTO DISCOS (id_disco, titulo, id_artista) VALUES ('{idDisco}','{tituloTratado}','{idArtista}')" 
            cursor.execute(insertarDiscoTratado)    #ejecutamos la query insertarDiscoTratado
        #Si el if anterior no se cumpliera significaria que ya esta en BBDD ese disco y alguna edicion de ese disco para ese artista, por lo que en ese caso solo insertamos en la tabla
        #ediciones_disco ya que en la tabla artista y disco ya estan los datos insertados
        #el hash hexadecimal de ediciones disco (que en tabla va en id_edicion) se genera con la funcion generarHashEdicionesDisco de tratamientoDatos.py 
        #juntando antes de generar el hash las variables {agno}{paisEdicionDisco}{edicion}{tituloTratado}
        insertarEdicion=f"INSERT INTO EDICIONES_DISCO (id_edicion, id_disco, edicion, agno, pais) VALUES ('{hashHexadecimalEdicionesDisco}','{idDisco}','{edicion}','{agno}','{paisEdicionDisco}')"
        cursor.execute(insertarEdicion) #ejecutamos la query insertarEdicion

        insertarEdicionUsuario=f"INSERT INTO EDICIONES_USUARIO(id_edicion, id_usuario) VALUES ('{hashHexadecimalEdicionesDisco}','{usuario}')"
        cursor.execute(insertarEdicionUsuario) #ejecutamos la query insertarEdicionUsuario    

        #Insercion de canciones
        contador=0  #Variable contador que usamos en este bucle para incrementar los arrays que usamos para insertar en BBDD hashHexadecimalCanciones
        #Y duracionCanciones
        #Recorremos el array de cancionesTratadas
        for cancionTratada in cancionesTratadas:
            #Comprobar si hay que introducir canciones en tabla canciones o ya estan ahi de antes buscando si el id_cancion a introducir
            #ya existe en la tabla canciones o no
            query=f"SELECT COUNT(*) FROM CANCIONES WHERE ID_CANCION='{hashHexadecimalCanciones[contador]}'"

            #Ejecuta la consulta
            cursor.execute(query)

            #Obtiene los resultados
            resultado = cursor.fetchall()
            #Recorremos las filas del resultado de la query
            for fila in resultado:
                cantidadEsaCancion=fila[0]   #[0] para asegurar coger la primera columna de la fila del resultado de la query
            if cantidadEsaCancion==0:   #si de resultado de la query anterior sale 0 significa que esta cancion no esta en la tabla,
                                        #por lo que la insertamos en todas las tablas necesarias
                #hashHexadecimalCanciones es un hash que se genera despues de juntar los valores de las variables {idArtista}{idDisco}{cancionTratada},
                #todo ello en la funcion generarHashCanciones de tratamientoDatos.py y se introduce en la columna id_cancion
                #este hash es un array porque en la funcion que genera el hash se le pasan todas las canciones a insertar para generar un hash único con cada canción
                #el array duracionCanciones sale de la funcion tratarDatos de tratamientoDatos.py
                insertarCancionTratada=f"INSERT INTO CANCIONES (id_cancion, cancion, duracion) VALUES ('{hashHexadecimalCanciones[contador]}','{cancionTratada}','{duracionCanciones[contador]}')"
                cursor.execute(insertarCancionTratada)  #ejecutamos la query insertarCancionTratada
                insertarArtistasCanciones=f"INSERT INTO ARTISTAS_CANCIONES (id_artista, id_cancion) VALUES ('{idArtista}','{hashHexadecimalCanciones[contador]}')"
                cursor.execute(insertarArtistasCanciones)   #ejecutamos la query insertarArtistasCanciones
                insertarDiscosCanciones=f"INSERT INTO DISCOS_CANCIONES (id_disco, id_cancion) VALUES ('{idDisco}','{hashHexadecimalCanciones[contador]}')"
                cursor.execute(insertarDiscosCanciones) #ejecutamos la query insertarDiscosCanciones
            contador+=1

        cursor.close()  #Cerramos el cursor que estabamos usando para ejecutar las querys
        conexion.commit()   #Confirmamos los cambios que hacemos con los insert a la base de datos para que sean visibles en esta de forma permanente
        conexion.close()    #Cerramos la conexion

    def consultar_en_base_datos(numeroOpcion, preguntarParametrosConexion):
        #Se le pasa de parametros el numero de opcion que introduce el usuario para ejecutar la consulta que este desea
        #y ask_conn_parameters que contiene todos los datos de conexion en variables
        """_summary_

        Args:
            numeroOpcion (_type_): _description_
            ask_conn_parameters (_type_): _description_
        """
        # Obtener los parámetros de conexión
        (host, puerto, usuario, contrasena, baseDatos) = preguntarParametrosConexion

        # Crear la cadena de conexión
        datosConexion = f'host={host} port={puerto} user={usuario} password={contrasena} dbname={baseDatos}'
        # Conectar a la base de datos
        conexion = psycopg2.connect(datosConexion)
        cursor = conexion.cursor()  #Crear el cursor que usaremos para ejecutar las consultas   

        if numeroOpcion == "1": #Si el numero de opcion introducido es 1
            #Se pedira por pantalla que se introduzca por teclado el artista del que quieres saber los discos almacenados en BBDD
            artistaConsultar=input("Introduce el artista del que quieres saber los discos almacenados en BBDD: ")
            #Una vez introducido se pasara el artista escrito a una consulta que saque todos los titulos de disco 
            #que sean de ese artista introducido por teclado
            #Poniendo los fstrings con triple comilla puedo poner la consulta en varias lineas para que se vea mejor
            #Ponemos distinct para asegurar contar solo los titulos distintos, no repetidos que salgan varias veces
            #por los cruces de tabla (inner join) que tenemos
            query=f"""SELECT DISTINCT(D.TITULO) FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
            INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION 
            WHERE A.ARTISTA='{artistaConsultar}' AND EU.ID_USUARIO=CURRENT_USER"""

            #Ejecuta la consulta con el cursor
            cursor.execute(query)

            #Obtiene los resultados de la consulta usando el cursor y los almacena en la variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                print(fila[0])   #Imprime la primera columna de la fila del resultado de la query
        elif numeroOpcion == "2":   #Si el numero de opcion introducido es 2
            #Se ejecuta esta query que muestra el numero total de discos introducidos en base de datos 
            #por el usuario que entro en el programa
            #Poniendo los fstrings con triple comilla puedo poner la consulta en varias lineas para que se vea mejor
            #Ponemos distinct para asegurar contar solo los titulos distintos, no repetidos que salgan varias veces
            #por los cruces de tabla (inner join) que tenemos
            query=f"""SELECT COUNT(DISTINCT(D.TITULO)) FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
            INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION 
            WHERE EU.ID_USUARIO=CURRENT_USER""" 
            #Ejecuta la consulta usando el cursor
            cursor.execute(query)

            #Obtiene los resultados de la consulta usando el cursor y los almacena en la variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                #imprime texto que se ve concatenado con casting a string de la primera columna de la fila del resultado de la query
                print("Número de discos almacenados = "+str(fila[0]))    
        elif numeroOpcion == "3":   #Si el numero de opcion introducido es 3
            #Se ejecuta esta query que muestra el numero total de artistas introducidos en base de datos
            #por el usuario que entro en el programa
            #la query la ponemos con distinct ya que si no cuenta 
            #Ponemos distinct para asegurar contar solo los titulos distintos, no repetidos que salgan varias veces
            #por los cruces de tabla (inner join) que tenemos
            query=f"""SELECT COUNT(DISTINCT(A.ARTISTA)) FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
            INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
            WHERE EU.ID_USUARIO=CURRENT_USER"""   
            #Ejecuta la consulta usando el cursor
            cursor.execute(query)

            #Obtiene los resultados de la consulta usando el cursor
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                #imprime texto que se ve concatenado con casting a string de la primera columna de la fila del resultado de la query
                print("Número de artistas almacenados = "+str(fila[0]))  
        elif numeroOpcion == "4":   #Si el numero de opcion introducido es 4
            #Pedimos por pantalla que se introduzca por teclado el disco del que quieres saber el artista almacenado en BBDD
            discoConsultar=input("Introduce el disco del que quieres saber el artista almacenado en BBDD: ")
            #Una vez introducido se pasa a la query el disco del que se quiere consultar el artista para que esta query devuelva el artista de ese disco
            #que tiene el usuario con el que se entro en el programa
            #Ponemos distinct para asegurar contar solo los titulos distintos, no repetidos que salgan varias veces
            #por los cruces de tabla (inner join) que tenemos
            query=f"""SELECT DISTINCT(A.ARTISTA) FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
            INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION 
            WHERE D.TITULO='{discoConsultar}' AND EU.ID_USUARIO=CURRENT_USER"""
            #Ejecuta la consulta usando el cursor
            cursor.execute(query)

            #Obtiene los resultados usando el cursor y se almacenan en variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                print(fila[0])   #Imprime la primera columna de la fila del resultado de la query
        elif numeroOpcion == "5":   #Si el numero de opcion introducido es 5  
            #Se muestran todos los titulos de discos almacenados en BBDD  
            #por el usuario con el que se entro al programa
            query=f"""SELECT DISTINCT(D.TITULO) FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
            INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
            WHERE EU.ID_USUARIO=CURRENT_USER ORDER BY D.TITULO ASC"""   
            #Ejecuta esta consulta usando el cursor
            cursor.execute(query)

            #Obtiene los resultados de la consulta usando el cursor
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                print(fila[0])   #Imprime la primera columna de la fila del resultado de la query 
        elif numeroOpcion == "6":   #Si el numero de opcion introducido es 6
            #Se muestran todos los artistas almacenados en BBDD
            #por el usuario con el que se entro al programa
            query=f"""SELECT DISTINCT(A.ARTISTA) FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
            INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION 
            WHERE EU.ID_USUARIO=CURRENT_USER ORDER BY A.ARTISTA ASC"""   
            #Ejecuta la consulta usando el cursor
            cursor.execute(query)

            #Obtiene los resultados usando el cursor y se almacenan en variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                print(fila[0])   #Imprime la primera columna de la fila del resultado de la query    
        elif numeroOpcion == "7":   #Si el numero de opcion introducido es 7
            #Se pide por pantalla que introduzca por teclado el artista del que quiere saber los discos almacenados en BBDD
            artistaConsultar=input("Introduce el artista del que quieres saber los discos almacenados en BBDD: ")
            #Se pasa a la query el artista introducido por teclado a la siguiente query que devolvera todos los discos de ese artista almacenados en BBDD
            query=f"""SELECT COUNT(DISTINCT(D.TITULO)) FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
            INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION 
            WHERE A.ARTISTA='{artistaConsultar}' AND EU.ID_USUARIO=CURRENT_USER"""

            #Ejecuta la consulta usando el cursor
            cursor.execute(query)

            #Obtiene los resultados usando el cursor y los almacena en variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                #Imprime este texto concatenado con casting de la primera columna de la fila del resultado de la query
                print("Hay "+str(fila[0])+ " discos del artista introducido") 
        elif numeroOpcion=="8":
            #Se pide por pantalla que introduzca por teclado la cancion de la que quiere saber los discos almacenados en BBDD
            cancionConsultar=input("Introduce el artista del que quieres saber los discos almacenados en BBDD: ")
            query=f"""SELECT DISTINCT(D.TITULO) FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
            INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
            INNER JOIN ARTISTAS_CANCIONES AC ON A.ID_ARTISTA=AC.ID_ARTISTA INNER JOIN CANCIONES C ON AC.ID_CANCION=C.ID_CANCION
            WHERE C.CANCION='{cancionConsultar}' AND EU.ID_USUARIO=CURRENT_USER"""   
            #Ejecuta la consulta usando el cursor
            cursor.execute(query)

            #Obtiene los resultados usando el cursor y se almacenan en variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                print("El disco de la cancion introducida se llama: "+str(fila[0]))   #Imprime la primera columna de la fila del resultado de la query   

            query=f"""SELECT DISTINCT(A.ARTISTA) FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA 
            INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO INNER JOIN EDICIONES_USUARIO EU ON ED.ID_EDICION=EU.ID_EDICION
            INNER JOIN ARTISTAS_CANCIONES AC ON A.ID_ARTISTA=AC.ID_ARTISTA INNER JOIN CANCIONES C ON AC.ID_CANCION=C.ID_CANCION
            WHERE C.CANCION='{cancionConsultar}' AND EU.ID_USUARIO=CURRENT_USER"""   
            #Ejecuta la consulta usando el cursor
            cursor.execute(query)

            #Obtiene los resultados usando el cursor y se almacenan en variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                print("El artista de la cancion introducida se llama: "+str(fila[0]))   #Imprime la primera columna de la fila del resultado de la query 
        else:
            print("Has introducido un numero de opción incorrecto")

    def eliminar_en_base_datos(preguntarParametrosConexion):
        #Se pasa por parametro ask_conn_parameters que contiene los datos de conexion almacenados en variables
        """_summary_

        Args:
            ask_conn_parameters (_type_): _description_
        """    
        #Se pide por pantalla que introduzca por teclado el nombre del disco a borrar         
        discoBorrar = input("Introduzca el nombre del disco a borrar: ")

        #Se obtienen los parámetros de conexión
        (host, puerto, usuario, contrasena, baseDatos) = preguntarParametrosConexion

        #Crear la cadena de conexión
        datosConexion = f'host={host} port={puerto} user={usuario} password={contrasena} dbname={baseDatos}'
        #Nos conectamos a la base de datos usando los datos de conexion que nos proporciona ask_conn_parameters
        conexion = psycopg2.connect(datosConexion)
        cursor = conexion.cursor()  #Creamos el cursor que usaremos para ejecutar querys
        #Pongo esto porque valor de id_disco se declaraba dentro de if y no se detectaba fuera del if
        #lo mismo sucede con numeroEdicionesMismoDiscoYartista
        id_disco=0
        numeroEdicionesMismoDiscoYartista=0
        #Comprobamos si hay varios artistas con ese nombre de disco y si los hubiera pedimos que introduzca nombre artista
        #Solo se puede repetir el nombre del disco si no es del mismo artista, si fuera del mismo artista no se puede almacenar 
        #en tabla discos porque salcdria con el mismo id_disco que seria la misma primary key (PK) y no puede haber varios con misma
        #primary key (PK)
        query=f"SELECT COUNT(*) FROM DISCOS WHERE TITULO = '{discoBorrar}'"

        #Se ejecuta la consulta usando el cursor
        cursor.execute(query)

        #Se obtiene los resultados de la consulta con el cursor
        resultado = cursor.fetchall()

        # Recorremos las filas del resultado de la query
        for fila in resultado:
            #print(row[0])
            numeroDiscosMismoTitulo=fila[0]  #Almacenamos la primera columna de la fila del resultado de la query

        
        if numeroDiscosMismoTitulo>1:   #Si hay mas de un disco con el mismo titulo en la tabla discos
            #Pedimos por pantalla que introduzca por teclado el artista del disco a borrar
            artistaDiscoBorrar = input("Introduzca el artista del disco a borrar: ") 

            #Comprobamos si hay varias ediciones con ese nombre de disco de ese artista
            query=f"SELECT COUNT(*) FROM EDICIONES_DISCO ED INNER JOIN DISCOS D ON ED.ID_DISCO=D.ID_DISCO INNER JOIN ARTISTAS A ON A.ID_ARTISTA=D.ID_ARTISTA" 
            f" WHERE D.TITULO='{discoBorrar}' AND A.ARTISTA='{artistaDiscoBorrar}'"

            #Ejecuta la consulta usando el cursor
            cursor.execute(query)

            #Obtiene los resultados usando el cursor y los almacenamos en la variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                #print(row[0])
                numeroEdicionesMismoDiscoYartista=fila[0]    #Almacenamos la primera columna de la fila del resultado de la query

            if numeroEdicionesMismoDiscoYartista>1: #Si hay mas de una edicion del mismo disco y artista
                #Pedimos por pantalla que se introduzca por teclado la edición del disco del artista introducido que quieres borrar
                edicionDiscoArtistaBorrar = input("Introduzca la edición del disco del artista introducido que quieres borrar: ")    
                #Una vez introducido en este caso sacamos el id_disco único a partir del titulo del disco, del artista del disco y de la edicion del disco 
                #de ese artista que hemos introducido por teclado
                query=f"SELECT D.ID_DISCO FROM DISCOS D INNER JOIN ARTISTAS A ON D.ID_ARTISTA=A.ID_ARTISTA INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO" 
                f" WHERE D.TITULO = '{discoBorrar}' AND A.ARTISTA='{artistaDiscoBorrar}' AND ED.EDICION='{edicionDiscoArtistaBorrar}'"
                
                #Ejecuta la consulta usando el cursor
                cursor.execute(query)

                #Obtiene los resultados usando el cursor y los almacenamos en la variable
                resultado = cursor.fetchall()

                # Recorremos las filas del resultado de la query
                for fila in resultado:
                    #print(row[0])
                    id_disco=fila[0] #Aseguramos guardar la primera columna de la fila del resultado de la query    
            else:
                #En el caso en el que no hubiera mas de una edicion para el titulo del disco y artista introducido
                #Con la siguiente query obtenemos el id del disco unico a partir del disco y del artista introducido
                query=f"SELECT D.ID_DISCO FROM DISCOS D INNER JOIN ARTISTAS A ON D.ID_ARTISTA=A.ID_ARTISTA WHERE D.TITULO = '{discoBorrar}' AND A.ARTISTA='{artistaDiscoBorrar}'"

                #Ejecuta la consulta usando el cursor
                cursor.execute(query)

                #Obtiene los resultados de la consulta usando el cursor y los almacena en variable
                resultado = cursor.fetchall()

                # Recorremos las filas del resultado de la query
                for fila in resultado:
                    #print(row[0])
                    id_disco=fila[0]     #Aseguramos guardar la primera columna de la fila del resultado de la query     

        else: 
            #Si solo hay un disco con ese titulo
            #Comprobamos si hay varias ediciones con ese nombre de disco
            query=f"SELECT COUNT(*) FROM EDICIONES_DISCO ED INNER JOIN DISCOS D ON ED.ID_DISCO=D.ID_DISCO WHERE D.TITULO='{discoBorrar}'"

            #Ejecutamos la consulta usando el cursor
            cursor.execute(query)

            #Obtenemos los resultados usando el cursor
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                #print(row[0])
                numeroEdicionesMismoDisco=fila[0]    #Almacenamos la primera columna de la fila del resultado de la query
            
            if numeroEdicionesMismoDisco>1:     #Si hay mas de una edicion para el disco que queremos borrar
                #Pedimos por pantalla que se introduzca por teclado la edición del disco que quieres borrar
                edicionDiscoBorrar = input("Introduzca la edición del disco del artista introducido que quieres borrar: ")    
                #Y una vez introducido obtenemos el id del disco unico a partir del titulo del disco y la edicion del disco introducidos por teclado
                query=f"SELECT D.ID_DISCO FROM DISCOS D INNER JOIN EDICIONES_DISCO ED ON D.ID_DISCO=ED.ID_DISCO WHERE D.TITULO = '{discoBorrar}' AND ED.EDICION='{edicionDiscoBorrar}'"
                
                #Ejecutamos la consulta usando el cursor
                cursor.execute(query)

                #Obtenemos los resultados usando el cursor
                resultado = cursor.fetchall()

                # Recorremos las filas del resultado de la query
                for fila in resultado:
                    #print(row[0])
                    id_disco=fila[0]     #Almacenamos la primera columna de la fila del resultado de la query  
            else:
                #Si solo hay una edicion de ese disco
                #Se obtiene el id del disco unico a partir de solamente el titulo del disco    
                query=f"SELECT ID_DISCO FROM DISCOS WHERE TITULO = '{discoBorrar}'"

                #Ejecutamos la consulta usando el cursor
                cursor.execute(query)

                #Obtenemos los resultados usando el cursor
                resultado = cursor.fetchall()

                # Imprime los resultados
                for fila in resultado:
                    #print(row[0])
                    id_disco=fila[0]     #Almacenamos la primera columna de la fila del resultado de la query       

        #Con esta query sacamos todos los id de canciones que pertenecen al id_disco unico que hemos 
        #hallado antes
        query=f"SELECT ID_CANCION FROM DISCOS_CANCIONES WHERE ID_DISCO='{id_disco}'"
        #Ejecutamos la consulta usando el cursor
        cursor.execute(query)

        #Obtenemos los resultados usando el cursor y los almacenamos en variable
        resultado = cursor.fetchall()

        # Recorremos las filas del resultado de la query
        for fila in resultado:
            #Eliminando de la tabla ARTISTAS_CANCIONES todas las filas que contengan los id_cancion
            #que nos da la primera columna la fila del resultado de la query que ejecutamos justo antes
            query=f"DELETE FROM ARTISTAS_CANCIONES WHERE ID_CANCION='{fila[0]}'"
            #Ejecutamos la consulta de eliminacion usando el cursor
            cursor.execute(query) 

        #En la tabla DISCOS_CANCIONES como todas las canciones a eliminar son del mismo id de disco unico hallado antes
        #Con hacer una vez la siguiente consulta ya se eliminan todas las canciones de ese disco en esta tabla
        query=f"DELETE FROM DISCOS_CANCIONES WHERE ID_DISCO='{id_disco}'"
        #Ejecutamos la consulta de eliminacion usando el cursor
        cursor.execute(query)

        # Recorremos las filas del resultado de la query
        for fila in resultado:
            #Eliminando de la tabla CANCIONES todas las filas que contengan los id_cancion
            #que nos da la primera columna de la fila del resultado de la query SELECT ID_CANCION FROM DISCOS_CANCIONES WHERE ID_DISCO='{id_disco}'
            query=f"DELETE FROM CANCIONES WHERE ID_CANCION='{fila[0]}'"
            #Ejecutamos la consulta de eliminacion usando el cursor
            cursor.execute(query)

        #Eliminamos de la tabla EDICIONES_DISCO todas las filas que tengan el mismo id_disco unico hallado antes
        query=f"DELETE FROM EDICIONES_DISCO WHERE ID_DISCO = '{id_disco}'"
        #Ejecutamos la consulta de eliminacion usando el cursor
        cursor.execute(query)
        
        #Comprobar si puedo eliminar el artista porque haya antes de eliminar solo un disco de ese artista
        query=f"SELECT COUNT(*) FROM DISCOS D INNER JOIN ARTISTAS A ON D.ID_ARTISTA=A.ID_ARTISTA WHERE D.ID_DISCO = '{id_disco}'"

        #Ejecutamos la consulta usando el cursor
        cursor.execute(query)

        #Obtenemos los resultados usando el cursor y los almacenamos en variable
        resultado = cursor.fetchall()

        # Recorremos las filas del resultado de la query
        for fila in resultado:
            #print(row[0])
            numeroDiscosDeEseArtista=fila[0] #Almacenamos la primera columna de la fila del resultado de la query
        #print(numeroDiscosDeEseArtista)
        #Una vez comprobado si puedo eliminar artista aplico eliminacion si puedo
        #Ponemos esta variable aqui iniciada a 0 ya que si no no se detecta despues la variable por ser local
        idArtistaEliminar=0
        if numeroDiscosDeEseArtista==1: #Si solo hay un disco de ese artista
            #Obtenemos el id unico del artista a partir del id del disco para mas adelante eliminar ese artista de la tabla artistas
            query=f"SELECT A.ID_ARTISTA FROM DISCOS D INNER JOIN ARTISTAS A ON D.ID_ARTISTA=A.ID_ARTISTA WHERE D.ID_DISCO = '{id_disco}'"

            #Ejecutamos la consulta usando el cursor
            cursor.execute(query)

            #Obtenemos los resultados usando el cursor y los almacenamos en variable
            resultado = cursor.fetchall()

            
            # Recorremos las filas del resultado de la query
            for fila in resultado:
                #print(row[0])
                idArtistaEliminar=fila[0]    #Almacenamos la primera columna de la fila del resultado de la query    
        #Comprobar que existen ediciones de ese disco
        query=f"SELECT COUNT(*) FROM EDICIONES_DISCO WHERE ID_DISCO = '{id_disco}'"

        #Ejecutamos la consulta usando el cursor
        cursor.execute(query)

        #Obtenemos los resultados usando el cursor y los almacenamos en variable
        resultado = cursor.fetchall()

        # Recorremos las filas del resultado de la query   
        for fila in resultado:
            #print(row[0])
            numeroEdicionesDisco=fila[0]     #Almacenamos la primera columna de la fila del resultado de la query    
        #Comprobar si se puede eliminar el disco
        if numeroEdicionesDisco==0: #Si despues de haber eliminado una edicion de disco no hay mas ediciones de disco  
            #eliminamos de la tabla discos la fila que tenga ese id_disco unico
            query=f"DELETE FROM discos WHERE id_disco = '{id_disco}'"
            cursor.execute(query)   #ejecutamos la query
            #Eliminamos de la tabla artistas la fila que tenga ese id de artista unico
            query=f"DELETE FROM ARTISTAS WHERE ID_ARTISTA = '{idArtistaEliminar}'"
            cursor.execute(query)   #ejecutamos la query  


        conexion.commit()   #Confirmamos los cambios en la base de datos para que se apliquen

    def modificarBBDD(preguntarParametrosConexion):
        #Se pasa por parametro ask_conn_parameters que contiene los datos de conexion almacenados en variables
        """_summary_

        Args:
            ask_conn_parameters (_type_): _description_
        """
        #Se obtienen los parámetros de conexión
        (host, puerto, usuario, contrasena, baseDatos) = preguntarParametrosConexion

        #Se introducen en la siguiente variable
        datosConexion = f'host={host} port={puerto} user={usuario} password={contrasena} dbname={baseDatos}'

        #Nos conectamos a la base de datos usando los datos de conexion almacenados en datosConexion
        conexion = psycopg2.connect(datosConexion)

        #Creamos un cursor para nuestra conexion que usaremos para realizar consultas
        cursor = conexion.cursor()
        #Pedimos por pantalla que se introduzca por teclado el disco del que desea modificar su información almacenada en BBDD
        discoModificar=input("Introduce el disco del que desea modificar su información almacenada en BBDD: ")
        #Comprobamos cuantos discos en la tabla discos tienen ese titulo
        query=f"SELECT COUNT(*) FROM DISCOS WHERE TITULO='{discoModificar}'"

        #Ejecutamos la consulta usando el cursor
        cursor.execute(query)

        #Obtenemos los resultados de la consulta y los almacenamos en la variable
        resultado = cursor.fetchall()

        # Recorremos las filas del resultado de la query
        for fila in resultado:
            numeroDiscosEseTitulo=fila[0]    #Almacenamos la primera columna de la fila del resultado de la query
        
        if numeroDiscosEseTitulo==0:    #Si no existe ningun disco con el titulo introducido
            print("Error: no existe ese disco") #Avisamos por pantalla de que no existe el disco introducido
        else:   
            #Si si existe ese disco sacamos el nombre del artista de ese disco
            query=f"SELECT A.ARTISTA FROM ARTISTAS A INNER JOIN DISCOS D ON A.ID_ARTISTA=D.ID_ARTISTA WHERE D.TITULO='{discoModificar}'"

            #Ejecutamos la consulta usando el cursor
            cursor.execute(query)

            #Obtenemos los resultados de la consulta y los almacenamos en la variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                artista=fila[0]  #Guardamos el valor de la primera columna de la fila del resultado de la consulta   
            #Sacamos la edicion de ese disco
            query=f"SELECT ED.EDICION FROM EDICIONES_DISCO ED INNER JOIN DISCOS D ON ED.ID_DISCO=D.ID_DISCO WHERE D.TITULO='{discoModificar}'"

            #Ejecutamos la consulta usando el cursor
            cursor.execute(query)

            #Obtenemos los resultados de la consulta y los almacenamos en la variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                edicion=fila[0]   #Guardamos el valor de la primera columna de la fila del resultado de la consulta  
            #Sacamos el año de la edicion del disco del titulo del disco que introdujimos por teclado
            query=f"SELECT ED.AGNO FROM EDICIONES_DISCO ED INNER JOIN DISCOS D ON ED.ID_DISCO=D.ID_DISCO WHERE D.TITULO='{discoModificar}'"

            #Ejecutamos la consulta usando el cursor
            cursor.execute(query)

            #Obtenemos los resultados de la consulta y los almacenamos en la variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                agno=fila[0] #Guardamos el valor de la primera columna de la fila del resultado de la consulta 
            #Sacamos el pais de la edicion del disco del titulo del disco que introdujimos por teclado
            query=f"SELECT ED.PAIS FROM EDICIONES_DISCO ED INNER JOIN DISCOS D ON ED.ID_DISCO=D.ID_DISCO WHERE D.TITULO='{discoModificar}'"

            #Ejecutamos la consulta usando el cursor
            cursor.execute(query)

            #Obtenemos los resultados de la consulta y los almacenamos en la variable
            resultado = cursor.fetchall()

            # Recorremos las filas del resultado de la query
            for fila in resultado:
                pais=fila[0] #Guardamos el valor de la primera columna de la fila del resultado de la consulta
            #Sacamos todas las canciones del disco introducido por teclado
            query=f"SELECT C.CANCION FROM CANCIONES C INNER JOIN DISCOS_CANCIONES DC ON C.ID_CANCION=DC.ID_CANCION INNER JOIN DISCOS D ON DC.ID_DISCO=D.ID_DISCO WHERE D.TITULO='{discoModificar}'"

            #Ejecutamos la consulta usando el cursor
            cursor.execute(query)

            #Obtenemos los resultados de la consulta y los almacenamos en la variable
            resultado = cursor.fetchall()

            canciones=[]
            # Recorremos las filas del resultado de la query
            for fila in resultado:
                cancion=fila[0]  #Guardamos el valor de la primera columna de la fila del resultado de la consulta
                canciones.append(cancion)   #Lo guardamos en array y en la siguiente columna se cogerá la primera columna de la siguiente fila del resultado de la query, y asi sucesivamente
            #Sacamos las duraciones de todas las canciones del disco introducido por teclado
            query=f"SELECT C.DURACION FROM CANCIONES C INNER JOIN DISCOS_CANCIONES DC ON C.ID_CANCION=DC.ID_CANCION INNER JOIN DISCOS D ON DC.ID_DISCO=D.ID_DISCO WHERE D.TITULO='{discoModificar}'"

            #Ejecutamos la consulta usando el cursor
            cursor.execute(query)

            #Obtenemos los resultados de la consulta y los almacenamos en la variable
            resultado = cursor.fetchall()

            duraciones=[]
            # Recorremos las filas del resultado de la query
            for fila in resultado:
                duracion=fila[0]     #Guardamos el valor de la primera columna de la fila del resultado de la consulta
                duraciones.append(duracion)     #Lo guardamos en array y en la siguiente columna se cogerá la primera columna de la siguiente fila del resultado de la query, y asi sucesivamente
            
            print("titulo= "+str(discoModificar))   #mostramos por pantalla el titulo del disco 
            print("artista= "+str(artista))     #mostramos por pantalla el artista
            print("edicion= "+str(edicion))      #mostramos por pantalla la edicion
            print("agno= "+str(agno)) #mostramos por pantalla el año de la edicion
            print("pais= "+str(pais)) #mostramos por pantalla el pais de la edicion        
            i=1
            for cancion, duracion in zip(canciones, duraciones):    #usamos zip para poder usar los dos en un solo for y que asi si salga bien primero cancion y luego duracion
                print("cancion"+str(i)+"= "+str(cancion))   #mostramos por pantalla el nombre de la cancion
                print("duracion"+str(i)+"= "+str(duracion)) #mostramos por pantalla la duracion de la cancion
                i+=1    #incrementamos esta variable por cada vuelta de bucle para que escriba por pantalla por cada vuelta de bucle un numero de cancion y duracion
            #Pedimos por pantalla que se introduzca por teclado el campo del que desea modificar su información almacenada en BBDD
            #cuyo nombre será cada uno de los que se muestran en los prints anteriores
            campoModificar=input("Introduce el campo del que desea modificar su información almacenada en BBDD (si es cancion o duracion poner esto sin el numero, se pregunta despues el numero): ")
            if campoModificar=="titulo":    #Si se introdujo por teclado titulo
                #Se pide por pantalla que introduzca por teclado el nuevo valor de titulo de disco que desea
                nuevoValorTitulo=input("Introduce el nuevo valor de titulo de disco que desea: ")
                #se hace query que actualice el valor del campo titulo de la tabla discos con el que introducimos por teclado para el que tiene el titulo de disco que se introdujo antes por teclado
                query=f"UPDATE DISCOS SET TITULO='{nuevoValorTitulo}' WHERE TITULO='{discoModificar}'"
                #Ejecutamos la consulta usando el cursor
                cursor.execute(query)    
            elif campoModificar=="artista": #Si se introdujo por teclado artista
                #Se pide por pantalla que introduzca por teclado el nuevo valor de artista que desea
                nuevoValorArtista=input("Introduce el nuevo valor de artista que desea: ")   
                #se hace query que actualice el valor del campo artista por el introducido el teclado en la fila en la que tuviera el tiulo de artisra anterior y el titulo del disco
                #introducido antes por teclado
                query=f"UPDATE ARTISTAS A SET ARTISTA='{nuevoValorArtista}' FROM DISCOS D WHERE A.ID_ARTISTA=D.ID_ARTISTA AND A.ARTISTA='{artista}' AND D.TITULO='{discoModificar}'"
                #Ejecutamos la consulta usando el cursor
                cursor.execute(query)
            elif campoModificar=="edicion": #Si se introdujo por teclado edicion
                #Se pide por pantalla que introduzca por teclado el nuevo valor de edicion que desea
                nuevoValorEdicion=input("Introduce el nuevo valor de edicion que desea: ")
                #se hace query que actualiza la edicion del disco por la nueva introducida en la fila de la tabla EDICIONES_DISCO en la que tenia el nombre de edicion que tenia antes
                #y de titulo de disco el introducido antes por teclado
                query=f"UPDATE EDICIONES_DISCO ED SET EDICION='{nuevoValorEdicion}' FROM DISCOS D WHERE ED.ID_DISCO=D.ID_DISCO AND ED.EDICION='{edicion}' AND D.TITULO='{discoModificar}'"
                #Ejecutamos la consulta usando el cursor
                cursor.execute(query)
            elif campoModificar=="agno":    #Si se introdujo por teclado agno
                #Se pide por pantalla que introduzca por teclado el nuevo valor de año que desea
                nuevoValorAgno=input("Introduce el nuevo valor de año que desea: ")
                #se hace query que actualiza el año de la edicion del disco por la nueva introducida en la fila en la que tuviera antes el anterior valor de año de la edicion del disco y del titulo de disco el anteriormente
                #introducido por teclado
                query=f"UPDATE EDICIONES_DISCO ED SET AGNO='{nuevoValorAgno}' FROM DISCOS D WHERE ED.ID_DISCO=D.ID_DISCO AND ED.AGNO='{agno}' AND D.TITULO='{discoModificar}'"
                #Ejecutamos la consulta usando el cursor
                cursor.execute(query)
            elif campoModificar=="pais":    #Si se introdujo por teclado pais
                #Se pide por pantalla que introduzca por teclado el nuevo valor de pais que desea
                nuevoValorPais=input("Introduce el nuevo valor de pais que desea: ")
                #se hace query que actualiza el pais del disco por el nuevo introducido en la fila en la que antes tenia el anterior valor de pais y de titulo de disco el anteriormente introducido por teclado
                query=f"UPDATE EDICIONES_DISCO ED SET PAIS='{nuevoValorPais}' FROM DISCOS D WHERE ED.ID_DISCO=D.ID_DISCO AND ED.PAIS='{pais}' AND D.TITULO='{discoModificar}'"
                #Ejecutamos la consulta usando el cursor
                cursor.execute(query)
            elif campoModificar=="cancion": #Si se introdujo por teclado cancion
                #Se pide por pantalla que introduzca por teclado el numero de cancion que desea editar
                numeroCancion=input("Introduzca el numero de cancion que desea editar: ")
                #Se pide por pantalla que introduzca por teclado el nuevo valor de cancion que desea para ese numero de cancion
                nuevoValorCancion=input("Introduce el nuevo valor de cancion que desea para ese numero de cancion: ")
                #se hace query que actualiza el nombre del valor de la cancion por el nuevo introducido en la fina en la que el nombre de la cancion sea el anterior que tenia
                #y el titulo del disco el anteriormente introducido
                query=f"UPDATE CANCIONES C SET CANCION='{nuevoValorCancion}' FROM DISCOS_CANCIONES DC INNER JOIN DISCOS D ON DC.ID_DISCO=D.ID_DISCO" 
                f" WHERE DC.ID_CANCION=C.ID_CANCION AND CANCION='{canciones[int(numeroCancion)-1]}' AND D.TITULO='{discoModificar}'"
                #Ejecutamos la consulta usando el cursor
                cursor.execute(query)
            elif campoModificar=="duracion":    #Si se introdujo por teclado duracion
                #Se pide por pantalla que introduzca por teclado el numero de cancion que la que desea editar su duracion
                numeroDuracion=input("Introduzca el numero de cancion que la que desea editar su duracion: ")
                #Se pide por pantalla que introduzca por teclado el nuevo valor de duracion de cancion que desea para ese numero de cancion
                nuevoValorDuracion=input("Introduce el nuevo valor de duracion de cancion que desea para ese numero de cancion: ")
                #se hace query que actualiza el valor de la duracion del numero de cancion elegido por la nueva duraciokn introducda por teclado en la fila
                #de la tabla en la que la duracion anterior sea la anterior y el nombre de la cancion sea el de esa duracion y el titulo del disco sea el 
                #anteriormente introducido por teclado
                query=f"UPDATE CANCIONES C SET DURACION='{nuevoValorDuracion}' FROM DISCOS_CANCIONES DC INNER JOIN DISCOS D ON DC.ID_DISCO=D.ID_DISCO" 
                f" WHERE DC.ID_CANCION=C.ID_CANCION AND DURACION='{duraciones[int(numeroDuracion)-1]}' AND CANCION='{canciones[int(numeroDuracion)-1]}' AND D.TITULO='{discoModificar}'"
                #Ejecutamos la consulta usando el cursor
                cursor.execute(query)
        conexion.commit()   #Confirmamos los cambios en base de datos para que se apliquen