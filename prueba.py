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
"""
coordenada del personaje
coord_x = 10
coord_y = 10
velocidad
x_speed = 0
y_speed = 0
"""
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_speed = -3
            if event.key == pygame.K_RIGHT:
                x_speed = 3
            if event.key == pygame.K_UP:
                y_speed = -3
            if event.key == pygame.K_DOWN:
                y_speed = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_speed = 0
            if event.key == pygame.K_RIGHT:
                x_speed = 0
            if event.key == pygame.K_UP:
                y_speed = 0
            if event.key == pygame.K_DOWN:
                y_speed = 0
        """

    screen.blit(imageb, [0, 0])
    screen.blit(titulob, [80, -50])
    """
    coord_x += x_speed
    coord_y += y_speed
    pygame.draw.rect(screen, red, (coord_x, coord_y, 100,100))
    """
    pygame.display.flip()
    clock.tick(60)

