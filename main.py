import pygame, sys
from boy import Characterb
from Guardian import Characternpc
from dialogo import DialogBox
from velotex import TypewriterText
from Interfazpreguntas import InventoryWindow
# Importan de las distintos archivos la información
#Hola
pygame.init()
size = (900, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Think Fast!!")
clock = pygame.time.Clock()

# ------------------- VARIABLES -------------------
font = pygame.font.SysFont(None, 32)
player = Characterb(450, 570, 0.4)
Guardia = Characternpc(300, 260, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')
background_image = pygame.image.load('Materials/Pictures/Assets/Fund_level1.jpg')

pygame.mixer.music.load('Materials/Music/prinsipal.wav')
pygame.mixer.music.play(-1)

speed = 4
state = "game"  # Estado del juego: "game" para el juego normal, "dialog" para el diálogo, o "inventory" para el inventario
dialogo_text = "¡Alto! Tienes que responder estas preguntas!!."
typewriter = None
dialogo_active = False
player_can_move = True

inventory_window = InventoryWindow(size)
# Crea una instancia de la ventana de inventario

# ------------------- FUNCIONES -------------------
def Background(image):
    size_img = pygame.transform.scale(image, (900, 700))
    screen.blit(size_img, (0, 0))
 
# ------------------- BUCLE PRINCIPAL -------------------
while True:
    #------------------- EVENTOS -------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Control del diálogo
        if event.type == pygame.KEYDOWN:
            if state == "dialog" and event.key == pygame.K_SPACE:
                if typewriter.finished():
                    # Cerrar el diálogo
                    state = "inventory"
                    dialogo_active = False
                    typewriter = None
            
            elif state == "inventory" and (event.key == pygame.K_ESCAPE or event.key == pygame.KSCAN_DELETE):
                # Cerrar inventario
                state = "game"
                
    keys = pygame.key.get_pressed()

    #------------------- MOVIMIENTO -------------------
    if state == "game":
        player.move(keys, size[0], size[1], Guardia.rect)
        
        # Activa el diálogo si el jugador está lo suficientemente cerca del guardia y presiona ESPACIO
        if player.rect.colliderect(Guardia.rect.inflate(20,20)) and keys[pygame.K_SPACE]:
            if not dialogo_active:
                state = "dialog"
                dialogo_active = True
                typewriter = TypewriterText(dialogo_text, font, (255,255,255), speed=25)

    # ------------------- DIBUJO -------------------
    Background(background_image)
    player.draw(screen)
    Guardia.draw(screen)

    # Dibuja diálogo con efecto máquina de escribir
    if dialogo_active and typewriter:
        typewriter.update()
        box_rect = pygame.Rect(50, 550, 800, 100)
        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 3)
        typewriter.draw(screen, (box_rect.x + 20, box_rect.y + 30))
    
    # Dibuja el inventario
    if state == "inventory":
        inventory_window.draw(screen)

    pygame.display.update()
