from ClienteS import Cliente
from multiprocessing.managers import BaseManager
from multiprocessing import Manager, Process
import SalaJuegos

class CustomManager(BaseManager):
    pass

class Clientes():
    def __init__(self):
        self.d = []
        
    def anade(self,c):
        self.d.append(c)  
        n = len(self.d) 
        if n==1:
            c.espera()
            print('1')
        elif n== 2:
            for c in self.d:
                c.send(1)        
            c = [None, None]
            Jugadores = [None, None]
            manager = Manager()
            juego = SalaJuegos.Game(manager)
            for n in range(2):
                c[n] = self.d.pop()
                Jugadores[n] = Process(target=SalaJuegos.jugar, args=(n, c[n], juego))
            juego.setClientes(c[0], c[1])     
            Jugadores[0].start()
            Jugadores[1].start()
            print('Jugando:', c[0].getUsuario(), c[1].getUsuario())
            Jugadores[0].join()
            Jugadores[1].join()
            c[1].notifica()
            print('2')
    
    def __str__(self):
        return self.d
            
class Chats():
    def __init__(self):
        self.d = []
        
    def anade(self,c):
        print('nuevo Chat')
        self.d.append(c)
        
    def esta(self, c):
        return c in self.d
    
    def __str__(self):
        return self.d
            
