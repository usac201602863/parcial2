
import os               # Ejecutar comandos de terminal
import logging          # Logging
import datetime         # Para generar fecha/hora actual

logging.basicConfig(    # Configuracion inicial para logging. logging.DEBUG muestra todo.
    level = logging.DEBUG, 
    format = '[%(levelname)s] %(message)s'
    )
"""
audio = str(datetime.datetime.now().ctime())    # Nombre de audio con timestamp
audio=audio.replace(" ","_")  # Eliminando espacios del nombre
print(audio)


d = input("Ingrese duracion en segundos: ")   #manejo de excepciones
print(d.isnumeric())
"""

"""
El método join se utiliza para que el hilo que ejecuta la llamada se
bloquee hasta que finalice el thread sobre el que se llama. En este caso
se utiliza para que el hilo principal no termine su ejecución antes que
los hijos, lo cuál podría resultar en algunas plataformas en la termina-
ción de los hijos antes de finalizar su ejecución. El método join puede
tomar como parámetro un número en coma flotante indicando el
número máximo de segundos a esperar.
"""
import threading

class MiThread(threading.Thread):
    def __init__(self,audio, d,daemon=None):
        threading.Thread.__init__(self)
        self.d = d
        self.audio=audio

    def run(self):  # Contiene el codigo que queremos se ejecute en el hilo
        logging.info('Iniciando grabacion')
        os.system('arecord -d '+str(self.d)+' -f U8 -r 8000 '+str(self.audio)+'.wav')
        logging.info('Grabacion finalizada. Iniciando envio.')

for i in range(0, 1):
    t = MiThread("hola",5)
    t.start()
    t.join()    # Espera a que el hilo pricipal termine de ejecutarse

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






