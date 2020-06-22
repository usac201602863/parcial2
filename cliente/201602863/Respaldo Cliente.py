# ssh pr10@167.71.243.238  conectarse al servidor
# Librerias utilizadas
from brokerData import * #Informacion de la conexion
from usuario import*    # Credenciales del usuario
from salas import*      # Salas a las que pertenece el usuario
import threading        # Concurrencia con hilos
import datetime         # Para generar fecha/hora actual
import logging          # Logging
import time             # Retardos
import sys              # Requerido para salir (sys.exit())
import os               # Ejecutar comandos de terminal
#########################################################################################################
#               Funciones Utilizadas
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
#               Codigo principal
"""
logging.basicConfig(    # Configuracion inicial para logging.
    level = logging.DEBUG,  #  logging.DEBUG muestra todo. ############## cambiar antes de entrega a .info
    format = '\n\n[%(levelname)s] %(message)s'
    )

###################################################################################################3
#               HILO PRINCIPAL
State=True
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
            pass
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
                    #grabar(audio,d)
                    #reproducir(audio,d)
                else:
                    #print("\n[ERROR]El mensaje no debe ser mayor a 30 segundos")
                    logging.error('El mensaje no debe ser mayor a 30 segundos')
            else:
                logging.error('Debe ingresar un numero.')

        elif(opcion==4):    # Enviar voz a sala
            pass
        elif(opcion==5):    # Salir
            os.system('clear')
        elif(opcion==6):    # Salir
            # Matar todos los hilos
            logging.info("Terminando hilos")
            logging.info("Saliendo de la Aplicacion...")
            print("Saliendo de la Aplicacion...")
            State=False
    else:
        print("\n [ERROR]Debe ingresar un numero para seleccionar una opcion.")
"""

    


