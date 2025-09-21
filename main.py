import pygame, sys
from boy import Characterb
from Guardian import Characternpc

pygame.init()
size = (900, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Think Fast!!")

background_image = pygame.image.load('Materials/Pictures/Assets/Fund_level1.jpg')
def Background(image):

    size = pygame.transform.scale(image, (900, 700))
    #Redimensiona la imagen al tamaño de la ventana

    screen.blit(size, (0, 0))

player = Characterb(450, 570, 0.4)
Guardia = Characternpc(300, 260, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')

pygame.mixer.music.load('Materials/Music/prinsipal.wav')

pygame.mixer.music.play(-1)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()

    # Pasa el rectángulo del guardia a la función move del jugador
    player.move(keys, size[0], size[1], Guardia.rect)
    
    if Guardia.is_interacting(player.rect, keys):
        print("¡El jugador está interactuando con el NPC!")
    Background(background_image)

    player.draw(screen)
    Guardia.draw(screen)
    
    pygame.display.update()
