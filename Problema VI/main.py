'''
Simulacion del problema 6 de la guia
'''
from random import random, expovariate, uniform
from math import log, sqrt
from scipy import stats
from collections import deque

sd = 83 # Desviacion estandar de la distribucion que sigue el numero
# de pasajeros que se embarcan en una estacion

class Tren:
    '''
    Clase que representa al tren
    '''
    def __init__(self):
        '''
        Constructor de la clase
        '''
        self.tiempo = 0
        self.pasajeros_embarcados = []
        self.cantidad_embarcados_por_estacion = []

class Pasajero:
    '''
    Clase que representa el pasajero
    del tren
    '''
    def __init__(self):
        '''
        Constructor de la clase
        '''
        self.tiempo_en_el_tren = 0

def generar_pasajeros_que_embarca():
    '''
    Genera los pasajeros que se embarcan
    en una estacion
    '''
    media = 176

    pasajeros = []
    muestra = expovariate(1/media)
    muestra = int(round(muestra, 0))
    for i in range(muestra):
        pasajeros.append(Pasajero())
    
    return pasajeros


def calculo_tiempo_recorrido(num_pasajeros):
    '''
    Calcula el tiempo de recorrido entre
    una estacion y otra
    '''
    if num_pasajeros > 0:
        return 100*(1 + 0.1*(log(num_pasajeros, 10)))
    return 0

def calculo_tiempo_embarque_desembarque(num_desembarque, num_embarque):
    '''
    Calcula el tiempo de embarque y desembarque de los pasajeros
    '''
    if num_desembarque + num_embarque > 0:
        return 20*(1 + 0.1*(log(num_desembarque + num_embarque, 10)))
    return 0

def pasajero_se_baja_del_tren(estacion):
    '''
    Genera el numero de estaciones que recorrera el
    pasajero en el tren
    '''
    num_aleatorio = random()
    if num_aleatorio < 0.5:
        return True
    return False

def simulacion():
    '''
    Funcion que simula el problema
    '''
    tren = Tren() # Se crea el tren

    numero_pasajeros_por_parada = []
    estacion_actual = 1 # Estacion en la cual se encuentra actualmente el tren

    while estacion_actual <= 10:
        
        numero_pasajeros_por_parada.append(len(tren.pasajeros_embarcados))
        tren.tiempo += calculo_tiempo_recorrido(len(tren.pasajeros_embarcados)) # Tiempo que dura en llegar a la estacion
        pasajeros_desembarcan = []

        # Veo que pasajeros se desembarcan
        for pasajero in tren.pasajeros_embarcados:
            pasajero_se_baja = pasajero_se_baja_del_tren(estacion_actual)
            if pasajero_se_baja:
                tren.pasajeros_embarcados.remove(pasajero) # Desmonto al pasejero
                pasajeros_desembarcan.append(pasajero) # Lo saco del tren

        pasajeros_embarca = generar_pasajeros_que_embarca() # Genera los pasajeros que se van a embarcar
        tren.pasajeros_embarcados += pasajeros_embarca # Monto a los pasajeros
        tren.cantidad_embarcados_por_estacion.append(len(pasajeros_embarca))
        tren.tiempo += calculo_tiempo_embarque_desembarque(len(pasajeros_desembarcan), len(pasajeros_embarca)) # Calculo el tiempo en la estacion

        estacion_actual += 1
    
    # Se termina la simulacion
    return tren, numero_pasajeros_por_parada, numero_pasajeros_por_parada

def print_intervalo(promedio, delta):
    return "[" + str(round(promedio - delta,2)) + ", " + str(round(promedio + delta,2)) + "]"

tren_resultado, pasajeros_por_parada, pasajeros_en_el_tren = simulacion()



def main(iteraciones):
    tiempo_por_iteracion = []
    media_pasajeros_array = []
    promedio_de_pasajeros_en_el_tren = []
    maximo_de_pasajeros_embarcados = []

    iter = 0
    while iter < iteraciones:
        aux1, aux2, aux3 = simulacion()
        tiempo_por_iteracion.append(aux1.tiempo)
        aux2 = sum(pasajeros for pasajeros in aux2) / 10
        media_pasajeros_array.append(aux2)
        aux3 = sum(num_pasajeros for num_pasajeros in aux3) / 10
        promedio_de_pasajeros_en_el_tren.append(aux3)
        maximo_de_pasajeros_embarcados.append(max(aux1.cantidad_embarcados_por_estacion))
        iter += 1

    tiempo_promedio = sum(tiempo for tiempo in tiempo_por_iteracion)/iteraciones

    # RESPUESTAS A LAS PREGUNTAS
    # a) Tiempo total recorrido
    print("Tiempo total recorrido por el tren fue: " + str(tiempo_promedio))
    # Calculo del intervalo de confianza

    sd = sum((tiempo - tiempo_promedio)**2 for tiempo in tiempo_por_iteracion)
    sd = sqrt(sd / (iteraciones - 1))
    t_valor = stats.t.ppf(1-0.05, iteraciones - 1)
    delta = t_valor*(sd/sqrt(iteraciones))
    print("El intervalo de confianza es: " + print_intervalo(tiempo_promedio, delta))

    # b) El numero de pasajeros promedio a bordo del tren.
    promedio_pasajeros = sum(pasajeros for pasajeros in promedio_de_pasajeros_en_el_tren)/iteraciones
    print("Numero de pasajeros promedio a bordo del tren: " + str(promedio_pasajeros))
    # Calculo del intervalo de confianza
    sd = sum((pasajeros - promedio_pasajeros)**2 for pasajeros in promedio_de_pasajeros_en_el_tren)
    sd = sqrt(sd / (iteraciones - 1))
    delta = t_valor*(sd/sqrt(iteraciones))
    print("El intervalo de confianza es: " + print_intervalo(promedio_pasajeros, delta))

    # c) El numero maximo de pasajeros embarcados
    promedio_maximo = sum(maximo for maximo in maximo_de_pasajeros_embarcados) / iteraciones
    print("Numero maximo de pasajeros embarcados: " + str(round(promedio_maximo,0)))
    sd = sum((maximo - promedio_maximo)**2 for maximo in maximo_de_pasajeros_embarcados)
    sd = sqrt(sd/(iteraciones - 1))
    delta = t_valor*(sd/sqrt(iteraciones))
    print("El intervalo de confianza es: " + print_intervalo(promedio_maximo, delta))


main(100)