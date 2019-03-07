from random import random, expovariate, uniform
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
    cola_espera = deque([])
    clientes_listos = [] # Va a almacenar todos los clientes que salieron del banco
    clientes_se_rindieron = 0 # Lleva la cuenta del numero de clientes que no hicieron la cola

    tiempo_actual = 0.0
    while tiempo_actual < minutos:

        # Simulacion de las personas cuando llegan a la cola
        for cliente in clientes:
            # Veo si el tiempo ya llego al banco
            if cliente.tiempo_llegada <= tiempo_actual:
                # Veo si el cliente decide declinar o no
                if cliente.cliente_declina(len(cola_espera)):
                    clientes_se_rindieron += 1
                    clientes.remove(cliente)
                else:
                    # Si no declina procede a entrar en la cola
                    cola_espera.append(cliente)
                    clientes.remove(cliente)
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

cant_clientes = 100
minutos = 60
servidores, clientes, cant_declinados = simulacion(minutos, cant_clientes)


# ZONA DE RESULTADOS
# a) El tiempo esperado que pasa un cliente en el sistema
promedio_cliente_sistema = 0
for cliente in clientes:
    promedio_cliente_sistema += cliente.tiempo_en_el_sistema
promedio_cliente_sistema /= len(clientes)

# Desviacion estandar 
s = 0
for cliente in clientes:
    s += (cliente.tiempo_en_el_sistema - promedio_cliente_sistema)**2
s = sqrt(s / (len(clientes) - 1))

# Intervalo de confianza
t_valor = stats.t.ppf(1-0.05, len(clientes) - 1)
delta = t_valor*(s / sqrt(len(clientes) - 1))
intervalo_confianza = "[" + str(round(promedio_cliente_sistema - delta, 2)) + ", " + str(round(promedio_cliente_sistema + delta, 2))  + "]"

# Impresion de resultados
print("a) Tiempo de espera de un cliente en el sistema")
print("El tiempo esperado en el sistema de un cliente: " + str(round(promedio_cliente_sistema, 2)))
print("El intervalo de confianza al 95 de significancia " + intervalo_confianza)
print("---------------------------------------------------------------------------------------")

# b) Porcentaje de clientes que declinan
porcentaje = cant_declinados*100/cant_clientes

# Impresion de resultados
print("b) Porcentaje de clientes que declinaron")
print("El porcentaje de clientes que declinaron fue: " + str(porcentaje) + "%")
print("----------------------------------------------------------------------------------------")
# c) Porcentaje de tiempo libre para cada cajero
porcentaje_cajero_1 = servidores.lista_cajeros[0].tiempo_libre*100/minutos
porcentaje_cajero_2 = servidores.lista_cajeros[1].tiempo_libre*100/minutos
porcentaje_cajero_3 = servidores.lista_cajeros[2].tiempo_libre*100/minutos
porcentaje_cajero_4 = servidores.lista_cajeros[3].tiempo_libre*100/minutos

# Calculo de intervalo de confianza
promedio_tiempo_libre = 0
for cajero in servidores.lista_cajeros:
    promedio_tiempo_libre += cajero.tiempo_libre
promedio_tiempo_libre /= 4

# Calculo de la desviacion estandar
s = 0
for cajero in servidores.lista_cajeros:
    s += (cajero.tiempo_libre - promedio_tiempo_libre)**2
s = sqrt(s / (3))

t_valor = stats.t.ppf(1-0.05, 3)
delta = t_valor*(s / sqrt(4))
intervalo_confianza = "[" + str(round(promedio_tiempo_libre - delta, 2)) + ", " + str(round(promedio_cliente_sistema + delta, 2)) + "]"

# Impresion de resultados
print("c) Porcentaje de tiempo libre para cada cajero")
print("Para el cajero 1: " + str(round(porcentaje_cajero_1, 2)) + "%")
print("Para el cajero 2: " + str(round(porcentaje_cajero_2, 2)) + "%")
print("Para el cajero 3: " + str(round(porcentaje_cajero_3, 2)) + "%")
print("Para el cajero 4: " + str(round(porcentaje_cajero_4, 2)) + "%")
print("Tiempo libre promedio de un cajero: " + str(round(promedio_tiempo_libre, 2)))
print("Intervalo de confianza: " + intervalo_confianza)
