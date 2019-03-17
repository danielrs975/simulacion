'''
Script de simulacion para el problema 9
'''
from random import random, expovariate, uniform
from math import log, sqrt
from scipy import stats
from collections import deque

def generar_tiempo_llegada():
    '''
    Funcion que genera el tiempo en que
    llega un nuevo trabajo
    '''
    return expovariate(1/5)

def generar_tiempo_procesamiento_a():
    '''
    '''
    return uniform(6, 10)