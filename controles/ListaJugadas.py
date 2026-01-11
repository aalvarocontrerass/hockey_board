import pygame

pygame.init()

from constantes import *

class ListaJugadas:
    def __init__(self, rect, options, default_index=0, on_change=None):
        self.rect = pygame.Rect(rect)
        self.options = options[:]  # copia
        self.selected = default_index
        self.on_change = on_change

        self.open = False
        self.hover = False
        self.hover_index = -1

        self.item_h = self.rect.height
        self._recalc_dropdown()

        # Ajuste de selected si no hay opciones
        if len(self.options) == 0:
            self.selected = -1
        else:
            if self.selected < 0:
                self.selected = 0
            if self.selected >= len(self.options):
                self.selected = len(self.options) - 1

    def _recalc_dropdown(self):
        self.dropdown_rect = pygame.Rect(
            self.rect.x,
            self.rect.y + self.rect.height,
            self.rect.width,
            self.item_h * len(self.options)
        )

    def add_option(self, value, select_new=True):
        value = value.strip()
        if value != "":
            self.options.append(value)
            self._recalc_dropdown()
            if select_new:
                self.selected = len(self.options) - 1
                if self.on_change:
                    self.on_change(self.options[self.selected], False)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
            self.hover_index = -1

            if self.open and self.dropdown_rect.collidepoint(event.pos):
                rel_y = event.pos[1] - self.dropdown_rect.y
                idx = int(rel_y // self.item_h)
                if 0 <= idx < len(self.options):
                    self.hover_index = idx

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Click en el combo (abre/cierra)
            if self.rect.collidepoint(event.pos):
                if len(self.options) > 0:
                    self.open = not self.open
            else:
                # Click en una opción
                if self.open and self.dropdown_rect.collidepoint(event.pos):
                    rel_y = event.pos[1] - self.dropdown_rect.y
                    idx = int(rel_y // self.item_h)
                    if 0 <= idx < len(self.options):
                        self.selected = idx
                        self.open = False
                        if self.on_change:
                            self.on_change(self.options[self.selected])
                else:
                    # Click fuera: cierra
                    self.open = False

    def dibujar(self, surface):
        # Caja principal
        if self.hover: 
            color = COLOR_WIDGET_HOVER
        else:
            color = COLOR_WIDGET_BG
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, width=2, border_radius=8)

        # Texto seleccionado
        if self.selected >= 0 and self.selected < len(self.options):
            sel_text = self.options[self.selected]
        else:
            sel_text = ""

        label = FUENTE.render(sel_text, True, COLOR_TEXT)
        label_rect = label.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(label, label_rect)

        # Flecha
        cx = self.rect.right - 18
        cy = self.rect.centery
        pygame.draw.polygon(surface, COLOR_TEXT, [(cx - 6, cy - 3), (cx + 6, cy - 3), (cx, cy + 5)])

        # Dropdown
        if self.open and len(self.options) > 0:
            pygame.draw.rect(surface, COLOR_WIDGET_BG, self.dropdown_rect, border_radius=8)
            pygame.draw.rect(surface, COLOR_BORDER, self.dropdown_rect, width=2, border_radius=8)

            i = 0
            while i < len(self.options):
                item_rect = pygame.Rect(
                    self.dropdown_rect.x,
                    self.dropdown_rect.y + i * self.item_h,
                    self.dropdown_rect.width,
                    self.item_h
                )

                if i == self.hover_index:
                    pygame.draw.rect(surface, COLOR_WIDGET_HOVER, item_rect)

                txt = FUENTE.render(self.options[i], True, COLOR_TEXT)
                txt_rect = txt.get_rect(midleft=(item_rect.x + 10, item_rect.centery))
                surface.blit(txt, txt_rect)

                i += 1
