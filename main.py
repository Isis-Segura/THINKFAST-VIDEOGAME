import pygame, sys
# Importa la librería de juegos Pygame y el módulo sys para salir del programa
from boy import Characterb


pygame.init()
# Inicializa todos los módulos de Pygame (necesario antes de usarlo)

size = (900, 700)
#Tamaño de la ventana (ancho=900 px, alto=700 px)

screen = pygame.display.set_mode(size)
#Crea la ventana de juego con ese tamaño

pygame.display.set_caption("Think Fast!!")
#Título que se muestra en la barra de la ventana

#Imagende fondo

background_image = pygame.image.load('Materials/Pictures/Assets/Fund_level1.jpg')
# Carga la imagen de fondo desde la carpeta indicada

# Dibuja la imagen de fondo escalada al tamaño de la ventana.
def Background(image):

    size = pygame.transform.scale(image, (900, 700))
    #Redimensiona la imagen al tamaño de la ventana

    screen.blit(size, (0, 0))
    #Dibuja (blit) la imagen en la esquina superior izquierda

player = Characterb(450, 570, 0.4)
# Crea una instancia del personaje

pygame.mixer.music.load('Materials/Music/prinsipal.wav')

pygame.mixer.music.play(-1)
# Importar musica

#Bucle principal del juego
while True:
    #Manejo de eventos (teclado, ratón, cerrar ventana, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Si se pulsa el botón de cerrar ventana
            sys.exit()                #Cierra el programa

    #Lectura del teclado
    keys = pygame.key.get_pressed()
    #Devuelve una lista con el estado de todas las teclas

    player.move(keys, size[0], size[1])
    #Mueve el personaje según las teclas presionadas (definido en Characterg)


    #Dibujar en la pantalla
    Background(background_image)
    # Dibuja el fondo

    player.draw(screen)
    #Dibuja al personaje sobre el fondo

    #Actualizar la ventana
    pygame.display.update()
    #Refresca la pantalla para mostrar los cambios