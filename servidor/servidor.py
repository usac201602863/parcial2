from configuracion import*
from brokerData import * #Informacion de la conexion
import paho.mqtt.client as mqtt
import binascii
import logging
import time
import os 
###########################################################################################################
#               Configuracion Broker
def on_connect(client, userdata, rc):   #Callback que se ejecuta cuando nos conectamos al broker
    logging.info("Conectado al broker")

def on_message(client, userdata, msg):  #Callback que se ejecuta cuando llega un mensaje al topic suscrito
    mensaje=msg.payload.split("$".encode("utf-8"))  # Se divide la informacion por el caracter especial
    
    if(mensaje[0]==ALIVE):  # Recibe en la trama un ALIVE
        mensaje[1]=mensaje[1].decode("utf-8")
        logging.debug("Ha llegado el mensaje al topic: " + str(msg.topic))
        logging.debug("ALIVE recibido de: " + mensaje[1])
        logging.debug(str(msg.payload))
    
    #Y se almacena en el log 
    logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME
    os.system(logCommand)

LOG_FILENAME = 'mqtt.log'

logging.basicConfig(    #Configuracion inicial de logging
    level = logging.DEBUG,   #INFO
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

client = mqtt.Client(clean_session=True)    # Nueva instancia de cliente
client.on_connect = on_connect  # Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message  # Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS)    # Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT)    # Conectar al servidor remoto

###########################################################################################################
def salas(fileName = 'salas.txt'):    # Lista de salas registradas
    datos=[]
    archivo = open(fileName,'r')    # Abre el archivo en modo de LECTURA
    for i in archivo:    # Lee cada linea del archivo
        linea=i.split(',')  # Separa cada dato luego de una coma
        linea[-1] = linea[-1].replace('\n', '')     # Se remplaza el ultimo salto de linea
        datos.append(linea)     # Se agrega el dato a la lista
    archivo.close() #Cerrar el archivo al finalizar
    return datos     # Se regresa una tupla porque no se deben editar los datos

def usuarios(fileName = 'usuarios.txt'):    # Lista de salas registradas
    datos=[]
    archivo = open(fileName,'r')    # Abre el archivo en modo de LECTURA
    for i in archivo:    # Lee cada linea del archivo
        linea=i.split(',')  # Separa cada dato luego de una coma
        linea[-1] = linea[-1].replace('\n', '')     # Se remplaza el ultimo salto de linea
        datos.append(linea)   # Se agrega el dato a la lista
    archivo.close() #Cerrar el archivo al finalizar
    return datos    # Se regresa una tupla porque no se deben editar los datos

#print(type(usuarios()))
#print(usuarios())
#tupla=tuple(usuarios())
#print(tupla[0][1])
#print("\n\n")
#print(type(salas()))
#print(salas())
#print(len(salas()[0]))
#sala=usuarios()
#for i in range(len(sala)):
#    for j in range(len(sala[i])):
#        print(sala[i])

#############################################################################################
"""
for i in range(len(salas())):   #Subscripcion a salas (topic,qos)
    sala=salas()[i][0].split("S")   # Separa el numero de grupo con el numero de sala
    topic=str("salas/"+str(sala[0])+"/S"+str(sala[1]))  # Concatena el topic
    client.subscribe((topic, qos))  # Realiza la suscripcion al topic indicado
    logging.info("Suscripcion a: "+topic)   

for i in range(len(usuarios())):    #Subscripcion a usuarios (topic,qos)
    topic=str("usuarios/"+str(usuarios()[i][0]))
    client.subscribe((topic, qos))
    logging.info("Suscripcion a: "+topic)
"""

logging.warning("Conectando con el broker MQTT...")     # Estableciendo conexion con MQTT
qos = 2 # QoS de los topics
for i in range(len(usuarios())):    # Suscripcion a topics
    topic=str("comandos/10/"+str(usuarios()[i][0]))
    client.subscribe((topic, qos))
    logging.info("Suscripcion a: "+topic)

#Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start() # Crea un loop infinito tipo demonio, permite seguir trabajando
#client.loop_forever()  # Funcion bloqueante, no ejecuta el hilo principal

try:
    while True:
        logging.info("olakease")
        time.sleep(10)


except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")

