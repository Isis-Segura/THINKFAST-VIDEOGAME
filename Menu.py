import pygame, sys
import Levels.Level1F as Level1F
import Levels.Level2F as Level2F
import Levels.Level3F as Level3F  # CORREGIDO: Importación necesaria para Nivel 3
from Interacciones.Controldeobjetos.pyvidplayer import Video

pygame.init()

# -------------------- CONFIGURACIÓN INICIAL Y COLORES --------------------
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
brown=(87, 27, 15)
# Tamaños
size = (900, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Think Fast!")

# Fuentes
try:
    font_super_large = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 48)
    font_large = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 36)
    font_medium = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 28)
    font_small = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 22)
    font_tiny = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 18)
except pygame.error:
    print("Advertencia: No se encontraron fuentes personalizadas. Usando fuente por defecto.")
    font_medium = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 30)

# -------------------- VIDEO DE INTRODUCCIÓN --------------------
# Este bloque se deja intacto, asumiendo la funcionalidad del módulo pyvidplayer
try:
    intro_path = "Materials/videos/ramiro.mp4" 
    vid = Video(intro_path)
    
    intro_running = True
    while intro_running and vid.active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vid.close()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                intro_running = False
                break 

        if intro_running and vid.active:
            vid.draw(screen, (0, 0)) 
            pygame.display.flip()
            pygame.time.wait(int(vid.frame_delay * 1000))
            
    vid.close() 

except Exception as e:
    print(f"Advertencia/Error al reproducir el video: {e}. Iniciando en el menú.")
# -------------------- FIN DEL BLOQUE DE VIDEO --------------------

# -------------------- IMÁGENES Y BOTONES --------------------
# Carga de Fondos
menu_background = pygame.image.load("Materials/Pictures/Assets/fondo.png").convert()
menu_background = pygame.transform.scale(menu_background, size)
imageb = pygame.image.load("Materials/Pictures/Assets/fondo_sin.png").convert()
imageb = pygame.transform.scale(imageb, size)
config_background = pygame.transform.scale(imageb, size)
text_background_img = pygame.image.load("Materials/Pictures/Assets/botontitusoli.png").convert_alpha()
text_background_img = pygame.transform.scale(text_background_img, (730, 80))

# Carga de Botones
spanish_button_img = pygame.image.load("Materials/Pictures/Assets/btn_spanish.png").convert_alpha()
english_button_img = pygame.image.load("Materials/Pictures/Assets/btn_inglish.png").convert_alpha()
play_button_img = pygame.image.load("Materials/Pictures/Assets/btn_play.png").convert_alpha()
quit_button_img = pygame.image.load("Materials/Pictures/Assets/btn_quit.png").convert_alpha()
beginner_button_img = pygame.image.load("Materials/Pictures/Assets/buttonsoli.png").convert_alpha()
advanced_button_img = pygame.image.load("Materials/Pictures/Assets/buttonsoli.png").convert_alpha()
char1_button_img = pygame.image.load("Materials/Pictures/Assets/btn_boy.png").convert_alpha()
char2_button_img = pygame.image.load("Materials/Pictures/Assets/btn_girl.png").convert_alpha()
level1_button_img = pygame.image.load("Materials/Pictures/Assets/btn_principiante_1.png").convert_alpha()
level2_button_img = pygame.image.load("Materials/Pictures/Assets/btn_principiante_2.png").convert_alpha()
level3_button_img = pygame.image.load("Materials/Pictures/Assets/btn_principiante_3.png").convert_alpha()
back_button_img = pygame.image.load("Materials/Pictures/Assets/btn_regresar.png").convert_alpha()
config_button_img = pygame.image.load("Materials/Pictures/Assets/btn_confi.png").convert_alpha()
volume_up_img = pygame.image.load("Materials/Pictures/Assets/btn_volum_mas.png").convert_alpha()
volume_down_img = pygame.image.load("Materials/Pictures/Assets/btn_volum_menos.png").convert_alpha()

clock = pygame.time.Clock()

# Música
pygame.mixer.music.load('Materials/Music/Menu.wav')
pygame.mixer.music.play(-1)

# -------------------- ESTADOS Y VARIABLES GLOBALES --------------------
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
language = "es" 
volume_level = 0.7 
pygame.mixer.music.set_volume(volume_level) 

texts = {
    "es": {
        "play": "Jugar", "quit": "Salir", "config": "Configuración",
        "volume": "Volumen", "language": "Idioma", "back": "Regresar",
        "spanish": "Español", "english": "Inglés", "title_config": "Menú de Configuración",
        "select_difficulty": "Selecciona la dificultad", "beginner": "Principiante", "advanced": "Avanzado",
        "select_character": "Selecciona tu personaje", "boy": "Niño", "girl": "Niña",
        "select_level": "Selecciona el nivel", "level": "Nivel", "coming_soon": "¡Proximamente!"
    },
    "en": {
        "play": "Play", "quit": "Quit", "config": "Settings",
        "volume": "Volume", "language": "Language", "back": "Back",
        "spanish": "Spanish", "english": "English", "title_config": "Settings Menu",
        "select_difficulty": "Select difficulty", "beginner": "Beginner", "advanced": "Advanced",
        "select_character": "Select your character", "boy": "Boy", "girl": "Girl",
        "select_level": "Select level", "level": "Level", "coming_soon": "Coming soon!"
    }
}

show_coming_soon = False
coming_soon_timer = 0
COMING_SOON_DURATION = 2000 

# -------------------- FUNCIONES DE DIBUJO --------------------
def render_text_with_outline(text, font, text_color, outline_color, offset=3):
    outline_surface = font.render(text, True, outline_color)
    text_surface = font.render(text, True, text_color)
    width = text_surface.get_width() + 2 * offset
    height = text_surface.get_height() + 2 * offset
    final_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for dx in [-offset, 0, offset]:
        for dy in [-offset, 0, offset]:
            if dx != 0 or dy != 0:
                final_surface.blit(outline_surface, (dx + offset, dy + offset))
    final_surface.blit(text_surface, (offset, offset))
    return final_surface

def draw_button(image, rect):
    scaled_img = pygame.transform.scale(image, (rect.width, rect.height))
    screen.blit(scaled_img, rect)
    return rect

def draw_button_with_text(image, rect, text, font, text_color=brown, outline_color=white):
    draw_button(image, rect)
    if text:
        text_surface = render_text_with_outline(text, font, text_color, outline_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
    return rect

def draw_volume_slider(x, y, width, height, volume, color):
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), border_radius=10)
    fill_width = int(width * volume)
    pygame.draw.rect(screen, color, (x, y, fill_width, height), border_radius=10)
    pygame.draw.rect(screen, black, (x, y, width, height), 2, border_radius=10)
    thumb_x = x + fill_width
    thumb_y = y + height // 2
    pygame.draw.circle(screen, purple, (thumb_x, thumb_y), height + 5)
    pygame.draw.circle(screen, white, (thumb_x, thumb_y), height + 3)
    return pygame.Rect(x, y, width, height)

# -------------------- CREACIÓN DE RECTÁNGULOS --------------------
def create_menu_buttons():
    play_button_rect = pygame.Rect(0, 0, 250, 80); play_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 50)
    quit_button_rect = pygame.Rect(0, 0, 250, 80); quit_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 50)
    config_button_rect = pygame.Rect(0, 0, 200, 80); config_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 150)
    return play_button_rect, quit_button_rect, config_button_rect

def create_difficulty_buttons():
    beginner_button_rect = pygame.Rect(0, 0, 285, 80); beginner_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 20)
    advanced_button_rect = pygame.Rect(0, 0, 250, 80); advanced_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 80)
    back_button_rect = pygame.Rect(0, 0, 200, 80); back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    return beginner_button_rect, advanced_button_rect, back_button_rect

def create_character_buttons():
    char1_button_rect = pygame.Rect(0, 0, 180, 250); char1_button_rect.center = (screen.get_width() // 2 - 150, screen.get_height() // 2 + 40)
    char2_button_rect = pygame.Rect(0, 0, 180, 250); char2_button_rect.center = (screen.get_width() // 2 + 150, screen.get_height() // 2 + 40)
    back_button_rect = pygame.Rect(0, 0, 200, 80); back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    return char1_button_rect, char2_button_rect, back_button_rect

def create_level_buttons():
    level1_button_rect = pygame.Rect(0, 0, 250, 80); level1_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 -20)
    level2_button_rect = pygame.Rect(0, 0, 250, 80); level2_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 80)
    level3_button_rect = pygame.Rect(0, 0, 250, 80); level3_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 180)
    back_button_rect = pygame.Rect(0, 0, 200, 80); back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    return level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect

def create_config_buttons():
    back_button_rect = pygame.Rect(0, 0, 200, 80); back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    return back_button_rect

# -------------------- PANTALLAS --------------------
def draw_menu(play_button_rect, quit_button_rect, config_button_rect):
    screen.blit(menu_background, [0, 0])
    draw_button(play_button_img, play_button_rect)
    draw_button(quit_button_img, quit_button_rect)  
    draw_button(config_button_img, config_button_rect)

def draw_difficulty_selection(beginner_button_rect, advanced_button_rect, back_button_rect):
    screen.blit(imageb, [0, 0])
    bg_rect = text_background_img.get_rect(center=(size[0] // 2, size[1] // 2 - 180))
    screen.blit(text_background_img, bg_rect)
    difficulty_surface = render_text_with_outline(texts[language]["select_difficulty"], font_medium, brown, white)
    screen.blit(difficulty_surface, difficulty_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 180)))
    draw_button_with_text(beginner_button_img, beginner_button_rect, texts[language]["beginner"], font_small, brown, white)
    draw_button_with_text(advanced_button_img, advanced_button_rect, texts[language]["advanced"], font_small, brown, white)
    draw_button(back_button_img, back_button_rect)
    if show_coming_soon:
        coming_soon_text = render_text_with_outline(texts[language]["coming_soon"], font_medium, red, white)
        text_rect = coming_soon_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(coming_soon_text, text_rect)

def draw_character_selection(char1_button_rect, char2_button_rect, back_button_rect):
    screen.blit(imageb, [0, 0])
    bg_rect = text_background_img.get_rect(center=(size[0] // 2, size[1] // 2 - 180))
    screen.blit(text_background_img, bg_rect)
    select_surface = render_text_with_outline(texts[language]["select_character"], font_medium, brown, white)
    screen.blit(select_surface, select_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 180)))
    draw_button(char1_button_img, char1_button_rect)
    draw_button(char2_button_img, char2_button_rect)
    draw_button(back_button_img, back_button_rect)

def draw_level_selection(level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect):
    screen.blit(imageb, [0, 0])
    bg_rect = text_background_img.get_rect(center=(size[0] // 2, size[1] // 2 - 180))
    screen.blit(text_background_img, bg_rect)
    level_surface = render_text_with_outline(texts[language]["select_level"], font_medium, brown, white)
    screen.blit(level_surface, level_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 180)))
    draw_button_with_text(level1_button_img, level1_button_rect, f"{texts[language]['level']} 1", font_small, brown, white)
    draw_button_with_text(level2_button_img, level2_button_rect, f"{texts[language]['level']} 2", font_small, brown, white)
    draw_button_with_text(level3_button_img, level3_button_rect, f"{texts[language]['level']} 3", font_small, brown, white)
    draw_button(back_button_img, back_button_rect)
    if show_coming_soon:
        coming_soon_text = render_text_with_outline(texts[language]["coming_soon"], font_medium, red, white)
        text_rect = coming_soon_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(coming_soon_text, text_rect)

def draw_config_menu(back_button_rect):
    screen.blit(config_background, [0, 0])
    center_x = size[0] // 2
    
    bg_rect = text_background_img.get_rect(center=(center_x, 120))
    screen.blit(text_background_img, bg_rect)
    title_surface = render_text_with_outline(texts[language]["title_config"], font_medium, brown, white)
    screen.blit(title_surface, title_surface.get_rect(center=(center_x, 120)))
    
    lang_y = 220
    lang_label = render_text_with_outline(f"{texts[language]['language']}:", font_medium, brown, white)
    screen.blit(lang_label, lang_label.get_rect(center=(center_x, lang_y)))
    
    flag_button_width, flag_button_height = 120, 70
    flag_spacing = 30
    global language_es_rect, language_en_rect
    language_es_rect = pygame.Rect(0, 0, flag_button_width, flag_button_height)
    language_es_rect.center = (center_x - flag_button_width//2 - flag_spacing, lang_y + 50)
    draw_button(spanish_button_img, language_es_rect) 
    language_en_rect = pygame.Rect(0, 0, flag_button_width, flag_button_height)
    language_en_rect.center = (center_x + flag_button_width//2 + flag_spacing, lang_y + 50)
    draw_button(english_button_img, language_en_rect)
    
    vol_y = 220 + 140
    vol_label = render_text_with_outline(f"{texts[language]['volume']}: {int(volume_level * 100)}%", font_medium, brown, white)
    screen.blit(vol_label, vol_label.get_rect(center=(center_x, vol_y)))
    
    slider_width, slider_height = 400, 20
    global volume_slider_rect, volume_down_rect, volume_up_rect
    volume_slider_rect = draw_volume_slider(center_x - slider_width//2, vol_y + 40, slider_width, slider_height, volume_level, pink)
    
    vol_button_width, vol_button_height = 80, 60
    vol_button_spacing = 250
    volume_down_rect = pygame.Rect(0, 0, vol_button_width, vol_button_height)
    volume_down_rect.center = (center_x - vol_button_spacing//2, vol_y + 100)
    draw_button(volume_down_img, volume_down_rect)
    volume_up_rect = pygame.Rect(0, 0, vol_button_width, vol_button_height)
    volume_up_rect.center = (center_x + vol_button_spacing//2, vol_y + 100)
    draw_button(volume_up_img, volume_up_rect)
    
    back_button_rect.center = (center_x, size[1] - 100)
    draw_button(back_button_img, back_button_rect)

# -------------------- INICIALIZACIÓN DE RECTÁNGULOS --------------------
play_button_rect, quit_button_rect, config_button_rect = create_menu_buttons()
beginner_button_rect, advanced_button_rect, back_button_rect_difficulty = create_difficulty_buttons()
char1_button_rect, char2_button_rect, back_button_rect_character = create_character_buttons()
level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect_level = create_level_buttons()
back_button_rect_config = create_config_buttons()

language_es_rect = None; language_en_rect = None
volume_slider_rect = None; volume_down_rect = None; volume_up_rect = None

# -------------------- BUCLE PRINCIPAL --------------------
running = True
dragging_volume = False

while running:
    if show_coming_soon and pygame.time.get_ticks() > coming_soon_timer + COMING_SOON_DURATION:
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
            # Continúa el bucle para no procesar eventos de menú mientras está en nivel
            continue 
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Lógica de Botones REGRESAR
            if game_state == SELECT_DIFFICULTY and back_button_rect_difficulty.collidepoint(event.pos):
                if len(state_history) > 1: state_history.pop(); game_state = state_history[-1]; show_coming_soon = False
            elif game_state == SELECT_CHARACTER and back_button_rect_character.collidepoint(event.pos):
                if len(state_history) > 1: state_history.pop(); game_state = state_history[-1]
            elif game_state == SELECT_LEVEL and back_button_rect_level.collidepoint(event.pos):
                if len(state_history) > 1: state_history.pop(); game_state = state_history[-1]; show_coming_soon = False
            elif game_state == CONFIG_MENU and back_button_rect_config.collidepoint(event.pos):
                if len(state_history) > 1: state_history.pop(); game_state = state_history[-1]
            
            # Lógica de botones de MENÚ
            elif game_state == MENU:
                if play_button_rect.collidepoint(event.pos):
                    game_state = SELECT_DIFFICULTY; state_history.append(game_state)
                elif quit_button_rect.collidepoint(event.pos):
                    running = False
                elif config_button_rect.collidepoint(event.pos):
                    game_state = CONFIG_MENU; state_history.append(game_state)
            
            # Lógica de botones de CONFIGURACIÓN
            elif game_state == CONFIG_MENU:
                if language_es_rect and language_es_rect.collidepoint(event.pos):
                    language = "es"
                elif language_en_rect and language_en_rect.collidepoint(event.pos):
                    language = "en"
                elif volume_down_rect and volume_down_rect.collidepoint(event.pos):
                    volume_level = max(0.0, volume_level - 0.1); pygame.mixer.music.set_volume(volume_level)
                elif volume_up_rect and volume_up_rect.collidepoint(event.pos):
                    volume_level = min(1.0, volume_level + 0.1); pygame.mixer.music.set_volume(volume_level)
                elif volume_slider_rect and volume_slider_rect.collidepoint(event.pos):
                    dragging_volume = True
            
            # Lógica de botones de DIFICULTAD
            elif game_state == SELECT_DIFFICULTY:
                if beginner_button_rect.collidepoint(event.pos):
                    is_advanced = False
                    game_state = SELECT_CHARACTER; state_history.append(game_state); show_coming_soon = False
                elif advanced_button_rect.collidepoint(event.pos):
                    if not show_coming_soon:
                        show_coming_soon = True
                        coming_soon_timer = pygame.time.get_ticks()
            
            # Lógica de botones de PERSONAJE
            elif game_state == SELECT_CHARACTER:
                if char1_button_rect.collidepoint(event.pos):
                    selected_character = "boy"
                    game_state = SELECT_LEVEL; state_history.append(game_state)
                elif char2_button_rect.collidepoint(event.pos):
                    selected_character = "girl"
                    game_state = SELECT_LEVEL; state_history.append(game_state)
            
            # Lógica de botones de SELECCIÓN DE NIVEL
            elif game_state == SELECT_LEVEL:
                if level1_button_rect.collidepoint(event.pos):
                    game_state = GAME_LEVEL_1
                    level_instance = Level1F.Level1(screen, size, font_small, selected_character)
                    show_coming_soon = False
                
                elif level2_button_rect.collidepoint(event.pos):
                    game_state = GAME_LEVEL_1
                    level_instance = Level2F.Level2(screen, size, font_small, selected_character)
                    show_coming_soon = False
                
                # *** CÓDIGO CORREGIDO PARA INICIAR NIVEL 3 ***
                elif level3_button_rect.collidepoint(event.pos):
                    game_state = GAME_LEVEL_1
                    # Se asume que Level3F.Level3 existe.
                    level_instance = Level3F.Level3(screen, size, font_small, selected_character) 
                    show_coming_soon = False
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging_volume = False
            
        elif event.type == pygame.MOUSEMOTION and dragging_volume:
            if volume_slider_rect:
                relative_x = event.pos[0] - volume_slider_rect.left
                volume_level = max(0.0, min(1.0, relative_x / volume_slider_rect.width))
                pygame.mixer.music.set_volume(volume_level)

    # -------------------- DIBUJAR --------------------
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