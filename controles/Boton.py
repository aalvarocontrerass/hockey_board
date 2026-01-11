import pygame

pygame.init()

from constantes import *

class Boton:
    def __init__(self, rect, text, on_click):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()

    def dibujar(self, surface):
        if self.hover:
            color = COLOR_WIDGET_HOVER 
        else:
            color = COLOR_WIDGET_BG
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, width=2, border_radius=8)

        label = FUENTE.render(self.text, True, COLOR_TEXT)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)
