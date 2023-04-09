import pygame
import random
from math import dist
from spaceInvaders.avatares import Asteroide, Disparo, Jugador

class JuegoIndividual():  
    
    def game_over(self):
        game_over_text = self.game_over_font.render("GAME OVER", True, (255,255,255))
        self.pantalla.blit(game_over_text, (190, 250))
    
    def jugar(self):
        running = True
        while running:
            self.pantalla.fill((0, 0, 0)) #Pantalla negra
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit() 
                    pygame.quit()
                    running = False    
                    return 0
                else:
                    self.jugador.eventos(event, self.disparo)
                  
            self.jugador.X += self.jugador.Xchange
            self.disparo.movimiento()
                
            for a in self.asteroides:
                self.puntos_val += a.movimiento(self.jugador, self.disparo, self.asteroides)       
            
            self.jugador.movimiento()
            self.pantalla.blit(self.font.render("Puntos: " + str(self.puntos_val), True, (255,255,255)), (5,5))
            pygame.display.update()   
            
    def __init__(self, no_asteroides = 10):
        pygame.init()
        self.pantalla = pygame.display.set_mode((800, 600))        
        pygame.display.set_caption("Juego Space Invaders")
        self.puntos_val = 0        
        self.font = pygame.font.Font('freesansbold.ttf', 20)        
        self.game_over_font = pygame.font.Font('freesansbold.ttf', 64)        
        self.jugador = Jugador(self.pantalla)   
        self.asteroides = [Asteroide(self.pantalla) for num in range(no_asteroides)]       
        self.disparo = Disparo(self.pantalla)        
        salida = self.jugar()        
