import pygame, sys
import Levels.Level1F as Level1F
import Levels.Level2F as Level2F
import Levels.Level3F as Level3F
# Importar los nuevos niveles (debes crear estos archivos)
import Levels.Level4F as Level4F
import Levels.Level5F as Level5F
import Levels.Level6F as Level6F
# Importa las clases de movimiento y la función del video
from Interacciones.Menu_Dynamics import Cloud, HotAirBalloon 
from Interacciones.Intro_Video import run_intro_video 
from Interacciones.Settings import SettingsPanel # Importación de la clase Panel

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
orange2=(211,134,81)
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
    font_large = pygame.font.Font(None, 50) # Añadir fallback para large

# -------------------- IMÁGENES Y BOTONES --------------------
# Carga de Fondos
sky_background = pygame.image.load("Materials/Pictures/Assets/sky_background.png").convert() 
sky_background = pygame.transform.scale(sky_background, size)

# Elementos dinámicos y primer plano
cloud_img = pygame.image.load("Materials/Pictures/Assets/cloud.png").convert_alpha()
balloon_img = pygame.image.load("Materials/Pictures/Assets/hot_air_balloon.png").convert_alpha()

# --- IMAGEN DE ESCUELA PRINCIPAL (Para MENU y CONFIG_MENU) ---
try:
    school_foreground_img = pygame.image.load("school_foreground.jpg").convert_alpha()
except:
    school_foreground_img = pygame.image.load("Materials/Pictures/Assets/school_foreground.png").convert_alpha()
    
school_foreground_img = pygame.transform.scale(school_foreground_img, size)
school_rect = school_foreground_img.get_rect(bottomleft=(0, size[1]))

# --- IMAGEN DE ESCUELA SECUNDARIA (Para SUB-MENÚS) ---
try:
    school_secondary_img = pygame.image.load("Materials/Pictures/Assets/school_secondary_foreground.png").convert_alpha()
    school_secondary_img = pygame.transform.scale(school_secondary_img, size)
    school_secondary_rect = school_secondary_img.get_rect(bottomleft=(0, size[1]))
except pygame.error:
    print("ADVERTENCIA: No se encontró la imagen secundaria de la escuela. Usando la imagen principal.")
    school_secondary_img = school_foreground_img
    school_secondary_rect = school_rect
    
# Inicialización de objetos dinámicos
NUM_CLOUDS = 15 
clouds = [Cloud(cloud_img, size[0], size[1]) for _ in range(NUM_CLOUDS)]
balloon = HotAirBalloon(balloon_img, size[0], size[1])

# Otros assets de fondo para marcos de texto
text_background_img = pygame.image.load("Materials/Pictures/Assets/marco_titles.png").convert_alpha()
text_background_img = pygame.transform.scale(text_background_img, (700, 80))

# --- BOTONES DE MENÚ PRINCIPAL (Play, Quit, Config) ---
play_button_img = pygame.image.load("Materials/Pictures/Assets/btn_play1.png").convert_alpha()
quit_button_img = pygame.image.load("Materials/Pictures/Assets/btn_quit1.png").convert_alpha()
config_button_img = pygame.image.load("Materials/Pictures/Assets/btn_confi1.png").convert_alpha()
play_button_hover_img = pygame.image.load("Materials/Pictures/Assets/btn_play3.png").convert_alpha()
quit_button_hover_img = pygame.image.load("Materials/Pictures/Assets/btn_quit3.png").convert_alpha()
config_button_hover_img = pygame.image.load("Materials/Pictures/Assets/btn_confi3.png").convert_alpha()
play_button_click_img = pygame.image.load("Materials/Pictures/Assets/btn_play2.png").convert_alpha()
quit_button_click_img = pygame.image.load("Materials/Pictures/Assets/btn_quit2.png").convert_alpha()
config_button_click_img = pygame.image.load("Materials/Pictures/Assets/btn_confi2.png").convert_alpha()

# Botones de Dificultad/Nivel (btn_normal)
avanzado_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_avanzado1.png").convert_alpha()
avanzado_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_avanzado3.png").convert_alpha()
avanzado_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_avanzado2.png").convert_alpha()
normal_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_normal1.png").convert_alpha()
normal_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_normal3.png").convert_alpha()
normal_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_normal2.png").convert_alpha()
# Botones de Niveles
level1_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_patio1.png").convert_alpha()
level1_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_patio3.png").convert_alpha()
level1_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_patio2.png").convert_alpha()
level2_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_pasillo1.png").convert_alpha()
level2_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_pasillo3.png").convert_alpha()
level2_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_pasillo2.png").convert_alpha()
level3_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_salon1.png").convert_alpha()
level3_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_salon3.png").convert_alpha()
level3_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_salon2.png").convert_alpha()

# Botones de Personaje (btn_boy/btn_girl)
boy_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_boy1.png").convert_alpha()
boy_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_boy3.png").convert_alpha()
boy_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_boy2.png").convert_alpha()
girl_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_girl1.png").convert_alpha()
girl_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_girl3.png").convert_alpha()
girl_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_girl2.png").convert_alpha()

# Botón Regresar (btn_back)
back_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_back1.png").convert_alpha()
back_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_back3.png").convert_alpha()
back_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_back2.png").convert_alpha()

# --- BOTONES NUEVOS DE PAUSA (Continuar, Menú Principal) ---
# Si no tienes estas imágenes, puedes usar las de 'play'/'quit' o crear rectángulos con texto.
try:
    btn_continue1 = pygame.image.load("Materials/Pictures/Assets/btn_continue1.png").convert_alpha()
    btn_continue3 = pygame.image.load("Materials/Pictures/Assets/btn_continue3.png").convert_alpha()
    btn_continue2 = pygame.image.load("Materials/Pictures/Assets/btn_continue2.png").convert_alpha()
    btn_menu1 = pygame.image.load("Materials/Pictures/Assets/btn_menu1.png").convert_alpha()
    btn_menu3 = pygame.image.load("Materials/Pictures/Assets/btn_menu3.png").convert_alpha()
    btn_menu2 = pygame.image.load("Materials/Pictures/Assets/btn_menu2.png").convert_alpha()
    btn_reset1 = pygame.image.load("Materials/Pictures/Assets/btn_reset1.png").convert_alpha()
    btn_reset3 = pygame.image.load("Materials/Pictures/Assets/btn_reset3.png").convert_alpha()
    btn_reset2 = pygame.image.load("Materials/Pictures/Assets/btn_reset2.png").convert_alpha()
except pygame.error:
    # Usar las imágenes del menú principal si fallan
    print("ADVERTENCIA: No se encontraron imágenes de botones de pausa. Usando Play/Quit.")
    btn_continue1, btn_continue3, btn_continue2 = play_button_img, play_button_hover_img, play_button_click_img
    btn_menu1, btn_menu3, btn_menu2 = quit_button_img, quit_button_hover_img, quit_button_click_img,btn_reset1, btn_reset3, btn_reset2 = config_button_img, config_button_hover_img, config_button_click_img

# --- BOTÓN DE SALTAR INTRO (Lógica de Carga) ---
try:
    # 1. Cargar la imagen base
    skip_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_skip1.png").convert_alpha()
    skip_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_skip3.png").convert_alpha()
    skip_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_skip2.png").convert_alpha()
except pygame.error:
    print("ADVERTENCIA: No se encontró 'btn_skip1.png'. Usando un botón de color sólido.")
    # Fallback si falla la carga
    btn_skip1 = pygame.Surface((100, 50), pygame.SRCALPHA); btn_skip1.fill((255, 0, 0, 150))
    btn_skip3 = pygame.Surface((100, 50), pygame.SRCALPHA); btn_skip3.fill((255, 50, 50, 200)) 
    btn_skip2 = pygame.Surface((100, 50), pygame.SRCALPHA); btn_skip2.fill((200, 0, 0, 255)) 

# --- BOTÓN DE PAUSA (Esquina superior izquierda) ---
try:
    pause_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_pause1.png").convert_alpha()
    pause_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_pause3.png").convert_alpha()
    pause_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_pause2.png").convert_alpha()
except pygame.error:
    print("ADVERTENCIA: No se encontraron imágenes de botón de pausa. Usando Conf/Conf/Conf.")
    pause_button_img_1, pause_button_img_3, pause_button_img_2 = config_button_img, config_button_hover_img, config_button_click_img

PAUSE_BUTTON_SIZE = (60, 60)
PAUSE_PADDING = 10
pause_button_img_1 = pygame.transform.scale(pause_button_img_1, PAUSE_BUTTON_SIZE)
pause_button_img_3 = pygame.transform.scale(pause_button_img_3, PAUSE_BUTTON_SIZE)
pause_button_img_2 = pygame.transform.scale(pause_button_img_2, PAUSE_BUTTON_SIZE)
pause_button_rect = pygame.Rect(PAUSE_PADDING, PAUSE_PADDING, PAUSE_BUTTON_SIZE[0], PAUSE_BUTTON_SIZE[1])
# --- FIN DE BOTONES ---

clock = pygame.time.Clock()

# -------------------- EJECUCIÓN DEL VIDEO DE INTRODUCCIÓN --------------------
# El programa se detiene aquí hasta que el video termine o se salte.
run_intro_video(screen, size, skip_button_img_1, skip_button_img_2, skip_button_img_3) 

# -------------------- INICIO DE MÚSICA DESPUÉS DEL VIDEO --------------------
# La música comienza ahora, después de que el video de introducción ha terminado.
pygame.mixer.music.load('Materials/Music/Menu.wav')
pygame.mixer.music.play(-1)

# -------------------- ESTADOS Y VARIABLES GLOBALES --------------------
MENU = 0
SELECT_DIFFICULTY = 1
SELECT_CHARACTER = 2
SELECT_CHARACTER2 = 6  
SELECT_LEVEL = 3
SELECT_ADVANCED_LEVEL = 8  
GAME_LEVEL_1 = 4 
CONFIG_MENU = 5 
# PAUSE_MENU = 7 # Ya no es necesario si usamos solo la bandera 'is_paused'

# Variables de Animación de Configuración
SLIDE_SPEED = 30 
PANEL_WIDTH = 700 
config_target_x = (size[0] - PANEL_WIDTH) // 2 
config_panel_x = -PANEL_WIDTH 
config_closing = False 

game_state = MENU
state_history = [MENU]
is_advanced = False
selected_character = "boy"
level_instance = None
language = "es" 
volume_level = 0.7 
pygame.mixer.music.set_volume(volume_level) 
is_paused = False # <--- BANDERA DE PAUSA

# --- INICIALIZAR MENÚ DE CONFIGURACIÓN ---
settings_panel = SettingsPanel(screen, size) 

button_pressed = None 

texts = {
    "es": {
        "play": "Jugar", "quit": "Salir", "config": "Configuración",
        "volume": "Volumen", "language": "Idioma", "back": "Regresar",
        "spanish": "Español", "english": "Inglés", "title_config": "Menú de Configuración",
        "select_difficulty": "Selecciona la dificultad", "beginner": "Normal", "advanced": "Avanzado",
        "select_character": "Selecciona tu personaje", "boy": "Niño", "girl": "Niña",
        "select_level": "Selecciona el desafío", 
        "level1_name": "Entrada", "level2_name": "Pasillo", "level3_name": "Salón",  
        "coming_soon": "¡Proximamente!",
        "pause": "PAUSA", "continue": "Continuar", "main_menu": "Menú Principal","reset_level": "Reset Level", 
    },
    "en": {
        "play": "Play", "quit": "Quit", "config": "Settings",
        "volume": "Volume", "language": "Language", "back": "Back",
        "spanish": "Spanish", "english": "English", "title_config": "Settings Menu",
        "select_difficulty": "Select difficulty", "beginner": "Beginner", "advanced": "Advanced",
        "select_character": "Select your character", "boy": "Boy", "girl": "Girl",
        "select_level": "Select the challenge", 
        "level1_name": "Entrance", "level2_name": "Aisle", "level3_name": "Classroom", 
        "coming_soon": "Coming soon!",
        "pause": "PAUSA", "continue": "Continue", "main_menu": "Main Menu","reset_level": "Reset Level", 
    }
}

show_coming_soon = False
coming_soon_timer = 0
COMING_SOON_DURATION = 2000 

# -------------------- FUNCIONES DE DIBUJO Y AYUDA --------------------
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

def draw_3_state_button(rect, img_1, img_3, img_2, mouse_pos, current_pressed_state, button_id):
    """Dibuja un botón con 3 estados de imagen (Normal, Hover, Clicked) sin texto."""
    if current_pressed_state == button_id:
        image = img_2
    elif rect.collidepoint(mouse_pos):
        image = img_3
    else:
        image = img_1
    return draw_button(image, rect)


def draw_button_with_text_3_state(rect, text, font, mouse_pos, current_pressed_state, button_id, img_1, img_3, img_2, text_color=white, outline_color=brown, text_adjust_x=-40, text_adjust_y=-5):
    """Dibuja un botón con texto, 3 estados de imagen, desplazamiento y ajuste de posición del texto."""
    
    if current_pressed_state == button_id:
        image = img_2 
        text_offset_y = 5 
    elif rect.collidepoint(mouse_pos):
        image = img_3 
        text_offset_y = 0 
    else:
        image = img_1 
        text_offset_y = 0 
        
    draw_button(image, rect)
    
    text_c = text_color 
    
    if text:
        text_surface = render_text_with_outline(text, font, text_c, outline_color)
        
        text_rect = text_surface.get_rect(
            center=(
                rect.center[0] + text_adjust_x,             
                rect.center[1] + text_adjust_y + text_offset_y
            )
        )
        
        screen.blit(text_surface, text_rect)
    return rect

def create_menu_buttons():
    play_button_rect = pygame.Rect(0, 0, 190, 80); play_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 50)
    quit_button_rect = pygame.Rect(0, 0, 190, 80); quit_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 50)
    config_button_rect = pygame.Rect(0, 0, 190, 80); config_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 150)
    return play_button_rect, quit_button_rect, config_button_rect

def create_difficulty_buttons():
    btn_w, btn_h = 260, 80 
    beginner_button_rect = pygame.Rect(0, 0, 290, btn_h); beginner_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 60)
    advanced_button_rect = pygame.Rect(0, 0, 290, btn_h); advanced_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 40)
    back_button_rect = pygame.Rect(0, 0, 160, 80); back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    return beginner_button_rect, advanced_button_rect, back_button_rect

def create_character_buttons():
    char1_button_rect = pygame.Rect(0, 0, 150, 330); char1_button_rect.center = (screen.get_width() // 2 - 150, screen.get_height() // 2 + 20)
    char2_button_rect = pygame.Rect(0, 0, 150, 330); char2_button_rect.center = (screen.get_width() // 2 + 150, screen.get_height() // 2 + 20)
    back_button_rect = pygame.Rect(0, 0, 160, 80); back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    return char1_button_rect, char2_button_rect, back_button_rect

def create_level_buttons():
    btn_w, btn_h = 270, 80
    center_x = screen.get_width() // 2
    
    spacing_y = btn_h + 30 

    level1_button_rect = pygame.Rect(0, 0, 280, btn_h)
    level1_button_rect.center = (center_x - 100, screen.get_height() // 2 - spacing_y)
    
    level2_button_rect = pygame.Rect(0, 0, btn_w, btn_h)
    level2_button_rect.center = (center_x, screen.get_height() // 2)
    
    level3_button_rect = pygame.Rect(0, 0, 300, btn_h)
    level3_button_rect.center = (center_x + 100, screen.get_height() // 2 + spacing_y)
    
    back_button_rect = pygame.Rect(0, 0, 160, 80)
    back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    
    return level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect

def create_advanced_level_buttons():
    btn_w, btn_h = 270, 80
    center_x = screen.get_width() // 2
    
    spacing_y = btn_h + 30 

    level4_button_rect = pygame.Rect(0, 0, btn_w, btn_h)
    level4_button_rect.center = (center_x - 100, screen.get_height() // 2 - spacing_y)
    
    level5_button_rect = pygame.Rect(0, 0, btn_w, btn_h)
    level5_button_rect.center = (center_x, screen.get_height() // 2)
    
    level6_button_rect = pygame.Rect(0, 0, btn_w, btn_h)
    level6_button_rect.center = (center_x + 100, screen.get_height() // 2 + spacing_y)
    
    back_button_rect = pygame.Rect(0, 0, 160, 80)
    back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    
    return level4_button_rect, level5_button_rect, level6_button_rect, back_button_rect

def create_pause_menu_buttons(): 
    btn_w, btn_h = 100, 100 
    # Botón Reset Level
    reset_button_rect_pause = pygame.Rect(0, 0, btn_w, btn_h)
    reset_button_rect_pause.center = (screen.get_width() // 2 + 130, screen.get_height() // 2)
    # Botón Continuar
    continue_button_rect = pygame.Rect(0, 0, btn_w, btn_h)
    continue_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    
    # Botón Menú Principal
    menu_button_rect_pause = pygame.Rect(0, 0, btn_w, btn_h)
    menu_button_rect_pause.center = (screen.get_width() // 2 - 130, screen.get_height() // 2)
    
    return continue_button_rect, menu_button_rect_pause, reset_button_rect_pause

# -------------------- FUNCIONES DE DIBUJO DE PANTALLAS (REDUCIDAS) --------------------
def draw_menu(play_button_rect, quit_button_rect, config_button_rect, mouse_pos, button_pressed):
    
    # 4. DIBUJAR LOS BOTONES (Lógica de 3 estados)
    if button_pressed == "play":
        draw_button(play_button_click_img, play_button_rect) 
    elif play_button_rect.collidepoint(mouse_pos):
        draw_button(play_button_hover_img, play_button_rect) 
    else:
        draw_button(play_button_img, play_button_rect) 

    if button_pressed == "quit":
        draw_button(quit_button_click_img, quit_button_rect)
    elif quit_button_rect.collidepoint(mouse_pos):
        draw_button(quit_button_hover_img, quit_button_rect)
    else:
        draw_button(quit_button_img, quit_button_rect)
        
    if button_pressed == "config":
        draw_button(config_button_click_img, config_button_rect)
    elif config_button_rect.collidepoint(mouse_pos):
        draw_button(config_button_hover_img, config_button_rect)
    else:
        draw_button(config_button_img, config_button_rect)

def draw_difficulty_selection(beginner_button_rect, advanced_button_rect, back_button_rect_difficulty, mouse_pos, button_pressed):
    
    # Título
    bg_rect = text_background_img.get_rect(center=(size[0] // 2, size[1] // 2 - 200))
    screen.blit(text_background_img, bg_rect)
    difficulty_surface = render_text_with_outline(texts[language]["select_difficulty"], font_medium, white, brown)
    screen.blit(difficulty_surface, difficulty_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 200)))
    
    # Botones
    draw_button_with_text_3_state(beginner_button_rect, texts[language]["beginner"], font_small, mouse_pos, button_pressed, "beginner", normal_button_img_1, normal_button_img_3, normal_button_img_2, text_adjust_x=-40, text_adjust_y=-4)
    draw_button_with_text_3_state(advanced_button_rect, texts[language]["advanced"], font_small, mouse_pos, button_pressed, "advanced", avanzado_button_img_1, avanzado_button_img_3, avanzado_button_img_2, text_adjust_x=-41, text_adjust_y=-4)
    
    # Botón Regresar (btn_back)
    draw_3_state_button(back_button_rect_difficulty, back_button_img_1, back_button_img_3, back_button_img_2, mouse_pos, button_pressed, "back_difficulty")
    
    if show_coming_soon:
        coming_soon_text = render_text_with_outline(texts[language]["coming_soon"], font_medium, red, white)
        text_rect = coming_soon_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(coming_soon_text, text_rect)

def draw_character_selection(char1_button_rect, char2_button_rect, back_button_rect_character, mouse_pos, button_pressed):
    
    # Título
    bg_rect = text_background_img.get_rect(center=(size[0] // 2, size[1] // 2 - 200))
    screen.blit(text_background_img, bg_rect)
    select_surface = render_text_with_outline(texts[language]["select_character"], font_medium, white, brown)
    screen.blit(select_surface, select_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 200)))
    
    # Botones Personaje
    draw_3_state_button(char1_button_rect, boy_button_img_1, boy_button_img_3, boy_button_img_2, mouse_pos, button_pressed, "char_boy")
    draw_3_state_button(char2_button_rect, girl_button_img_1, girl_button_img_3, girl_button_img_2, mouse_pos, button_pressed, "char_girl")
    
    # Botón Regresar
    draw_3_state_button(back_button_rect_character, back_button_img_1, back_button_img_3, back_button_img_2, mouse_pos, button_pressed, "back_character")

def draw_level_selection(level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect_level, mouse_pos, button_pressed):
    
    # Título
    bg_rect = text_background_img.get_rect(center=(size[0] // 2, size[1] // 2 - 200))
    screen.blit(text_background_img, bg_rect)
    level_surface = render_text_with_outline(texts[language]["select_level"], font_medium, white, brown)
    screen.blit(level_surface, level_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 200)))
    
    # Botones Nivel 
    draw_button_with_text_3_state(level1_button_rect, texts[language]["level1_name"], font_small, mouse_pos, button_pressed, "lvl1", level1_button_img_1, level1_button_img_3, level1_button_img_2, text_adjust_x=-45, text_adjust_y=-4)
    draw_button_with_text_3_state(level2_button_rect, texts[language]["level2_name"], font_small, mouse_pos, button_pressed, "lvl2", level2_button_img_1, level2_button_img_3, level2_button_img_2, text_adjust_x=-41, text_adjust_y=-4)
    draw_button_with_text_3_state(level3_button_rect, texts[language]["level3_name"], font_small, mouse_pos, button_pressed, "lvl3", level3_button_img_1, level3_button_img_3, level3_button_img_2, text_adjust_x=-41, text_adjust_y=-4)
    # Botón Regresar
    draw_3_state_button(back_button_rect_level, back_button_img_1, back_button_img_3, back_button_img_2, mouse_pos, button_pressed, "back_level")
    
    if show_coming_soon:
        coming_soon_text = render_text_with_outline(texts[language]["coming_soon"], font_medium, red, white)
        text_rect = coming_soon_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(coming_soon_text, text_rect)

def draw_advanced_level_selection(level4_button_rect, level5_button_rect, level6_button_rect, back_button_rect_advanced, mouse_pos, button_pressed):
    
    # Título
    bg_rect = text_background_img.get_rect(center=(size[0] // 2, size[1] // 2 - 200))
    screen.blit(text_background_img, bg_rect)
    level_surface = render_text_with_outline(texts[language]["select_level"], font_medium, white, brown)
    screen.blit(level_surface, level_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 200)))
    
    # Botones Nivel 
    draw_button_with_text_3_state(level4_button_rect, texts[language]["level1_name"], font_small, mouse_pos, button_pressed, "lvl4", level1_button_img_1, level1_button_img_3, level1_button_img_2, text_adjust_x=-41, text_adjust_y=-4)
    draw_button_with_text_3_state(level5_button_rect, texts[language]["level2_name"], font_small, mouse_pos, button_pressed, "lvl5", level2_button_img_1, level2_button_img_3, level2_button_img_2, text_adjust_x=-41, text_adjust_y=-4)
    draw_button_with_text_3_state(level6_button_rect, texts[language]["level3_name"], font_small, mouse_pos, button_pressed, "lvl6", level3_button_img_1, level3_button_img_3, level3_button_img_2, text_adjust_x=-41, text_adjust_y=-4)
    # Botón Regresar
    draw_3_state_button(back_button_rect_advanced, back_button_img_1, back_button_img_3, back_button_img_2, mouse_pos, button_pressed, "back_advanced")
    
    if show_coming_soon:
        coming_soon_text = render_text_with_outline(texts[language]["coming_soon"], font_medium, red, white)
        text_rect = coming_soon_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(coming_soon_text, text_rect)

# -------------------- INICIALIZACIÓN DE RECTÁNGULOS --------------------
play_button_rect, quit_button_rect, config_button_rect = create_menu_buttons()
beginner_button_rect, advanced_button_rect, back_button_rect_difficulty = create_difficulty_buttons()
char1_button_rect, char2_button_rect, back_button_rect_character = create_character_buttons()
level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect_level = create_level_buttons()
level4_button_rect, level5_button_rect, level6_button_rect, back_button_rect_advanced = create_advanced_level_buttons()
continue_button_rect, menu_button_rect_pause, reset_button_rect_pause = create_pause_menu_buttons() 

# -------------------- BUCLE PRINCIPAL --------------------
running = True
button_pressed = None 

while running:
    mouse_pos = pygame.mouse.get_pos() 

    # 1. ACTUALIZACIÓN DEL MOVIMIENTO DINÁMICO Y ANIMACIÓN DEL PANEL
    # Actualiza la posición de las nubes y el globo en todos los estados del menú
    if game_state in [MENU, SELECT_DIFFICULTY, SELECT_CHARACTER, SELECT_CHARACTER2, SELECT_LEVEL, SELECT_ADVANCED_LEVEL, CONFIG_MENU, GAME_LEVEL_1]:
        for cloud in clouds:
            cloud.move()
        balloon.move()

    # Lógica de Animación de Configuración
    if game_state == CONFIG_MENU:
        if config_closing:
            # Animación de salida: deslizar hacia la izquierda
            config_panel_x = max(-PANEL_WIDTH, config_panel_x - SLIDE_SPEED)
            if config_panel_x <= -PANEL_WIDTH:
                config_panel_x = -PANEL_WIDTH
                config_closing = False
                # Vuelve al estado anterior cuando termina la animación
                if len(state_history) > 1: state_history.pop(); game_state = state_history[-1] 
        else:
            # Animación de entrada: deslizar hacia la derecha hasta el centro
            config_panel_x = min(config_target_x, config_panel_x + SLIDE_SPEED)


    if show_coming_soon and pygame.time.get_ticks() > coming_soon_timer + COMING_SOON_DURATION:
        show_coming_soon = False
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # =========================================================================
        # === 1. Lógica de PAUSA y MENU de PAUSA (CORREGIDA) ===
        # =========================================================================
        if game_state == GAME_LEVEL_1 and level_instance:
            
            # Bandera de control para saber si el nivel NO está en la pantalla de introducción
            is_level_not_in_intro = hasattr(level_instance, 'state') and level_instance.state != "controls_screen"
            
            # 1. Manejar eventos del menú de PAUSA (prioritario si ya está pausado)
            if is_paused:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if continue_button_rect.collidepoint(event.pos): button_pressed = "continue"
                    elif menu_button_rect_pause.collidepoint(event.pos): button_pressed = "main_menu"
                    elif reset_button_rect_pause.collidepoint(event.pos): button_pressed = "reset_level"
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if button_pressed == "continue" and continue_button_rect.collidepoint(event.pos):
                        is_paused = False # Salir de pausa
                        button_pressed = None
                    elif button_pressed == "main_menu" and menu_button_rect_pause.collidepoint(event.pos):
                        is_paused = False
                        game_state = MENU
                        level_instance = None
                        # **********************************************
                        # CAMBIO CLAVE: Reiniciar la música al volver al menú principal
                        pygame.mixer.music.stop() 
                        pygame.mixer.music.load('Materials/Music/Menu.wav')
                        pygame.mixer.music.play(-1)
                        # **********************************************
                        button_pressed = None
                    elif button_pressed == "reset_level" and reset_button_rect_pause.collidepoint(event.pos):
                        is_paused = False
                        # Recargar el nivel según su clase 
                        current_level_class = type(level_instance) 
                        level_instance = current_level_class(screen, size, font_small, selected_character, language)
                        button_pressed = None
                
                # Si está en pausa, NO procesamos los eventos del nivel o el botón de pausa
                continue
            
            # 2. Chequeo para ENTRAR en pausa (Solo si NO está en controles)
            if is_level_not_in_intro:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pause_button_rect.collidepoint(event.pos) and not is_paused:
                    is_paused = True # Entrar en el estado de pausa
                    button_pressed = "pause"

            # 3. El nivel maneja los eventos del juego (solo si NO está en pausa)
            returned_state = level_instance.handle_events(event,language)
            if returned_state == "menu":
                game_state = MENU
                level_instance = None
                # **********************************************
                # CAMBIO CLAVE: Reiniciar la música al volver al menú principal
                pygame.mixer.music.stop()
                pygame.mixer.music.load('Materials/Music/Menu.wav')
                pygame.mixer.music.play(-1)
                # **********************************************
            continue
            
        # Lógica de CONFIG_MENU (prioritaria para manejar clics dentro del panel)
        if game_state == CONFIG_MENU and not config_closing and config_panel_x == config_target_x:
            # Solo procesa eventos cuando el panel está totalmente abierto y no se está cerrando
            language, volume_level, action = settings_panel.update_logic(event, language, volume_level, config_panel_x)
            
            if action == "CLOSE":
                config_closing = True # Inicia animación de cierre
            continue 

        # Si NO estamos en CONFIG_MENU o GAME_LEVEL_1, procesamos los eventos normales
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            # --- Lógica de Botones REGRESAR ---
            if game_state == SELECT_DIFFICULTY and back_button_rect_difficulty.collidepoint(event.pos):
                button_pressed = "back_difficulty"
            elif game_state == SELECT_CHARACTER and back_button_rect_character.collidepoint(event.pos):
                button_pressed = "back_character"
            elif game_state == SELECT_CHARACTER2 and back_button_rect_character.collidepoint(event.pos):
                button_pressed = "back_character"
            elif game_state == SELECT_LEVEL and back_button_rect_level.collidepoint(event.pos):
                button_pressed = "back_level"
            elif game_state == SELECT_ADVANCED_LEVEL and back_button_rect_advanced.collidepoint(event.pos):
                button_pressed = "back_advanced"
            
            # --- Lógica de botones de MENÚ ---
            elif game_state == MENU:
                if play_button_rect.collidepoint(event.pos): button_pressed = "play"
                elif quit_button_rect.collidepoint(event.pos): button_pressed = "quit"
                elif config_button_rect.collidepoint(event.pos): button_pressed = "config"
            
            # --- Lógica de botones de DIFICULTAD, PERSONAJE, NIVELES ---
            elif game_state == SELECT_DIFFICULTY:
                if beginner_button_rect.collidepoint(event.pos): button_pressed = "beginner"
                elif advanced_button_rect.collidepoint(event.pos): button_pressed = "advanced"
            
            elif game_state == SELECT_CHARACTER or game_state == SELECT_CHARACTER2:
                if char1_button_rect.collidepoint(event.pos): button_pressed = "char_boy"
                elif char2_button_rect.collidepoint(event.pos): button_pressed = "char_girl"
            
            elif game_state == SELECT_LEVEL:
                if level1_button_rect.collidepoint(event.pos): button_pressed = "lvl1"
                elif level2_button_rect.collidepoint(event.pos): button_pressed = "lvl2"
                elif level3_button_rect.collidepoint(event.pos): button_pressed = "lvl3"
                
            elif game_state == SELECT_ADVANCED_LEVEL:
                if level4_button_rect.collidepoint(event.pos): button_pressed = "lvl4"
                elif level5_button_rect.collidepoint(event.pos): button_pressed = "lvl5"
                elif level6_button_rect.collidepoint(event.pos): button_pressed = "lvl6"
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            
            # Lógica de REGRESAR
            if button_pressed and "back_" in button_pressed and eval(button_pressed.replace('back_', 'back_button_rect_')).collidepoint(event.pos):
                if len(state_history) > 1: state_history.pop(); game_state = state_history[-1]; show_coming_soon = False
                button_pressed = None # Importante: resetear button_pressed después de usarlo

            # Lógica de MENU
            elif button_pressed == "play" and play_button_rect.collidepoint(event.pos):
                game_state = SELECT_DIFFICULTY; state_history.append(game_state)
            elif button_pressed == "quit" and quit_button_rect.collidepoint(event.pos):
                running = False
            
            # Lógica de CONFIGURACIÓN (Inicia animación de entrada)
            elif button_pressed == "config" and config_button_rect.collidepoint(event.pos):
                game_state = CONFIG_MENU; state_history.append(game_state)
                config_panel_x = -PANEL_WIDTH # Inicia desde fuera de pantalla
                config_closing = False
            
            # Lógica de DIFICULTAD
            elif button_pressed == "beginner" and beginner_button_rect.collidepoint(event.pos):
                is_advanced = False
                game_state = SELECT_CHARACTER; state_history.append(game_state); show_coming_soon = False
            elif button_pressed == "advanced" and advanced_button_rect.collidepoint(event.pos):
                is_advanced = True
                game_state = SELECT_CHARACTER2; state_history.append(game_state); show_coming_soon = False

            # Lógica de PERSONAJE
            elif (button_pressed == "char_boy" and char1_button_rect.collidepoint(event.pos)) or \
                 (button_pressed == "char_girl" and char2_button_rect.collidepoint(event.pos)):
                selected_character = "boy" if button_pressed == "char_boy" else "girl"
                if game_state == SELECT_CHARACTER:
                    game_state = SELECT_LEVEL; state_history.append(game_state)
                elif game_state == SELECT_CHARACTER2:
                    game_state = SELECT_ADVANCED_LEVEL; state_history.append(game_state)
                
            # Lógica de NIVELES NORMALES/AVANZADOS (Inicia el nivel)
            elif (button_pressed == "lvl1" and level1_button_rect.collidepoint(event.pos)) or \
                 (button_pressed == "lvl2" and level2_button_rect.collidepoint(event.pos)) or \
                 (button_pressed == "lvl3" and level3_button_rect.collidepoint(event.pos)) or \
                 (button_pressed == "lvl4" and level4_button_rect.collidepoint(event.pos)) or \
                 (button_pressed == "lvl5" and level5_button_rect.collidepoint(event.pos)) or \
                 (button_pressed == "lvl6" and level6_button_rect.collidepoint(event.pos)):
                
                # Detener la música del menú al iniciar un nivel
                pygame.mixer.music.stop() 
                
                # Determinar e iniciar el nivel
                if button_pressed == "lvl1":
                    level_instance = Level1F.Level1(screen, size, font_small, selected_character, language)
                elif button_pressed == "lvl2":
                    level_instance = Level2F.Level2(screen, size, font_small, selected_character, language)
                elif button_pressed == "lvl3":
                    level_instance = Level3F.Level3(screen, size, font_small, selected_character, language) 
                elif button_pressed == "lvl4":
                    level_instance = Level4F.Level4(screen, size, font_small, selected_character, language)
                elif button_pressed == "lvl5":
                    level_instance = Level5F.Level5(screen, size, font_small, selected_character, language) 
                elif button_pressed == "lvl6":
                    level_instance = Level6F.Level6(screen, size, font_small, selected_character, language) 
                
                game_state = GAME_LEVEL_1
                show_coming_soon = False
                

            button_pressed = None 

# -------------------- DIBUJAR --------------------
    if game_state == GAME_LEVEL_1 and level_instance:
         # Pasa la bandera de pausa al método update del nivel
        level_state = level_instance.update(is_paused, language) 
        
        # 💡 DEPURATION: Imprime el estado actual del nivel en la consola
        if hasattr(level_instance, 'state'):
            pass # print(f"Level State: {level_instance.state}") 
        
        if level_state == "quit":
            running = False
        elif level_state == "menu":
            game_state = MENU
            level_instance = None
            # **********************************************
            # CAMBIO CLAVE: Reiniciar la música al volver al menú principal (desde el nivel)
            pygame.mixer.music.stop()
            pygame.mixer.music.load('Materials/Music/Menu.wav')
            pygame.mixer.music.play(-1)
            # **********************************************
            is_paused = False # Asegurar que la pausa se desactive
        else:
            level_instance.draw(language)
            
            # Comprobación de que el nivel tiene la propiedad 'state' y que NO es 'controls_screen'
            is_level_not_in_intro = hasattr(level_instance, 'state') and level_instance.state != "controls_screen"

            # DIBUJAR EL BOTÓN DE PAUSA SOBRE EL NIVEL (solo si NO está en pausa y el juego NO está en intro)
            if not is_paused and is_level_not_in_intro:
                current_pause_img = pause_button_img_2 if button_pressed == "pause" and pause_button_rect.collidepoint(mouse_pos) else \
                                    pause_button_img_3 if pause_button_rect.collidepoint(mouse_pos) else \
                                    pause_button_img_1
                screen.blit(current_pause_img, pause_button_rect)

            # Si está en pausa, dibujar el menú de pausa
            if is_paused:
                # Semi-transparente de fondo
                s = pygame.Surface(size, pygame.SRCALPHA)
                s.fill((0, 0, 0, 150)) # Negro con 150 de transparencia (de 255)
                screen.blit(s, (0, 0))
                
                # Título "PAUSA"
                pause_text = render_text_with_outline(texts[language]["pause"], font_large, white, black)
                screen.blit(pause_text, pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 150)))
                
                # Botón Continuar
                draw_button_with_text_3_state(
                    continue_button_rect, "", font_medium, mouse_pos, button_pressed, 
                    "continue", btn_continue1, btn_continue3, btn_continue2, 
                    text_adjust_x=-40, text_adjust_y=-4)
                draw_button_with_text_3_state(
                    reset_button_rect_pause, "", font_medium, mouse_pos, button_pressed, 
                    "reset_level", btn_reset1, btn_reset3, btn_reset2, 
                    text_adjust_x=-40, text_adjust_y=-4)
                # Botón Menú Principal
                draw_button_with_text_3_state(
                    menu_button_rect_pause,"", font_medium, mouse_pos, button_pressed, 
                    "main_menu", btn_menu1, btn_menu3, btn_menu2, 
                    text_adjust_x=-40, text_adjust_y=-4)
            
    else:
        # 1. DIBUJAR FONDO Y ELEMENTOS DINÁMICOS (Siempre visibles)
        screen.blit(sky_background, [0, 0])
        for cloud in clouds:
            cloud.draw(screen)
        balloon.draw(screen)
        
        # 2. DIBUJAR FOREGROUND DE LA ESCUELA (Principal o Secundaria)
        if game_state == MENU or game_state == CONFIG_MENU or config_closing:
            # Escuela principal para el menú base y cuando el panel se desliza sobre él
            screen.blit(school_foreground_img, school_rect) 
        elif game_state in [SELECT_DIFFICULTY, SELECT_CHARACTER, SELECT_CHARACTER2, SELECT_LEVEL, SELECT_ADVANCED_LEVEL]:
            # Escuela secundaria para sub-menús
            screen.blit(school_secondary_img, school_secondary_rect)

        # 3. DIBUJAR ELEMENTOS ESPECÍFICOS DEL ESTADO
        if game_state == MENU:
            draw_menu(play_button_rect, quit_button_rect, config_button_rect, mouse_pos, button_pressed)
        elif game_state == SELECT_DIFFICULTY:
            draw_difficulty_selection(beginner_button_rect, advanced_button_rect, back_button_rect_difficulty, mouse_pos, button_pressed)
        elif game_state == SELECT_CHARACTER:
            draw_character_selection(char1_button_rect, char2_button_rect, back_button_rect_character, mouse_pos, button_pressed)
        elif game_state == SELECT_LEVEL:
            draw_level_selection(level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect_level, mouse_pos, button_pressed)
        elif game_state == SELECT_CHARACTER2: 
            draw_character_selection(char1_button_rect, char2_button_rect, back_button_rect_character, mouse_pos, button_pressed)
        elif game_state == SELECT_ADVANCED_LEVEL:
            draw_advanced_level_selection(level4_button_rect, level5_button_rect, level6_button_rect, back_button_rect_advanced, mouse_pos, button_pressed)
        
        # 4. DIBUJAR EL PANEL DE CONFIGURACIÓN POR ENCIMA (Si está activo o cerrándose)
        if game_state == CONFIG_MENU or config_closing: 
            settings_panel.draw(language, volume_level, mouse_pos, config_panel_x) 


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()