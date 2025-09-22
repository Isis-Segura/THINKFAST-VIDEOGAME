import pygame, sys
pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

#Tamaños
size = (900, 700)
sizetitulo = (750, 350)

#Ejecucion de la ventana
screen = pygame.display.set_mode(size)

#Llamado del fondo y titulo del juego
titulo = pygame.image.load("titulo.png").convert()
titulo.set_colorkey([0,0,0])
titulob = pygame.transform.scale(titulo, (sizetitulo))
background = pygame.image.load("background.png").convert()
imageb = pygame.transform.scale(background, (size))
clock = pygame.time.Clock()


pygame.mouse.set_visible(1)

    screen.blit(imageb, [0, 0])
    screen.blit(titulob, [80, -50])

    pygame.display.flip()
    clock.tick(60)

