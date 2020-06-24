import paho.mqtt.client as mqtt
import threading        # Concurrencia con hilos
import datetime         # Para generar fecha/hora actual
import binascii
import logging          # Logging
import time             # Retardos
import sys              # Requerido para salir (sys.exit())
import os               # Ejecutar comandos de terminal
from brokerData import *
salas = 'salas'             #LFMV salas donde estan todas las salas a que pertenece este usuario
usuarios = 'usuarios'       #LFMV usuarios que estan inscritos en el sistema
Id_user = 'Usuario'         #LFMV ID del usuario

class cliente(object): #LFMV se inicia la clase cliente
    #LFMV constructor de la clase
    def __init__(self):         #LFMV se crea el constructor
        self.loggingConfig()   #LFMV comienza la funcion de looging
        self.initMqttclient()  #LFMV inicia MQTT
    
    def initMqttclient(self):    #LFMV se llaman los metodos de configuracion de mqtt
        self.setup()            
        self.Mqtttopic()
    
    def setup(self):
        self.client = mqtt.Client(clean_session=True) #LFMV Nueva instancia de cliente
        self.client.on_connect = self.on_connect #LFMV Se configura la funcion "Handler" cuando suceda la conexion
        self.client.on_message = self.on_message #LFMV Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
        self.client.username_pw_set(MQTT_USER, MQTT_PASS) #LFMV Credenciales requeridas por el broker
        self.client.connect(host=MQTT_HOST, port = MQTT_PORT) #LFMV Conectar al servidor remoto

    #LFMV Callback que se ejecuta cuando nos conectamos al broker
    def on_connect(self, client, userdata, rc):
        self.logging.info("Conectado al broker")

    #LFMV Callback que se ejecuta cuando llega un mensaje al topic suscrito
    def on_message(self, client, userdata, msg):
    #LFMV Se muestra a que topic a llegado el mensaje
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic)) 
        t = str(msg.topic) 
        tema = t.split('/') #LFMV Se separan los topic para verificar si es audio o es texto
        if tema[0] == "audio": #LFMV if para poder recibir los audios o recibir los mensajes
            audio = str(datetime.datetime.now().ctime())    # EAMA Nombre de audio con timestamp
            audio=audio.replace(" ","_")  #EAMA Eliminando espacios del nombre
            f = open(audio+'.wav', 'wb')   #LFMV Abre el nuevo archivo
            f.write(msg.payload)        # LFMV Escribe los archivo
            f.close()                   # LFMV cerramos el archivo
            logging.info("audio guardado")      #LFMV Mensaje de que se guardo bien el audio
            self.hilo(audio)                     # WAIG Inicia el hilo para la reproduccion
        else:
            logging.info("El contenido del mensaje es: " + str(msg.payload)) #LFMV Muestra el mensaje de texto recibido
    
    def hilo(self,audio):                 #WAIG iniciamos hilo para recibir el hilo
        logging.debug("iniciando hilo") 
        t1 = threading.Thread(name = 'reproducir audio',        #WAIG se configura el hilo
                        target = self.reproducir(audio),               #WAIG metodo a ejecutar
                        args = (),                              #WAIG argumentos del hilo
                        daemon = False                          #WAIG el hilo se detendra cuando termine de ejecutar el metodo
                        )
        t1.start()                                              #WAIG inicializamos el hilo
        t1.join()                                               #WAIG el hilo se detiene cuando termina el metodo a ejecutar

    def reproducir(self,audio):                                       #WAIG metodo para reproducir el audio
        logging.info("Reproduciendo audio")
        os.system('aplay '+audio+'.wav')                            #WAIG Reproduce el audio
        
    def Mqtttopic(self):                                        #LFMV Metodo para subscribirnos a las salas
        #LFMV Nos conectaremos a distintos topics:        
        salas = self.leersalas()                                #LFMV lee el texto salas donde estan definidas las salas del usuario
        logging.info("Salas subscritas: " + str(salas))         
        #LFMV Subscripcion simple con tupla (topic,qos)
        for i in salas:                                         #LFMV se concatenan las salas para poder recibir audio y texto
            topic1 = "audio/10/"+str(i)
            topic2 = "texto/10/"+str(i)
            self.MqttSubs(topic1,topic2)                        #LFMV metodo que subscribe a los temas
        file = open(Id_user,'r')                                #WAIG Abre el archivo donde esta el ID del usuario
    
        ID_USER = str(file.readline(9))                         #WAIG Lee al archivo para poder conocer el ID del usuario
        file.close()                                            #WAIG cierra el archivo
        self.MqttSubs("texto/10/"+ID_USER,"audio/10/"+ID_USER)  #LFMV funcion para publicar      
        self.client.loop_start()                                #LFMV inicia el hilo para la recepcion de mensajes de mqtt
    def MqttSubs(self,topic1,topic2,qos = 2):
        self.client.subscribe([(topic1,qos),(topic2,qos)]) #LFMV Comando para subscribirse a los topic
    def leersalas(self): #WAIG lee el texto salas 
        salas_sub = []          #WAIG crea una lista donde guardaremos las salas
        file = open(salas, 'r') #WAIG abre el archivo salas
        for linea in file.readlines():  #WAIGlista donde se guardaran las salas del usuario
            sala = linea.split('\n')    #WAIG quita los saltos de linea y guarda en una lista
            salas_sub.append(sala[0])   #guarda los datos en la lista
            #logging.debug("salas a las que se susbscribio: " + str(salas_sub))
        file.close()                    #WAIG cerramos el archivo lista
        return salas_sub                #WAIG regresa las salas a las que esta suscrito el usuario
    def loggingConfig(self):
    #LFMV Configuracion inicial de logging
        logging.basicConfig(
            level = logging.INFO, 
            format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
            )
    def closeMqtt(self):
        self.client.loop_stop() #LFMV Se mata el hilo que verifica los topics en el fondo
        self.client.disconnect() #LFMV Se desconecta del broker
    def comando(self):                  #WAIG metodo para ingresar los comandp
        logging.info("01 para enviar un audio \n 02 para enviar texto \n 03 exit")
        a = str(input("Ingrese accion:  " ))  #WAIG se ingresa comando para enviar texto o audio y la sala o usuario donde se manda
        self.mostrarusuarios()                #WAIG muestra los usuarios inscritos
        if a == '01':                          #WAIG comado para enviar audio
            logging.info("Salas o usuarios a enviar el audio")
            salas = str(input("Separe las salas y usuarios con $: "))  #WAIG pide ingresar las salas o los usuarios separados por $ 
            self.grabar(salas)                  #WAIG llama al metodo para grabar

        elif a == '02':                             #WAIG comando para enviar texto
            logging.info("Salas y usuarios a enviar el texto")
            salas = str(input("Separe las salas y usuarios con $: ")) #WAIG pide ingresar las salas o los usuarios separados por $
            self.enviartexto(salas)                                   #WAIG llama la funcion para enviar el texto
        elif a == '03':                                                #WAIG comando para salir
            self.exit()                                                #WAIG funcion para salir
    def grabar(self,sala):                                          #EAMA funcion para grabar audio
        while(True):                                                #EAMA no se permite enviar audios mayores a 30s 
            d = int(input("ingrese duracion:  "))                   # EAMA pide al usuario la duracion del audio
            if d > 30:                                              #EAMA solo permite audios menores de 30s
                logging.info("Duracion mayor a 30 segundos")
            else:
                break       
        logging.info("Se grabara audio: " + str(d) + "s \n")
        logging.info('Comenzando grabacion\n')
        os.system('arecord -d '+str(d)+' -f U8 -r 8000 audio.wav')      #EAMA graba el audio
        logging.info('Grabacion finalizada, inicia reproduccion\n')
        os.system('aplay audio.wav')                                    #EAMA reproduce el audio
        self.enviararchivo(sala)                                        #EAMA manda a llamar la funcion para enviar el audio y lleva de parametro las salas a enviar
    def enviartexto(self,comando):                                      #EAMA funcion para enviar el texto 
        msg = str(input("Ingrese mensaje:"))                            #EAMA pide al usuario ingresar el mensaje a enviar
        tt = "texto"                                                    #EAMA tema principal donde se publicara
        salas = comando.split("$")                                      #EAMA separas las salas ingresadas por un $
        for i in range(len(salas)):                                     #EAMA for para en separar las salas para enviar una por una
            sala = salas[i]                                             #EAMA guarda temporalmente la sala a enviar
            topic = str(tt)+'/10/'+str(sala)                            #EAMA arregla el topic a enviar
            self.MqttPub(topic,msg)                                     #EAMA llama la funcion para publicar
        
    def enviararchivo(self,comando):            #WAIG funcion para enviar archivo, recibe como argumento las salas
        logging.info("Enviar audio grabado\n")
        with open('audio.wav', 'rb') as a: #WAIG abrimos el archivo en lectura binaria
            imagestring = a.read()         #WAIG guarda el archivo en una variable
        a.close()                          #WAIG se cierra el archivo
        
        byteArray = bytearray(imagestring)  #EAMA convertimos los datos a un array de bytes
        tf = "audio"                        #EAMA tema al que se va a enviar
        salas = comando.split("$")          #EAMA se separa las salas o usuarios ingresados

        for i in range(len(salas)):                 #EAMA for para poder concatener las salas con el topic principal de audio
            self.publicar(salas[i], byteArray,tf)       #EAMA llama a la funcion de publicar con argumento la sala a enviar, el archivo en binario
            logging.info("\n\nArchivo enviado a: "+ str(salas[i]))
    def publicar(self,comando,mensaje,tf):      #EAMA metodo para concatenar la sala
        #sala = comando                          
        topic = str(tf)+'/10/'+str(comando)        #EAMA concatena los temas
        self.MqttPub(topic,mensaje)                 #EAMA se llama la funcion para publicar en mqtt
    def MqttPub(self,topic,mss):        
        self.client.publish(topic, mss, qos = 0, retain = False) #EAMA funcion para publicar en mqtt
        logging.debug("Publicado en:" + str(topic))
    def exit(self):  #EAMA método para salir del programa
        sys.exit()      #EAMA funcion para salir del programa
    def mostrarusuarios(self):      #EAMA funcion para mostrar usuarios
        salas = self.leersalas()       #EAMA funcion que llama las salas
        usuarios = self.leerusuarios() #EAMA funcion que llama a los usuarios
        logging.info("Salas suscritas: "+str(salas))  #EAMA muestra las salas
        logging.info("Usuarios: "+str(usuarios))       #EAMA muestra a los usuarios con sus datos
    def leerusuarios(self): #WAIG lee el texto salas 
        usuarios_sub = []          #WAIG crea una lista donde guardaremos las salas
        file = open(usuarios, 'r') #abre el archivo salas
        for linea in file.readlines():  #WAIG lista donde se guardaran las salas del usuario
            usuario = linea.split('\n')    #WAIG quita los saltos de linea y guarda en una lista
            usuarios_sub.append(usuario[0])   #WAIG guarda los datos en la lista
            #logging.debug("salas a las que se susbscribio: " + str(salas_sub))
        file.close()                    #WAIG cerramos el archivo lista
        return usuarios_sub                #WAIG regresa las salas a las que esta suscrito el usuario

cliente = cliente()  #LFMV Inicia la clase

try:
    while True:
        logging.debug("Iniciando ...") #LFMV mensaje de comienzo
        cliente.comando()               #LFMV llama a la primera funcion para ingresar los datos

except KeyboardInterrupt:
    logging.warning("Desconectando del broker...") #LFMV por si cerramos el programa con ctrl+c

finally:
    cliente.closeMqtt()                                     #LFMV mensaje al finalizar el programa
    logging.info("Desconectado del broker. Saliendo...")