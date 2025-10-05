import pygame, sys
import Levels.Level1F as Level1F

pygame.init()

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
orange = (252, 138, 38)

# Tamaños
size = (900, 700)
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("Materials/Fonts/PressStart2P-Regular.ttf", 32)
pygame.display.set_caption("Think Fast!")

# Fuentes
font_large = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 38)
font_medium = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 38)
font_small = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 38)

# -------------------- IMÁGENES --------------------
menu_background = pygame.image.load("Materials/Pictures/Assets/fondo.png").convert()
menu_background = pygame.transform.scale(menu_background, size)

imageb = pygame.image.load("Materials/Pictures/Assets/fondo_sin.png").convert()
imageb = pygame.transform.scale(imageb, size)

config_background = pygame.image.load("Materials/Pictures/Assets/fondo_sin.png").convert()
config_background = pygame.transform.scale(config_background, size)

# -------------------- BOTONES --------------------
play_button_img = pygame.image.load("Materials/Pictures/Assets/btn_play.png").convert_alpha()
quit_button_img = pygame.image.load("Materials/Pictures/Assets/btn_quit.png").convert_alpha()
beginner_button_img = pygame.image.load("Materials/Pictures/Assets/btn_play.png").convert_alpha()
advanced_button_img = pygame.image.load("Materials/Pictures/Assets/btn_play.png").convert_alpha()
char1_button_img = pygame.image.load("Materials/Pictures/Assets/btn_boy.png").convert_alpha()
char2_button_img = pygame.image.load("Materials/Pictures/Assets/btn_girl.png").convert_alpha()
level1_button_img = pygame.image.load("Materials/Pictures/Assets/btn_principiante_1.png").convert_alpha()
level2_button_img = pygame.image.load("Materials/Pictures/Assets/btn_principiante_2.png").convert_alpha()
level3_button_img = pygame.image.load("Materials/Pictures/Assets/btn_principiante_3.png").convert_alpha()
back_button_img = pygame.image.load("Materials/Pictures/Assets/btn_regresar.png").convert_alpha()
config_button_img = pygame.image.load("Materials/Pictures/Assets/btn_confi.png").convert_alpha()
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
CONFIG_MENU = 5

game_state = MENU
state_history = [MENU]
is_advanced = False
selected_character = "boy"
level_instance = None

# --- VARIABLES GLOBALES PARA EL MENSAJE DE PRÓXIMAMENTE ---
show_coming_soon = False
coming_soon_timer = 0
COMING_SOON_DURATION = 2000 # Duración en milisegundos (2 segundos)

# -------------------- FUNCIONES DE DIBUJO Y AYUDA --------------------
def render_text_with_outline(text, font, text_color, outline_color, offset=3):
    outline_surface = font.render(text, True, outline_color)
    text_surface = font.render(text, True, text_color)

    blit_list = []
    
    blit_list.append((outline_surface, (-offset, 0)))
    blit_list.append((outline_surface, (offset, 0)))
    blit_list.append((outline_surface, (0, -offset)))
    blit_list.append((outline_surface, (0, offset)))

    blit_list.append((outline_surface, (-offset, -offset)))
    blit_list.append((outline_surface, (offset, -offset)))
    blit_list.append((outline_surface, (-offset, offset)))
    blit_list.append((outline_surface, (offset, offset)))

    blit_list.append((text_surface, (0, 0)))

    width = text_surface.get_width() + 2 * offset
    height = text_surface.get_height() + 2 * offset
    
    final_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for surface, pos in blit_list:
        final_surface.blit(surface, (pos[0] + offset, pos[1] + offset))
        
    return final_surface

def draw_button(image, rect, text_surface=None):
    scaled_img = pygame.transform.scale(image, (rect.width, rect.height))
    screen.blit(scaled_img, rect)
    if text_surface:
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
# ---------------------------------------------------------------------

# Definimos COMING_SOON_TEXT aquí (después de definir la función render_text_with_outline)
COMING_SOON_TEXT = render_text_with_outline("¡Próximamente!", font_medium, red, white)

# Menú principal
def create_menu_buttons():
    play_text = font_medium.render("", True, black)
    play_button_rect = pygame.Rect(0, 0, 250, 80)
    play_button_rect.center = (screen.get_width() // 2 + 5, screen.get_height() // 2 - 20)
    play_button_rect = play_button_rect.inflate(-0, -0)

    quit_text = font_medium.render("", True, black)
    quit_button_rect = pygame.Rect(0, 0, 250, 80)
    quit_button_rect.center = (screen.get_width() // 2 + 5, screen.get_height() // 2 + 80)
    quit_button_rect = quit_button_rect.inflate(-0, -0)

    return play_text, play_button_rect, quit_text, quit_button_rect

def create_difficulty_buttons():
    difficulty_surface = render_text_with_outline("Selecciona la dificultad", font_large, black, orange)
    difficulty_text_rect = difficulty_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 180))

    beginner_text = None
    beginner_button_rect = pygame.Rect(0, 0, 250, 80)
    beginner_button_rect.center = (screen.get_width() // 2 + 5, screen.get_height() // 2 - 20)

    advanced_text = None
    advanced_button_rect = pygame.Rect(0, 0, 250, 80)
    advanced_button_rect.center = (screen.get_width() // 2 + 5, screen.get_height() // 2 + 80)

    return difficulty_surface, difficulty_text_rect, beginner_text, beginner_button_rect, advanced_text, advanced_button_rect

def create_character_buttons():
    select_surface = render_text_with_outline("Selecciona tu personaje", font_large, black, orange)
    select_text_rect = select_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 180))

    char1_text = None
    char1_button_rect = pygame.Rect(0, 0, 250, 80)
    char1_button_rect.center = (screen.get_width() // 2 - 140, screen.get_height() // 2 + 40)

    char2_text = None
    char2_button_rect = pygame.Rect(0, 0, 250, 80)
    char2_button_rect.center = (screen.get_width() // 2 + 150, screen.get_height() // 2 + 40)

    return select_surface, select_text_rect, char1_text, char1_button_rect, char2_text, char2_button_rect

def create_level_buttons():
    level_surface = render_text_with_outline("Selecciona el nivel", font_large, black, orange)
    level_text_rect = level_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 180))

    level1_text = None
    level1_button_rect = pygame.Rect(0, 0, 250, 80)
    level1_button_rect.center = (screen.get_width() // 2 + 5, screen.get_height() // 2 -20)

    level2_text = None
    level2_button_rect = pygame.Rect(0, 0, 250, 80)
    level2_button_rect.center = (screen.get_width() // 2 + 5, screen.get_height() // 2 + 80)

    level3_text = None
    level3_button_rect = pygame.Rect(0, 0, 250, 80)
    level3_button_rect.center = (screen.get_width() // 2 + 5, screen.get_height() // 2 + 180)

    return level_surface, level_text_rect, level1_text, level1_button_rect, level2_text, level2_button_rect, level3_text, level3_button_rect

# -------------------- PANTALLAS --------------------
def draw_menu(play_text, play_button_rect, quit_text, quit_button_rect, config_button_rect):
    screen.blit(menu_background, [0, 0])
    draw_button(play_button_img, play_button_rect, play_text)
    draw_button(quit_button_img, quit_button_rect, quit_text)

    scaled_config_img = pygame.transform.scale(config_button_img, (config_button_rect.width, config_button_rect.height))
    screen.blit(scaled_config_img, config_button_rect)
    config_button_rect = pygame.Rect(0, 0, 900, 100)
    config_button_rect.topright = (screen.get_width() - 30, 25)

def draw_difficulty_selection(difficulty_text_surface, difficulty_text_rect, beginner_text, beginner_button_rect, advanced_text, advanced_button_rect, back_text, back_button_rect):
    global show_coming_soon, COMING_SOON_TEXT
    
    screen.blit(imageb, [0, 0])
    screen.blit(difficulty_text_surface, difficulty_text_rect)
    
    draw_button(beginner_button_img, beginner_button_rect, beginner_text)
    draw_button(advanced_button_img, advanced_button_rect, advanced_text)
    
    draw_button(back_button_img, back_button_rect, back_text)
    
    # Dibuja el mensaje de "Próximamente" si está activo
    if show_coming_soon:
        text_rect = COMING_SOON_TEXT.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(COMING_SOON_TEXT, text_rect)

def draw_character_selection(select_text_surface, select_text_rect, char1_text, char1_button_rect, char2_text, char2_button_rect, back_text, back_button_rect):
    screen.blit(imageb, [0, 0])
    screen.blit(select_text_surface, select_text_rect)
    draw_button(char1_button_img, char1_button_rect, char1_text)
    draw_button(char2_button_img, char2_button_rect, char2_text)
    draw_button(back_button_img, back_button_rect, back_text)

def draw_level_selection(level_text_surface, level_text_rect, level1_text, level1_button_rect, level2_text, level2_button_rect, level3_text, level3_button_rect, back_text, back_button_rect):
    global show_coming_soon, COMING_SOON_TEXT
    screen.blit(imageb, [0, 0])
    screen.blit(level_text_surface, level_text_rect)
    
    draw_button(level1_button_img, level1_button_rect, level1_text)
    draw_button(level2_button_img, level2_button_rect, level2_text)
    draw_button(level3_button_img, level3_button_rect, level3_text)
    
    draw_button(back_button_img, back_button_rect, back_text)
if show_coming_soon:
        text_rect = COMING_SOON_TEXT.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(COMING_SOON_TEXT, text_rect)

def draw_config_menu(back_text, back_button_rect):
    screen.blit(config_background, [0, 0])
    msg_surface = render_text_with_outline("Menú de Configuración", font_large, black, orange)
    screen.blit(msg_surface, msg_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100)))
    draw_button(back_button_img, back_button_rect, back_text)

# -------------------- CREACIÓN DE ELEMENTOS --------------------
play_text, play_button_rect, quit_text, quit_button_rect = create_menu_buttons()
difficulty_surface, difficulty_text_rect, beginner_text, beginner_button_rect, advanced_text, advanced_button_rect = create_difficulty_buttons()
select_surface, select_text_rect, char1_text, char1_button_rect, char2_text, char2_button_rect = create_character_buttons()
level_surface, level_text_rect, level1_text, level1_button_rect, level2_text, level2_button_rect, level3_text, level3_button_rect = create_level_buttons()
back_text = font_small.render("", True, white)
back_button_rect = pygame.Rect(60, 550, 200, 80)

config_button_rect = pygame.Rect(60, 550, 200, 80)

# -------------------- BUCLE PRINCIPAL --------------------
running = True
while running:
    # Manejo del temporizador de "Próximamente"
    if show_coming_soon:
        if pygame.time.get_ticks() > coming_soon_timer + COMING_SOON_DURATION:
            show_coming_soon = False
            
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
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if back_button_rect.collidepoint(event.pos) and game_state != MENU:
                    if len(state_history) > 1:
                        state_history.pop()
                        game_state = state_history[-1]
                        show_coming_soon = False
                elif game_state == MENU:
                    if play_button_rect.collidepoint(event.pos):
                        game_state = SELECT_DIFFICULTY
                        state_history.append(game_state)
                    if quit_button_rect.collidepoint(event.pos):
                        running = False
                    if config_button_rect.collidepoint(event.pos):
                        game_state = CONFIG_MENU
                        state_history.append(game_state)
                elif game_state == SELECT_DIFFICULTY:
                    if beginner_button_rect.collidepoint(event.pos):
                        is_advanced = False
                        game_state = SELECT_CHARACTER
                        state_history.append(game_state)
                        show_coming_soon = False
                    if advanced_button_rect.collidepoint(event.pos):
                        # Lógica de "Próximamente" para el botón avanzado (segundo botón)
                        if not show_coming_soon:
                            show_coming_soon = True
                            coming_soon_timer = pygame.time.get_ticks()
                        # El estado no cambia, se queda en SELECT_DIFFICULTY
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
                    if level2_button_rect.collidepoint(event.pos):
                        # Lógica de "Próximamente" para el botón avanzado (segundo botón)
                        if not show_coming_soon:
                            show_coming_soon = True
                            coming_soon_timer = pygame.time.get_ticks()

    # -------------------- DIBUJAR PANTALLAS --------------------
    if game_state == MENU:
        draw_menu(play_text, play_button_rect, quit_text, quit_button_rect, config_button_rect)
    elif game_state == SELECT_DIFFICULTY:
        draw_difficulty_selection(difficulty_surface, difficulty_text_rect, beginner_text, beginner_button_rect, advanced_text, advanced_button_rect, back_text, back_button_rect)
    elif game_state == SELECT_CHARACTER:
        draw_character_selection(select_surface, select_text_rect, char1_text, char1_button_rect, char2_text, char2_button_rect, back_text, back_button_rect)
    elif game_state == SELECT_LEVEL:
        draw_level_selection(level_surface, level_text_rect, level1_text, level1_button_rect, level2_text, level2_button_rect, level3_text, level3_button_rect, back_text, back_button_rect)
    elif game_state == CONFIG_MENU:
        draw_config_menu(back_text, back_button_rect)
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