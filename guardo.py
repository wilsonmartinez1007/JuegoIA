""" config.py
    import pygame
    import os

    #CONFIGURACION DE LA VENTANA
    SCREEN_WIDTH = 800
    SCREEN_HEIGTH = 600

    #Configuracion del jugador
    PLAYER_SIZE = 25 #Tamaño del cuadro que representa a LUigi
    PLAYER_SPEED = 5 #Velocidad de movimiento
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
        "1011110111111111111111101",
        "1011110000000000011111101",
        "1000011111011111011100001",
        "1011011111011111000001111",
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
        return pygame.image.load(os.path.join('assets', 'images', name)).convert_alpha()


sprites.py:
from Logica import logicaJuegoIA
from config import*
import pygame

class Wall:
    def __init__(self,x,y):
            self.rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    def draw(self, screen):
        pygame.draw.rect(screen, WALL_COLOR,self.rect)  


class Player:
    def __init__(self, x, y):
        #pos inicial del jugado
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE + TILE_SIZE // 2

        #cargar sprite sheet de pacman
        self.sprite_sheet = load_image('liugui.png')

        #Cargar todos los frames de animacion
        self.animation_frames = []
        for i in range(ANIMATION_FRAMES):
             #Craer superficie para el frame
             frame = pygame.Surface((16,16),pygame.SRCALPHA)

             #Copiar el frame del sprite sheep
             frame.blit(self.sprite_sheet,(0,0), (i*16, 0, 16, 16))
             #Escalar el frame al tamaño del jugador
             frame = pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE))
             self.animation_frames.append(frame)
        #Variables de animacion
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()
        self.is_moving = False
        
        #Imagen actual del jugador
        self.original_image = self.animation_frames[0]
        self.image = self.animation_frames[0]

        #CREAR EL REGTANGULO para colisiones y posicionamientos
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        #Direccion actual 
        self.direction = RIGHT

        #deltas
        self.dx = 0
        self.dy = 0


    def update_animation(self):
        if not self.is_moving:
              self.current_frame = 0
              return
        
        current_time = pygame.time.get_ticks()

        if current_time - self.animation_timer>ANIMATION_SPEED:
            #Avanzar el siguiente frame
            self.current_frame = (self.current_frame + 1)%ANIMATION_FRAMES
            self.animation_timer = current_time
        
                 
    def update_image(self):
        self.original_image = self.animation_frames[self.current_frame]
        

        #Actualizar direccion basada en el movimiento horizontal
        if self.dx > 0:
                self.direction = RIGHT #Derecha
                self.image = self.original_image
                
        elif self.dx < 0:
                self.direction = LEFT #Izquierda
                self.image = pygame.transform.flip(self.original_image, True, False)
                
        elif self.dy < 0:
                self.direction = UP #arriba
                self.image = pygame.transform.rotate(self.original_image, 90)
                
        elif self.dy > 0:
                self.direction = DOWN #abajo
                self.image = pygame.transform.rotate(self.original_image, -90)
                
                   
         




    def move(self, walls):
            #Intentar el mov en x
            if self.dx != 0:
                #Comprobar colision en x
                if not self.check_collision(walls, self.dx, 0):
                    self.x += self.dx
                else:
                      #Intentar deslizarse verticalmente si hay colision
                    if self.check_collision(walls, self.dx, -SLIDE_SPEED):
                        if not self.check_collision(walls, self.dx, SLIDE_SPEED):
                            self.y += SLIDE_SPEED
                    else:
                        self.y -= SLIDE_SPEED

            #Mantener al jugador dentro de la pantalla
            if self.x > SCREEN_WIDTH - PLAYER_SIZE:
                self.x = 0
            elif self.x < 0:
                  self.x = SCREEN_WIDTH - PLAYER_SIZE
            
            if self.y > SCREEN_HEIGTH - PLAYER_SIZE:
                self.y = 0
            elif self.y < 0:
                  self.y = SCREEN_HEIGTH - PLAYER_SIZE
                  

                        
            
    def handle_input(self):
            keys = pygame.key.get_pressed()

            #Reiniciar la velocidad
            self.dx = 0
            self.dy = 0

            #Actualizar velocidad y direccion basado en las teclas presionadas
            if keys[pygame.K_RIGHT]:
                  self.dx = PLAYER_SPEED
                  self.direction = RIGHT
            elif keys[pygame.K_LEFT]:
                  self.dx = -PLAYER_SPEED
                  self.direction = LEFT
            elif keys[pygame.K_UP]:
                  self.dy = -PLAYER_SPEED
                  self.direction = UP
            elif keys[pygame.K_DOWN]:
                  self.dy = PLAYER_SPEED
                  self.direction = DOWN
            

            #Actualizar  estado de mov
            self.is_moving = self.dx != 0 or self.dy != 0
            
    def check_collision(self, walls, dx=0, dy=0):
        #Comprobar si hay colsion en una posicion futura
        #Creaer un rectangulo temporal en la posicion futura
        future_rect = self.rect.copy()
        future_rect.x += dx
        future_rect.y += dy

        for wall in walls:
            if future_rect.colliderect(wall.rect):
                return True
        return False
            
                    
           
    def update(self, walls):
          self.handle_input()
          self.update_animation()
          self.update_image()
          self.move(walls)
       

           
                 
    def draw(self, screen):
            screen.blit(self.image, self.rect)

    """