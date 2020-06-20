# Librerias utilizadas
from usuario import*
from salas import*
import os

# Clases Utilizadas


# Codigo principal
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
    opcion=int(input('Ingrese un numero: ')) # Crear validaciones, si ingresa letra, valor diferente u otras

    if(opcion==1):  # Enviar texto a usuario
        pass
    elif(opcion==2):    # Enviar texto a sala
        pass
    elif(opcion==3):    # Enviar voz a usuario
        pass
    elif(opcion==4):    # Enviar voz a sala
        pass
    elif(opcion==5):    # Salir
        os.system('clear')
    elif(opcion==6):    # Salir
        print("Saliendo de la Aplicación...")
        State=False

