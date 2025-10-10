import pygame, sys
import Levels.Level1F as Level1F

pygame.init()

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
orange = (252, 138, 38)
light_blue = (173, 216, 230)
pink = (255, 182, 193)
green = (144, 238, 144)
purple = (147, 112, 219)

# Tamaños
size = (900, 700)
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("Materials/Fonts/PressStart2P-Regular.ttf", 32)
pygame.display.set_caption("Think Fast!")

# Fuentes
font_large = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 38)
font_medium = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 28)
font_small = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 20)
font_tiny = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 16)

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
beginner_button_img = pygame.image.load("Materials/Pictures/Assets/btn_libro_solo.png").convert_alpha()
advanced_button_img = pygame.image.load("Materials/Pictures/Assets/btn_montana_libros.png").convert_alpha()
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

# -------- CONFIGURACIÓN GLOBAL --------
language = "es"  # 'es' o 'en'
volume_level = 0.7  # Volumen por defecto 70%

texts = {
    "es": {
        # Menú principal
        "play": "Jugar",
        "quit": "Salir", 
        "config": "Configuración",
        "title_menu": "Think Fast!",
        
        # Configuración
        "volume": "Volumen",
        "language": "Idioma", 
        "back": "Regresar",
        "spanish": "Español",
        "english": "Inglés",
        "title_config": "Menú de Configuración",
        "sound_on": "Sonido: ON",
        "sound_off": "Sonido: OFF",
        
        # Selección de dificultad
        "select_difficulty": "Selecciona la dificultad",
        "beginner": "Principiante",
        "advanced": "Avanzado",
        
        # Selección de personaje
        "select_character": "Selecciona tu personaje",
        "boy": "Niño",
        "girl": "Niña",
        
        # Selección de nivel
        "select_level": "Selecciona el nivel",
        "level": "Nivel",
        
        # Mensajes
        "coming_soon": "¡Próximamente!"
    },
    "en": {
        # Main menu
        "play": "Play",
        "quit": "Quit",
        "config": "Settings", 
        "title_menu": "Think Fast!",
        
        # Settings
        "volume": "Volume",
        "language": "Language",
        "back": "Back",
        "spanish": "Spanish", 
        "english": "English",
        "title_config": "Settings Menu",
        "sound_on": "Sound: ON",
        "sound_off": "Sound: OFF",
        
        # Difficulty selection
        "select_difficulty": "Select difficulty",
        "beginner": "Beginner", 
        "advanced": "Advanced",
        
        # Character selection
        "select_character": "Select your character",
        "boy": "Boy",
        "girl": "Girl",
        
        # Level selection  
        "select_level": "Select level",
        "level": "Level",
        
        # Messages
        "coming_soon": "Coming soon!"
    }
}

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

def draw_button_with_text(image, rect, text, font, text_color=yellow, outline_color=black):
    """Dibuja un botón con imagen y texto con borde"""
    # Escalar y dibujar la imagen del botón
    scaled_img = pygame.transform.scale(image, (rect.width, rect.height))
    screen.blit(scaled_img, rect)
    
    # Renderizar texto con borde si se proporciona texto
    if text:
        text_surface = render_text_with_outline(text, font, text_color, outline_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
    
    return rect

def draw_colorful_button(rect, color, text, font, text_color=white, border_color=purple, border_width=4):
    # Dibujar borde
    pygame.draw.rect(screen, border_color, rect, border_width, border_radius=15)
    # Dibujar fondo
    pygame.draw.rect(screen, color, rect.inflate(-border_width*2, -border_width*2), border_radius=12)
    
    # Dibujar texto
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    
    return rect

def draw_volume_slider(x, y, width, height, volume, color):
    # Fondo del slider
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), border_radius=10)
    
    # Nivel de volumen
    fill_width = int(width * volume)
    pygame.draw.rect(screen, color, (x, y, fill_width, height), border_radius=10)
    
    # Borde
    pygame.draw.rect(screen, black, (x, y, width, height), 2, border_radius=10)
    
    # Indicador de volumen (círculo)
    thumb_x = x + fill_width
    thumb_y = y + height // 2
    pygame.draw.circle(screen, purple, (thumb_x, thumb_y), height + 5)
    pygame.draw.circle(screen, white, (thumb_x, thumb_y), height + 3)
    
    return pygame.Rect(x, y, width, height)

# Definimos COMING_SOON_TEXT aquí (después de definir la función render_text_with_outline)
COMING_SOON_TEXT = render_text_with_outline("¡Próximamente!", font_medium, red, white)

# -------------------- CREACIÓN DE BOTONES --------------------
def create_menu_buttons():
    play_button_rect = pygame.Rect(0, 0, 250, 80)
    play_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 50)
    
    quit_button_rect = pygame.Rect(0, 0, 250, 80)
    quit_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 50)
    
    config_button_rect = pygame.Rect(0, 0, 200, 80)
    config_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 150)
    
    return play_button_rect, quit_button_rect, config_button_rect

def create_difficulty_buttons():
    beginner_button_rect = pygame.Rect(0, 0, 250, 80)
    beginner_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 20)

    advanced_button_rect = pygame.Rect(0, 0, 250, 80)
    advanced_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 80)

    back_button_rect = pygame.Rect(0, 0, 200, 80)
    back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)

    return beginner_button_rect, advanced_button_rect, back_button_rect

def create_character_buttons():
    char1_button_rect = pygame.Rect(0, 0, 180, 250)
    char1_button_rect.center = (screen.get_width() // 2 - 150, screen.get_height() // 2 + 40)

    char2_button_rect = pygame.Rect(0, 0, 180, 250)
    char2_button_rect.center = (screen.get_width() // 2 + 150, screen.get_height() // 2 + 40)

    back_button_rect = pygame.Rect(0, 0, 200, 80)
    back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)

    return char1_button_rect, char2_button_rect, back_button_rect

def create_level_buttons():
    level1_button_rect = pygame.Rect(0, 0, 250, 80)
    level1_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 -20)

    level2_button_rect = pygame.Rect(0, 0, 250, 80)
    level2_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 80)

    level3_button_rect = pygame.Rect(0, 0, 250, 80)
    level3_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 180)

    back_button_rect = pygame.Rect(0, 0, 200, 80)
    back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)

    return level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect

def create_config_buttons():
    back_button_rect = pygame.Rect(0, 0, 200, 80)
    back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    
    return back_button_rect

# -------------------- PANTALLAS --------------------
def draw_menu(play_button_rect, quit_button_rect, config_button_rect):
    screen.blit(menu_background, [0, 0])
    
    # Título del juego traducido
    title_surface = render_text_with_outline(texts[language]["title_menu"], font_large, yellow, black)
    title_rect = title_surface.get_rect(center=(size[0] // 2, 150))
    screen.blit(title_surface, title_rect)
    
    # Botones con texto traducido
    play_text_surface = render_text_with_outline(texts[language]["play"], font_medium, yellow, black)
    quit_text_surface = render_text_with_outline(texts[language]["quit"], font_medium, yellow, black)
    config_text_surface = render_text_with_outline(texts[language]["config"], font_small, yellow, black)
    
    draw_button_with_text(play_button_img, play_button_rect, "", font_medium)
    draw_button_with_text(quit_button_img, quit_button_rect, "", font_medium)
    draw_button_with_text(config_button_img, config_button_rect, "", font_small)
    
    # Dibujar texto sobre los botones
    screen.blit(play_text_surface, play_text_surface.get_rect(center=play_button_rect.center))
    screen.blit(quit_text_surface, quit_text_surface.get_rect(center=quit_button_rect.center))
    screen.blit(config_text_surface, config_text_surface.get_rect(center=config_button_rect.center))

def draw_difficulty_selection(beginner_button_rect, advanced_button_rect, back_button_rect):
    global show_coming_soon
    
    screen.blit(imageb, [0, 0])
    
    # Texto traducido
    difficulty_surface = render_text_with_outline(texts[language]["select_difficulty"], font_large, yellow, black)
    difficulty_text_rect = difficulty_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 180))
    screen.blit(difficulty_surface, difficulty_text_rect)
    
    # Texto para botones
    beginner_text_surface = render_text_with_outline(texts[language]["beginner"], font_medium, yellow, black)
    advanced_text_surface = render_text_with_outline(texts[language]["advanced"], font_medium, yellow, black)
    back_text_surface = render_text_with_outline(texts[language]["back"], font_small, yellow, black)
    
    # Dibujar botones
    draw_button_with_text(beginner_button_img, beginner_button_rect, "", font_medium)
    draw_button_with_text(advanced_button_img, advanced_button_rect, "", font_medium)
    draw_button_with_text(back_button_img, back_button_rect, "", font_small)
    
    # Dibujar texto sobre botones
    screen.blit(beginner_text_surface, beginner_text_surface.get_rect(center=beginner_button_rect.center))
    screen.blit(advanced_text_surface, advanced_text_surface.get_rect(center=advanced_button_rect.center))
    screen.blit(back_text_surface, back_text_surface.get_rect(center=back_button_rect.center))
    
    if show_coming_soon:
        coming_soon_text = render_text_with_outline(texts[language]["coming_soon"], font_medium, red, white)
        text_rect = coming_soon_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(coming_soon_text, text_rect)

def draw_character_selection(char1_button_rect, char2_button_rect, back_button_rect):
    screen.blit(imageb, [0, 0])
    
    # Texto traducido
    select_surface = render_text_with_outline(texts[language]["select_character"], font_large, yellow, black)
    select_text_rect = select_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 180))
    screen.blit(select_surface, select_text_rect)
    
    # Texto para botones
    boy_text_surface = render_text_with_outline(texts[language]["boy"], font_small, yellow, black)
    girl_text_surface = render_text_with_outline(texts[language]["girl"], font_small, yellow, black)
    back_text_surface = render_text_with_outline(texts[language]["back"], font_small, yellow, black)
    
    draw_button_with_text(char1_button_img, char1_button_rect, "", font_small)
    draw_button_with_text(char2_button_img, char2_button_rect, "", font_small)
    draw_button_with_text(back_button_img, back_button_rect, "", font_small)
    
    # Dibujar texto sobre botones
    screen.blit(boy_text_surface, boy_text_surface.get_rect(center=char1_button_rect.center))
    screen.blit(girl_text_surface, girl_text_surface.get_rect(center=char2_button_rect.center))
    screen.blit(back_text_surface, back_text_surface.get_rect(center=back_button_rect.center))

def draw_level_selection(level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect):
    global show_coming_soon
    
    screen.blit(imageb, [0, 0])
    
    # Texto traducido
    level_surface = render_text_with_outline(texts[language]["select_level"], font_large, yellow, black)
    level_text_rect = level_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 180))
    screen.blit(level_surface, level_text_rect)
    
    # Texto para botones
    level1_text_surface = render_text_with_outline(f"{texts[language]['level']} 1", font_medium, yellow, black)
    level2_text_surface = render_text_with_outline(f"{texts[language]['level']} 2", font_medium, yellow, black)
    level3_text_surface = render_text_with_outline(f"{texts[language]['level']} 3", font_medium, yellow, black)
    back_text_surface = render_text_with_outline(texts[language]["back"], font_small, yellow, black)
    
    draw_button_with_text(level1_button_img, level1_button_rect, "", font_medium)
    draw_button_with_text(level2_button_img, level2_button_rect, "", font_medium)
    draw_button_with_text(level3_button_img, level3_button_rect, "", font_medium)
    draw_button_with_text(back_button_img, back_button_rect, "", font_small)
    
    # Dibujar texto sobre botones
    screen.blit(level1_text_surface, level1_text_surface.get_rect(center=level1_button_rect.center))
    screen.blit(level2_text_surface, level2_text_surface.get_rect(center=level2_button_rect.center))
    screen.blit(level3_text_surface, level3_text_surface.get_rect(center=level3_button_rect.center))
    screen.blit(back_text_surface, back_text_surface.get_rect(center=back_button_rect.center))
    
    if show_coming_soon:
        coming_soon_text = render_text_with_outline(texts[language]["coming_soon"], font_medium, red, white)
        text_rect = coming_soon_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(coming_soon_text, text_rect)

def draw_config_menu(back_button_rect):
    screen.blit(config_background, [0, 0])
    
    # Título traducido
    title_surface = render_text_with_outline(texts[language]["title_config"], font_large, yellow, black)
    screen.blit(title_surface, title_surface.get_rect(center=(size[0] // 2, 100)))
    
    # Sección idioma
    lang_label = render_text_with_outline(f"{texts[language]['language']}:", font_medium, yellow, black)
    screen.blit(lang_label, (150, 200))
    
    # Botones de idioma
    global language_es_rect, language_en_rect
    language_es_rect = draw_button_with_text(
        play_button_img,
        pygame.Rect(150, 250, 200, 60),
        texts["es"]["spanish"], font_small
    )
    
    language_en_rect = draw_button_with_text(
        play_button_img,  
        pygame.Rect(400, 250, 200, 60),
        texts["en"]["english"], font_small
    )
    
    # Sección volumen
    vol_label = render_text_with_outline(f"🔊 {texts[language]['volume']}: {int(volume_level * 100)}%", font_medium, yellow, black)
    screen.blit(vol_label, (150, 350))
    
    # Slider de volumen
    global volume_slider_rect
    volume_slider_rect = draw_volume_slider(150, 400, 400, 20, volume_level, pink)
    
    # Botones de volumen
    global volume_down_rect, volume_up_rect
    volume_down_rect = draw_button_with_text(
        play_button_img,
        pygame.Rect(150, 450, 80, 60),
        "-", font_medium
    )
    
    volume_up_rect = draw_button_with_text(
        play_button_img,
        pygame.Rect(470, 450, 80, 60),
        "+", font_medium
    )
    
    # Botón regresar
    back_text_surface = render_text_with_outline(texts[language]["back"], font_small, yellow, black)
    draw_button_with_text(back_button_img, back_button_rect, "", font_small)
    screen.blit(back_text_surface, back_text_surface.get_rect(center=back_button_rect.center))

# -------------------- CREACIÓN DE ELEMENTOS --------------------
# Crear todos los botones necesarios
play_button_rect, quit_button_rect, config_button_rect = create_menu_buttons()
beginner_button_rect, advanced_button_rect, back_button_rect_difficulty = create_difficulty_buttons()
char1_button_rect, char2_button_rect, back_button_rect_character = create_character_buttons()
level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect_level = create_level_buttons()
back_button_rect_config = create_config_buttons()

# Rectángulos para configuración (se inicializan en draw_config_menu)
language_es_rect = None
language_en_rect = None
volume_slider_rect = None
volume_down_rect = None
volume_up_rect = None

# -------------------- BUCLE PRINCIPAL --------------------
running = True
dragging_volume = False

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
                # Manejo del botón regresar para cada estado
                if game_state == SELECT_DIFFICULTY and back_button_rect_difficulty.collidepoint(event.pos):
                    if len(state_history) > 1:
                        state_history.pop()
                        game_state = state_history[-1]
                        show_coming_soon = False
                elif game_state == SELECT_CHARACTER and back_button_rect_character.collidepoint(event.pos):
                    if len(state_history) > 1:
                        state_history.pop()
                        game_state = state_history[-1]
                elif game_state == SELECT_LEVEL and back_button_rect_level.collidepoint(event.pos):
                    if len(state_history) > 1:
                        state_history.pop()
                        game_state = state_history[-1]
                elif game_state == CONFIG_MENU and back_button_rect_config.collidepoint(event.pos):
                    if len(state_history) > 1:
                        state_history.pop()
                        game_state = state_history[-1]
                
                elif game_state == MENU:
                    if play_button_rect.collidepoint(event.pos):
                        game_state = SELECT_DIFFICULTY
                        state_history.append(game_state)
                    elif quit_button_rect.collidepoint(event.pos):
                        running = False
                    elif config_button_rect.collidepoint(event.pos):
                        game_state = CONFIG_MENU
                        state_history.append(game_state)
                
                elif game_state == CONFIG_MENU:
                    if language_es_rect and language_es_rect.collidepoint(event.pos):
                        language = "es"
                    elif language_en_rect and language_en_rect.collidepoint(event.pos):
                        language = "en"
                    elif volume_down_rect and volume_down_rect.collidepoint(event.pos):
                        volume_level = max(0.0, volume_level - 0.1)
                        pygame.mixer.music.set_volume(volume_level)
                    elif volume_up_rect and volume_up_rect.collidepoint(event.pos):
                        volume_level = min(1.0, volume_level + 0.1)
                        pygame.mixer.music.set_volume(volume_level)
                    elif volume_slider_rect and volume_slider_rect.collidepoint(event.pos):
                        dragging_volume = True
                
                elif game_state == SELECT_DIFFICULTY:
                    if beginner_button_rect.collidepoint(event.pos):
                        is_advanced = False
                        game_state = SELECT_CHARACTER
                        state_history.append(game_state)
                        show_coming_soon = False
                    elif advanced_button_rect.collidepoint(event.pos):
                        # Lógica de "Próximamente" para el botón avanzado
                        if not show_coming_soon:
                            show_coming_soon = True
                            coming_soon_timer = pygame.time.get_ticks()
                
                elif game_state == SELECT_CHARACTER:
                    if char1_button_rect.collidepoint(event.pos):
                        selected_character = "boy"
                        game_state = SELECT_LEVEL
                        state_history.append(game_state)
                    elif char2_button_rect.collidepoint(event.pos):
                        selected_character = "girl"
                        game_state = SELECT_LEVEL
                        state_history.append(game_state)
                
                elif game_state == SELECT_LEVEL:
                    if level1_button_rect.collidepoint(event.pos):
                        game_state = GAME_LEVEL_1
                        level_instance = Level1F.Level1(screen, size, font, selected_character)
                    elif level2_button_rect.collidepoint(event.pos) or level3_button_rect.collidepoint(event.pos):
                        # Lógica de "Próximamente" para niveles no implementados
                        if not show_coming_soon:
                            show_coming_soon = True
                            coming_soon_timer = pygame.time.get_ticks()
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_volume = False
                
        elif event.type == pygame.MOUSEMOTION and dragging_volume:
            if volume_slider_rect:
                # Calcular nuevo volumen basado en la posición del mouse
                relative_x = event.pos[0] - volume_slider_rect.left
                volume_level = max(0.0, min(1.0, relative_x / volume_slider_rect.width))
                pygame.mixer.music.set_volume(volume_level)

    # -------------------- DIBUJAR PANTALLAS --------------------
    if game_state == MENU:
        draw_menu(play_button_rect, quit_button_rect, config_button_rect)
    elif game_state == SELECT_DIFFICULTY:
        draw_difficulty_selection(beginner_button_rect, advanced_button_rect, back_button_rect_difficulty)
    elif game_state == SELECT_CHARACTER:
        draw_character_selection(char1_button_rect, char2_button_rect, back_button_rect_character)
    elif game_state == SELECT_LEVEL:
        draw_level_selection(level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect_level)
    elif game_state == CONFIG_MENU:
        draw_config_menu(back_button_rect_config)
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