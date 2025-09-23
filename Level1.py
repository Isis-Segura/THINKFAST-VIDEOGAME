import pygame, sys
from Personajes.boy import Characterb
from Personajes.Guardian import Characternpc
from Interacciones.dialogo import DialogBox
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Interfazpreguntas import InventoryWindow
from Interacciones.Controldeobjetos.timer import Timer 
from Interacciones.Controldeobjetos.corazones import LifeManager

# Importan de los distintos archivos la información

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
timer = Timer(120) 
life_manager = LifeManager(3, 'Materials/Pictures/Assets/corazones.png')

# Carga la música principal del juego al inicio
pygame.mixer.music.load('Materials/Music/Level1.wav')
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
                    timer.start()
            
            elif state == "inventory" and (event.key == pygame.K_ESCAPE or event.key == pygame.K_r):
                # Cerrar inventario
                state = "game"

            if event.key == pygame.K_l:  # Presiona "L" para perder una vida
                life_manager.lose_life()
                if life_manager.is_dead():
                    pygame.mixer.music.stop() # Detiene la música principal
                    state = "game_over" # Cambia el estado del juego
            
            if state == "game_over":
                if event.key == pygame.K_r:
                    # Reiniciar
                    player = Characterb(450, 570, 0.4)
                    Guardia = Characternpc(300, 260, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')
                    timer = Timer(120)
                    life_manager = LifeManager(3, 'Materials/Pictures/Assets/corazones.png')
                    dialogo_active = False
                    typewriter = None
                    state = "game"
                    
                    # Vuelve a cargar y reproducir la música de fondo del juego
                    pygame.mixer.music.load('Materials/Music/Level1.wav')
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # Lógica para cambiar la música a 'Game Over'
    if state == "game_over" and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('Materials/Music/GameOver.wav')
        pygame.mixer.music.play(-1)
            
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
    # Dibuja la pantalla según el estado del juego
    if state == "game" or state == "dialog" or state == "inventory":
        Background(background_image)
        player.draw(screen)
        Guardia.draw(screen)
        timer.draw(screen, font)
        life_manager.draw(screen)

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
            
        if timer.finished:
            life_manager.lose_life()
            timer.reset()
            if life_manager.is_dead():
                pygame.mixer.music.stop() # Detiene la música principal
                state = "game_over"
            else:
                state = "game"

    elif state == "game_over":
        screen.fill((0, 0, 0))  # Fondo negro
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        retry_text = font.render("Presiona R para reiniciar o ESC para salir", True, (255, 255, 255))

        screen.blit(game_over_text, game_over_text.get_rect(center=(size[0] // 2, size[1] // 2 - 40)))
        screen.blit(retry_text, retry_text.get_rect(center=(size[0] // 2, size[1] // 2 + 20)))

    pygame.display.update()