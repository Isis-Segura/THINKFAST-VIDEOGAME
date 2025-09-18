import pygame, sys
pygame.init()

#Tamano de la pantalla
size = (900, 700)
#crear ventana
screen = pygame.display.set_mode(size)
#titulo
pygame.display.set_caption("Think Fast!!")
#fondo del nivel 1
image = pygame.image.load('Pictures/Assets/Fund_level1.jpg')
def Background(image):
    size = pygame.transform.scale(image, (900, 700))
    screen.blit(size, (0, 0))

screen.fill((0, 255, 0))

Background(image)

#bucle de ejecucion
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()




