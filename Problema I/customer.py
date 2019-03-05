'''
Contiene la clase que representa a un
cliente
'''
import random


def probabilidad(prob):
    '''
    Funcion que representa una probabilidad
    '''
    random_number = random.random()

    if random_number <= prob:
        return True
    return False

class Customer:
    '''
    Clase que representa un cliente
    '''
    def __init__(self, id):
        '''
        Constructor de la clase
        '''
        self.tiempo_llegada_cola = -1
        self.tiempo_salida_cola = -1
        self.tiempo_atencion = -1
        self.servidor = -1
        self.id = id

    def customerDecline(self, long_cola):
        '''
        Funcion que retorna un booleano
        si un cliente decide o no hacer la cola
        '''

        if long_cola < 6:
            return False

        if 6 <= long_cola <= 8:
            return probabilidad(0.20)
        if 9 <= long_cola <= 10:
            return probabilidad(0.40)
        if 11 <= long_cola <= 14:
            return probabilidad(0.60)
        if long_cola >= 15:
            return probabilidad(0.80)
    
    def __str__(self):
        tiempo_llegada = '%.3f'%(self.tiempo_llegada_cola)
        tiempo_salida = '%.3f'%(self.tiempo_salida_cola)
        total = '%.3f'%(self.tiempo_atencion - self.tiempo_llegada_cola)
        tiempos = "        " + str(tiempo_llegada) + "              " + str(tiempo_salida) + "                  " + str(total)
        if self.id in range(10):
            return "Cliente 0" + str(self.id) +  tiempos
        return "Cliente " + str(self.id) + tiempos
        