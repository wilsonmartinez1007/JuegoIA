import pygame
from sprites import*
from config import*
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
                    self.player = Player(col_index, row_index)

    def handle_events(self):
        for event in pygame.event.get():
            #Si el usuario cierrra ventana
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        """actualizar el estado del juego"""
        self.player.update(self.walls)

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
        #bucle principal del juego
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
