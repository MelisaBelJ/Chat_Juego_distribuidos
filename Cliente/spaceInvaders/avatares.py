import pygame
import random
from math import dist

class avatar():
    def __init__(self, pantalla, imagen, x, y, xc, yc):
        self.Image = pygame.image.load('spaceInvaders/'+imagen)
        self.X = x
        self.Y = y
        self.Xchange = xc
        self.Ychange = yc
        self.pantalla = pantalla
        
    def actualiza(self, a=0,b=0):
        self.pantalla.blit(self.Image, (self.X-a, self.Y+b))
            
class Disparo(avatar):
    def __init__(self, pantalla):
        super(Disparo, self).__init__(pantalla, 'laser.png', 0, 600, 0, 3)
        self.disparado = False
        
    def movimiento(self):
        if self.Y <= 0:
            self.choque()
        if self.disparado:
            self.actualiza()
            self.Y -= self.Ychange
            
    def dispara(self, x):
        if not self.disparado:
            self.actualiza()
            self.X = x
            self.disparado = True
            
    def choque(self):
        self.Y = 600
        self.disparado =  False
        
class Asteroide(avatar):
    def __init__(self, pantalla):
        super(Asteroide, self).__init__(pantalla, 'asteroide.png', random.randint(64, 737), random.randint(30, 180), 0.6, 0.6)
        
    def movimiento(self, jugador, disparo, asteroides):  
        self.X += self.Xchange               
        if self.X >= 735 or self.X <= 0: #si da contra la pared rebota :)
            self.Xchange *= -1
        
        collision = dist([disparo.X, disparo.Y], [self.X, self.Y]) <= 20
        
        if collision:
            disparo.choque()
            self.X = random.randint(64, 736)
            self.Y = random.randint(30, 200)
        
        self.actualiza()
        return int(collision)
    
class Jugador(avatar):
    def __init__(self, pantalla):
        super(Jugador, self).__init__(pantalla, 'nave.png', 370, 523, 0, 0)
    
    def eventos(self, event, disparo):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.Xchange = -1.7
            elif event.key == pygame.K_RIGHT:
                self.Xchange = 1.7
            elif event.key == pygame.K_SPACE:
                disparo.dispara(self.X)
        elif event.type == pygame.KEYUP:
            self.Xchange = 0
            
    def movimiento(self):      
        if self.X  <= 16:
            self.X  = 16;
        elif self.X  >= 750:
            self.X  = 750
        self.actualiza(20, 10)
