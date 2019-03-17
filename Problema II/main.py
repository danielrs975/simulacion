from random import random, expovariate, uniform, randint
from math import sqrt
from scipy import stats
from collections import deque

# Funciones para calculo de probabilidades
def probabilidad_binomial(prob):
    numero_aleatorio = random()
    if numero_aleatorio <= prob:
        return True
    return False


# CLASES PARA LA SIMULACION
class Cliente:
    '''
    Clase que representa a los clientes
    del sistema
    '''
    def __init__(self, tiempo_llegada=None):
        '''
        Constructor de la clase
        '''
        self.tiempo_llegada = tiempo_llegada # Tiempo en el cual entra al sistema
        self.tiempo_salida_cola = None # Tiempo en el cual sale de la cola
        self.tiempo_en_el_sistema = None # Tiempo total en el sistema
        self.tiempo_atencion = None # Tiempo que dura el servidor en atenderlo

    def cliente_declina(self, long_cola):
        '''
        Metodo que devuelve un booleano
        si el cliente declina a hacer la cola
        o no
        '''
        if 6 <= long_cola <= 8:
            return probabilidad_binomial(0.20)
        elif 9 <= long_cola <= 10:
            return probabilidad_binomial(0.40)
        elif 11 <= long_cola <= 14:
            return probabilidad_binomial(0.60)
        elif long_cola >= 15:
            return probabilidad_binomial(0.80)
        return False

class Cajero:
    '''
    Clase que representa a los
    servidores del sistema
    '''
    def __init__(self):
        '''
        Constructor de la clase
        '''
        self.tiempo_libre = 0
        self.tiempo_llega_cliente = 0
        self.tiempo_sale_cliente = 0
        self.ocupado = False
        self.cliente = None
        self.cola_espera = deque([])

class Servidores:
    '''
    Clase que representa los servidores
    de un sistema
    '''
    def __init__(self, cant):
        '''
        Constructor de la clase
        '''
        self.lista_cajeros = []
        for i in range(cant):
            self.lista_cajeros.append(Cajero())

    def hay_cajero_disponible(self):
        '''
        Funcion que ve si existe un cajero
        disponible y lo retorna
        '''
        cajeros_disponibles = []
        for cajero in self.lista_cajeros:
            if not cajero.ocupado:
                cajeros_disponibles.append(cajero)
        return cajeros_disponibles

def generar_clientes(cant):
    '''
    Funcion que genera la cantidad de clientes
    para el sistema
    '''
    tiempo_inicial = 0
    clientes = []
    for i in range(cant):
        tiempo_llegada = tiempo_inicial + generar_tiempo_llegada()
        tiempo_inicial = tiempo_llegada
        clientes.append(Cliente(tiempo_llegada))
    return clientes


def generar_tiempo_llegada():
    '''
    Funcion que se encarga de generar el
    tiempo de llegada de un cliente
    '''
    return expovariate(1)

def generar_tiempo_servicio():
    '''
    Funcion que genera el tiempo de servicio
    de un cajero
    '''
    return uniform(3, 5)


# Funcion que realiza la simulacion
def simulacion(minutos, cant_clientes):
    '''
    Funcion que va a correr la simulacion
    '''

    # Inicializacion de los recursos necesario para
    # la simulacion
    clientes = generar_clientes(cant_clientes) # Genera los clientes que participaran en el sistema
    servidores = Servidores(4)
    clientes_listos = [] # Va a almacenar todos los clientes que salieron del banco
    clientes_se_rindieron = 0 # Lleva la cuenta del numero de clientes que no hicieron la cola

    tiempo_actual = 0.0
    while tiempo_actual < minutos:

        # Simulacion de las personas cuando llegan a la cola
        for cliente in clientes:
            # Veo si el tiempo ya llego al banco
            if cliente.tiempo_llegada <= tiempo_actual:
                # Veo si el cliente decide declinar o no
                for cajero in servidores.lista_cajeros:
                    cola_espera = cajero.cola_espera    
                    if cliente.cliente_declina(len(cola_espera)):
                        clientes_se_rindieron += 1
                        try:
                            clientes.remove(cliente)
                        except:
                            pass
                    else:
                        # Si no declina procede a entrar en la cola
                        cola_espera.append(cliente)
                        try:
                            clientes.remove(cliente)
                        except:
                            pass
            else:
                break # Esto se hace porque estan ordenados cronologicamente

        # Primero recorro los servidores para ver cuales
        # han terminado con sus clientes y liberarlos
        for cajero in servidores.lista_cajeros:
            # Esto solo tiene sentido si el cajero esta ocupado
            if cajero.ocupado: 
                # Tomo al cliente que esta atendiendo el cajero
                cliente_en_proceso = cajero.cliente
                tiempo_finalizacion = cliente_en_proceso.tiempo_salida_cola + cliente_en_proceso.tiempo_atencion
                if tiempo_finalizacion <= tiempo_actual: # Esto significa que ya termino de atenderlo
                    cliente_en_proceso.tiempo_en_el_sistema = tiempo_finalizacion - cliente_en_proceso.tiempo_llegada 
                    clientes_listos.append(cliente_en_proceso) # Saca del banco al cliente
                    cajero.ocupado = False # El cajero deja de estar ocupado
                    cajero.cliente = None # No tiene ningun cliente
                    cajero.tiempo_sale_cliente = tiempo_actual # Guarda el tiempo en donde sale el cliente
        
        # Veo si en la cola hay personas para atender
        for cajero in servidores.lista_cajeros:
            cola_espera = cajero.cola_espera
            if len(cola_espera) > 0:
                # Veo si hay servidores disponibles para atender a las personas
                cajeros_disponibles = servidores.hay_cajero_disponible()
                if len(cajeros_disponibles) > 0: # existen 1 o mas cajeros disponibles
                    for cajero in cajeros_disponibles: # Recorro cada cajero y le pongo clientes
                        if len(cola_espera) == 0: # Si no hay mas personas en la cola termino
                            break
                        siguiente = cola_espera.popleft() # Saco al cliente de la cola
                        siguiente.tiempo_salida_cola = tiempo_actual # Pongo el tiempo que salio de la cola
                        siguiente.tiempo_atencion = generar_tiempo_servicio() # Genero el tiempo que estara con el cajero
    
                        # Actualizo informacion del cajero
                        cajero.ocupado = True # Pongo al cajero ocupado
                        cajero.cliente = siguiente # Le coloco al cliente que va a ser atendido
                        cajero.tiempo_llega_cliente = tiempo_actual # El tiempo de llegada
                        cajero.tiempo_libre += (tiempo_actual - cajero.tiempo_sale_cliente) # Sumo el tiempo que estuvo libre el cajero

        tiempo_actual += 0.1
    return servidores, clientes_listos, clientes_se_rindieron

servidores, clientes_listos, clientes_declinaron = simulacion(420, 100)