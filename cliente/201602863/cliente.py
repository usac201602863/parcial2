# ssh pr10@167.71.243.238  conectarse al servidor
# Librerias utilizadas
from configuracion import*  # Constantes de configuracion
from brokerData import * #Informacion de la conexion
import paho.mqtt.client as paho
import threading        # Concurrencia con hilos
import datetime         # Para generar fecha/hora actual
import binascii
import logging          # Logging
import time             # Retardos
import sys              # Requerido para salir (sys.exit())
import os               # Ejecutar comandos de terminal
#########################################################################################################
#               Funciones Utilizadas
def salas(fileName = 'salas.txt'):    # Lista de salas registradas
    datos=[]
    archivo = open(fileName,'r')    # Abre el archivo en modo de LECTURA
    for i in archivo:    # Lee cada linea del archivo
        linea = i   # Separa cada dato luego de una coma
        linea = linea.replace('\n', '')     # Se remplaza el ultimo salto de linea
        datos.append(linea)     # Se agrega el dato a la lista
    archivo.close() #Cerrar el archivo al finalizar
    return datos     # Se regresa una tupla porque no se deben editar los datos

def usuario(fileName = 'usuario.txt'):    # Lista de salas registradas
    archivo = open(fileName,'r')    # Abre el archivo en modo de LECTURA
    for i in archivo:    # Lee cada linea del archivo
        linea = i     # Separa cada dato luego de una coma
        linea = linea.replace('\n', '')     # Se remplaza el ultimo salto de linea
    archivo.close() #Cerrar el archivo al finalizar
    return str(linea)    # Se regresa una tupla porque no se deben editar los datos

def grabar(audio="archivo",d=1):    # Funcion para grabar audio
    #audio = str(datetime.datetime.now().ctime())    # Nombre de audio con timestamp
    #audio=audio.replace(" ","_")  # Eliminando espacios del nombre
    logging.info('Iniciando grabacion')
    os.system('arecord -d '+str(d)+' -f U8 -r 8000 '+str(audio)+'.wav')
    logging.info('Grabacion finalizada. Iniciando envio.')

def reproducir(audio="archivo",d=1):    # Funcion para reproducir audio 
    #audio = str(datetime.datetime.now().ctime())    # Nombre de audio con timestamp
    #audio=audio.replace(" ","_")  # Eliminando espacios del nombre
    print("\n")
    logging.info('Recepcion finalizada. Iniciando reproduccion')
    os.system('aplay '+audio+'.wav')
    logging.info('El mensaje se ha terminado de reproducir.')
##########################################################################################################
#               Configuracion MQTT
logging.basicConfig(    # Configuracion inicial para logging.
    level = logging.DEBUG,  #  logging.DEBUG muestra todo. ############## cambiar antes de entrega a .info
    format = '\n\n[%(levelname)s] %(message)s'
    )

def on_connect(client, userdata, flags, rc):    #Handler en caso suceda la conexion con el broker MQTT
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
    logging.info(connectionText)


def on_publish(client, userdata, mid):          #Handler en caso se publique satisfactoriamente
    publishText = "Publicacion satisfactoria."
    logging.debug(publishText)

logging.info("Conexion exitosa cliente MQTT") #Mensaje en consola

#Config. inicial del cliente MQTT
client = paho.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto
"""
#   Suscripciones a topic
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
def publishData(topic, value, retain = False):  # Funcion para publicar 
    client.publish(topic, value, QoS, retain)

def sendCommand(command, retain = False):  # Funcion para publicar 
    topic='comandos/'+str(Grupo)+'/'+usuario()
    val=command+b'$'+usuario().encode("utf-8")
    client.publish(topic, val, QoS, retain)

def sendFTR(command,Filsize, retain = False):  # Funcion para publicar 
    topic='comandos/'+str(Grupo)+'/'+usuario()
    val=command+b'$'+usuario().encode("utf-8")+b'$'+Filsize.encode("utf-8")
    client.publish(topic, val, QoS, retain)

###################################################################################################3
#               HILO PRINCIPAL

DEFAULT_DELAY = 30 #1 minuto
try:

    #print(usuario().encode("utf-8"))
    #publishData("test","Mensaje Inicial pr80")
    #logging.info("Los datos han sido enviados al broker")            
    #time.sleep(DEFAULT_DELAY)   # Retardo hasta la proxima publicacion de info
    while(State):
        print("\n\nEnviar texto")
        print("\t 1 - Enviar a usuario")
        print("\t 2 - Enviar a sala")
        print("Enviar mensaje de voz: ") 
        print("\t 3 - Enviar a usuario")
        print("\t 4 - Enviar a sala")
        print("5 - Limpiar pantalla")
        print("6 - Salir")
        opcion=input('Ingrese un numero: ') # Crear validaciones, si ingresa letra, valor diferente u otras

        if(opcion.isnumeric()):
            opcion=int(opcion)
            if(opcion==1):  # Enviar texto a usuario
                publishData("test","Mensaje Inicial pr80")
                logging.info("Los datos han sido enviados al broker") 
                sendCommand(ALIVE)
                sendAlive()
            elif(opcion==2):    # Enviar texto a sala
                pass
            elif(opcion==3):    # Enviar voz a usuario
                # Selecciona usuario a publicar
                # Ingresa duracion del audio
                # Graba del audio
                # Envia el audio al servidor 

                # Manejo de excepciones +++++++++++++++++++++++++++++++++++++++++++++++
                d = input("Ingrese duracion en segundos: ") # Duracion del mensaje en segundos   
                if(d.isnumeric()):
                    d=int(d)
                    if (d<=30):
                        audio = str(datetime.datetime.now().ctime())    # Nombre de audio con timestamp
                        audio=audio.replace(" ","_")  # Eliminando espacios del nombre
                        grabar(audio,d)
                        reproducir(audio,d)
                    else:
                        logging.error('El mensaje no debe ser mayor a 30 segundos')
                else:
                    logging.error('Debe ingresar un numero.')
            elif(opcion==4):    # Enviar voz a sala
                pass
            elif(opcion==5):    # Salir
                os.system('clear')
            elif(opcion==6):    # Salir
                # Matar todos los hilos
                logging.warning("Terminando hilos...")
                State=False
        else:
            print("\n [ERROR]Debe ingresar un numero para seleccionar una opcion.")
except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")

finally:
    client.disconnect()
    logging.info("Se ha desconectado del broker.")
    logging.info("Saliendo de la Aplicacion...")


