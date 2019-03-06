from random import random
from math import log, sqrt
from scipy import stats
from collections import deque

# CLASES PARA SIMULACION:
class Maquina:
    '''
    Objeto que representa una maquina
    '''
    def __init__(self, id, tiempo_vida=None, tiempo_inicio=0):
        '''
        Constructor de la clase
        '''
        self.tiempo_vida = tiempo_vida
        self.tiempo_inicio = tiempo_inicio
        self.id = id
        self.tiempo_falla = 0
    
    def __str__(self):
        return 'Maquina ' + str(self.id)

class Mecanico:
    '''
    Clase que representa al mecanico
    '''
    def __init__(self, maquina=None, tiempo_inicio=None):
        '''
        Constructor de la clase
        '''
        self.maquina = maquina
        self.tiempo_inicio = tiempo_inicio
        self.tiempo_reparacion = None

    def esta_ocupado(self):
        return self.maquina != None

# Variables globales
n = 4 # Maquinas principales
s = 3 # Maquinas de repuesto

# Funciones de probabilidad
# F = 1 - e^(-x)    G = 1 - e^(-2x)

# Esta funcion genera valores para una variable
# aleatorio con funcion de distribucion G
def generar_tiempo_reparacion():
    '''
    Funcion que se encarga de generar un tiempo
    de reparacion para una maquina
    '''
    numero_aleatorio = random()
    x = -(log(1 - numero_aleatorio))/2
    return round(x, 3)


# Esta funcion genera valores para una variable
# aleatoria F
def generar_tiempo_funcionamiento():
    '''
    Funcion que se encarga de generar el tiempo
    de funcionamiento de una maquina
    '''
    numero_aleatorio = random()
    x = -(log(1 - numero_aleatorio))
    return round(x, 3)

def generar_maquinas_a_usar(cant):
    '''
    Genera un arreglo de maquinas que son
    usadas
    '''
    resultado = []
    for i in range(cant):
        tiempo = generar_tiempo_funcionamiento()
        maquina = Maquina(i, tiempo)
        maquina.tiempo_falla = tiempo
        resultado.append(maquina)
    return resultado

def generar_maquinas_repuesto(cant):
    '''
    Genera las maquinas que seran usadas como repuesto
    '''
    resultado = []
    for i in range(cant):
        resultado.append(Maquina(cant+i))
    return resultado

# Zona de simulacion
def simulacion(n, s, minutos):
    '''
    Funcion que representa la simulacion
    '''
    # Zona de inicializacion de las variables necesaria
    # para la simulacion
    # Genero las maquinas que son usadas y sus tiempo de vida
    maquinas_en_uso = generar_maquinas_a_usar(n)
    maquinas_repuesto = generar_maquinas_repuesto(s)
    cola_maquinas = deque(maquinas_repuesto)

    # Genero al mecanico y su cola de reparacion
    mecanico = Mecanico()
    cola_reparar = deque([])

    # Tiempo del ambiente
    tiempo = 0.0
    segundo = 0.1

    while tiempo < minutos:

        # ZONA QUE SIMULA SI SE DANA UNA MAQUINA
        # Recorro todas las maquinas para ver cuales necesitan
        # reparacion
        for i in range(n):
            maquina = maquinas_en_uso[i] 
            danado = maquina.tiempo_inicio + maquina.tiempo_vida
            if danado <= tiempo:
                maquina_danada = maquinas_en_uso.pop(i) # Saco la maquina que esta danada
                cola_reparar.append(maquina_danada) # La mando a reparar
                if len(cola_maquinas) == 0: # Retorno todas las maquinas que se usaron
                    maquinas = list(maquinas_en_uso) + list(cola_reparar)
                    if mecanico.esta_ocupado():
                        maquinas.append(mecanico.maquina) 
                    return maquinas
                maquina_siguiente_usar = cola_maquinas.popleft() # Saco la maquina de repuesto
                maquina_siguiente_usar.tiempo_inicio = tiempo # Le pongo como tiempo de inicio al momento de sacarla
                maquina_siguiente_usar.tiempo_vida = generar_tiempo_funcionamiento() # Le pongo el tiempo que va a durar
                maquina_siguiente_usar.tiempo_falla += maquina_siguiente_usar.tiempo_vida # Agrego a la maquina el tiempo que va a durar con propositos para sacar promedio
                maquinas_en_uso.append(maquina_siguiente_usar) # La pongo en maquinas en uso
        
        # ZONA QUE SIMULA AL MECANICO
        # Veo si el mecanico tiene una maquina reparando
        # si la termino de reparar la envio a la cola de repuesto y desencolo
        # la siguiente maquina a reparar si existe
        if mecanico.esta_ocupado():
            # Veo si la maquina ya la termino de reparar
            tiempo_donde_reparo = mecanico.tiempo_inicio + mecanico.tiempo_reparacion
            if tiempo_donde_reparo <= tiempo:
                # Como la termino de reparar
                maquina_reparada = mecanico.maquina # Recojo la maquina
                cola_maquinas.append(maquina_reparada) # Coloco la maquina reparada en la cola de maquina de repuesto
                mecanico.maquina = None
                # Veo si existe otra maquina para reparar
                if len(cola_reparar) > 0:
                    maquina_a_reparar = cola_reparar.popleft() # Saco la maquina
                    mecanico.maquina = maquina_a_reparar # Se la doy al mecanico
                    mecanico.tiempo_inicio = tiempo # Coloco el tiempo de inicio de la reparacion
                    mecanico.tiempo_reparacion = generar_tiempo_reparacion() # Genero el tiempo que va a tardar en repararla
        else:
            # Si no esta ocupado veo si existen maquinas para reparar
            if len(cola_reparar) > 0:
                maquina_a_reparar = cola_reparar.popleft() # Saco la maquina
                mecanico.maquina = maquina_a_reparar # Se la doy al mecanico
                mecanico.tiempo_inicio = tiempo # Coloco el tiempo de inicio de la reparacion
                mecanico.tiempo_reparacion = generar_tiempo_reparacion() # Genero el tiempo que va a tardar en repararla

        tiempo += segundo
    
    maquinas = list(maquinas_en_uso) + list(cola_maquinas) + list(cola_reparar)
    if mecanico.esta_ocupado():
        maquinas.append(mecanico.maquina)
    return maquinas

minutos = 1.0
maquinas = simulacion(n, s, minutos)

promedio_total = 0
s = 0

# Promediamos tiempo de fallo para cada maquina
for maquina in maquinas:
    maquina.tiempo_falla /= minutos
    promedio_total += maquina.tiempo_falla

promedio_total /= (n+s)
# calculo de la desviacion estandar
for maquina in maquinas:
    s += (maquina.tiempo_falla - promedio_total)**2

s = sqrt(s / ((n+s) - 1)) # Desviacion estandar
t_valor = stats.t.ppf(1-0.05, (n+s) - 1)
delta = t_valor*(s / sqrt(n+s))

intervalo_confianza = "[" + str(promedio_total - delta) + ", " + str(promedio_total + delta) + "]"
# Zona de resultados:
# Calcular el tiempo esperado de falla
print("------------------------------------------------------------")
print("El tiempo esperado de falla es: " + str(promedio_total))
print("Obteniendo intervalo de confianza.....")
print("Intervalo de confianza: " + intervalo_confianza)
