import socket
import binascii
import os
import paho.mqtt.client as mqtt
import logging
import time
from brokerData import * #Informacion de la conexion

comandos = 'coman.txt'

#LFMV Configuracion inicial de logging
logging.basicConfig(
    level = logging.DEBUG, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )
#LFMV Callback que se ejecuta cuando nos conectamos al broker
def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")

#LFMV Callback que se ejecuta cuando llega un mensaje al topic suscrito
def on_message(client, userdata, msg):
    """
    Aqui guardo los datos enviados de mqttp, aqui pensaba hacer que se verificara si se podia hacer la transmision de archivos
    y tambien enviar la señal para que se conecte el cliente al socket
    """
    #LFMV Se muestra en pantalla informacion que ha llegado
    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
    logging.info("El contenido del mensaje es: " + str(msg.payload))
    archivo = open(comandos, 'w')
    archivo.write(str(msg.payload))
    #archivo.write("\n")
    archivo.close
    #if  msg.payload  == b'x0a':  #LFMV para iniciar la transferencia de archivos
        #enviar(msg.payload)
    #return msg


client = mqtt.Client(clean_session=True) #LFMV Nueva instancia de cliente
client.on_connect = on_connect #LFMV Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message #LFMV Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #LFMV Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #LFMV Conectar al servidor remoto

#LFMV Nivel de qos
qos = 2

#LFMV Subscripcion simple con tupla (topic,qos)
client.subscribe(("comandos/10/#", qos))
#LFMV Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()

# LFMV Crea un socket TCP
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER_ADDR = 'localhost'
SERVER_PORT = 9810

BUFFER_SIZE = 64 * 1024 #LFMV habilita el buffer de 64kb

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_ADDR, SERVER_PORT))
server_socket.listen(5) 

#def leer():
 #   msg = on_message()
  #  return msg


#def enviar(msg):               #LFMV definicion que enciende el socket e inicia el envio de archivos
    
print("Encendiendo Servidor TCP")
    #i = 0
try:
    while True:
        print("\nEsperando conexion remota...\n")
        
        conn, addr = server_socket.accept()         #LFMV Datos del quien se conecta al socket
        print(conn , addr)
        print('Conexion establecida desde ', addr)  #LFMV Muestra la ip de donde se conectaron
        print('Enviando audio...')
            #a = leer()           #
            #print (a)
        #print(msg)
        archivo = open(comandos, 'r')
        mensaje = archivo.read()
        print(len(mensaje))

        archivo.close()
        m = mensaje.split("'")
        """
        Aqui por medio de los datos guardados se mandaria un mensaje para que el cliente se prepare para 
        recibir o para enviar los archivos
        """
        print(m[1])
        if m[1] == "x0a":
            mens = b'recibir archivo'  #esta parte hay que cambiarla 
            conn.sendall(mens)
            with open('pr10_server.wav', 'rb') as f: #LFMV Se abre el archivo a enviar en BINARIO
                bytes = f.read() #LFMV leeemos el archivo en forma de bytes para enviar
                conn.sendall(str(len(bytes)).encode())
                conn.sendfile(f, 0) #LFMV Enviamos el archivo
            f.close()
            print("\n\nArchivo envio a: ", addr)
        else:
            mens = b'enviar archivo'
            conn.sendall(mens)
            print(mensaje)
            with open('pr10_server.wav', 'rb') as f: #LFMV Se abre el archivo a enviar en BINARIO
                bytes = f.read() #LFMV leeemos el archivo en forma de bytes para enviar
                conn.sendall(str(len(bytes)).encode())
                conn.sendfile(f, 0) #LFMV Enviamos el archivo
            f.close()
            print("\n\nArchivo enviado a: ", addr)
            #i += 1
            #if i >= 3:
            #    print(i)
            #    break
            
finally:
    print("Cerrando el servidor...") #LFMV se cierra el socket cuando termina el envio
    server_socket.close()

#while(True):
    #logging.info("olakease")        #LFMV  ciclo para que no se cierre el programa
    #time.sleep(10)


