import pygame, sys
import Levels.Level1F as Level1F

pygame.init()

# Colores y fuentes
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
dark_gray = (50, 50, 50)
light_gray = (200, 200, 200)
green = (0, 200, 0)
blue = (0, 0, 200)
rosa = (255, 0, 127)

# Tamaños
size = (900, 700)
sizetitulo = (750, 350)
screen = pygame.display.set_mode(size)
font = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 50)
pygame.display.set_caption("Think Fast!")

# Fuentes
font_large = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 15)
font_medium = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 15)
font_small = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 15)

# Carga de recursos del menú
titulo = pygame.image.load("Materials/Pictures/Assets/titulo.png").convert_alpha()
titulob = pygame.transform.scale(titulo, sizetitulo)
background = pygame.image.load("Materials/Pictures/Assets/background.png").convert()
imageb = pygame.transform.scale(background, size)
clock = pygame.time.Clock()

# Música
pygame.mixer.music.load('Materials/Music/Menu.wav')
pygame.mixer.music.play(-1)

# Estados del juego
MENU = 0
SELECT_DIFFICULTY = 1
SELECT_CHARACTER = 2
SELECT_LEVEL = 3
GAME_LEVEL_1 = 4

game_state = MENU
state_history = [MENU]
is_advanced = False
selected_character = "boy"
level_instance = None  # Variable para la instancia del nivel activo

# Funciones de botones
def create_menu_buttons():
    play_text = font_medium.render("PLAY", True, black)
    play_button_rect = pygame.Rect(0, 0, 200, 60)
    play_button_rect.center = (size[0] // 2, size[1] // 2)

    quit_text = font_medium.render("QUIT", True, black)
    quit_button_rect = pygame.Rect(0, 0, 200, 60)
    quit_button_rect.center = (size[0] // 2, size[1] // 2 + 80)
    return play_text, play_button_rect, quit_text, quit_button_rect

def create_difficulty_buttons():
    difficulty_text = font_large.render("Selecciona la dificultad", True, white)
    difficulty_text_rect = difficulty_text.get_rect(center=(size[0] // 2, size[1] // 2 - 150))
    
    beginner_text = font_medium.render("Principiante", True, white)
    beginner_button_rect = pygame.Rect(0, 0, 300, 60)
    beginner_button_rect.center = (size[0] // 2, size[1] // 2)

    advanced_text = font_medium.render("Avanzado", True, white)
    advanced_button_rect = pygame.Rect(0, 0, 300, 60)
    advanced_button_rect.center = (size[0] // 2, size[1] // 2 + 80)
    return difficulty_text, difficulty_text_rect, beginner_text, beginner_button_rect, advanced_text, advanced_button_rect

def create_character_buttons():
    select_text = font_large.render("Selecciona tu personaje", True, white)
    select_text_rect = select_text.get_rect(center=(size[0] // 2, size[1] // 2 - 150))
    
    char1_text = font_medium.render("Niño", True, white)
    char1_button_rect = pygame.Rect(0, 0, 250, 60)
    char1_button_rect.center = (size[0] // 2 - 150, size[1] // 2)

    char2_text = font_medium.render("Niña", True, white)
    char2_button_rect = pygame.Rect(0, 0, 250, 60)
    char2_button_rect.center = (size[0] // 2 + 150, size[1] // 2)
    return select_text, select_text_rect, char1_text, char1_button_rect, char2_text, char2_button_rect

def create_level_buttons():
    level_text = font_large.render("Selecciona el nivel", True, white)
    level_text_rect = level_text.get_rect(center=(size[0] // 2, size[1] // 2 - 150))
    
    level1_text = font_medium.render("Nivel 1", True, white)
    level1_button_rect = pygame.Rect(0, 0, 250, 60)
    level1_button_rect.center = (size[0] // 2, size[1] // 2)

    level2_text = font_medium.render("Nivel 2", True, white)
    level2_button_rect = pygame.Rect(0, 0, 250, 60)
    level2_button_rect.center = (size[0] // 2, size[1] // 2 + 80)

    level3_text = font_medium.render("Nivel 3", True, white)
    level3_button_rect = pygame.Rect(0, 0, 250, 60)
    level3_button_rect.center = (size[0] // 2, size[1] // 2 + 160)
    return level_text, level_text_rect, level1_text, level1_button_rect, level2_text, level2_button_rect, level3_text, level3_button_rect

def draw_menu(titulob, play_text, play_button_rect, quit_text, quit_button_rect, imageb):
    screen.blit(imageb, [0, 0])
    screen.blit(titulob, [80, -50])
    pygame.draw.rect(screen, light_gray, play_button_rect, border_radius=10)
    pygame.draw.rect(screen, dark_gray, play_button_rect, 4, border_radius=10)
    screen.blit(play_text, play_text.get_rect(center=play_button_rect.center))
    pygame.draw.rect(screen, light_gray, quit_button_rect, border_radius=10)
    pygame.draw.rect(screen, dark_gray, quit_button_rect, 4, border_radius=10)
    screen.blit(quit_text, quit_text.get_rect(center=quit_button_rect.center))

def draw_difficulty_selection(difficulty_text, difficulty_text_rect, beginner_text, beginner_button_rect, advanced_text, advanced_button_rect, back_text, back_button_rect, imageb):
    screen.blit(imageb, [0, 0])
    screen.blit(difficulty_text, difficulty_text_rect)
    pygame.draw.rect(screen, blue, beginner_button_rect, border_radius=10)
    screen.blit(beginner_text, beginner_text.get_rect(center=beginner_button_rect.center))
    pygame.draw.rect(screen, rosa, advanced_button_rect, border_radius=10)
    screen.blit(advanced_text, advanced_text.get_rect(center=advanced_button_rect.center))
    pygame.draw.rect(screen, dark_gray, back_button_rect, border_radius=10)
    screen.blit(back_text, back_text.get_rect(center=back_button_rect.center))

def draw_character_selection(select_text, select_text_rect, char1_text, char1_button_rect, char2_text, char2_button_rect, back_text, back_button_rect, imageb):
    screen.blit(imageb, [0, 0])
    screen.blit(select_text, select_text_rect)
    pygame.draw.rect(screen, blue, char1_button_rect, border_radius=10)
    screen.blit(char1_text, char1_text.get_rect(center=char1_button_rect.center))
    pygame.draw.rect(screen, rosa, char2_button_rect, border_radius=10)
    screen.blit(char2_text, char2_text.get_rect(center=char2_button_rect.center))
    pygame.draw.rect(screen, dark_gray, back_button_rect, border_radius=10)
    screen.blit(back_text, back_text.get_rect(center=back_button_rect.center))

def draw_level_selection(level_text, level_text_rect, level1_button_rect, level2_button_rect, level3_button_rect, back_text, back_button_rect, imageb, is_advanced):
    screen.blit(imageb, [0, 0])
    screen.blit(level_text, level_text_rect)
    
    level1_display_text = font_medium.render(f"Nivel 1 ({'Avanzado' if is_advanced else 'Principiante'})", True, white)
    level2_display_text = font_medium.render(f"Nivel 2 ({'Avanzado' if is_advanced else 'Principiante'})", True, white)
    level3_display_text = font_medium.render(f"Nivel 3 ({'Avanzado' if is_advanced else 'Principiante'})", True, white)
    
    pygame.draw.rect(screen, green, level1_button_rect, border_radius=10)
    screen.blit(level1_display_text, level1_display_text.get_rect(center=level1_button_rect.center))
    pygame.draw.rect(screen, green, level2_button_rect, border_radius=10)
    screen.blit(level2_display_text, level2_display_text.get_rect(center=level2_button_rect.center))
    pygame.draw.rect(screen, green, level3_button_rect, border_radius=10)
    screen.blit(level3_display_text, level3_display_text.get_rect(center=level3_button_rect.center))
    pygame.draw.rect(screen, dark_gray, back_button_rect, border_radius=10)
    screen.blit(back_text, back_text.get_rect(center=back_button_rect.center))

# Creación de elementos del menú
play_text, play_button_rect, quit_text, quit_button_rect = create_menu_buttons()
difficulty_text, difficulty_text_rect, beginner_text, beginner_button_rect, advanced_text, advanced_button_rect = create_difficulty_buttons()
select_text, select_text_rect, char1_text, char1_button_rect, char2_text, char2_button_rect = create_character_buttons()
level_text, level_text_rect, level1_text, level1_button_rect, level2_text, level2_button_rect, level3_text, level3_button_rect = create_level_buttons()
back_text = font_small.render("Regresar", True, white)
back_button_rect = pygame.Rect(50, 600, 150, 50)

# Bucle principal del juego
running = True
while running:
    # Manejo de eventos del juego y el menú
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == GAME_LEVEL_1 and level_instance:
            returned_state = level_instance.handle_events(event)
            if returned_state == "menu":
                game_state = MENU
                level_instance = None
                pygame.mixer.music.load('Materials/Music/Menu.wav')
                pygame.mixer.music.play(-1)
            elif returned_state == "restart":
                # La lógica de reinicio ya está en el __init__ de Level1F
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if back_button_rect.collidepoint(event.pos) and game_state != MENU:
                    if len(state_history) > 1:
                        state_history.pop()
                        game_state = state_history[-1]
                elif game_state == MENU:
                    if play_button_rect.collidepoint(event.pos):
                        game_state = SELECT_DIFFICULTY
                        state_history.append(game_state)
                    if quit_button_rect.collidepoint(event.pos):
                        running = False
                elif game_state == SELECT_DIFFICULTY:
                    if beginner_button_rect.collidepoint(event.pos):
                        is_advanced = False
                        game_state = SELECT_CHARACTER
                        state_history.append(game_state)
                    if advanced_button_rect.collidepoint(event.pos):
                        is_advanced = True
                        game_state = SELECT_CHARACTER
                        state_history.append(game_state)
                elif game_state == SELECT_CHARACTER:
                    if char1_button_rect.collidepoint(event.pos):
                        selected_character = "boy"
                        game_state = SELECT_LEVEL
                        state_history.append(game_state)
                    if char2_button_rect.collidepoint(event.pos):
                        selected_character = "girl"
                        game_state = SELECT_LEVEL
                        state_history.append(game_state)
                elif game_state == SELECT_LEVEL:
                    if level1_button_rect.collidepoint(event.pos):
                        game_state = GAME_LEVEL_1
                        level_instance = Level1F.Level1(screen, size, font, selected_character)
    
    # Lógica de actualización y dibujo
    if game_state == MENU:
        draw_menu(titulob, play_text, play_button_rect, quit_text, quit_button_rect, imageb)
    elif game_state == SELECT_DIFFICULTY:
        draw_difficulty_selection(difficulty_text, difficulty_text_rect, beginner_text, beginner_button_rect, advanced_text, advanced_button_rect, back_text, back_button_rect, imageb)
    elif game_state == SELECT_CHARACTER:
        draw_character_selection(select_text, select_text_rect, char1_text, char1_button_rect, char2_text, char2_button_rect, back_text, back_button_rect, imageb)
    elif game_state == SELECT_LEVEL:
        draw_level_selection(level_text, level_text_rect, level1_button_rect, level2_button_rect, level3_button_rect, back_text, back_button_rect, imageb, is_advanced)
    elif game_state == GAME_LEVEL_1 and level_instance:
        level_state = level_instance.update()
        if level_state == "quit":
            running = False
        elif level_state == "menu":
            game_state = MENU
            level_instance = None
            pygame.mixer.music.load('Materials/Music/Menu.wav')
            pygame.mixer.music.play(-1)
        else:
            level_instance.draw()

    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
sys.exit()