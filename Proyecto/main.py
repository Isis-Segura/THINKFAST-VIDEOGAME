import pygame, sys
pygame.init()

#Tamano de la pantalla
size = (800, 600)
#crear ventana
screen = pygame.display.set_mode(size)
#titulo
pygame.display.set_caption("Video Game")


#bucle de ejecucion
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()




