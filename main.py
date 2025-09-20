import pygame, sys
from boy import Characterb

pygame.init()


size = (900, 700)

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Think Fast!!")

background_image = pygame.image.load('Materials/Pictures/Assets/Fund_level1.jpg')

def Background(image):
    size = pygame.transform.scale(image, (900, 700))
    screen.blit(size, (0, 0))

player = Characterb(450, 600, 'Materials/Pictures/Characters/Chico.png', 0.6) 

pygame.mixer.music.load('Materials/Music/prinsipal.wav')
pygame.mixer.music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    
    player.move(keys, size[0], size[1])
    
    Background(background_image)
    player.draw(screen)
    
    pygame.display.update()
    