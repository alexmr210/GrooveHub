#imports nuevo lector codigo de barras
import cv2  #import libreria para procesamiento de imagenes
import time #se usa para un sleep que se usa en la funcion nuevoEscanearCodigoBarrasWebcam

#import codigo de barras arm 
try:
    import zxing    #se usa para decodificar codigos de barras si la arquitectura del procesador es ARM
except Exception:   #Si la arquitectura del procesador no soporta este import salta excepcion 
    pass    #y hacemos que este import no se haga

try:
    from pyzbar.pyzbar import decode    #se usa para decodificar codigos de barras si la arquitectura del procesador es x64
except Exception:   #Si la arquitectura del procesador no soporta este import salta excepcion
    pass    #y hacemos que este import no se haga

import platform     #Para saber arquitectura procesador


class lecturaCodigos:
    
    def detectarArquitecturaEscaneoCodigoBarrasWebcam():
        """_summary_

        >>> lecturaCodigos.detectarArquitecturaEscaneoCodigoBarrasWebcam()
        '886978057327'
        """
        #En función de la arquitectura del procesador ejecutaremos una funcion o otra que escanea el código de barras a partir de la webcam
        procesador = platform.processor()   #Detectamos la arquitectura del procesador en el que se ejecuta el programa y lo guardamos en la variable 
        #print(procesador)
        if procesador != "arm": #si no es arm, es decir, si es x64
            codigo_barras=lecturaCodigos.nuevoEscanearCodigoBarrasWebcam(decode)    #ejecutamos esta funcion a la cual se la pasa el decode de pyzbar 
            #y el resultado de esta funcion que es el codigo de barras que lee, lo guardamos en la variable
        else:   #si es arm
            codigo_barras=lecturaCodigos.escanear_codigo_barras_webcam()    #se ejecuta esta otra funcion de escaneo de codigo de barras con la webcam
            #y el resultado de esta funcion que es el codigo de barras que lee, lo guardamos en la variable
        return codigo_barras    #devolvemos el codigo de barras que hemos obtenido de escanear con la webcam    

    def multiplesCodigosBarrasWebcam(codigo_barras):
        #En función de la arquitectura del procesador ejecutaremos una funcion o otra que escanea el código de barras a partir de la webcam
        procesador = platform.processor()   #Detectamos la arquitectura del procesador en el que se ejecuta el programa y lo guardamos en la variable
        listaCodigosBarras=[]
        while True:
            print("1.Escanear mas códigos de barras")
            print("2.Proceder a insertar códigos de barras ya escaneados")    
            opcion=input("Elige una opción: ")    #Preguntamos por el numero de opcion del menú  que se desea para que sea introducido por teclado
            if opcion=="1":
                
                #Si hay 0 elementos en el array se introduce el primer codigo de barras que ya habiamos escaneado antes en el array
                if len(listaCodigosBarras)==0:  
                    listaCodigosBarras.append(codigo_barras) 

                if procesador != "arm": #si no es arm, es decir, si es x64
                    codigo_barras=lecturaCodigos.nuevoEscanearCodigoBarrasWebcam(decode)    #ejecutamos esta funcion a la cual se la pasa el decode de pyzbar 
                    #y el resultado de esta funcion que es el codigo de barras que lee, lo guardamos en la variable
                    listaCodigosBarras.append(codigo_barras)
                else:   #si es arm
                    codigo_barras=lecturaCodigos.escanear_codigo_barras_webcam()    #se ejecuta esta otra funcion de escaneo de codigo de barras con la webcam
                    #y el resultado de esta funcion que es el codigo de barras que lee, lo guardamos en la variable
                    listaCodigosBarras.append(codigo_barras)
                return listaCodigosBarras
            if opcion=="2":
                break   #Rompemos el bucle para salir de el
        return codigo_barras
        
        
        
                
                

    def nuevoEscanearCodigoBarrasWebcam(decode):
        """_summary_

        >>> lecturaCodigos.nuevoEscanearCodigoBarrasWebcam(decode)
        '886978057327'
        """
        try:
            #El parámetro decode sale de from pyzbar.pyzbar import decode
            
            captura=cv2.VideoCapture(0) #llamamos a VideoCapture del import de cv2 metiendo de parametro el valor 0 para que coja la primera camara que haya
            detectado=False  #Esta variable la cambiaremos a true cuando haya detectado un código de barras
            #estas dos variables las pongo asi ya que si no como son variables locales despues no puede acceder a menos que ponga esto
            imagen=0
            datosCodigoBarras=0
            while captura.isOpened() and not detectado:  #se hace este bucle mientras la camara este abierta y la variable detectado esté a False
                esLeido,fotograma=captura.read() #de aqui cogemos captura que es la imagen capturada por la webcam
                fotograma=cv2.flip(fotograma,1) #se hace esto para que no se vea en efecto espejo la captura 
                codigoBarrasDetectado=decode(fotograma)   #se usa decode de pyzbar para detectar códigos de barras   
                for codigoBarras in codigoBarrasDetectado: #Se recorren todos los codigos de barras detectados en el fotograma
                    (x, y, w, h) = codigoBarras.rect #Obtenemos del codigo de barras detectado coordenadas x e y, y el largo y ancho del rectangulo
                    #en el que se encuentra el código de barras

                    #Aqui se dibuja sobre captura rectangulo cuyas coordenadas arriba a la izquierda del rectangulo son (x, y)
                    #las coordenadas abajo a la derecha del rectángulo son (x + w, y + h)
                    #(255, 0, 0) es que pone al maximo el azul, los que estan a 0 son el verde y el rojo
                    #2 es el grosor del rectángulo
                    cv2.rectangle(fotograma, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    datosCodigoBarras = codigoBarras.data.decode('utf-8')  #Se decodifica el numero del codigo de barras y se guarda en esa variable
                    tipoCodigoBarras = codigoBarras.type  #Aqui se guarda el tipo de codigo de barras que se ha escaneado
                    texto = "{} ( {} )".format(datosCodigoBarras, tipoCodigoBarras) #Se mete barcodeData y barcodeType en los corchetes puestos antes
                    #Pone el texto del codigo de barras sobre la captura en el que se ha detectado el codigo de barras
                    #(x, y - 10) es la posicion en la que pone el texto que es 10 pixeles mas arriba que la esquina superior izquierda 
                    #del rectangulo dibujado antes
                    #cv2.FONT_HERSHEY_COMPLEX es la fuente del texto, 0.5 es el tamaño de esa fuente
                    #(255, 0, 0) es que lo pone en azul, los que estan a 0 son el rojo y el verde
                    #2 es el grosor del texto
                    cv2.putText(fotograma, texto, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2)    
                    imagen=fotograma    #guardamos la captura en la variable imagen
                    detectado=True   #ponemos detected a True ya que hemos detectado codigo de barras en la captura


                cv2.imshow('Escaneo de codigo de barras', fotograma)    #muestra el fotograma actual que ve la camara
                #si durante 1 milisegundo lee la letra q rompemos el bucle while que hace que se vea el
                #fotograma actual que ve la camara
                #Si durante un milisegundo cv2.waitKey(1) detecta valor de tecla presionada lo devuelve y se comprueba que sea igual que valor 
                #que da ord('q') que es el valor que tiene que tener la letra q, si coinciden es que se presionó la letra q
                if cv2.waitKey(1)==ord('q'):    #Si durante un milisegundo se detecta presionada la tecla q se sale del escaneo de códigos de barras  
                    break
            
            #muestra el fotograma en el que se detectó el código de barras con el rectangulo y el texto puestos en el fotograma
            cv2.imshow('Escaneo de codigo de barras', imagen)   
            time.sleep(5)   #Para que de tiempo a ver el rectangulo y texto puestos en el fotograma

            #print('El código de barras es:',barcodeData)
            #Retorna el valor del codigo de barras que ha decodificado del fotograma en el que se detectó el código de barras
            return datosCodigoBarras  
        except TypeError:
            print("Error: se esta introduciendo por los parámetros otros tipos de datos diferentes a los esperados")
        
    def escanearCodigoBarrasImagen():
        lector = zxing.BarCodeReader()  #Lector codigo de barras
        rutaImagen=input("Introduce la ruta de la imagen de la que quieres escanear su código de barras: ")
        resultado = lector.decode(rutaImagen)   #decodificar codigo barras imagen
        codigo_barras=resultado.raw     #variable resultado da mas de una cosa, si pones .raw devuelve codigo de barras en si
        stringCodigoBarras=str(codigo_barras)
        if codigo_barras is not None:
            print("Código de barras detectado: ", stringCodigoBarras)        
        return stringCodigoBarras    #Retorna el valor de codigo de barras detectado en la imagen
    
    def escanear_codigo_barras_webcam():
        """_summary_

        Returns:
            _type_: _description_
        """
        try:
            captura = cv2.VideoCapture(0)   #Capturo video desde la webcam, numero 0 hace que se coja primera webcam disponible
            lector = zxing.BarCodeReader()  #Lector codigo de barras
            while True:
                esLeido, fotograma = captura.read()  #Leer fotograma actual
                if esLeido:  # Si la lectura fue exitosa
                    cv2.imwrite('temp.png', fotograma)  #fotograma como imagen temporal lo guardamos
                    resultado = lector.decode('temp.png')   #decodificar codigo barras imagen
                    #print(resultado)
                    codigo_barras=resultado.raw     #variable resultado da mas de una cosa, si pones .raw devuelve codigo de barras en si
                    if codigo_barras is not None: 
                        #Avisamos de que se detectó coódigo de barras por pantalla mostrando que código de barras leyó
                        print("Código de barras detectado: ", codigo_barras)    
                        #Sacamos array que contiene dos puntos que saca de donde se encuentra codigo de barras
                        puntos=resultado.points 
                        #print(len(esquinasRectangulo)) #devuelve solo 2 elementos el array, que son los dos puntos que cojo despues
                        x1,y1=puntos[0] #coordenadas x e y de uno de los puntos que devuelve
                        x2,y2=puntos[1] #coordenadas x e y de otro de los puntos que devuelve
                        #print(f"x1: {x1}")
                        #print(f"y1: {y1}")
                        #print(f"x2: {x2}")
                        #print(f"y2: {y2}")

                        #Unimos las 2 puntos dibujando una linea cada vez que detecte un código de barras
                        #No entiendo por que no se visualiza la linea
                        cv2.line(fotograma, (int(x1),int(y1)), (int(x2),int(y2)), (255,0,0), 2)
                        imagen=fotograma    #guardamos la captura en la variable imagen
                        

                        break
                cv2.imshow('Escaneo de codigo de barras', fotograma)    #Mostrar fotograma en una ventana    
                    #cv2.waitKey(1)
                    
                #Si durante un milisegundo cv2.waitKey(1) detecta valor de tecla presionada lo devuelve y se comprueba que sea igual que valor 
                #que da ord('q') que es el valor que tiene que tener la letra q, si coinciden es que se presionó la letra q
                if cv2.waitKey(1)==ord('q'):    #Si durante un milisegundo se detecta presionada la tecla q se sale del escaneo de códigos de barras 
                    #Importante comentar que sin linea de codigo cv2.waitKey(1) ventana de visualizacion de la webcam no funciona, es como si en ese
                    #caso al no esperar a tecla para cerrar cerrase instantaneo
                    break 
            #time.sleep(5)   #Para que de tiempo a ver la linea puesta sobre el código de barras
            # Liberar la captura de video y cerrar las ventanas
            captura.release()
            cv2.destroyAllWindows() #Cierras ventana que abre imshow
            return codigo_barras

        except Exception as e:
            print("Se ha producido un error: ", str(e)) 
    
    def multiplesCodigosBarrasTeclado(codigo_barras):
        listaCodigosBarras=[]
        while True:
            print("1.Introducir mas códigos de barras")
            print("2.Proceder a insertar códigos de barras ya introducidos")    
            opcion=input("Elige una opción: ")    #Preguntamos por el numero de opcion del menú que se desea para que sea introducido por teclado
            if opcion=="1":
                #Si hay 0 elementos en el array se introduce el primer codigo de barras que ya habiamos introducido antes en el array
                if len(listaCodigosBarras)==0:  
                    listaCodigosBarras.append(codigo_barras) 
                     #se ejecuta la funcion de leer_codigo_barras que usabamos para introducir un solo código de barras
                    codigo_barras=lecturaCodigos.leer_codigo_barras()     
                    #y el resultado de esta funcion que es el codigo de barras que lee, lo guardamos en la variable
                    listaCodigosBarras.append(codigo_barras)
                else:
                    #se ejecuta la funcion de leer_codigo_barras que usabamos para introducir un solo código de barras
                    codigo_barras=lecturaCodigos.leer_codigo_barras()     
                    #y el resultado de esta funcion que es el codigo de barras que lee, lo guardamos en la variable
                    listaCodigosBarras.append(codigo_barras)
            elif opcion=="2":
                #Asi sale de funcion directamente sin necesidad de romper bucle devolviendo el parametro que se introdujo en la funcion
                if len(listaCodigosBarras)==0:  #en el caso de no introducir mas de un codigo de barras devolvemos el parametro que se introdujo
                    return codigo_barras
                else:   #Si hay mas de un codigo de barras introducido se devuelve la lista
                    return listaCodigosBarras 
            else: 
                print("Opción no válida. Por favor, elige una opción del menú.")
                
        
    
    def leer_codigo_barras():
        """Función que lee el código de barras que se introduzca por teclado

        >>> lecturaCodigos.leer_codigo_barras()
        Por favor, introduce un código de barras: 314 526 013-2
        '314 526 013-2'
        """
        codigo_barras = input("Por favor, introduce un código de barras: ") #Se pide por pantalla que introduzca por teclado el codigo de barras
        return codigo_barras    #Devuelve el código de barras introducido por teclado