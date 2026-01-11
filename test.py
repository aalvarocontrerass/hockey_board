import pygame
pygame.init()
import funciones as f
from constantes import *
from objetos import Jugador

def test1():
    jugadores:Jugador = f.crear_jugadores()
    if len(jugadores) == 8:
        print("OK:")
        for jugador in jugadores:
            print(jugador)
    else:
        print("ERROR")

def test2():
    """
    Rehacer fichero de jugadas
    """
    dic_jugadas = f.abrir_jugadas()
    print(dic_jugadas.keys())

    jugada = dic_jugadas["Jugada por defecto"]
    dicc = {}
    dicc["Jugada por defecto"] = dic_jugadas["Jugada por defecto"]
    f.guardar_jugadas(dicc)


test1()