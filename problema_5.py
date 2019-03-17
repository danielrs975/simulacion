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
    return cantidadTanques, tanquesEnPuerto, tiempoDesocupadoA, tiempoDesocupadoB

dias = 1000
cantidadTanques, tanquesEnPuerto, tiempoDesocupadoA, tiempoDesocupadoB = simulacion(dias)

def get_intervalo(promedio, delta):
    return "[" + str(promedio - delta) + ", " + str(promedio + delta) + "]"

def print_resultado(promedio, intervalo, msg):
    print("Promedio de " + msg + ": " + str(promedio))
    print("Intervalo de confianza: " + intervalo)
    print("----------------------------------------------------------------")

promedio_tanques = cantidadTanques / dias
print("Promedio de tanques: " + str(promedio_tanques))

promedio_libre_a = tiempoDesocupadoA / dias
print("Promedio de desocupado A: " + str(promedio_libre_a))

promedio_libre_b = tiempoDesocupadoB / dias
print("Promedio de desocupado B: " + str(promedio_libre_b))



promedio_tanques_puerto = tanquesEnPuerto / dias

