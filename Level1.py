import pygame, sys
from Personajes.boy import Characterb
from Personajes.Guardian import Characternpc
from Interacciones.dialogo import DialogBox
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Interfazpreguntas import InventoryWindow
from Interacciones.Controldeobjetos.timer import Timer 
from Interacciones.Controldeobjetos.corazones import LifeManager


pygame.init()
size = (900, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Think Fast!")
clock = pygame.time.Clock()

# ------------------- VARIABLES -------------------
font = pygame.font.SysFont(None, 32)
player = Characterb(450, 570, 0.4)
Guardia = Characternpc(300, 260, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')
background_image = pygame.image.load('Materials/Pictures/Assets/Fund_level1.jpg')
timer = Timer(120) 
life_manager = LifeManager(3, 'Materials/Pictures/Assets/corazones.png')

pygame.mixer.music.load('Materials/Music/prinsipal.wav')
pygame.mixer.music.play(-1)

speed = 4
state = "game"  # Puede ser "game", "dialog", "inventory"
dialogo_text = "¡Alto! Tienes que responder estas preguntas!!."
typewriter = None
dialogo_active = False
player_can_move = True
inventory_window = None  # Inicializa como None

# ------------------- PREGUNTAS -------------------
questions = [ 
        {
            "image": "Materials/Pictures/imagen1.jpg",
            "question": "¿Cómo se llama nuestro país?",
            "choices": ["España", "México", "Roma", "Berlín"],
            "correct_answer": 1
        },
        {
            "image": "Materials/Pictures/imagen2.jpg",
            "question": "Si tienes 5 manzanas y te comes 2, ¿cuántas manzanas te quedan?",
            "choices": ["5", "4", "3", "10"],
            "correct_answer": 1
        },
        {
            "image": "Materials/Pictures/imagen3.jpg",
            "question": "¿En qué estación del año las hojas de los árboles cambian de color y caen?",
            "choices": ["primavera", "verano", "otoño", "invierno"],
            "correct_answer": 2
        },
        {
            "image": "Materials/Pictures/imagen4.jpg",
            "question": "que se celebra el 1 de noviembre?",
            "choices": ["DIA DE MUERTOS", "NAVIDAD", "10 DE MAYO", "AÑO NUEVO"],
            "correct_answer": 0
        }
    ]


# ------------------- FUNCIONES -------------------
def Background(image):
    size_img = pygame.transform.scale(image, (900, 700))
    screen.blit(size_img, (0, 0))

# ------------------- BUCLE PRINCIPAL --------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Diálogo
        if event.type == pygame.KEYDOWN:
            if state == "dialog" and event.key == pygame.K_SPACE:
                if typewriter and typewriter.finished():
                    state = "inventory"
                    dialogo_active = False
                    typewriter = None
                    inventory_window = InventoryWindow(size, questions)

        # Evento para responder preguntas
        if state == "inventory" and inventory_window:
            inventory_window.handle_event(event)

    keys = pygame.key.get_pressed()

    # Movimiento del jugador
    if state == "game":
        player.move(keys, size[0], size[1], Guardia.rect)

        # Iniciar diálogo con espacio cerca del guardia
        if player.rect.colliderect(Guardia.rect.inflate(20, 20)) and keys[pygame.K_SPACE]:
            if not dialogo_active:
                state = "dialog"
                dialogo_active = True
                typewriter = TypewriterText(dialogo_text, font, (255, 255, 255), speed=25)

    # ------------------- DIBUJO -------------------
    Background(background_image)
    player.draw(screen)
    Guardia.draw(screen)
    timer.draw(screen, font)
    life_manager.draw(screen)



    # Mostrar diálogo
    if dialogo_active and typewriter:
        typewriter.update()
        box_rect = pygame.Rect(50, 550, 800, 100)
        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 3)
        typewriter.draw(screen, (box_rect.x + 20, box_rect.y + 30))

    # Mostrar preguntas
    if state == "inventory" and inventory_window:
        inventory_window.draw(screen)

        if timer.finished:
            print("Se acabo el tiempo")
            life_manager.lose_life()
            state = "game"

            if life_manager.is_dead():
                print("Game Over")
                pygame.quit()
                sys.exit()

    pygame.display.update()