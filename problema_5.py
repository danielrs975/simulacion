from random import randint, uniform, random
from collections import deque
from math import modf, log, sqrt, fabs

def generarTiempoEntreLlegadas():
    tiempo = random()
    if tiempo <= 0.20:
        return 1
    elif tiempo <= 0.45:
        return 2
    elif tiempo <= 0.80:
        return 3
    elif tiempo <= 0.95:
        return 4
    else:
        return 5

def generarTipoDeTanque():
    tipo = random()
    if tipo <= 0.40:
        return [4,3]
    elif tipo <= 0.75:
        return [3,2]
    else:
        return [2,1]

def simulacion(dias):
    n = 0
    tiempoRestanteA = 1
    tiempoRestanteB = 1

    proximosTanques = 1
    cantidadTanques = 1
    tiempoDesocupadoA = 0
    tiempoDesocupadoB = 0

    colaTanques = deque([])
    tanquesEnPuerto = 0
    tiempoProximoTanque = 1

    nuevoTanque = generarTipoDeTanque()
    colaTanques.append(nuevoTanque)

    arr_tanques_en_puerto = []
    arr_tanques_llegada = []
    arr_terminal_A = []
    arr_terminal_B = []

    while n < dias:
        tiempoRestanteA -= 1
        tiempoRestanteB -= 1
        tanquesEnPuerto += len(colaTanques)
        if tiempoProximoTanque <= 0:
            nuevoTanque = generarTipoDeTanque()
            colaTanques.append(nuevoTanque)
            tiempoProximoTanque = generarTiempoEntreLlegadas()
            cantidadTanques += 1
            tanquesEnPuerto += 1
        tiempoProximoTanque -= 1
        if tiempoRestanteB <= 0:
            if tiempoRestanteB <= -1:
                tiempoDesocupadoB += 1
            if len(colaTanques) > 0:
                siguienteTanque = colaTanques.popleft()
                tiempoRestanteB = siguienteTanque[1]
        else:
            tanquesEnPuerto += 1

        if tiempoRestanteA <= 0:
            if tiempoRestanteA <= -1:
                tiempoDesocupadoA += 1
            if len(colaTanques) > 0:
                siguienteTanque = colaTanques.popleft()
                tiempoRestanteA = siguienteTanque[1]
        else:
            tanquesEnPuerto += 1

        n += 1
        arr_tanques_en_puerto.append(tanquesEnPuerto)
        arr_tanques_llegada.append(cantidadTanques)
        arr_terminal_A.append(tiempoDesocupadoA)
        arr_terminal_B.append(tiempoDesocupadoB)
    return cantidadTanques, tanquesEnPuerto, tiempoDesocupadoA, tiempoDesocupadoB, arr_tanques_en_puerto, arr_tanques_llegada, arr_terminal_A, arr_terminal_B

dias = 1000
cantidadTanques, tanquesEnPuerto, tiempoDesocupadoA, tiempoDesocupadoB, arr_tanques_en_puerto, arr_tanques_llegada, arr_terminal_A, arr_terminal_B = simulacion(dias)

def get_intervalo(promedio, delta):
    return "[" + str(promedio - delta) + ", " + str(promedio + delta) + "]"

def print_resultado(promedio, intervalo, msg):
    print("Promedio de " + msg + ": " + str(promedio))
    print("Intervalo de confianza 95%: " + intervalo)
    print("----------------------------------------------------------------")

promedio_libre_a = tiempoDesocupadoA / dias

promedio_libre_b = tiempoDesocupadoB / dias
print("Promedio de desocupado B: " + str(promedio_libre_b))


# promedio tanques por dia en puerto
promedio_tanques_puerto = tanquesEnPuerto / dias
cuadrados = []
for tanque in arr_tanques_en_puerto:
    r = (tanque - promedio_tanques_puerto)**2
    cuadrados.append(r)

sd = (sum(cuadrados)/(dias-1))**0.5
delta = 1.96 * (sd/(dias**0.5))
int_conf = get_intervalo(promedio_tanques_puerto,delta)
print_resultado(promedio_tanques_puerto, int_conf, "tanques en el puerto")

# promedio de dias que pasa un tanque en el puerto
promedio_tanques = cantidadTanques / dias
cuadrados = []
for tanque in arr_tanques_llegada:
    r = (tanque - promedio_tanques)**2
    cuadrados.append(r)

sd = (sum(cuadrados)/(dias-1))**0.5
delta = 1.96 * (sd/(dias**0.5))
int_conf = get_intervalo(promedio_tanques,delta)
print_resultado(promedio_tanques, int_conf, "tanques que llegan")

# promedio de tiempo desocupado terminal A
promedio_libre_a = tiempoDesocupadoA / dias
cuadrados = []
for tanque in arr_terminal_A:
    r = (tanque - promedio_libre_a)**2
    cuadrados.append(r)

sd = (sum(cuadrados)/(dias-1))**0.5
delta = 1.96 * (sd/(dias**0.5))
int_conf = get_intervalo(promedio_libre_a,delta)
print_resultado(promedio_libre_a, int_conf, "de tiempo desocupado terminal A")

# promedio de tiempo desocupado terminal B
promedio_libre_b = tiempoDesocupadoB / dias
cuadrados = []
for tanque in arr_terminal_B:
    r = (tanque - promedio_libre_b)**2
    cuadrados.append(r)

sd = (sum(cuadrados)/(dias-1))**0.5
delta = 1.96 * (sd/(dias**0.5))
int_conf = get_intervalo(promedio_libre_b,delta)
print_resultado(promedio_libre_b, int_conf, "de tiempo desocupado terminal B")

