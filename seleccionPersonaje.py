import pygame, sys
pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

#Tamaños
size = (900, 700)

#Ejecucion de la ventana
screen = pygame.display.set_mode(size)

#Llamado del fondo y titulo del juego
background = pygame.image.load("background.png").convert()
imageb = pygame.transform.scale(background, (size))
clock = pygame.time.Clock()


pygame.mouse.set_visible(1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            

    screen.blit(imageb, [0, 0])

    pygame.display.flip()
    clock.tick(60)