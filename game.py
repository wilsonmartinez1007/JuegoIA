import pygame
from sprites import*
from config import*
import sys
#acordarme cambiar interptrete con crt+ship+p y colocar el global para el proyecto
class Game: 
   
    def __init__(self):
        #inicializar pygame
        pygame.init()

        #crear la ventana
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGTH))
        pygame.display.set_caption("Juego IA")
        #Reloj controlar el juego
        self.clock = pygame.time.Clock()

        #Variable para controlar el bucle del juego
        self.running = True

        #CREAR JUGADOR, paredes, gato
        self.walls = []
        self.gato = None
        self.queso =None
        self.player = None
        self.create_level()


        self.meDesplazo = False
        
    def create_level(self):
        """Crear el nivel a partir el diseño en level"""
        for row_index, row in enumerate(LEVEL):
            for col_index, cell in enumerate(row):
                if cell == "1":
                    self.walls.append(Wall(col_index, row_index))
                elif cell == "G":
                    self.gato = Gato(col_index, row_index)
                elif cell == "Q":
                    self.queso = Queso(col_index, row_index)
                elif cell =="P":
                    self.player = Player(col_index, row_index, self)

    def handle_events(self):
        for event in pygame.event.get():
            #Si el usuario cierrra ventana
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        """actualizar el estado del juego"""
        self.player.update(self.walls)

    def pantalla_inicio(self):
        font_inicio = pygame.font.Font("assets/fonts/Silver.ttf", 30)
        boton_jugar = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGTH / 2 - 50, 200, 50)
        boton_salir = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGTH / 2 + 50, 200, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_jugar.collidepoint(event.pos):
                        return  # Sale del menú y empieza el juego
                    if boton_salir.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            self.screen.fill(YELLOW)

            pygame.draw.rect(self.screen, MORADO, boton_jugar)
            pygame.draw.rect(self.screen, ROJO, boton_salir)

            texto_boton_jugar = font_inicio.render("Jugar", True, (0, 0, 0))
            texto_boton_salir = font_inicio.render("Salir", True, (255, 255, 255))

            self.screen.blit(texto_boton_jugar, (boton_jugar.x + 60, boton_jugar.y + 10))
            self.screen.blit(texto_boton_salir, (boton_salir.x + 60, boton_salir.y + 10))

            pygame.display.flip()
            self.clock.tick(60)
    def pantalla_gano(self):
        font_inicio = pygame.font.Font("assets/fonts/Silver.ttf", 30)
        boton_desplazarJugador = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGTH / 2 - 50, 300, 50)
        boton_salir = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGTH / 2 + 50, 300, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_desplazarJugador.collidepoint(event.pos):
                        self.meDesplazo = True
                        return   # Sale del menú y me desplazo
                    if boton_salir.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            
            self.screen.fill(YELLOW)

            pygame.draw.rect(self.screen, MORADO, boton_desplazarJugador)
            pygame.draw.rect(self.screen, ROJO, boton_salir)

            texto_boton_jugar = font_inicio.render("Desplazar Jugador", True, (0, 0, 0))
            texto_boton_salir = font_inicio.render("Salir", True, (255, 255, 255))

            self.screen.blit(texto_boton_jugar, (boton_desplazarJugador.x + 60, boton_desplazarJugador.y + 10))
            self.screen.blit(texto_boton_salir, (boton_salir.x + 60, boton_salir.y + 10))

            pygame.display.flip()
            self.clock.tick(60)

    def draw(self):
        """Dibujar en la pantalla"""
        "llenar la pantalla con color negro"
        self.screen.fill(BLACK)

        #Dibujar paredes
        for wall in self.walls:
            wall.draw(self.screen)
            
        #dibujar el gato
        self.gato.draw(self.screen)

        self.queso.draw(self.screen)

        #Dibujar el jugador
        self.player.draw(self.screen)
       #actualizar pantalla
        pygame.display.flip()
    def run(self):
        self.pantalla_inicio()  # Mostrar pantalla de inicio antes del juego
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
