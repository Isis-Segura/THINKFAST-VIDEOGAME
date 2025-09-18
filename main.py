import pygame, sys
from girl import Characterg

pygame.init()


size = (900, 700)

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Think Fast!!")

background_image = pygame.image.load('Pictures/Assets/Fund_level1.jpg')

def Background(image):
    size = pygame.transform.scale(image, (900, 700))
    screen.blit(size, (0, 0))

player = Characterg(450, 570, 'Pictures/Characters/chica.png', 5)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    keys = pygame.key.get_pressed()
    
    player.move(keys)
    
    Background(background_image)
    player.draw(screen)
    
    pygame.display.update()

