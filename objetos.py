import pygame
from constantes import *

pygame.font.init()



class Jugador:
    def __init__(self, x, y, color, numero:int):
        ANCHO = 30
        ALTO = 30
        self.rect = pygame.Rect(x, y, ANCHO, ALTO)
        self.color = color
        self.pasando = False    # Permite colorear el jugador pasador
        self.offset_x = 0
        self.offset_y = 0
        self.numero = numero
        self.puck = None    # Movemos el puck siempre con el jugador. Cuando hay pase, ninguno tiene el puck
    

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 20)    # Relleno
        if self.pasando:
            pygame.draw.circle(superficie, (0, 255, 0), self.rect.center, 20, 4)    # Borde del pasador
        else:
            pygame.draw.circle(superficie, (255, 255, 255), self.rect.center, 20, 2)    # Borde del resto
        
        if self.puck != None:    # Si el jugadro tiene el puck, se pinta junto al jugador
            self.puck.rect = self.rect.copy()      
        
        texto_numero = FUENTE_JUGADORES.render(str(self.numero), True, (255, 255, 255))
        texto_rect = texto_numero.get_rect()
        texto_rect.center = self.rect.center
        superficie.blit(texto_numero, texto_rect)

    def __str__(self):
        return f"#{self.numero} Color: {self.color}"


class Puck:
    def __init__(self):
        ANCHO = 8
        ALTO = 8
        self.rect = pygame.Rect(0, 0, ANCHO, ALTO)

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, (0,0,0), (self.rect.x, self.rect.y), 8)