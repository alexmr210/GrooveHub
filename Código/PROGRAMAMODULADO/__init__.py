import argparse     #para pasar argumentos por terminal al programa Python
import sys          #se usa para ver si por terminal introduces --test, se usa esto en el if de abajo del todo de este código
import psycopg2     #aunque este en consultasBBDD.py se necesita aqui porque si no no detecta en except para filtrar errores de esto


#Importo todas las clases que he creado
from lecturaCodigos import lecturaCodigos
from conexionBBDD import conexionBBDD
from extraccionDatosDiscogs import extraccionDatosDiscogs
from tratamientoDatos import tratamientoDatos
from consultasBBDD import consultasBBDD

#parser
parser = argparse.ArgumentParser()  #se usa para poder decir despues usando esto que argumentos queremos pasar por la terminal al ejecutar el programa

#ñadimos argumentos
parser.add_argument('puerto', type=int) #para poder introducir por terminal un argumento que será un entero al que se le asignara el nombre puerto
#ya que ahi se introducirá el número de puerto de nuestra base de datos.    
parser.add_argument('usuario', type=str)    #para poder introducir por terminal un argumento que será un string al que se le asignara el nombre usuario 
#ya que ahi se introducira el usuario de nuestra base de datos.      
parser.add_argument('contrasena', type=str) #para poder introducir por terminal un argumento que será un string al que se le asignara el nombre contrasena
#ya que ahi se introducira la contrasena de nuestra base de datos.  
parser.add_argument('baseDatos', type=str) #para poder introducir por terminal un argumento que será un string al que se le asignara el nombre baseDatos
#ya que ahi se introducira el nombre de nuestra base de datos. 

#Juntamos argumentos de la terminal y pasamos esto a funcion ask_conn_parameters para conectarnos a nuestra base de datos
argumentosTerminal = parser.parse_args() #esto se usara en ask_conn_parameters() poniendo argumentosTerminal.puerto, argumentosTerminal.usuario, 
#argumentosTerminal.contrasena y argumentosTerminal.baseDatos
class Main:
    
    def main():
        while True:
            try:
                # Imprimimos el menú principal
                print("1.Insertar un nuevo disco")
                print("2.Hacer consultas a la base de datos")
                print("3.Borrar disco de la base de datos")
                print("4.Modificar algo de la base de datos")
                print("5.Salir del programa")
                opcion=input("Elige una opción: ")    #Preguntamos por el numero de opcion del menú principal que se desea para que sea introducido por teclado
                if opcion == "1":   #Si el numero de opcion del menú principal introducido por teclado es 1
                    print("-------------------------")  #Imprimimos menu que nos da la opcion de introducir el codigo de barras por teclado o por webcam
                    print("1.Introducir código de barras por teclado")
                    print("2.Escanear código de barras usando la webcam")
                    print("3.Escanear código de barras de imagen almacenada introduciendo su ruta")
                    #Preguntamos por el numero de opcion del menú en el que se pregunta si quiere introducir el codigo de barras por teclado o por webcam
                    #o imagen almacenada
                    opcion2=input("Elige una opción: ")   
                    #que se desea para que sea introducido por teclado
                    codigo_barras=0 #Pongo esto ya que si no la variable codigo_barras no se detecta fuera del if
                    if opcion2=="1":    #Si el numero de opcion del menú en el que se pregunta si quiere introducir el codigo de barras por teclado o webcam introducido por teclado es 1
                        codigo_barras=lecturaCodigos.leer_codigo_barras()    

                        #Por si se quieren introducir varios codigos de barras por teclado
                        codigo_barras=lecturaCodigos.multiplesCodigosBarrasTeclado(codigo_barras)
                    elif opcion2=="2":  #Si el numero de opcion del menú en el que se pregunta si quiere introducir el codigo de barras por teclado o webcam introducido por teclado es 2
                        codigo_barras=lecturaCodigos.detectarArquitecturaEscaneoCodigoBarrasWebcam()     #Llamamos a esta funcion que dependiendo de la arquitectura del procesador 
                        #llama a una funcion de escaneo de código de barras por webcam o otra para que funcione independientemente de si estamos en arquitectura ARM o x64, y devuelve
                        #despues de ejecutar esa funcion el codigo de barras
                        #codigo_barras = nuevoEscanearCodigoBarrasWebcam()

                        #Para que si se quieren escanear varios codigos de barras por webcam se pueda y siga funcionando bien en las dos arquitecturas de procesador
                        codigo_barras=lecturaCodigos.multiplesCodigosBarrasWebcam(codigo_barras)    
                    elif opcion2=="3":
                        codigo_barras=lecturaCodigos.escanearCodigoBarrasImagen()
                    else:   #Si el numero de opcion del menú en el que se pregunta si quiere introducir el codigo de barras por teclado o webcam introducido por teclado es un numero de opcion
                        #que no se encuentra en ese menú
                        print("Opción no válida. Por favor, elige una opción del menú.")
                    # A partir del código de barras introducido antes se extrae de discogs la informacion que se guarda en las variables que se ven aqui
                    #titulo, artista, canciones, edicion, agno, paisEdicionDisco, idDisco, idArtista = extraccionDatosDiscogs.extraer_discogs(codigo_barras) 
                    titulo, artista, canciones, edicion, agno, paisEdicionDisco, idDisco, idArtista=extraccionDatosDiscogs.deteccionCodigoBarrasLista(codigo_barras)
                    #En casos que no sean el else no continuamos con el proceso de insercion
                    #quitamos la variable canciones de la comprobacion porque si no siempre entra en esta condicion ya que canciones siempre es array
                    #print(f"titulo: {titulo}")
                    #print(f"artista: {artista}")
                    #print(f"edicion: {edicion}")
                    #print(f"agno: {agno}")
                    #print(f"paisEdicionDisco: {paisEdicionDisco}")
                    #print(f"idDisco: {idDisco}")
                    #print(f"idArtista: {idArtista}")
                    #artista, titulo y canciones no se comprueban si son lista aqui ya que todavia no estan tratados y pueden ser liesta
                    if isinstance(edicion,list) or isinstance(agno,list) or isinstance(paisEdicionDisco,list) or isinstance(idDisco,list) or isinstance(idArtista,list):
                        #print("Entra en condicion if recibe lista")
                        #En esta situacion recorremos array eliminando los elementos del array que son None para que luego solo se introduzcan en BBDD los que no son None
                        for i in range(len(titulo)):
                            if titulo[i] is None or artista[i] is None or canciones[i] is None or edicion[i] is None or agno[i] is None or paisEdicionDisco[i] is None or idDisco[i] is None or idArtista[i] is None: 
                                print("No se encontraron resultados para ese código de barras.")    #Avisamos por pantalla que no se encontraron resultados para ese código de barras
                                titulo.pop(i)     
                                artista.pop(i)
                                canciones.pop(i)
                                edicion.pop(i)
                                agno.pop(i)  
                                paisEdicionDisco.pop(i)
                                idDisco.pop(i)
                                idArtista.pop(i)
                        #Despues de hacer esto ejecutamos lo mismo que en el else para hacer la insercion de los datos en BBDD
                                
                        # Tratamos aquellos datos en los que no salen lo que queremos tal cual usando split para coger un trozo de texto
                        #artistaTratado, tituloTratado, cancionesTratadas, duracionCanciones= tratamientoDatos.tratarDatos(artista, titulo, canciones)
                        artistaTratado, tituloTratado, cancionesTratadas, duracionCanciones=tratamientoDatos.deteccionParametrosTratarDatosLista(artista, titulo, canciones)
                        #Creo hashes y lo paso a hexadecimal SHA256 que siempre tiene 64 caracteres 
                        #Este hash se genera de juntar valores de variables de parametro y convertirlo en hash que se usara como id de la tabla ediciones_disco
                        #hashHexadecimalEdicionDisco = tratamientoDatos.generarHashEdicionDisco(agno, paisEdicionDisco, edicion, tituloTratado)
                        hashHexadecimalEdicionDisco=tratamientoDatos.deteccionParametrosHashEdicionDiscoLista(agno, paisEdicionDisco, edicion, tituloTratado)
                        #Este hash se genera de juntar valores de variables de parametro y convertirlo en hash que se usara como id de la tabla canciones 
                        #hashHexadecimalCanciones= tratamientoDatos.generarHashCanciones(idArtista, idDisco, cancionesTratadas)
                        hashHexadecimalCanciones=tratamientoDatos.deteccionParametrosHashCancionesLista(idArtista, idDisco, cancionesTratadas)
                        # Insertar los datos una vez tratados los que era necesario tratar en la base de datos
                        #consultasBBDD.insertar_en_base_datos(artistaTratado, tituloTratado, cancionesTratadas, edicion, agno, hashHexadecimalEdicionDisco, 
                        #                                    hashHexadecimalCanciones, paisEdicionDisco, idDisco, idArtista, duracionCanciones, conexionDiscogs.preguntarParametrosConexion(argumentosTerminal))
                        consultasBBDD.detectarParametrosInsertar_en_base_datosLista(artistaTratado, tituloTratado, cancionesTratadas, edicion, agno, hashHexadecimalEdicionDisco,
                                                            hashHexadecimalCanciones, paisEdicionDisco, idDisco, idArtista, duracionCanciones, conexionBBDD.preguntarParametrosConexion(argumentosTerminal))                                                              
                        #Una vez hecha la inserción lo avisamos mostrando por pantalla el siguiente texto    
                        print("Información almacenada en BBDD")
                    elif titulo is None or artista is None or canciones is None or edicion is None or agno is None or paisEdicionDisco is None or idDisco is None or idArtista is None:   
                        #print("No se encontraron resultados para ese código de barras.")    #Avisamos por pantalla que no se encontraron resultados para ese código de barras
                        break   #Cierro el programa despues de esto ya que si continuo su ejecucion se queda pillado ventana webcam
                    else:   #En este caso si continuamos con el proceso de insercion
                        print("Entra en condicion if NO recibe lista")
                        # Tratamos aquellos datos en los que no salen lo que queremos tal cual usando split para coger un trozo de texto
                        #artistaTratado, tituloTratado, cancionesTratadas, duracionCanciones= tratamientoDatos.tratarDatos(artista, titulo, canciones)
                        artistaTratado, tituloTratado, cancionesTratadas, duracionCanciones=tratamientoDatos.deteccionParametrosTratarDatosLista(artista, titulo, canciones)
                        #Creo hashes y lo paso a hexadecimal SHA256 que siempre tiene 64 caracteres 
                        #Este hash se genera de juntar valores de variables de parametro y convertirlo en hash que se usara como id de la tabla ediciones_disco
                        #hashHexadecimalEdicionDisco = tratamientoDatos.generarHashEdicionDisco(agno, paisEdicionDisco, edicion, tituloTratado)
                        hashHexadecimalEdicionDisco=tratamientoDatos.deteccionParametrosHashEdicionDiscoLista(agno, paisEdicionDisco, edicion, tituloTratado)
                        #Este hash se genera de juntar valores de variables de parametro y convertirlo en hash que se usara como id de la tabla canciones 
                        #hashHexadecimalCanciones= tratamientoDatos.generarHashCanciones(idArtista, idDisco, cancionesTratadas)
                        hashHexadecimalCanciones=tratamientoDatos.deteccionParametrosHashCancionesLista(idArtista, idDisco, cancionesTratadas)
                        # Insertar los datos una vez tratados los que era necesario tratar en la base de datos
                        #consultasBBDD.insertar_en_base_datos(artistaTratado, tituloTratado, cancionesTratadas, edicion, agno, hashHexadecimalEdicionDisco, 
                        #                                    hashHexadecimalCanciones, paisEdicionDisco, idDisco, idArtista, duracionCanciones, conexionDiscogs.preguntarParametrosConexion(argumentosTerminal))
                        consultasBBDD.detectarParametrosInsertar_en_base_datosLista(artistaTratado, tituloTratado, cancionesTratadas, edicion, agno, hashHexadecimalEdicionDisco,
                                                            hashHexadecimalCanciones, paisEdicionDisco, idDisco, idArtista, duracionCanciones, conexionBBDD.preguntarParametrosConexion(argumentosTerminal))                                                              
                        #Una vez hecha la inserción lo avisamos mostrando por pantalla el siguiente texto    
                        print("Información almacenada en BBDD")
                elif opcion == "2": #Si el numero de opcion del menú principal elegido por teclado es 2
                    #Mostramos menu de consultas para ver cuales podemos hacer
                    print("-------------------------")
                    print("1.Consulta discos de artista que introduzcas")
                    print("2.Consulta numero de discos que tengo almacenados en BBDD")
                    print("3.Consulta numero de artistas que tengo almacenados en BBDD")
                    print("4.Consulta artista de disco que introduzcas")
                    print("5.Consulta discos almacenados alfabeticamente")
                    print("6.Consulta artistas almacenados alfabeticamente")
                    print("7.Consulta cuantos discos de artista que introduzcas")
                    print("8.Introduce una cancion de la que quieres saber su disco y artista")
                    #Introducimos numero de opcion del menu de consultas
                    opcion3 = input("Elige una opción: ")
                    if opcion3 == "1":  #Si el numero de opcion del menú de consultas introducido por teclado es 1
                        consultasBBDD.consultar_en_base_datos("1", conexionBBDD.preguntarParametrosConexion(argumentosTerminal))   #Llamamos a la funcion que realiza consultas pasando como parametros 
                        #el numero de consulta que queremos hacer que es el mismo que el del menú y a la funcion ask_conn_parameters para extraer de ahi los parámetros necesarios
                        #para realizar la conexion con nuestra base de datos (host, puerto, usuario, contrasena, baseDatos)        
                    elif opcion3 == "2": #Si el numero de opcion del menú de consultas introducido por teclado es 2    
                        consultasBBDD.consultar_en_base_datos("2", conexionBBDD.preguntarParametrosConexion(argumentosTerminal))   #Llamamos a la funcion que realiza consultas pasando como parametros
                        #el numero de consulta que queremos hacer que es el mismo que el del menú y la funcion ask_conn_parameters para extraer de ahi los parámetros necesarios
                        #para realizar la conexion con nuestra base de datos (host, puerto, usuario, contrasena, baseDatos) 
                    elif opcion3 == "3": #Si el numero de opcion del menú de consultas introducido por teclado es 3
                        consultasBBDD.consultar_en_base_datos("3", conexionBBDD.preguntarParametrosConexion(argumentosTerminal))   #Llamamos a la funcion que realiza consultas pasando como parametros
                        #el numero de consulta que queremos hacer que es el mismo que el del menú y la funcion ask_conn_parameters para extraer de ahi los parámetros necesarios
                        #para realizar la conexion con nuestra base de datos (host, puerto, usuario, contrasena, baseDatos) 
                    elif opcion3 == "4": #Si el numero de opcion del menú de consultas introducido por teclado es 4
                        consultasBBDD.consultar_en_base_datos("4", conexionBBDD.preguntarParametrosConexion(argumentosTerminal))   #Llamamos a la funcion que realiza consultas pasando como parametros
                        #el numero de consulta que queremos hacer que es el mismo que el del menú y la funcion ask_conn_parameters para extraer de ahi los parámetros necesarios
                        #para realizar la conexion con nuestra base de datos (host, puerto, usuario, contrasena, baseDatos)
                    elif opcion3 == "5": #Si el numero de opcion del menú de consultas introducido por teclado es 5
                        consultasBBDD.consultar_en_base_datos("5", conexionBBDD.preguntarParametrosConexion(argumentosTerminal))   #Llamamos a la funcion que realiza consultas pasando como parametros
                        #el numero de consulta que queremos hacer que es el mismo que el del menú y la funcion ask_conn_parameters para extraer de ahi los parámetros necesarios
                        #para realizar la conexion con nuestra base de datos (host, puerto, usuario, contrasena, baseDatos)
                    elif opcion3 == "6": #Si el numero de opcion del menú de consultas introducido por teclado es 6
                        consultasBBDD.consultar_en_base_datos("6", conexionBBDD.preguntarParametrosConexion(argumentosTerminal))   #Llamamos a la funcion que realiza consultas pasando como parametros
                        #el numero de consulta que queremos hacer que es el mismo que el del menú y la funcion ask_conn_parameters para extraer de ahi los parámetros necesarios
                        #para realizar la conexion con nuestra base de datos (host, puerto, usuario, contrasena, baseDatos)
                    elif opcion3 == "7": #Si el numero de opcion del menú de consultas introducido por teclado es 7
                        consultasBBDD.consultar_en_base_datos("7", conexionBBDD.preguntarParametrosConexion(argumentosTerminal))   #Llamamos a la funcion que realiza consultas pasando como parametros
                        #el numero de consulta que queremos hacer que es el mismo que el del menú y la funcion ask_conn_parameters para extraer de ahi los parámetros necesarios
                        #para realizar la conexion con nuestra base de datos (host, puerto, usuario, contrasena, baseDatos)
                    elif opcion3 == "8": #Si el numero de opcion del menú de consultas introducido por teclado es 8
                        consultasBBDD.consultar_en_base_datos("8", conexionBBDD.preguntarParametrosConexion(argumentosTerminal))   #Llamamos a la funcion que realiza consultas pasando como parametros
                        #el numero de consulta que queremos hacer que es el mismo que el del menú y la funcion ask_conn_parameters para extraer de ahi los parámetros necesarios
                        #para realizar la conexion con nuestra base de datos (host, puerto, usuario, contrasena, baseDatos)    
                    else:   #Si el numero de opcion del menú de consultas introducido por teclado es un número de opcion que no se encuentra en el menú de consultas
                        print("Opción no válida. Por favor, elige una opción del menú.")   
                elif opcion == "3": #Si el numero de opcion del menú principal elegido por teclado es 3               
                    consultasBBDD.eliminar_en_base_datos(conexionBBDD.preguntarParametrosConexion(argumentosTerminal))   #Llamamos a la función que borra discos de la base de datos pasando como parámetros
                    #la funcion ask_conn_parameters para extraer de ahi los parámetros necesarios para realizar la conexion con nuestra base de datos (host, puerto, usuario, contrasena, baseDatos)
                    print("Información borrada de BBDD") #Informamos por pantalla de que se ha borrado informacion de la base de datos
                elif opcion == "4": #Si el numero de opcion del menú principal elegido por teclado es 4
                    consultasBBDD.modificarBBDD(conexionBBDD.preguntarParametrosConexion(argumentosTerminal))
                    print("Información modificada de BBDD") #Informamos por pantalla de que se ha modificado informacion de la base de datos
                elif opcion == "5": #Si el numero de opcion del menú principal elegido por teclado es 5
                    break   #Rompo bucle para que finalice el programa ya que este numero de opcion es para eso
                else:   #Si el numero de opcion del menú principal elegido por teclado es un número de opcion que no se encuentra en el menú principal
                    print("Opción no válida. Por favor, elige una opción del menú.") #Aviso por pantalla de que el numero de opcion introducido no es válido
                    
            except conexionBBDD.portException:   #En caso de que salte excepcion por introducir un puerto que no sea valido
                #Mostrar por pantalla lo siguiente
                print("------------------------------------------------------------------------------------------------------\n")
                print("¡El puerto no es válido!")               
                break   #Rompe el bucle para que finalice el programa
            except KeyboardInterrupt:   #En caso de que salte excepcion por interrumpir el programa haciendo Control+C en la terminal para cerrar el programa
                #Mostrar por pantalla lo siguiente
                print("------------------------------------------------------------------------------------------------------\n")
                print("Programa interrumpido por el usuario")
                break   #Rompe el bucle para que finalice el programa
            except psycopg2.Error as e: #Para capturar cualquier error de base de datos 
                #Mostrar por pantalla toda la información respecto a ese error
                print("------------------------------------------------------------------------------------------------------\n")
                print("Ha sucedido el siguiente error en BBDD: "+str(e))                
                break   #Rompe el bucle para que finalice el programa 
            """except IndexError:  #En caso de que salte excepcion porque la lista en la que se almacena la informacion obtenida de discogs esta vacia
                # Mostrar por pantalla lo siguiente ya que en ese caso es que no se ha encontrado información en la base de datos de discogs para ese código de barras
                print("------------------------------------------------------------------------------------------------------\n")
                print("Este código de barras no se encuentra disponible en discogs, introduce un código de barras correcto")
                
                break   #Rompe el bucle para que finalice el programa"""
                     
            """except TypeError as e: 
                break   #Rompe el bucle para que finalice el programa"""
            """except NameError as e:
                print("------------------------------------------------------------------------------------------------------\n")
                print("Error: introducido por parámetro de la función una variable que no existe")
                print(str(e))
                break   #Rompe el bucle para que finalice el programa"""      

    if __name__ == "__main__":                                                      # Es el modula principal?
        if '--test' in sys.argv:                                                    # chequea el argumento cmdline buscando el modo test
            import doctest                                                          # importa la libreria doctest
            doctest.testmod()                                                       # corre los tests
        else:                                                                       # else
            main()                                                                  # ejecuta el programa principal


