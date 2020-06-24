import paho.mqtt.client as mqtt
import threading        # Concurrencia con hilos
import datetime         # Para generar fecha/hora actual
import binascii
import logging          # Logging
import time             # Retardos
import sys              # Requerido para salir (sys.exit())
import os               # Ejecutar comandos de terminal
from brokerData import *
salas = 'salas'
usuarios = 'usuarios'
Id_user = 'Usuario'

class cliente(object): #LFMV se inicia la clase cliente

    def __init__(self):         #LFMV se crea el constructor
        self.loggingConfig()
        self.initMqttclient()  
    
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
            f.write(msg.payload)        # Escribe los archivo
            f.close()                   # cerramos el archivo
            logging.info("audio guardado")      #Mensaje de que se guardo bien el audio
            self.hilo(audio)                     # Inicia el hilo para la reproduccion
        else:
            logging.info("El contenido del mensaje es: " + str(msg.payload)) #Muestra el mensaje de texto recibido
    
    def hilo(self,audio):                 #iniciamos hilo para recibir el hilo
        logging.debug("iniciando hilo") 
        t1 = threading.Thread(name = 'reproducir audio',        #se configura el hilo
                        target = self.reproducir(audio),               #metodo a ejecutar
                        args = (),                              #argumentos del hilo
                        daemon = False                          #el hilo se detendra cuando termine de ejecutar el metodo
                        )
        t1.start()                                              #inicializamos el hilo
        t1.join()

    def reproducir(self,audio):                                       #metodo para reproducir el audio
        logging.info("Reproduciendo audio")
        os.system('aplay '+audio+'.wav')
        
    def Mqtttopic(self):                                        #Metodo para subscribirnos a las salas
        #Nos conectaremos a distintos topics:        
        salas = self.leersalas()                                #lee el texto salas donde estan definidas las salas del usuario
        logging.info("Salas subscritas: " + str(salas))         
        #Subscripcion simple con tupla (topic,qos)
        for i in salas:                                         #se concatenan las salas para poder recibir audio y texto
            topic1 = "audio/10/"+str(i)
            topic2 = "texto/10/"+str(i)
            self.MqttSubs(topic1,topic2)                        #metodo que subscribe a los temas
        file = open(Id_user,'r')
    
        ID_USER = str(file.readline(9))
        file.close()
        print(ID_USER+'id user')
        self.MqttSubs("texto/10/"+ID_USER,"audio/10/"+ID_USER)        
        self.client.loop_start()
    def MqttSubs(self,topic1,topic2,qos = 2):
        self.client.subscribe([(topic1,qos),(topic2,qos)]) #comando para subscribirse a los topic
    def leersalas(self): #lee el texto salas 
        salas_sub = []          # crea una lista donde guardaremos las salas
        file = open(salas, 'r') #abre el archivo salas
        for linea in file.readlines():  #lista donde se guardaran las salas del usuario
            sala = linea.split('\n')    #quita los saltos de linea y guarda en una lista
            salas_sub.append(sala[0])   #guarda los datos en la lista
            #logging.debug("salas a las que se susbscribio: " + str(salas_sub))
        file.close()                    #cerramos el archivo lista
        return salas_sub                #regresa las salas a las que esta suscrito el usuario
    def loggingConfig(self):
    #Configuracion inicial de logging
        logging.basicConfig(
            level = logging.DEBUG, 
            format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
            )
    def closeMqtt(self):
        self.client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
        self.client.disconnect() #Se desconecta del broker
    def comando(self):                  #metodo para ingresar los comandp
        logging.info("01 para enviar un audio \n 02 para enviar texto \n 03 exit")
        a = str(input("Ingrese accion:  " ))  #se ingresa comando para enviar texto o audio y la sala o usuario donde se manda
        #comannd = a.split('$')
        self.mostrarusuarios()
        if a == '01':
            #logging.info("Enviar a salas o usarios ")
            #sou = str(input("Sala-> a \n Usuarios->b "))
            #if sou == 'a':
            
            logging.info("Salas o usuarios a enviar el audio")
            salas = str(input("Separe las salas y usuarios con $: "))
            self.grabar(salas)
            #elif sou == 'b':
            #    logging.info("Usuarios a enviar el audio")
            #    salas = str(input("Separe los usuarios con $: "))
            #    self.grabar(salas)
        elif a == '02':
            #logging.info("Enviar a salas o usarios ")
            #sou = str(input("Sala-> a \n Usuarios->b "))
            #if sou == 'a':
            logging.info("Salas y usuarios a enviar el texto")
            salas = str(input("Separe las salas y usuarios con $: "))
            self.enviartexto(salas)
            #elif sou == 'b':
            #    logging.info("Usuarios a enviar el texto")
            #    salas = str(input("Separe los usuarios con $: "))
            #    self.enviartexto(salas)
        elif a == '03':
            self.exit()
    def grabar(self,sala):
        while(True):
            d = int(input("ingrese duracion:  "))
            if d > 30:
                logging.info("Duracion mayor a 30 segundos")
            else:
                break       
        logging.info("Se grabara audio: " + str(d) + "s \n")
        logging.info('Comenzando grabacion\n')
        os.system('arecord -d '+str(d)+' -f U8 -r 8000 audio.wav')
        logging.info('Grabacion finalizada, inicia reproduccion\n')
        os.system('aplay audio.wav')        
        self.enviararchivo(sala)
    def enviartexto(self,comando):
        msg = str(input("Ingrese mensaje:"))
        tt = "texto"
        salas = comando.split("$")
        for i in range(len(salas)):
            sala = salas[i]
            topic = str(tt)+'/10/'+str(sala)
            self.MqttPub(topic,msg)
        
    def enviararchivo(self,comando):
        logging.info("Enviar audio grabado\n")
        with open('audio.wav', 'rb') as a: #AEGA abrimos el archivo en lectura binaria
            imagestring = a.read()
        a.close()
        
        byteArray = bytearray(imagestring)
        tf = "audio"
        salas = comando.split("$")

        for i in range(len(salas)):
            self.publicar(salas[i], byteArray,tf)
            logging.info("\n\nArchivo enviado a: "+ str(salas[i]))
    def publicar(self,comando,mensaje,tf):
        sala = comando
        topic = str(tf)+'/10/'+str(sala)
        self.MqttPub(topic,mensaje)
    def MqttPub(self,topic,mss):
        
        self.client.publish(topic, mss, qos = 0, retain = False)
        logging.debug("Publicado en:" + str(topic))
    def exit(self):
        self.cliente.closeMqtt()
    def mostrarusuarios(self):
        salas = self.leersalas()
        usuarios = self.leerusuarios()
        logging.info("Salas suscritas: "+str(salas))
        logging.info("Usuarios: "+str(usuarios))
    def leerusuarios(self): #lee el texto salas 
        usuarios_sub = []          # crea una lista donde guardaremos las salas
        file = open(usuarios, 'r') #abre el archivo salas
        for linea in file.readlines():  #lista donde se guardaran las salas del usuario
            usuario = linea.split('\n')    #quita los saltos de linea y guarda en una lista
            usuarios_sub.append(usuario[0])   #guarda los datos en la lista
            #logging.debug("salas a las que se susbscribio: " + str(salas_sub))
        file.close()                    #cerramos el archivo lista
        return usuarios_sub                #regresa las salas a las que esta suscrito el usuario

cliente = cliente()

try:
    while True:
        logging.debug("Iniciando ...")
        cliente.comando()

except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    cliente.closeMqtt()
    logging.info("Desconectado del broker. Saliendo...")