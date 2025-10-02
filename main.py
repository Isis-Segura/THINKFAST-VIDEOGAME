import pygame, sys
from settings import *
from menu import run_menu

pygame.init()

def main():
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Think Fast!")
    run_menu(screen)  # Arranca el menú principal

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
