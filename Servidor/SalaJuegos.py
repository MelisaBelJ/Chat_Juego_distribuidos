from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock
import traceback
import sys

ladoStr = ["Izquierda", "Derecha"]
tamVentana = (700, 525)
X, Y = 0, 1
numObstaculos = 4
Velocidad = 30

class Jugador():
    def __init__(self, lado):
        self.lado = lado
        self.inicializa()
        
    def inicializa(self):
        if self.lado  == 0:
            self.pos = [5, tamVentana[Y]//2]
        else:
            self.pos = [tamVentana[X] - 5, tamVentana[Y]//2]

    def get_pos(self):
        return self.pos

    def get_lado(self):
        return self.lado

    def moverAbajo(self):
        self.pos[Y] += Velocidad
        if self.pos[Y] > tamVentana[Y]:
            self.pos[Y] = tamVentana[Y]

    def moverArriba(self):
        self.pos[Y] -= Velocidad
        if self.pos[Y] < 0:
            self.pos[Y] = 0
            
    def moverAvanzar(self):
        self.pos[X] += (-1)**(self.lado)*Velocidad
        if self.pos[X] < 0:
            self.pos[X] = tamVentana[X]
            return 1
        if self.pos[X] > tamVentana[X]:
            self.pos[X] =  0
            return 1
        return 0

    def __str__(self):
        return f"P<{ladoStr[self.lado]}, {self.pos}>"

class Obstaculo():
    def __init__(self, velocity, pInicial):
        self.velocity = velocity
        self.posInicial = pInicial
        self.inicializa()

    def get_pos(self):
        return self.pos

    def actualiza(self):
        self.pos[Y] += self.velocity

    def rebota(self):
        self.velocity = -self.velocity

    def choca_Jugador(self, lado):
        self.inicializa()

    def inicializa(self):
        self.pos=[self.posInicial, tamVentana[Y]//2 ]

    def __str__(self):
        return f"B<{self.pos, self.velocity}>"


class Game():
    def __init__(self, manager):
        self.Jugadores = manager.list( [Jugador(0), Jugador(1)] )
        self.Obstaculos = manager.list( [ Obstaculo(-5, tamVentana[X]//4), Obstaculo(-4, tamVentana[X]-tamVentana[X]//4), 
                                         Obstaculo(8, tamVentana[X]//3), Obstaculo(6, tamVentana[X]-tamVentana[X]//3) ] )
        self.puntuacion = manager.list( [0,0] )
        self.jugando = Value('i', 1)
        self.lock = Lock()
        self.hayClientes = False
            
    def setClientes(self, c1, c2):     
        self.clientes = [c1,c2] 
        self.hayClientes = True     

    def get_Jugador(self, lado):
        return self.Jugadores[lado]

    def get_Obstaculo(self):
        return self.Obstaculos

    def get_puntuacion(self):
        return list(self.puntuacion)

    def is_jugando(self):
        return self.jugando.value == 1

    def stop(self):
        self.jugando.value = 0        
        if self.hayClientes:
            for c in self.clientes:
                c.notifica()

    def moverArriba(self, Jugador):
        with self.lock:
            p = self.Jugadores[Jugador]
            p.moverArriba()
            self.Jugadores[Jugador] = p

    def moverAbajo(self, Jugador):
        with self.lock:
            p = self.Jugadores[Jugador]
            p.moverAbajo()
            self.Jugadores[Jugador] = p
            
    def moverAvanzar(self, Jugador):
        with self.lock:
            p = self.Jugadores[Jugador]
            self.puntuacion[Jugador] += p.moverAvanzar()
            self.Jugadores[Jugador] = p

    def Obstaculo_choca(self, nObst, Jugador):
        with self.lock:
            Obstaculo = self.Obstaculos[nObst]
            p = self.Jugadores[Jugador]
            p.inicializa()
            self.Jugadores[Jugador] = p
            Obstaculo.choca_Jugador(Jugador)
            self.puntuacion[(Jugador+1)%2] += 1
            self.Obstaculos[nObst] = Obstaculo

    def get_info(self):
        info = {
            'pos_0': self.Jugadores[0].get_pos(),
            'pos_1': self.Jugadores[1].get_pos(),
            'pos_Obstaculo': [o.get_pos() for o in self.Obstaculos],
            'puntuacion': list(self.puntuacion),
            'jugando': self.jugando.value == 1
        }
        return info

    def move_Obstaculo(self, nObs):
        with self.lock:
            Obstaculo = self.Obstaculos[nObs]
            Obstaculo.actualiza()
            pos = Obstaculo.get_pos()
            if pos[Y]<0 or pos[Y]>tamVentana[Y]:
                Obstaculo.rebota()
            self.Obstaculos[nObs]=Obstaculo

    def __str__(self):
        return f"G<{self.Jugadores[1]}:{self.Jugadores[0]}:{self.Obstaculos}:{self.jugando.value}>"

def jugar(lado, conn, game):
    try:
        print(f"inicializaing Jugador {ladoStr[lado]}:{game.get_info()}")
        conn.send(lado)
        conn.send(game.get_info()) 
        while game.is_jugando():
            command = ""
            while command != "N":
                command = conn.recv()
                print(command)
                if command == "U":
                    game.moverArriba(lado)
                elif command == "D":
                    game.moverAbajo(lado)
                elif command == "A":
                    game.moverAvanzar(lado)
                elif command in range(numObstaculos):
                    game.Obstaculo_choca(command, lado)
                elif command == "Q":
                    game.stop()
            if lado == 1:
                for i in range(numObstaculos):
                    game.move_Obstaculo(i)
            conn.send(game.get_info())
    except:
        traceback.print_exc()
        conn.close()
    finally:
        print(f"Game ended {game}")


def main(ip_address):
    manager = Manager()
    try:
        with Listener((ip_address, 6000), authkey=b'secret password') as listener:
            n_Jugador = 0
            Jugadores = [None, None]
            game = Game(manager)
            while True:
                print(f"accepting connection {n_Jugador}")
                conn = listener.accept()
                Jugadores[n_Jugador] = Process(target=jugar, args=(n_Jugador, conn, game))
                n_Jugador += 1
                if n_Jugador == 2:
                    Jugadores[0].start()
                    Jugadores[1].start()
                    n_Jugador = 0
                    Jugadores = [None, None]
                    game = Game(manager)

    except:
        traceback.print_exc()

if __name__=='__main__':
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]

    main(ip_address)
