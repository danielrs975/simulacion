'''
Script de simulacion para el problema 9
'''
from random import random, expovariate, uniform
from math import log, sqrt
from scipy import stats
from collections import deque

class Centro:
    '''
    Clase que representa cada centro de trabajo
    '''
    def __init__(self, limite=None):
        '''
        Constructor de la clase
        '''
        self.trabajo_procesando = None
        self.numero_trabajos_procesados = 0
        self.tiempo_detenido = 0
        self.cola = deque([])
        self.limite = limite

class Trabajo:
    '''
    Clase que representa el trabajo
    a ser procesado
    '''
    def __init__(self, tiempo_llegada):
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_salida = None
        self.tiempo_procesamiento = None
        self.tiempo_en_procesar = None

def generar_tiempo_llegada():
    '''
    Funcion que genera el tiempo en que
    llega un nuevo trabajo
    '''
    return expovariate(1/5)

def generar_tiempo_procesamiento_a():
    '''
    Genera el tiempo de procesamiento de un
    trabajo por el centro A
    '''
    return uniform(6, 10)

def generar_tiempo_procesamiento_b():
    '''
    Genera el tiempo de procesamiento de un trabajo
    por el centro B
    '''
    # Genero dos numero aleatorios en el intervalo 0, 1
    u_uno = random()
    numero_aleatorio = uniform(0,0.5)
    if u_uno <= 0.5:
        return 4*numero_aleatorio + 1
    return 5 - 4*numero_aleatorio

def trabajo_va_centro_a():
    '''
    Funcion que dice si un trabajo va al
    centro a
    '''
    numero_aletorio = random()
    if numero_aletorio <= 0.5:
        return True
    return False

def generar_trabajos(cant):
    '''
    Funcion que se encarga de generar
    los trabajos y cuando llegan
    '''
    tiempo_inicial = 0
    trabajos = []
    for i in range(cant):
        tiempo_llegada = tiempo_inicial + generar_tiempo_llegada()
        tiempo_inicial = tiempo_llegada
        trabajos.append(Trabajo(tiempo_llegada))    
    return trabajos

def simulacion(horas, cant_trabajos):
    '''
    Funcion que simula el problema
    '''
    # Seccion de inicializacion de las variables
    centro_A = Centro()
    centro_B = Centro(4)

    trabajos = generar_trabajos(cant_trabajos)
    trabajos_completados = []

    hora_actual = 0.0
    while hora_actual < horas:
        # Llega un nuevo trabajo
        for trabajo in trabajos:
            # Veo si el trabajo ya llego al centro de atencion
            if trabajo.tiempo_llegada <= hora_actual:
                # Eligo a que centro mando el trabajo
                if trabajo_va_centro_a():
                    # Si el trabajo va al centro a lo incluyo en su cola
                    centro_A.cola.append(trabajo)
                    trabajos.remove(trabajo)
                else:
                    # Si va al centro B veo si hay espacion en la cola
                    if len(centro_B.cola) < centro_B.limite:
                        # Si hay espacio lo incluyo en la cola
                        centro_B.cola.append(trabajo)
                        trabajos.remove(trabajo)
                    else:
                        # Si no hay espacio mando el trabajo a la cola
                        # del centro A
                        centro_A.cola.append(trabajo)
                        trabajos.remove(trabajo)
            else:
                # Salgo de la lista porque los demas trabajos vienen despues
                break
        
        # Proceso los trabajos
        # Proceso los trabajos de b primero 

        # Si B esta procesando un trabajo veo si ya termino
        # con ese trabajo
        if centro_B.trabajo_procesando != None:
            trabajo_b = centro_B.trabajo_procesando # Tomo el trabajo de B
            # Veo si el trabajo de B esta terminado
            if trabajo_b.tiempo_procesamiento <= hora_actual:
                # Le quito el trabajo a B
                trabajos_completados.append(centro_B.trabajo_procesando)
                centro_B.trabajo_procesando = None
                centro_B.numero_trabajos_procesados += 1
                if len(centro_B.cola) > 0:
                    # Si el trabajo esta terminado tomo el siguiente trabajo
                    siguiente_trabajo = centro_B.cola.popleft()
                    # Genero el tiempo de procesamiento
                    siguiente_trabajo.tiempo_en_procesar = generar_tiempo_procesamiento_b()
                    siguiente_trabajo.tiempo_procesamiento = hora_actual + siguiente_trabajo.tiempo_en_procesar
                    # Le doy el trabajo a B
                    centro_B.trabajo_procesando = siguiente_trabajo
        else:
            # Veo que la cola no este vacia
            if len(centro_B.cola) > 0:
                # Tomo el trabajo
                trabajo_b = centro_B.cola.popleft()
                # Genero el tiempo de procesamiento
                trabajo_b.tiempo_en_procesar = generar_tiempo_procesamiento_b()
                trabajo_b.tiempo_procesamiento = hora_actual + trabajo_b.tiempo_en_procesar
                # Le doy el trabajo al centro B
                centro_B.trabajo_procesando = trabajo_b
        
        # Proceso los trabajo de A
        # Veo si hay espacio en la cola del centro B
        if len(centro_B.cola) < centro_B.limite:
            # Si hay espacio entonces el centro A puede
            # procesar trabajos
            # Veo si el centro A esta actualmente procesando trabajos
            if centro_A.trabajo_procesando != None:
                trabajo_a = centro_A.trabajo_procesando # Tomo el trabajo de A
                # Veo si para la hora actual esta terminado ese trabajo
                if trabajo_a.tiempo_procesamiento <= hora_actual:
                    # Si es asi le quito el trabajo al centro A
                    trabajos_completados.append(centro_A.trabajo_procesando)
                    centro_A.trabajo_procesando = None
                    centro_A.numero_trabajos_procesados += 1
                    # Veo si hay trabajos en cola
                    if len(centro_A.cola) > 0:
                        # Tomo el siguiente trabajo a realizar
                        siguiente_trabajo = centro_A.cola.popleft()
                        # Genero el tiempo de procesamiento
                        siguiente_trabajo.tiempo_en_procesar = generar_tiempo_procesamiento_a()
                        siguiente_trabajo.tiempo_procesamiento = hora_actual + siguiente_trabajo.tiempo_en_procesar
                        # Finalmente le doy el trabajo a A
                        centro_A.trabajo_procesando = siguiente_trabajo
            else:
                # Si no hay trabajos que esta haciendo A
                # Veo si la cola no esta vacia para agarrar un trabajo
                if len(centro_A.cola) > 0:
                    # Tomo el trabajo que esta en cola 
                    trabajo_a = centro_A.cola.popleft()
                    # Genero el tiempo de procesamiento
                    trabajo_a.tiempo_en_procesar = generar_tiempo_procesamiento_a()
                    trabajo_a.tiempo_procesamiento = hora_actual + trabajo_a.tiempo_en_procesar
                    # Finalmente le doy el trabajo a A
                    centro_A.trabajo_procesando = trabajo_a
        else:
            # Esto significa que el A esta detenido
            centro_A.tiempo_detenido += 0.1

        hora_actual += 0.1

    return trabajos_completados, centro_A, centro_B

def print_intervalo(promedio, delta):
    return "[" + str(round(promedio - delta,2)) + ", " + str(round(promedio + delta,2)) + "]"


def iteraciones(iter):
    '''
    Corre las simulaciones por un numero 
    de iteraciones
    '''

    i = 0
    promedio_trabajos = []
    promedio_tiempo_detenido = []
    tiempo_esperado_culminacion = []

    while i < iter:
        trabajos_completados, centro_a, centro_b = simulacion(10000, 2000)

        auxiliar_1 = centro_a.numero_trabajos_procesados + centro_b.numero_trabajos_procesados + len(centro_a.cola) + len(centro_b.cola)
        promedio_trabajos.append(auxiliar_1/1000)
        promedio_tiempo_detenido.append(centro_a.tiempo_detenido)
        auxiliar_2 = sum(trabajo.tiempo_en_procesar for trabajo in trabajos_completados)/(len(trabajos_completados))
        tiempo_esperado_culminacion.append(auxiliar_2)

        i += 1
    
    respuesta_a = sum(promedio for promedio in promedio_trabajos)/iter
    print("Respuesta pregunta a)")
    print("El numero esperado de trabajos en el recinto fue: " + str(respuesta_a))
    # Calculo del intervalo de confianza
    sd = sum((promedio - respuesta_a)**2 for promedio in promedio_trabajos)
    sd = sqrt(sd/(iter - 1))
    t_valor = stats.t.ppf(1-0.05, iter - 1)
    delta = t_valor*(sd/sqrt(iter))
    print("El intervalo de confianza es: " + print_intervalo(respuesta_a, delta))
    print("------------------------------------------------------------------------")
    print("Respuesta pregunta b)")
    respuesta_b = sum(promedio for promedio in promedio_tiempo_detenido)/iter
    respuesta_b = 100*respuesta_b/10000
    print("El porcentaje de tiempo detenido fue: " + str(respuesta_b))
    # Calculo del intervalo de confianza
    sd = sum(((100*promedio/10000) - respuesta_b)**2 for promedio in promedio_tiempo_detenido)
    sd = sqrt(sd/(iter - 1))
    delta = t_valor*(sd/sqrt(iter))
    print("El intervalo de confianza es: " + print_intervalo(respuesta_b, delta))
    print("-------------------------------------------------------------------------")
    print("Respuesta pregunta c)")
    respuesta_c = sum(tiempo for tiempo in tiempo_esperado_culminacion)/iter
    print("El tiempo esperado de culminacion: " + str(respuesta_c))
    # Calculo del intervalo de confianza
    sd = sum((tiempo - respuesta_c)**2 for tiempo in tiempo_esperado_culminacion)
    sd = sqrt(sd/(iter - 1))
    delta = t_valor*(sd/sqrt(iter))
    print("El intervalo de confianza es: " + print_intervalo(respuesta_c, delta))

    
    

iteraciones(100)