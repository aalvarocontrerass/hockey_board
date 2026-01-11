import pygame
import pickle
from objetos import Jugador

def cargar_imagen(imagen_fondo, ancho, alto):
    """
    Carga la imagen    
    """
    imagen = pygame.image.load(imagen_fondo).convert()
    fondo = pygame.transform.smoothscale(imagen, (ancho, alto))
    return fondo

def crear_jugadores():
    """
    Crea a todos los jugadores necesarios, en este caso 4 azules y 4 rojos
    """
    jugadores:list[Jugador] = []
    for i in range(1,5):
        jugadores.append(Jugador(45, 150 + (i * 60), (200, 0, 0),i))  # Rojos
        jugadores.append(Jugador(820, 150 + (i * 60), (0, 0, 200),i))  # Azules
    return jugadores

def remove_puck_todos(jugadores:list[Jugador])->None:
    """
    Establece que nadie tenga el puck
    """
    for jugador in jugadores:
        jugador.puck = None  

def get_jugador_con_puck(jugadores:list[Jugador])->Jugador:
    """
    Solo puede tener un jugador el puck
    """
    for jugador in jugadores:
        if jugador.puck != None:
            return jugador
        
def guardar_jugadas(dict_todas_las_jugadas:dict)->None:
    """
    Guarda las jugadas en un fichero para que se puedan ejecutar después de cerrar el programa y que no se pierdan    
    """
    with open("fichero_jugadas.obj","wb") as fichero:
        pickle.dump(dict_todas_las_jugadas,fichero)
    
def abrir_jugadas()->dict:
    """
    Abre las jugadas guardadas anteriormente
    """    
    with open("fichero_jugadas.obj","rb") as fichero:
        dict_todas_las_jugadas = pickle.load(fichero)
    return dict_todas_las_jugadas
    