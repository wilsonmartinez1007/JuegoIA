import pygame
import os

#CONFIGURACION DE LA VENTANA
SCREEN_WIDTH = 800
SCREEN_HEIGTH = 600

#Configuracion del jugador
PLAYER_SIZE = 30 #Tamaño del cuadro que representa a LUigi
PLAYER_SPEED = 4#Velocidad de movimiento
ANIMATION_SPEED = 100 #Milisegundos entre frames de animacion
ANIMATION_FRAMES = 8 #Numero total de frames en el sprite sheet

#Direcciones
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3


#Configuracion paredes
TILE_SIZE = 32 #tamaño de cada celda del lab
WALL_COLOR = (33, 33, 255)#color azul para las paredes

#configuracion del gato
GATO_SIZE = 40
GATO_ANIMATION_SPEED =200
GATO_FRAMES=8


#Configuracion de colisiones
COLLISION_TOLERANCE = 4 #Pixeles de tolerancia para colisiones
SLIDE_SPEED = 2 #Velocidad de deslizamiento en las paredes






#COLORES
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0) #color Luigi

LEVEL = [
    "1111111111111111111111111",
    "1P00000000000000000000001",
    "101111G111111111111111101",
    "1011110000000000011111101",
    "1100011111011111011100001",
    "1Q11011111011111000001111",
    "1011011111011111110111111",
    "1011000000011111110000001",
    "1011110111011111111111101",
    "1000000000000000000000001",
    "1011011111111111110111101",
    "1011011111111111110111101",
    "1011000000000000000000001",
    "1011111111011011111111101",
    "1000001111011000001111101",
    "1011100000011111101111101",
    "1011111111011111101111101",
    "1000000000000000000000001",
    "1111111111111111111111111",
]


#Funcion para cargar imagen
def load_image(name):
    """cargar una imagen desde la carpeta assets"""
    return pygame.image.load(os.path.join('assets', 'images', name)).convert_alpha()
