class matriz(object):   #Clase que representa la matriz
        
    def __init__(self, data = [],row=[]):   # Constructor de la clase
        row=list(data)  # Lista auxiliar para el control de filas
        for i in range(len(row)):   # Evalua la lista
            if(type(row[i])==int or type(row[i])==float):  # Verifica si la fila es entera
                pass
            else:   # En caso de no ser entera genera una  lista
                row[i]=list(row[i])
        self.data = list(row)   # Regresa una lista o una lista de listas

# Sobrecarga para evitar mostrar las direcciones de memoria
    def __str__(self):  #Sobrecarga de string
        return str(self.data)

    def __repr__(self): # Representacion del objeto
        return self.__str__()
