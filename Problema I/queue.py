'''
Contiene la implementacion de la cola
'''

class Queue:
    '''
    Clase que implementa una cola
    '''
    def __init__(self):
        '''
        Constructor de la clase
        '''
        self.queue = []

    def enqueue(self, objeto):
        '''
        Agrega un elemento a la cola
        '''
        self.queue.append(objeto)

    def dequeue(self):
        '''
        Elimina y retorna el primer elemento
        de la cola
        '''
        if len(self.queue) > 0:
            return self.queue.pop(0)
    
    def length(self):
        '''
        Retorna el numero de elementos de la cola
        '''
        return len(self.queue)