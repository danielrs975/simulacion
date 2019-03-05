'''
Script que corre la simulacion del problema
'''
import random
import math
from scipy import stats

from queue import Queue
from customer import Customer
from servidores import Servidores

cola = Queue()
cajeros = Servidores(4)
tiempo_sistema = 0
tiempo_libre_promedio = 0
tiempo_liberacion = 0
tiempo_reserva = 0

def actualizar_estado(long_cola, servidores_disponibles, tiempo_sistema):
    '''
    Funcion que se encarga de actualizar el estado
    del sistema
    '''
    estado = {
        "longitud_cola": long_cola,
        "servidores_disponibles": servidores_disponibles,
        "tiempo_sistema": tiempo_sistema       
    }
    return estado

def generar_clientes(numero_clientes):
    '''
    Funcion que genera clientes de forma aleatoria a una
    tasa de exponencial de 60 por hora
    '''
    tiempo_sistema = 0
    linea_tiempo = {
        0: Customer(0)
    }
    for i in range(1, numero_clientes):
        cliente = Customer(i)
        tiempo_llega = random.expovariate(1)
        tiempo_sistema += tiempo_llega
        linea_tiempo[tiempo_sistema] = cliente
    
    return linea_tiempo

def eliminar_cliente(cliente, lista):
    '''
    Funcion que simula que el cliente ya finalizo
    su estadia en el banco
    '''
    for i in range(len(lista)):
        if lista[i].id == cliente.id:
            lista.pop(i)
            if lista == None:
                lista = []
            return lista

cantidad_clientes = 100
linea_tiempo = generar_clientes(cantidad_clientes)
clientes_declinaron = 0
clientes_servidores = [] # Es una lista que almacena los clientes que estan siendo atendidos

# Inicio de la simulacion
for time in linea_tiempo.keys():
    # Actualizo el estado del sistema cuando
    # llego a ese tiempo
    while True:
        centinela = Customer(-1)
        centinela.tiempo_atencion = time
        for cliente in clientes_servidores:
            if cliente.tiempo_atencion < centinela.tiempo_atencion:
                centinela = cliente
        if centinela.tiempo_atencion <= time and centinela.id != -1:
            cajeros.liberar_servidor(centinela)
            tiempo_liberacion = centinela.tiempo_atencion
            clientes_servidores = eliminar_cliente(centinela, clientes_servidores)
        if cola.length() > 0 and cajeros.existe_servidor_libre():
            siguiente = cola.dequeue()
            cajeros.reservar_servidor(siguiente)
            tiempo_reserva = centinela.tiempo_atencion 
            siguiente.tiempo_salida_cola = centinela.tiempo_atencion
            tiempo_libre_promedio += (-tiempo_reserva + tiempo_liberacion)
            siguiente.tiempo_atencion = siguiente.tiempo_salida_cola + random.uniform(3,5)
            clientes_servidores.append(siguiente)
        else:
            break
            

    cliente = linea_tiempo[time] # Llega cliente
    cliente.tiempo_llegada_cola = time

    if cola.length() == 0:
        if cajeros.reservar_servidor(cliente):
            tiempo_libre_promedio += (-tiempo_reserva + tiempo_liberacion)
            cliente.tiempo_salida_cola = time
            cliente.tiempo_atencion = cliente.tiempo_salida_cola + random.uniform(3,5)
            clientes_servidores.append(cliente)
        else:
            cola.enqueue(cliente)
    else:
        if not cliente.customerDecline(cola.length()):
            cola.enqueue(cliente)
        else:
            clientes_declinaron += 1
    ultimo_tiempo = time


while cola.length() > 0:
    centinela = Customer(-1)
    centinela.tiempo_atencion = time
    for cliente in clientes_servidores:
        if cliente.tiempo_atencion < centinela.tiempo_atencion:
            centinela = cliente
    
    if centinela.id != -1:
        cajeros.liberar_servidor(centinela)
        clientes_servidores = eliminar_cliente(centinela, clientes_servidores)
        siguiente = cola.dequeue()
        cajeros.reservar_servidor(siguiente)
        siguiente.tiempo_salida_cola = centinela.tiempo_atencion
        siguiente.tiempo_atencion = siguiente.tiempo_salida_cola + random.uniform(3,5)
    else:
        siguiente = cola.dequeue()
        cajeros.reservar_servidor(siguiente)
        siguiente.tiempo_salida_cola = centinela.tiempo_atencion
        siguiente.tiempo_atencion = siguiente.tiempo_salida_cola + random.uniform(3,5)

    time += 1


print("Cliente          Tiempo llegada      Tiempo Salida Cola      Total")
print("-----------------------------------------------------------------")
for i in linea_tiempo.keys():
    if (linea_tiempo[i].tiempo_salida_cola != -1):
        print(linea_tiempo[i])

print("-----------------------------------------------------------------")
promedio = 0
s = 0
for i in linea_tiempo.values():
    if i.tiempo_salida_cola != -1:
        i.tiempo_en_el_lugar = i.tiempo_atencion - i.tiempo_llegada_cola
        promedio += (i.tiempo_en_el_lugar)

promedio /= cantidad_clientes 
tiempo_libre_promedio /= 4

for i in linea_tiempo.values():
    if i.tiempo_salida_cola != -1:
        s += ((i.tiempo_en_el_lugar - promedio)**2)

def calc_intervalo(s, promedio, nivel_sign, n):
    '''
    Funcion que calcula los intervalos de
    confianza
    '''
    t_value = stats.t.ppf(1-nivel_sign, grados_libertad)
    delta = t_value*(s / math.sqrt(n))
    return "[" + str(round(promedio - delta, 2)) + ", " + str(round(promedio + delta, 2)) + "]" 


s = math.sqrt(s / (cantidad_clientes - 1))
grados_libertad = cantidad_clientes - 1
nivel_sign = 0.05
intervalo = calc_intervalo(s, promedio, nivel_sign, cantidad_clientes)

print(" a) Tiempo de espera para un cliente: " + str(promedio))
print("    Calculo del intervalo de confianza de 95%: " + intervalo)
print("-------------------------------------------------------------------------")
print(" b) % De clientes que se rindieron: " + str(clientes_declinaron*100/cantidad_clientes))
print(" c) El promedio de tiempo libre de un cajero es: " + str(round(tiempo_libre_promedio, 2)))
