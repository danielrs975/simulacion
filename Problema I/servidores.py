'''
Clase que representa los servidores
de un servicio
'''

class Servidores:
    '''
    Clase que implementa a los servidores
    '''
    def __init__(self, cant_servidores):
        '''
        Constructor de la clase de servidores
        '''
        self.servidores = [0 for i in range(cant_servidores)]
        self.cant_servidores = cant_servidores

    def reservar_servidor(self, cliente):
        '''
        Funcion que se encarga de reservar un
        servidor
        '''
        if self.existe_servidor_libre():
            for i in range(self.cant_servidores):
                if self.servidores[i] == 0:
                    cliente.servidor = i # Almacena que servidor esta atendiendo al cliente
                    self.servidores[i] = 1
                    break
            return True
        return False

    def liberar_servidor(self, cliente):
        '''
        Metodo que se encarga de liberar un servidor
        cuando ya un cliente ha terminado con el
        '''
        servidor = cliente.servidor
        self.servidores[servidor] = 0
        

    def existe_servidor_libre(self):
        '''
        Metodo que retorna true si existe un servidor
        libre para atender un cliente, retorna false
        si no existe tal servidor
        '''
        return 0 in self.servidores