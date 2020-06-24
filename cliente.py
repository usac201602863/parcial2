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
                f = open('new.wav', 'wb')   #LFMV Abre el nuevo archivo
                f.write(msg.payload)        # Escribe los archivo
                f.close()                   # cerramos el archivo
                logging.info("audio guardado")      #Mensaje de que se guardo bien el audio
                self.hilo()                     # Inicia el hilo para la reproduccion
        else:
            logging.info("El contenido del mensaje es: " + str(msg.payload)) #Muestra el mensaje de texto recibido
    
    def hilo(self):                 #iniciamos hilo para recibir el hilo
        t1 = threading.Thread(name = 'reproducir audio',        #se configura el hilo
                        target = self.reproducir,               #metodo a ejecutar
                        args = (),                              #argumentos del hilo
                        daemon = False                          #el hilo se detendra cuando termine de ejecutar el metodo
                        )
        t1.start()                                              #inicializamos el hilo
        logging.debug("iniciando hilo") 
    def reproducir(self):                                       #metodo para reproducir el audio
        logging.info("Reproduciendo audio")
        os.system('aplay new.wav')
        
    def Mqtttopic(self):                                        #Metodo para subscribirnos a las salas
        #Nos conectaremos a distintos topics:        
        salas = self.leersalas()                                #lee el texto salas donde estan definidas las salas del usuario
        logging.info("Salas subscritas: " + str(salas))         
        #Subscripcion simple con tupla (topic,qos)
        for i in salas:                                         #se concatenan las salas para poder recibir audio y texto
            topic1 = "audio/10/"+str(i)
            topic2 = "texto/10/"+str(i)
            self.MqttSubs(topic1,topic2)                        #metodo que subscribe a los temas
        self.MqttSubs("texto/10/"+str(ID_USER),"audio/10/"+str(ID_USER))        
        self.client.loop_start()
    def MqttSubs(self,topic1,topic2,qos = 2):
        self.client.subscribe([(topic1,qos),(topic2,qos)]) #comando para subscribirse a los topic
    def leersalas(self): #lee el texto salas 
        salas_sub = []          # crea una lista donde guardaremos las salas
        file = open(salas, 'r') #abre el archivo salas
        for linea in file.readlines():  #lista donde se guardaran las salas del usuario
            sala = linea.split('\n')    #quita los saltos de linea y guarda en una lista
            salas_sub.append(sala[0])   #guarda los datos en la lista
            logging.debug("salas a las que se susbscribio: " + str(salas_sub))
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
        a = str(input("Ingrese comando$sala:  " ))  #se ingresa comando para enviar texto o audio y la sala o usuario donde se manda
        comannd = a.split('$')
        if comannd[0] == '01':
            self.grabar(comannd)
        elif comannd[0] == '02':
            self.enviartexto(comannd)
    def grabar(self,comando):
        d = input("ingrese duracion:  ")
        logging.info("Se grabara audio: " + str(d) + "s \n")
        logging.info('Comenzando grabacion\n')
        os.system('arecord -d '+d+' -f U8 -r 8000 audio.wav')
        logging.info('Grabacion finalizada, inicia reproduccion\n')
        os.system('aplay audio.wav')        
        self.enviararchivo(comando)
    def enviartexto(self,comando):
        msg = str(input("Ingrese mensaje:"))
        tt = "texto"
        sala = comando[1]
        topic = str(tt)+'/10/'+str(sala)
        self.MqttPub(topic,msg)
        
    def enviararchivo(self,comando):
        logging.info("Enviar audio grabado\n")
        with open('audio.wav', 'rb') as a: #AEGA abrimos el archivo en lectura binaria
            imagestring = a.read()
        a.close()
        
        byteArray = bytearray(imagestring)
        tf = "audio"
        self.publicar(comando, byteArray,tf)
        logging.info("\n\nArchivo enviado a: "+ str(comando[1]))
    def publicar(self,comando,mensaje,tf):
        sala = comando[1]
        topic = str(tf)+'/10/'+str(sala)
        self.MqttPub(topic,mensaje)
    def MqttPub(self,topic,mss):
        
        self.client.publish(topic, mss, qos = 0, retain = False)
        logging.debug("Publicado en:" + str(topic))

cliente = cliente()

try:
    while True:
        logging.debug("Iniciando ...")
        time.sleep(3)
        cliente.comando()

except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    cliente.closeMqtt()
    logging.info("Desconectado del broker. Saliendo...")