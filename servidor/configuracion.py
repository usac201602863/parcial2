import binascii
QoS = 0		# Calidad de envio del mensaje
State = True    # Control de main principal
Grupo= 10   # Numero de grupo

FRR = binascii.unhexlify("02")	# Constante para transferencia de archivos servidor a cliente
FTR = binascii.unhexlify("03")	# Constante para transferencia de archivos cliente a servidor
ALIVE = binascii.unhexlify("04")	# Constante para indicar que esta activo
ACK = binascii.unhexlify("05")	# Constante para indicar que esta activo
OK = binascii.unhexlify("06")	# Constante para indicar que esta activo
NO = binascii.unhexlify("07")	# Constante para indicar que esta activo

ALIVE_PERIOD = 2    # El alive se envia cada 2 segundos
ALIVE_CONTINUO = 0.1    # Periodo entre alive si no hay respuesta


