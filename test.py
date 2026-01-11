import pygame
pygame.init()
import funciones as f
from constantes import *
from objetos import Jugador

jugadores:Jugador = f.crear_jugadores()
if len(jugadores) == 8:
    print("OK:")
    for jugador in jugadores:
        print(jugador)
else:
    print("ERROR")