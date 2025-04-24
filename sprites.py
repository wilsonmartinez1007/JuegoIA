from config import*
import pygame
from Logica.logicaJuegoIA import encontrar_caminoAmplitud, matrizPos,mCostos, encontrar_camino_Profundidad, encontrar_camino_astar
from Logica.logicaJuegoIA import continuar_con_otra_busqueda


class Wall:
    def __init__(self,x,y):
            self.rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    def draw(self, screen):
        """Dibujar la pared en la pantalla"""
        pygame.draw.rect(screen, WALL_COLOR,self.rect)  

class Gato:
    def __init__(self,x,y):
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE + TILE_SIZE // 2
        #cargar sprite sheet de gato
        self.sprite_sheet = load_image('gato2.png')
        
        self.frames = []
        
        frame = pygame.Surface((16,16), pygame.SRCALPHA)
        frame.blit(self.sprite_sheet,(0,0), (1*16, 0, 16, 16))
        frame = pygame.transform.scale(frame, (GATO_SIZE, GATO_SIZE))
        self.frames.append(frame)

        #Variables de animacion
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()
        #CREAR EL REGTANGULO para colisiones y posicionamientos
        self.rect = self.frames[0].get_rect(center=(self.x, self.y))
    def update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.animation_timer>GATO_ANIMATION_SPEED:
            #Avanzar el siguiente frame
            self.current_frame = (self.current_frame + 1)%GATO_FRAMES
            self.animation_timer = current_time

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame],self.rect)
                
        
class Queso:
    def __init__(self,x,y):
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE + TILE_SIZE // 2
        #cargar sprite sheet de gato
        self.sprite_sheet = load_image('queso.png')
        
        self.frames = []
        
        frame = pygame.Surface((16,16), pygame.SRCALPHA)
        frame.blit(self.sprite_sheet,(0,0), (1*16, 0, 16, 16))
        frame = pygame.transform.scale(frame, (GATO_SIZE, GATO_SIZE))
        self.frames.append(frame)

        #Variables de animacion
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()
        #CREAR EL REGTANGULO para colisiones y posicionamientos
        self.rect = self.frames[0].get_rect(center=(self.x, self.y))

        
    def update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.animation_timer>GATO_ANIMATION_SPEED:
            #Avanzar el siguiente frame
            self.current_frame = (self.current_frame + 1)%GATO_FRAMES
            self.animation_timer = current_time

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame],self.rect)
               


class Player:
    def __init__(self, x, y, game):
        #pos inicial del jugado
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE + TILE_SIZE // 2

        #cargar sprite sheet de raton
        self.sprite_sheet = load_image('mickey.png')

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

        #desde aqui cambie
        self.destino_px = None  # Nueva variable para almacenar la posición destino en píxeles
        self.ruta_finalizada = False


        self.establecer_ruta(matrizPos)
        self.speed = PLAYER_SPEED
        self.index_direccion = 0


        self.game = game  # Guardamos la referencia a Game

    def establecer_ruta(self, matrizPos):
        self.ruta = continuar_con_otra_busqueda(matrizPos, mCostos)
        self.direcciones = self.convertir_a_direcciones(self.ruta)
        self.index_direccion = 0
        

    def convertir_a_direcciones(self, camino):
        direcciones_dict = {
            (0, 1): RIGHT,
            (0, -1): LEFT,
            (-1, 0): UP,
            (1, 0): DOWN
        }
        direcciones = []
        for i in range(len(camino) - 1):
            actual = camino[i]
            siguiente = camino[i + 1]
            dx = siguiente[0] - actual[0]
            dy = siguiente[1] - actual[1]
            mov =direcciones_dict.get((dx, dy))
            direcciones.append(mov)
        return direcciones
    def camino(self):
        self.dx, self.dy = 0, 0

        if self.index_direccion < len(self.ruta) - 1:
            if self.destino_px is None:
                destino = self.ruta[self.index_direccion + 1]
                self.destino_px = (
                    destino[1] * TILE_SIZE + TILE_SIZE // 2,
                    destino[0] * TILE_SIZE + TILE_SIZE // 2
                )

            # Movimiento hacia el destino
            if self.rect.centerx < self.destino_px[0]:
                self.dx = min(self.speed, self.destino_px[0] - self.rect.centerx)
            elif self.rect.centerx > self.destino_px[0]:
                self.dx = -min(self.speed, self.rect.centerx - self.destino_px[0])

            if self.rect.centery < self.destino_px[1]:
                self.dy = min(self.speed, self.destino_px[1] - self.rect.centery)
            elif self.rect.centery > self.destino_px[1]:
                self.dy = -min(self.speed, self.rect.centery - self.destino_px[1])

            self.rect.centerx += self.dx
            self.rect.centery += self.dy

            # Verificar llegada exacta
            if self.rect.center == self.destino_px:
                self.index_direccion += 1
                self.destino_px = None  # Preparar siguiente destino
            #Actualizar  estado de mov
            self.is_moving = self.dx != 0 or self.dy != 0

        else:
            self.dx = self.dy = 0
            self.ruta_finalizada = True
            self.game.pantalla_gano()
            if self.game.meDesplazo:
               self.handle_input()


    def update_animation(self):
        """Actualizar el frame de animacion"""
        if not self.is_moving:
              self.current_frame = 0
              return
        
        current_time = pygame.time.get_ticks()
        
        if current_time - self.animation_timer>ANIMATION_SPEED:
            #Avanzar el siguiente frame
            self.current_frame = (self.current_frame + 1)%ANIMATION_FRAMES
            self.animation_timer = current_time
        
                 
    def update_image(self):
        """Actualizar la imagen segun la direccion y frame actual"""
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
        """Mover el jugador segun la entrada de usuario"""
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
        #Intentar el mov en y
        if self.dy != 0:
            #Comprobar colision en y
            if not self.check_collision(walls, 0, self.dy):
                self.y += self.dy
            else:
                #Intentar deslizarse verticalmente si hay colision
                if self.check_collision(walls, -SLIDE_SPEED, self.dy):
                    if not self.check_collision(walls, SLIDE_SPEED, self.dy):
                        self.x += SLIDE_SPEED
                else:
                    self.x -= SLIDE_SPEED
        #Actualiza el rectangulo con la nueva pos
        self.rect.center = (self.x, self.y)

        
        
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
        """Manejar la entrada del usuario y actualizar velocidad"""
        keys = pygame.key.get_pressed()

        # Reiniciar la velocidad
        self.dx = 0
        self.dy = 0

        # Volver a calcular la ruta si se presiona ENTER
        if keys[pygame.K_RETURN]:
            self.rect.centerx = (self.rect.centerx // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
            self.rect.centery = (self.rect.centery // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
            self.actualizarMatriz()
            self.ruta_finalizada = False
            self.establecer_ruta(matrizPos)  # ← Recalcula la ruta
            self.destino_px = None  # ← Prepara nueva ruta
            self.index_direccion = 0
            return  # Evita moverse con teclas en el mismo frame

        # Actualizar velocidad y dirección basado en las teclas presionadas
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

        # Actualizar estado de movimiento
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
    def actualizarMatriz(self):
        self.fila = self.rect.centery // TILE_SIZE
        self.columna = self.rect.centerx // TILE_SIZE
        matrizPos[self.fila][self.columna] = "P"
        
         
           
    def update(self, walls):
          if not self.ruta_finalizada:
            self.camino()
            self.update_animation()
            self.update_image()
            self.move(walls)
          else:
               self.handle_input()
               self.update_animation()
               self.update_image()
               self.move(walls)
       

           
                 
    def draw(self, screen):
            """Dibujar el jugador en la pantalla"""
            screen.blit(self.image, self.rect)