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
    datos=[]
    archivo = open(fileName,'r')    # Abre el archivo en modo de LECTURA
    for i in archivo:    # Lee cada linea del archivo
        linea = i     # Separa cada dato luego de una coma
        linea = linea.replace('\n', '')     # Se remplaza el ultimo salto de linea
        datos.append(linea)
    archivo.close() #Cerrar el archivo al finalizar
    return datos    # Se regresa una tupla porque no se deben editar los datos

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

def leer_archivo(archivo):                          #WAIG Funcion para leer el archivo y mostrar opciones
    datos = open(archivo, "r")                      #WAIG Abrimos el archivo
    numero = 1                                      #WAIG Variable que nos ayudara a mostrar el numero de elemento            
    for linea in datos:                             #WAIG For que leera linea por linea los elementos del archivo
        print(str(numero)+ ". " + linea)            #WAIG Se muestra en pantalla cada elemento
        numero += 1                                 #WAIG Se le suma un numero por cada elemento mostrado
    datos.close()                                   #WAIG Se cierra el documento

def selec_usu_grup(archivo,numero):                 #WAIG Funcion para seleccionar opcion de la lista
    datos = open(archivo, "r")                      #WAIG Abrimos el archivo
    list_datos = []                                 #WAIG Se declara una lista para aguardar los elementos de la lista
    for linea in datos:                             #WAIG For para leer cada elemento de la lista
        list_datos.append(linea)                    #WAIG Agrega un elemento a la lista
    datos.close()                                   #WAIG Se cierra el documento
    return str(list_datos[numero - 1])              #WAIG Se escoge el numero de elemento de la lista 


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
    #logging.debug(publishText)

def on_message(client, userdata, msg):
    menm = str(msg.payload)
    topic_recibido = 'Mensaje entrante del topic ' + str(msg.topic) + ': ' +  menm.replace("b","")
    logging.info(topic_recibido)

logging.info("Conexion exitosa cliente MQTT") #Mensaje en consola

#Config. inicial del cliente MQTT
client = paho.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.on_message = on_message #WAIG Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
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

def sendALIVE(delay=ALIVE_PERIOD, retain = False):  # Funcion para publicar
    for i in range(100): 
        topic="comandos"+'/'+str(Grupo)+'/'+usuario()[0]
        print(topic)
        val=ALIVE+b'$'+usuario()[0].encode("utf-8")    # EAMA Concatena caracteres en binario
        client.publish(topic, val, QoS, retain)
        logging.debug("Alive Enviado.")
        time.sleep(delay) # EAMA Delay en segundos

def sendFTR(Filsize, retain = False):  # Funcion para publicar 
    topic = 'comandos/'+str(Grupo)+'/'+usuario()[0]
    val = FTR+b'$'+usuario()[0].encode("utf-8")+b'$'+Filsize.encode("utf-8")
    client.publish(topic, val, QoS, retain)

###################################################################################################3
#               HILO PRINCIPAL

AliveTh = threading.Thread(name = 'ALIVE',
                        target = sendALIVE,
                        args = (),
                        daemon = True
                        )

AliveTh.start()
logging.debug("Iniciando Hilo de Alive")



DEFAULT_DELAY_2 = 0.5                                 #WAIG Tiempo 0.5 s
User_ID = 201612200                                 #WAIG ID del cliente
DEFAULT_DELAY = 30 #1 minuto

#WAIG Subscripcion a los topic 
#client.subscribe(('usuarios/10/'+str(User_ID), 1))

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
                #publishData("test","Mensaje Inicial pr80")
                #logging.info("Los datos han sido enviados al broker") 
                print("¿A que usuario desea enviar el mensaje?:")           #WAIG Preguntamos a que usuario se quiere enviar el mensaje
                leer_archivo("usuarios.txt")                                 #WAIG leemos el archivo de usuario y lo despleguegamos
                usuarioa = int(input('Ingrese el numero:'))
                nusu = int(selec_usu_grup('usuarios.txt',usuarioa))
                topic = 'usuarios/'+str(Grupo)+'/'+ str(nusu)               #WAIG Se forma el topic para mandar el mensaje
                client.loop_start()                                         #WAIG Conmenzamos a estar pendiente de mensajes entrantes
                time.sleep(DEFAULT_DELAY_2)                                 #WAIG Esperamos 5 milisegundos para que aparezca el mensaje de la conexion al servidor
                print('*************CHAT*****************')
                print('Presione enter para enviar el mensaje: ')
                while True:    
                    mensaje = input("")                                        #WAIG Se obtiene el mensaje
                    client.publish(topic,mensaje, qos = 1, retain = False)     #WAIG Se envia el mensaje a travez del topic
                    if on_connect :                                            #WAIG Si le llega un mensaje 
                        time.sleep(DEFAULT_DELAY_2)                            #WAIG Esperara 0.5 s para mostrar el mensaje,
                        print('Presione enter para enviar el mensaje: ') #     esto es mas que todo para que se vea ordenado

                    #sendCommand(ALIVE)
                    #sendAlive()

            elif(opcion==2):    # Enviar texto a sala
                print('¿A que grupo desea enviar el mensaje?:')             #WAIG Preguntamos a que sala se quiere enviar el mensaje
                leer_archivo('salas.txt')                                   #WAIG Leemos el archivo de salas y lo desplegamos 
                salac = int(input('Ingrese el numero:'))
                nsal = int(selec_usu_grup('salas.txt',salac))                     
                topic = 'salas/'+str(Grupo)+'/'+ 'S' + str(nsal)            #WAIG Se forma el topic para mandar el mensaje
                client.loop_start()                                         #WAIG Conmenzamos a estar pendiente de mensajes entrantes
                time.sleep(DEFAULT_DELAY_2)                                   #WAIG Esperamos 5 milisegundos para que aparezca el mensaje de la conexion al servidor   
                print('*************CHAT*****************')
                print('Presione enter para enviar el mensaje: ')
                while True:    
                    mensaje = input("")                                         #WAIG Se obtiene el mensaje
                    client.publish(topic,mensaje, qos = 1, retain = False)      #WAIG Se envia el mensaje a travez del topic
                    if on_connect :                                             #WAIG Si le llega un mensaje 
                        time.sleep(DEFAULT_DELAY_2)                               #WAIG Esperara 0.5 s para mostrar el mensaje,
                        print('Presione enter para enviar el mensaje: ') #     esto es mas que todo para que se vea ordenado


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
                if AliveTh.is_alive():
                    AliveTh.stop()
                State=False
        else:
            print("\n [ERROR]Debe ingresar un numero para seleccionar una opcion.")
except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")

finally:
    client.disconnect()
    logging.info("Se ha desconectado del broker.")
    logging.info("Saliendo de la Aplicacion...")


