'''
Problema numero 8 de la guia
'''
from random import random, expovariate, uniform
from math import log, sqrt
from scipy import stats
from collections import deque

class Vendedor:
    '''
    Clase que representa al vendedor de
    carros
    '''
    def __init__(self):
        '''
        Constructor de la clase
        '''
        self.comision_obtenida = 0
        self.carros_vendidos = 0


def generar_numero_ventas_carros_semanal():
    '''
    Funcion que se encarga de generar
    la cantidad de carros vendidos por un
    vendedor
    '''
    numero_aleatorio = random()
    if numero_aleatorio <= 0.10:
        return 0
    elif numero_aleatorio <= 0.25:
        return 1
    elif numero_aleatorio <= 0.45:
        return 2
    elif numero_aleatorio <= 0.70:
        return 3
    elif numero_aleatorio <= 0.90:
        return 4
    else:
        return 5

def generar_tipo_automovil():
    '''
    Funcion que genera de manera aleatoria
    el tipo de automovil vendido
    '''
    numero_aleatorio = random()
    if numero_aleatorio <= 0.40:
        return 'compacto'
    elif numero_aleatorio <= 0.75:
        return 'mediano'
    return 'lujo'

def generar_ganancia_por_carro_lujo():
    '''
    Genera la ganancia si el carro vendido
    es de lujo
    '''
    numero_aleatorio = random()
    if numero_aleatorio <= 0.35:
        return 1000
    elif numero_aleatorio <= 0.75:
        return 1500
    return 2000

def generar_ganancia_por_carro_mediano():
    '''
    Genera la ganancia si el carro vendido
    es mediano
    '''
    numero_aleatorio = random()
    if numero_aleatorio <= 0.40:
        return 400
    return 500

def generar_ganancia(tipo):
    '''
    Funcion que genera la comision por
    carro vendido
    '''
    if tipo == 'compacto':
        return 250
    elif tipo == 'mediano':
        return generar_ganancia_por_carro_mediano()
    return generar_ganancia_por_carro_lujo()

def simulacion(numero_semanas):
    '''
    Funcion que realiza la simulacion del
    problema
    '''
    vendedores = [Vendedor() for i in range(5)]

    semanas = 0
    while semanas < numero_semanas:
        # Recorro todos los vendedores
        for vendedor in vendedores:
            # Por cada vendedor genero el numero de carros que vendio esa semana
            numero_carros_vendidos = generar_numero_ventas_carros_semanal()
            # Lo sumo a la cantidad total de carros vendido por el vendedor
            vendedor.carros_vendidos += numero_carros_vendidos
            # Para cada uno de los carros vendido veo que modelo es
            for carro in range(numero_carros_vendidos):
                tipo_carro = generar_tipo_automovil() # Genero el tipo de carro vendido
                vendedor.comision_obtenida += generar_ganancia(tipo_carro) # Sumo al vendedor la comision obtenida

        semanas += 1
    
    return vendedores

def print_intervalo(promedio, delta):
    return "[" + str(round(promedio - delta,2)) + ", " + str(round(promedio + delta,2)) + "]"

numero_semanas = 10
vendedores = simulacion(numero_semanas)

promedio_comision_por_vendedor = [vendedor.comision_obtenida/numero_semanas for vendedor in vendedores]
promedio_comision_general = sum(promedio_vendedor for promedio_vendedor in promedio_comision_por_vendedor)/len(vendedores)

# Respuesta a la pregunta a) es 
print("El promedio de comision de un vendedor por semana es: " + str(promedio_comision_general))

# Calculo del intervalo de confianza
sd = sum((promedio_vendedor - promedio_comision_general)**2 for promedio_vendedor in promedio_comision_por_vendedor)
sd = sqrt(sd / (numero_semanas - 1))
t_valor = stats.t.ppf(1-0.05, numero_semanas - 1)
delta = t_valor*(sd/sqrt(numero_semanas))

print("El intervalo de confianza es: " + print_intervalo(promedio_comision_general, delta))