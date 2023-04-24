from multiprocessing.connection import Client
import traceback
import pygame
import sys, os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
GREEN = (0,255,0)

tamVentana = (700, 525)
X, Y = 0, 1

SourceRana = ["RanaI.png", "RanaD.png"]
ladoStr = ["Izquierda", "Derecha"]

class Jugador():
    def __init__(self, lado):
        self.lado = lado
        self.pos = [None, None]

    def get_pos(self):
        return self.pos

    def get_lado(self):
        return self.lado

    def set_pos(self, pos):
        self.pos = pos

    def __str__(self):
        return f"P<{ladoStr[self.lado], self.pos}>"

class Obstaculo():
    def __init__(self, alto):
        self.pos=[ None, None ]
        self.alto = alto

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def __str__(self):
        return f"B<{self.pos}>"


class JuegoO():
    def __init__(self):
        self.Jugadores = [Jugador(i) for i in range(2)]
        self.Obstaculos = [Obstaculo(10), Obstaculo(10), Obstaculo(10), Obstaculo(10)]
        self.puntuacion = [0,0]
        self.jugando = True

    def get_Jugador(self, lado):
        return self.Jugadores[lado]

    def set_pos_Jugador(self, lado, pos):
        self.Jugadores[lado].set_pos(pos)


    def get_Obstaculo(self):
        return self.Obstaculos

    def set_Obstaculo_pos(self, pos):
        for i in range(len(pos)):
            self.Obstaculos[i].set_pos(pos[i])

    def get_puntuacion(self):
        return self.puntuacion

    def set_puntuacion(self, puntuacion):
        self.puntuacion = puntuacion


    def update(self, Juegoinfo):
        self.set_pos_Jugador(0, Juegoinfo['pos_0'])
        self.set_pos_Jugador(1, Juegoinfo['pos_1'])
        self.set_Obstaculo_pos(Juegoinfo['pos_Obstaculo'])
        self.set_puntuacion(Juegoinfo['puntuacion'])
        self.jugando = Juegoinfo['jugando']

    def is_jugando(self):
        return self.jugando

    def stop(self):
        self.jugando = False

    def __str__(self):
        return f"G<{self.Jugadores[1]}:{self.Jugadores[0]}:{self.Obstaculo}>"


class Rana(pygame.sprite.Sprite):
    def __init__(self, Jugador):
      super().__init__()
      self.image = pygame.image.load(SourceRana[Jugador.get_pos()])
      self.Jugador = Jugador
      self.rect = self.image.get_rect()
      self.update()

    def update(self):
        pos = self.Jugador.get_pos()
        self.rect.centerx, self.rect.centery = pos

    def __str__(self):
        return f"S<{self.Jugador}>"


class ObstaculoSprite(pygame.sprite.Sprite):
    def __init__(self, Obstaculo):
        super().__init__()
        self.Obstaculo = Obstaculo
        self.image = pygame.image.load("lillambo.png")
        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        pos = self.Obstaculo.get_pos()
        self.rect.centerx, self.rect.centery = pos

class Display():
    def __init__(self, Juego):
        self.Juego = Juego
        self.ranas = [Rana(self.Juego.get_Jugador(i)) for i in range(2)]
        self.obstaculos = [ObstaculoSprite(obs) for obs in self.Juego.get_Obstaculo()]
        self.obstaculo_group = pygame.sprite.Group()
        self.rana_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        for rana  in self.ranas:
            self.rana_group.add(rana)
            self.all_sprites.add(rana)
        for obstaculo in self.obstaculos:
            self.obstaculo_group.add(obstaculo)
            self.all_sprites.add(obstaculo)

        self.screen = pygame.display.set_mode(tamVentana)
        self.clock =  pygame.time.Clock()  #60
        self.background = pygame.image.load('background.png')
        pygame.init()

    def analyze_events(self, lado):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events.append("Q")
                elif event.key == pygame.K_UP:
                    events.append("U")
                elif event.key == pygame.K_DOWN:
                    events.append("D")
                elif event.key == pygame.K_LEFT:
                    events.append("A")
                elif event.key == pygame.K_RIGHT:
                    events.append("A")
            elif event.type == pygame.QUIT:
                events.append("Q")
        for i in range(len(self.obstaculos)):
            if pygame.sprite.collide_rect(self.obstaculos[i], self.ranas[lado]):
                events.append(i)
        return events


    def refresh(self):
        self.all_sprites.update()
        self.screen.blit(self.background, (0, 0))
        puntuacion = self.Juego.get_puntuacion()
        font = pygame.font.Font(None, 74)
        text = font.render(f"{puntuacion[0]}", 1, WHITE)
        self.screen.blit(text, (250, 10))
        text = font.render(f"{puntuacion[1]}", 1, WHITE)
        self.screen.blit(text, (tamVentana[X]-250, 10))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def tick(self):
        self.clock.tick(60)

    @staticmethod
    def quit():
        pygame.quit()

def main(ip_address):
    try:
        with Client((ip_address, 6000), authkey=b'secret password') as conn:
            empiezaJuego(conn)
    except:
        traceback.print_exc()
    finally:
        pygame.quit()

def empiezaJuego(conn):
    Juego = JuegoO()
    print('conectado')
    lado = conn.recv()
    Juegoinfo = conn.recv()
    print(f"Jugando en {ladoStr[lado]}")
    Juego.update(Juegoinfo)
    display = Display(Juego)
    while Juego.is_jugando():
        events = display.analyze_events(lado)
        for ev in events:
            conn.send(ev)
            if ev == 'Q':
                Juego.stop()
        conn.send("N")
        Juegoinfo = conn.recv()
        Juego.update(Juegoinfo)
        display.refresh()
        display.tick()

if __name__=="__main__":   
    getArg = lambda pD, numArg: pD if len(sys.argv) <= numArg else sys.argv[numArg]
    main(getArg("127.0.0.1", 1))
