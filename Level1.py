import pygame, sys
from Personajes.boy import Characterb
from Personajes.Guardian import Characternpc
from Interacciones.dialogo import DialogBox
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Interfazpreguntas import InventoryWindow
from Interacciones.Controldeobjetos.timer import Timer 
from Interacciones.Controldeobjetos.corazones import LifeManager

# Importa de los distintos archivos la información

pygame.init()
size = (900, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Think Fast!")
clock = pygame.time.Clock()

# ------------------- VARIABLES Y RECURSOS -------------------
font = pygame.font.SysFont(None, 32)
player = Characterb(450, 570, 0.4)
Guardia = Characternpc(455, 260, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')
background_image = pygame.image.load('Materials/Pictures/Assets/Fund_level1.jpg')
timer = Timer(120) 
life_manager = LifeManager(3, 'Materials/Pictures/Assets/corazones.png')

# Carga la música principal del juego al inicio
pygame.mixer.music.load('Materials/Music/Level1.wav')
pygame.mixer.music.play(-1)

speed = 4
state = "game"  # Puede ser "game", "dialog", "inventory", "game_over", "quiz_complete_dialog"
dialogo_text = "¡Alto! Tienes que responder estas preguntas!!."
typewriter = None
dialogo_active = False
inventory_window = None

# Nuevas variables para el diálogo post-quiz
post_quiz_dialogs = []
current_dialog_index = 0

# --- NUEVA VARIABLE DE CONTROL ---
guard_interacted = False

# ------------------- PREGUNTAS -------------------
questions = [
    {
        "image": "Materials/Pictures/Assets/imagen1.jpg",
        "question": "¿Cómo se llama nuestro país?",
        "choices": ["España", "México", "Roma", "Berlín"],
        "correct_answer": 1
    },
    {
        "image": "Materials/Pictures/Assets/imagen1.jpg",
        "question": "¿Cuánto es 2 + 2?",
        "choices": ["3", "4", "5", "6"],
        "correct_answer": 1
    },
    {
        "image": "Materials/Pictures/Assets/imagen1.jpg",
        "question": "¿Cuál es el animal más grande del mundo?",
        "choices": ["Ballena azul", "Elefante", "Tiburón blanco", "Jirafa"],
        "correct_answer": 0
    },
    {
        "image": "Materials/Pictures/Assets/imagen1.jpg",
        "question": "¿Cuál es el océano más grande?",
        "choices": ["Atlántico", "Índico", "Pacífico", "Ártico"],
        "correct_answer": 2
    }
]

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

        # Diálogo y manejo de preguntas
        if event.type == pygame.KEYDOWN:
            # Diálogo inicial del guardia
            if state == "dialog" and event.key == pygame.K_SPACE:
                if typewriter and typewriter.finished():
                    state = "inventory"
                    dialogo_active = False
                    typewriter = None
                    timer.start()
                    inventory_window = InventoryWindow(size, questions)
            
            # Diálogo post-quiz
            elif state == "quiz_complete_dialog" and event.key == pygame.K_SPACE:
                if typewriter and typewriter.finished():
                    current_dialog_index += 1
                    if current_dialog_index < len(post_quiz_dialogs):
                        dialogo_active = True
                        typewriter = TypewriterText(post_quiz_dialogs[current_dialog_index], font, (255,255,255), speed=25)
                    else:
                        state = "game"
                        dialogo_active = False
                        typewriter = None
                        
                        # Mueve al guardia un poco a la izquierda
                        Guardia.rect.x -= 98
                        
                        player.rect.x = 450
                        player.rect.y = 570
                        
            # Manejar el escape/reinicio durante el quiz
            elif state == "inventory" and (event.key == pygame.K_ESCAPE or event.key == pygame.K_r):
                state = "game"
                inventory_window = InventoryWindow(size, questions)

            if event.key == pygame.K_l:
                life_manager.lose_life()
                if life_manager.is_dead():
                    pygame.mixer.music.stop() 
                    state = "game_over" 
            
            if state == "game_over":
                if event.key == pygame.K_r:
                    player = Characterb(450, 570, 0.4)
                    Guardia = Characternpc(300, 260, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')
                    timer = Timer(120)
                    life_manager = LifeManager(3, 'Materials/Pictures/Assets/corazones.png')
                    dialogo_active = False
                    typewriter = None
                    inventory_window = None
                    state = "game"
                    # --- REINICIA LA VARIABLE DE CONTROL ---
                    guard_interacted = False
                    pygame.mixer.music.load('Materials/Music/Level1.wav')
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Manejar eventos de la ventana de inventario
        if state == "inventory" and inventory_window:
            inventory_window.handle_event(event)

    # Lógica para cambiar la música a 'Game Over'
    if state == "game_over" and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('Materials/Music/GameOver.wav')
        pygame.mixer.music.play(-1)
            
    keys = pygame.key.get_pressed()

    #------------------- MOVIMIENTO -------------------
    if state == "game":
        player.move(keys, size[0], size[1], Guardia.rect)
        if player.rect.colliderect(Guardia.rect.inflate(20,20)) and keys[pygame.K_SPACE]:
            # Solo inicia el quiz si no se ha completado Y no se ha interactuado antes
            if not dialogo_active and not guard_interacted:
                state = "dialog"
                dialogo_active = True
                typewriter = TypewriterText(dialogo_text, font, (255,255,255), speed=25)
                # --- MARCA LA INTERACCIÓN COMO HECHA ---
                guard_interacted = True
                # También puedes hacer que la interacción solo sea posible
                # si el jugador no ha interactuado, no importa si el diálogo ha terminado
                # if player.rect.colliderect(Guardia.rect.inflate(20,20)) and keys[pygame.K_SPACE] and not guard_interacted:
                #    ...
                # El código que tenías está bien para tu caso de uso, solo quería darte otra opción.


    # ------------------- DIBUJO -------------------
    if state == "game" or state == "dialog" or state == "quiz_complete_dialog":
        Background(background_image)
        player.draw(screen)
        Guardia.draw(screen)
        timer.draw(screen, font)
        life_manager.draw(screen)

        if dialogo_active and typewriter:
            typewriter.update()
            box_rect = pygame.Rect(50, 550, 800, 100)
            pygame.draw.rect(screen, (0, 0, 0), box_rect)
            pygame.draw.rect(screen, (255, 255, 255), box_rect, 3)
            typewriter.draw(screen, (box_rect.x + 20, box_rect.y + 30))

    elif state == "inventory":
        Background(background_image)
        player.draw(screen)
        Guardia.draw(screen)
        timer.draw(screen, font)
        life_manager.draw(screen)
        
        if not inventory_window.finished:
            inventory_window.draw(screen)
        else:
            # Aquí se activa la secuencia de diálogos
            print("Quiz terminado. ¡Volviendo al juego!")
            state = "quiz_complete_dialog"
            dialogo_active = True
            
            # Prepara la lista de diálogos
            score = inventory_window.correct_answers
            total = len(inventory_window.questions)
            post_quiz_dialogs = [
                f"Has respondido correctamente {score} de {total} preguntas.",
                "¡Muy bien hecho! Has demostrado tener una calidad de estudio bastante buena.",
                "Ahora puedes pasar. ¡Buena suerte en tu camino!"
            ]
            current_dialog_index = 0
            typewriter = TypewriterText(post_quiz_dialogs[current_dialog_index], font, (255,255,255), speed=25)
            inventory_window = None
            timer.reset()

    elif state == "game_over":
        screen.fill((0, 0, 0))
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        retry_text = font.render("Presiona R para reiniciar o ESC para salir", True, (255, 255, 255))
        screen.blit(game_over_text, game_over_text.get_rect(center=(size[0] // 2, size[1] // 2 - 40)))
        screen.blit(retry_text, retry_text.get_rect(center=(size[0] // 2, size[1] // 2 + 20)))

    pygame.display.update()