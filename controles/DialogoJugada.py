import pygame

pygame.init()

from constantes import *

class DialogoJugada:
    def __init__(self):
        self.active = False
        self.title = "Nombre de la jugada:"
        self.text = ""
        self.max_len = 25
        self.confirmed = False
        self.value = ""

    def open(self):
        self.active = True
        self.text = ""
        self.confirmed = False
        self.value = ""

    def close(self):
        self.active = False

    def handle_event(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.close()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    val = self.text.strip()
                    if val != "":
                        self.confirmed = True
                        self.value = val
                    self.close()
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                else:
                    # Añadir caracteres imprimibles
                    ch = event.unicode
                    if ch is not None:
                        if ch.isprintable():
                            if len(self.text) < self.max_len:
                                self.text += ch

    def dibujar(self, surface):
        if not self.active:
            return

        # Overlay semitransparente
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill(COLOR_DIALOG_OVERLAY)
        surface.blit(overlay, (0, 0))

        # Caja del diálogo
        w = 450
        h = 130
        rect = pygame.Rect(0, 0, w, h)
        rect.center = (surface.get_width() // 2, surface.get_height() // 2)

        pygame.draw.rect(surface, COLOR_DIALOG_BG, rect, border_radius=14)
        pygame.draw.rect(surface, COLOR_DIALOG_BORDER, rect, width=2, border_radius=14)

        # Título
        title_surf = FUENTE_GRANDE.render(self.title, True, COLOR_TEXT)
        surface.blit(title_surf, (rect.x + 10, rect.y + 10))

        # Caja de texto
        input_rect = pygame.Rect(rect.x + 10, rect.y + 40, rect.w - 20, 48)
        pygame.draw.rect(surface, (30, 30, 40), input_rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_DIALOG_BORDER, input_rect, width=2, border_radius=10)

        # Texto dentro
        text_surf = FUENTE.render(self.text, True, COLOR_TEXT)
        surface.blit(text_surf, (input_rect.x + 8, input_rect.y + 16))

        # Pista
        hint = "ENTER: añadir | ESC: cancelar"
        hint_surf = FUENTE.render(hint, True, (200, 200, 210))
        surface.blit(hint_surf, (rect.x + 230, rect.y + 110))
