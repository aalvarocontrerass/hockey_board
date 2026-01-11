import pygame
import sys
pygame.init()
import funciones as f
from constantes import *
from objetos import Puck
from controles.Boton import *
from controles.DialogoJugada import *
from controles.ListaJugadas import *

from funciones import *

"""
DEFINICIÓN DE EVENTOS DE CONTROLES - No se pueden mover a funciones.py
"""

def on_boton_grabar():
    global grabando
    if boton_grabar.text == "Grabar":
        # EMPIEZA LA GRABACIÓN
        grabando = True
        boton_grabar.text = "Parar"
    elif boton_grabar.text == "Parar":
        # TERMIA LA GRABACIÓN
        dialogo.open()
        boton_grabar.text = "Grabar"
        grabando = False

def on_boton_limpiar():
    i = 1
    for jugador in jugadores:
        if i % 2 != 0:    # ROJOS
            jugador.rect.x = 45
            jugador.rect.y = 150 + ((i+1)//2 * 60)
        else:    # AZULES
            jugador.rect.x = 820
            jugador.rect.y = 150 + ((i+1)//2 * 60)
        i += 1
    f.remove_puck_todos(jugadores)
    jugadores[0].puck = puck

def on_lista_jugadas_change(nombre_jugada, is_seleccionado_de_la_lista=True):
    global lista_grabacion_actual, reproduciendo
    if is_seleccionado_de_la_lista:
        lista_grabacion_actual = dict_todas_las_jugadas[nombre_jugada]
        reproduciendo = True

"""
INICIALIZACIÓN DE LA APLICACIÓN
"""

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Hockey Board")


lista_grabacion_actual = []  # Aquí guardaremos la jugada actual
grabando = False
reproduciendo = False
index_frame_reproduccion = 0

combo_jugadas = ListaJugadas((ANCHO - MARGEN - 220, 14, 220, 42), [], default_index = 0, on_change = on_lista_jugadas_change)

dialogo = DialogoJugada()

boton_limpiar = Boton((MARGEN, 14, 140, 42), "Limpiar", on_boton_limpiar)
boton_grabar = Boton((MARGEN + 160, 14, 140, 42), "Grabar", on_boton_grabar)

ancho_imagen = ANCHO - 2 * MARGEN
alto_imagen = ALTO - BARRA_TAREAS - 2 * MARGEN

"""
CARGA DE DATOS
"""
try:
    dict_todas_las_jugadas:dict[str, dict] = f.abrir_jugadas()
    for nombre_jugada in dict_todas_las_jugadas:
        combo_jugadas.add_option(nombre_jugada)
except FileNotFoundError:
    dict_todas_las_jugadas:dict[str, dict] = {} # nombre_jugada:dict_jugadores y puck

try:
    fondo = cargar_imagen("imagenes/fondo.jpg", ancho_imagen, alto_imagen)
except Exception as error:
    print("No se pudo cargar 'imagen.png':", error)

"""
INICIALIZACIÓN DE VARIABLES
"""
clock = pygame.time.Clock()

jugadores = f.crear_jugadores()
puck = Puck()
jugadores[0].puck = puck

moviendo_puck = False
tiempo_ms_down = 0
start_rec = False
jugador_seleccionado = None
jugador_pasador = None
ejecutando = True
estado_anterior = {}
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                encontrado = False
                i = 0
                while i < len(jugadores) and not encontrado:
                    jugador = jugadores[i]
                    if jugador.rect.collidepoint(evento.pos):
                        # Movimiento del jugador correcto se pulse donde se pulse
                        mouse_x, mouse_y = evento.pos
                        jugador.offset_x = jugador.rect.x - mouse_x
                        jugador.offset_y = jugador.rect.y - mouse_y
                        jugador_seleccionado = jugador
                        tiempo_ms_down = pygame.time.get_ticks()
                        encontrado = True
                    i += 1
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                tiempo_ms_up = pygame.time.get_ticks()
                if tiempo_ms_up - tiempo_ms_down < TIEMPO_DIFERENCIAR_CLICK: 
                    # INICIO DEL CLICK
                    if jugador_seleccionado != None and jugador_seleccionado.puck != None:
                        # INICIO DEL PASE
                        jugador_pasador = jugador_seleccionado
                        jugador_pasador.pasando = True
                    elif jugador_pasador != None:
                        punto1_x, punto1_y = jugador_pasador.rect.x, jugador_pasador.rect.y
                        punto2_x, punto2_y = jugador_seleccionado.rect.x, jugador_seleccionado.rect.y
                        
                        jugador_pasador.puck = None
                        jugador_seleccionado.puck = None
                        
                        dx = punto2_x-punto1_x
                        dy = punto2_y-punto1_y
                        offset = 0
                        moviendo_puck = True
                        if dx ==  0:
                            dx = 10
                    else:
                        jugador_seleccionado = None                     
                else: 
                    # FIN DEL MOTION
                    jugador_seleccionado = None 
        elif evento.type == pygame.MOUSEMOTION:
            if jugador_seleccionado != None and jugador_pasador == None:
                mouse_x, mouse_y = evento.pos
                jugador_seleccionado.rect.x = mouse_x + jugador_seleccionado.offset_x
                jugador_seleccionado.rect.y = mouse_y + jugador_seleccionado.offset_y
        
        if dialogo.active:
            dialogo.handle_event(evento)
        else:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                running = False
            boton_limpiar.handle_event(evento)
            boton_grabar.handle_event(evento)
            combo_jugadas.handle_event(evento)


    ### FIN DE EVENTOS 
    if reproduciendo:
        if index_frame_reproduccion < len(lista_grabacion_actual):
            jugador_temp = f.get_jugador_con_puck(jugadores)
            if jugador_temp != None:
                ultimo_jugador_con_puck = jugador_temp
            diccionario_objetos = lista_grabacion_actual[index_frame_reproduccion]
            # Mover jugadores a la posición grabada
            for i, pos in enumerate(diccionario_objetos['jugadores']):
                jugadores[i].rect.x, jugadores[i].rect.y = pos
            f.remove_puck_todos(jugadores)    # Quitamos el puck al jugador para que se pueda mover en los pases
            puck.rect.x, puck.rect.y = diccionario_objetos["puck_pos"]    # Mover el puck a la posición grabada
            index_frame_reproduccion += 1
        else:
            reproduciendo = False
            index_frame_reproduccion = 0
            pos = len(lista_grabacion_actual) - 1
            diccionario_ultimo_objeto = lista_grabacion_actual[pos]
            index_jugador_puck = diccionario_ultimo_objeto["index_jugador_puck"]
            jugadores[index_jugador_puck].puck = puck
            lista_grabacion_actual = []
    elif moviendo_puck:
        if not puck.rect.colliderect(jugador_seleccionado.rect):
            puck.rect.x =  offset + punto1_x
            puck.rect.y = offset * dy/dx + punto1_y
            if dx > 0:
                offset += SPEED_PUCK
            else:
                offset -= SPEED_PUCK
        else:
            # FIN DEL PASE
            jugador_seleccionado.puck = puck  
            jugador_pasador.pasando = False
            jugador_pasador = None 
            jugador_seleccionado = None   
            moviendo_puck = False

    if grabando:
        dict_estado_actual = {"jugadores":[]}
        for jugador in jugadores:
            dict_estado_actual["jugadores"].append((jugador.rect.x, jugador.rect.y))
        dict_estado_actual["puck_pos"] = (puck.rect.x, puck.rect.y)
        for i in range(len(jugadores)):
            if dict_estado_actual["jugadores"][i] == dict_estado_actual["puck_pos"]:
                dict_estado_actual["index_jugador_puck"] = i     # Lo utilizamos para saber quien fue el último jugador con puck, si su posición coincie con la del puck
        if estado_anterior != dict_estado_actual:
            lista_grabacion_actual.append(dict_estado_actual)
            estado_anterior = dict_estado_actual


    # FIN DE GRABACIÓN Y CIERRE DE DIALOGO de NOMBRE JUGADA 

    # Se confirma el nombre de la jugada y se agrega al diccionario de jugadas 
    if not dialogo.active and dialogo.confirmed:
        nombre_jugada = dialogo.value
        combo_jugadas.add_option(nombre_jugada)
        if len(lista_grabacion_actual) > 0:
            dict_todas_las_jugadas[nombre_jugada] = lista_grabacion_actual
            lista_grabacion_actual = []
        dialogo.confirmed = False
        dialogo.value = ""

# Barra de tareas
    barra_tareas_rect = pygame.Rect(0, 0, ANCHO, BARRA_TAREAS)
    pygame.draw.rect(pantalla, COLOR_TB_BG, barra_tareas_rect)
    pygame.draw.line(pantalla, COLOR_BORDER, (0, BARRA_TAREAS), (ANCHO, BARRA_TAREAS), 2)

    imagen_rect = fondo.get_rect()
    area_rect = pygame.Rect(MARGEN, BARRA_TAREAS + MARGEN, ANCHO - 2 * MARGEN, ALTO - BARRA_TAREAS - 2 * MARGEN)
    imagen_rect.center = area_rect.center

    pantalla.blit(fondo, imagen_rect)

    boton_limpiar.dibujar(pantalla)
    boton_grabar.dibujar(pantalla)
    combo_jugadas.dibujar(pantalla)


    for jugador in jugadores:
        jugador.dibujar(pantalla)
    puck.dibujar(pantalla)
    
    dialogo.dibujar(pantalla)
    
    # Actualizar la pantalla
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()

f.guardar_jugadas(dict_todas_las_jugadas)

sys.exit()