'''
Script que corre la simulacion del problema
'''
import random

from queue import Queue
from customer import Customer
from servidores import Servidores

cola = Queue()
cajeros = Servidores(4)
tiempo_sistema = 0

# Este diccionario contiene informacion sobre el
# estado del sistema


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
            clientes_servidores = eliminar_cliente(centinela, clientes_servidores)
        if cola.length() > 0 and cajeros.existe_servidor_libre():
            siguiente = cola.dequeue()
            cajeros.reservar_servidor(siguiente)
            siguiente.tiempo_salida_cola = centinela.tiempo_atencion
            siguiente.tiempo_atencion = siguiente.tiempo_salida_cola + random.uniform(3,5)
            clientes_servidores.append(siguiente)
        else:
            break
            

    cliente = linea_tiempo[time] # Llega cliente
    cliente.tiempo_llegada_cola = time

    if cola.length() == 0:
        if cajeros.reservar_servidor(cliente):
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
print(" % De clientes que se rindieron: " + str(clientes_declinaron*100/cantidad_clientes))
promedio = 0
for i in linea_tiempo.values():
    if i.tiempo_salida_cola != -1:
        promedio += (i.tiempo_atencion - i.tiempo_llegada_cola)

promedio /= cantidad_clientes   

print(" Tiempo de espera para un cliente: " + str(promedio))