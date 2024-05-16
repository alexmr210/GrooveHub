class conexionBBDD:

    class portException(Exception): pass    #Se crea excepcion portException que hacemos que salte en el except de la funcion comprobacionPuerto

    def comprobacionPuerto(puerto):
        """

        >>> conexionDiscogs.comprobacionPuerto(1025)
        1025
        >>> conexionDiscogs.comprobacionPuerto(1000)
        Traceback (most recent call last):
        File "/Users/cealsan/Desktop/TFG/TFGAlvaroSantander/LOQUEUSO/TFG/PROGRAMAMODULADO/conexionDiscogs.py", line 14, in comprobacionPuerto
            raise ValueError     #hacemos saltar la excepcion ValueError que hace que se ejecute el bloque except que hace saltar la excepcion portException    
        ValueError

        During handling of the above exception, another exception occurred:

        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/Users/cealsan/Desktop/TFG/TFGAlvaroSantander/LOQUEUSO/TFG/PROGRAMAMODULADO/conexionDiscogs.py", line 18, in comprobacionPuerto
            raise conexionDiscogs.portException  #hacemos saltar excepcion portException que se creo antes       
        conexionDiscogs.portException
        """
        try:                                                                        

            intPuerto    = int(puerto)  #convertimos a entero el puerto que se introduce como parámetro en la función                                                   
            if (intPuerto < 1024) or (intPuerto > 65535):   # si el puerto no es valido                                                            
                raise ValueError     #hacemos saltar la excepcion ValueError que hace que se ejecute el bloque except que hace saltar la excepcion portException    
            else:
                return intPuerto    #devolvemos el numero de puerto en caso de que el puerto que recibe la función como parámetro es válido
        except ValueError:  #si salta excepcion ValueError     
            raise conexionBBDD.portException  #hacemos saltar excepcion portException que se creo antes       

    def preguntarParametrosConexion(argumentosTerminal):  #Obtenemos los parámetros de conexion, args contiene los argumentos que pasamos por la terminal al ejecutar el programa __init__.py
        """
        >>> preguntarParametrosConexion(argumentosTerminal)
        ('localhost', 5433, 'postgres', 'tfg', 'tfg7')
        >>> conexionDiscogs.preguntarParametrosConexion(23476)
        Error: el parámetro introducido no tiene los atributos que se piden en la funcion
        """
        try:
            host = 'localhost'                                                        #el nombre del host siempre suele ser localhost
            #port = ask_port('TCP port number: ')                                        
            puerto = conexionBBDD.comprobacionPuerto(argumentosTerminal.puerto)    #Recibimos el puerto del argumento que introducimos por la terminal al ejecutar el programa y lo pasamos por 
            #la funcion comprobacionPuerto para comprobar que el puerto sea correcto. En mi caso introduzco 5433
            usuario = argumentosTerminal.usuario                        #Recibimos el usuario del argumento que introducimos por la terminal al ejecutar el programa. En mi caso introduzco postgres                                                                                
            contrasena = argumentosTerminal.contrasena                #Recibimos la contrasena del argumento que introducimos por la terminal al ejecutar el programa. En mi caso introduzco tfg                                               
            baseDatos = argumentosTerminal.baseDatos                #Recibimos la base de datos del argumento que introducimos por la terminal al ejecutar el programa. En mi caso introduzco tfg7                                                            
            return (host, puerto, usuario, contrasena, baseDatos)   #Devolvemos todas estas variables cuyos valores de estas usaremos para podernos conectar con nuestra base de datos
        except AttributeError:
            print("Error: el parámetro introducido no tiene los atributos que se piden en la funcion")