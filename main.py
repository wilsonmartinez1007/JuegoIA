import pygame
import sys
from config import*
from game import Game
#acordarme cambiar interptrete con crt+ship+p y colocar el global para el proyecto


def main():
    try:
        #inicializar pygame
        pygame.init()

        #crear y correr juego
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
