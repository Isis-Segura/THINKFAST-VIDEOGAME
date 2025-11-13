import pygame, sys
import Levels.Level1F as Level1F
import Levels.Level2F as Level2F
import Levels.Level3F as Level3F
# Importa las clases de movimiento y la función del video
from Interacciones.Menu_Dynamics import Cloud, HotAirBalloon 
from Interacciones.Intro_Video import run_intro_video 

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

# -------------------- EJECUCIÓN DEL VIDEO DE INTRODUCCIÓN --------------------
run_intro_video(screen, size)

# -------------------- IMÁGENES Y BOTONES --------------------
# Carga de Fondos
sky_background = pygame.image.load("Materials/Pictures/Assets/sky_background.png").convert() 
sky_background = pygame.transform.scale(sky_background, size)

# Elementos dinámicos y primer plano
cloud_img = pygame.image.load("Materials/Pictures/Assets/cloud.png").convert_alpha()
balloon_img = pygame.image.load("Materials/Pictures/Assets/hot_air_balloon.png").convert_alpha()

# --- IMAGEN DE ESCUELA PRINCIPAL (Para MENU) ---
# Se utiliza el archivo cargado: school_foreground.jpg
# NOTA: Tu código original usa "school_foreground.png", asumimos que quieres usar el cargado.
try:
    school_foreground_img = pygame.image.load("school_foreground.jpg").convert_alpha()
except:
    # Si la carga falla por no ser PNG o no encontrar el archivo, se usa la ruta original
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

# Botones de Idioma (btn_spanish/btn_english)
spanish_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_spanish1.png").convert_alpha()
spanish_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_spanish3.png").convert_alpha()
spanish_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_spanish2.png").convert_alpha()
english_button_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_english1.png").convert_alpha()
english_button_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_english3.png").convert_alpha()
english_button_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_english2.png").convert_alpha()

# Botones de Volumen (+/-) (btn_mas/btn_menos)
volume_up_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_mas1.png").convert_alpha()
volume_up_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_mas3.png").convert_alpha()
volume_up_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_mas2.png").convert_alpha()
volume_down_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_menos1.png").convert_alpha()
volume_down_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_menos3.png").convert_alpha()
volume_down_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_menos2.png").convert_alpha()

# Thumb del Slider (btn_subir_bajar)
volume_thumb_img_1 = pygame.image.load("Materials/Pictures/Assets/btn_subir_bajar1.png").convert_alpha()
volume_thumb_img_3 = pygame.image.load("Materials/Pictures/Assets/btn_subir_bajar3.png").convert_alpha()
volume_thumb_img_2 = pygame.image.load("Materials/Pictures/Assets/btn_subir_bajar2.png").convert_alpha()


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
button_pressed = None # Variable para rastrear el estado Clicked

# Reemplaza completamente tu diccionario 'texts' con este:
texts = {
    "es": {
        "play": "Jugar", "quit": "Salir", "config": "Configuración",
        "volume": "Volumen", "language": "Idioma", "back": "Regresar",
        "spanish": "Español", "english": "Inglés", "title_config": "Menú de Configuración",
        "select_difficulty": "Selecciona la dificultad", "beginner": "Normal", "advanced": "Avanzado",
        "select_character": "Selecciona tu personaje", "boy": "Niño", "girl": "Niña",
        
        "select_level": "Selecciona el desafío", 
        "level1_name": "Entrada",  
        "level2_name": "Pasillo",  
        "level3_name": "Salón",  
        "coming_soon": "¡Proximamente!"
    },
    "en": {
        "play": "Play", "quit": "Quit", "config": "Settings",
        "volume": "Volume", "language": "Language", "back": "Back",
        "spanish": "Spanish", "english": "English", "title_config": "Settings Menu",
        "select_difficulty": "Select difficulty", "beginner": "Beginner", "advanced": "Advanced",
        "select_character": "Select your character", "boy": "Boy", "girl": "Girl",
        
        "select_level": "Select the challenge", 
        "level1_name": "Learn to Add", 
        "level2_name": "Multiply Fast", 
        "level3_name": "Equations", 
        "coming_soon": "Coming soon!"
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
    
    # text_adjust_x y text_adjust_y ahora son parámetros de la función
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
        
        # Aplicamos el desplazamiento y los ajustes de alineación
        text_rect = text_surface.get_rect(
            center=(
                rect.center[0] + text_adjust_x,             # Centro X del botón + ajuste constante (PARÁMETRO)
                rect.center[1] + text_adjust_y + text_offset_y  # Centro Y del botón + ajuste constante (PARÁMETRO) + hundimiento
            )
        )
        
        screen.blit(text_surface, text_rect)
    return rect

def draw_volume_slider(x, y, width, height, volume, thumb_img_1, thumb_img_3, thumb_img_2, mouse_pos, dragging):
    """Dibuja la barra de volumen y el thumb con imagen (btn_subir_bajar)."""
    
    # Dibujar la barra
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), border_radius=10)
    fill_width = int(width * volume)
    pygame.draw.rect(screen, pink, (x, y, fill_width, height), border_radius=10)
    pygame.draw.rect(screen, black, (x, y, width, height), 2, border_radius=10)
    
    # Dibujar el thumb (btn_subir_bajar)
    thumb_x = x + fill_width
    thumb_y = y + height // 2
    
    thumb_size = (50, 35) 
    thumb_rect = pygame.Rect(0, 0, thumb_size[0], thumb_size[1])
    thumb_rect.center = (thumb_x, thumb_y)
    
    # Lógica de 3 estados para el thumb de volumen
    if dragging:
        thumb_image = volume_thumb_img_2 # Clicked state
    elif thumb_rect.collidepoint(mouse_pos):
        thumb_image = volume_thumb_img_3 # Hover state
    else:
        thumb_image = volume_thumb_img_1 # Normal state
        
    scaled_thumb = pygame.transform.scale(thumb_image, thumb_size)
    screen.blit(scaled_thumb, thumb_rect)
    
    # Devolvemos el rect del área de arrastre (la barra)
    return pygame.Rect(x, y, width, height)


def create_menu_buttons():
    play_button_rect = pygame.Rect(0, 0, 190, 80); play_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 50)
    quit_button_rect = pygame.Rect(0, 0, 190, 80); quit_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 50)
    config_button_rect = pygame.Rect(0, 0, 190, 80); config_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 150)
    return play_button_rect, quit_button_rect, config_button_rect

def create_difficulty_buttons():
    # Usando el tamaño de los botones btn_normal
    btn_w, btn_h = 260, 80 
    beginner_button_rect = pygame.Rect(0, 0, btn_w, btn_h); beginner_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 60)
    advanced_button_rect = pygame.Rect(0, 0, 290, btn_h); advanced_button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 40)
    back_button_rect = pygame.Rect(0, 0, 160, 80); back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    return beginner_button_rect, advanced_button_rect, back_button_rect

def create_character_buttons():
    char1_button_rect = pygame.Rect(0, 0, 150, 330); char1_button_rect.center = (screen.get_width() // 2 - 150, screen.get_height() // 2 + 20)
    char2_button_rect = pygame.Rect(0, 0, 150, 330); char2_button_rect.center = (screen.get_width() // 2 + 150, screen.get_height() // 2 + 20)
    back_button_rect = pygame.Rect(0, 0, 160, 80); back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    return char1_button_rect, char2_button_rect, back_button_rect

# *** FUNCIÓN MODIFICADA PARA EVITAR SUPERPOSICIÓN DE BOTONES ***
def create_level_buttons():
    btn_w, btn_h = 270, 80
    center_x = screen.get_width() // 2
    
    # Espacio vertical entre botones
    spacing_y = btn_h + 30 

    # Nivel 1 (Arriba)
    level1_button_rect = pygame.Rect(0, 0, btn_w, btn_h)
    level1_button_rect.center = (center_x - 100, screen.get_height() // 2 - spacing_y)
    
    # Nivel 2 (Medio)
    level2_button_rect = pygame.Rect(0, 0, btn_w, btn_h)
    level2_button_rect.center = (center_x, screen.get_height() // 2)
    
    # Nivel 3 (Abajo)
    level3_button_rect = pygame.Rect(0, 0, btn_w, btn_h)
    level3_button_rect.center = (center_x + 100, screen.get_height() // 2 + spacing_y)
    
    back_button_rect = pygame.Rect(0, 0, 160, 80)
    back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    
    return level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect
# ***************************************************************


def create_config_buttons():
    back_button_rect = pygame.Rect(0, 0, 160, 80); back_button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)
    return back_button_rect

# -------------------- FUNCIONES DE DIBUJO DE PANTALLAS --------------------
def draw_menu(play_button_rect, quit_button_rect, config_button_rect, mouse_pos, button_pressed):
    
    # Fondo Dinámico y Escuela Principal
    screen.blit(sky_background, [0, 0])
    for cloud in clouds:
        cloud.draw(screen)
    balloon.draw(screen)
    screen.blit(school_foreground_img, school_rect) 
    
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
    
    # Fondo Dinámico y ESCUELA SECUNDARIA
    screen.blit(sky_background, [0, 0])
    for cloud in clouds:
        cloud.draw(screen)
    balloon.draw(screen)
    screen.blit(school_secondary_img, school_secondary_rect) 
    
    # Título
    bg_rect = text_background_img.get_rect(center=(size[0] // 2, size[1] // 2 - 200))
    screen.blit(text_background_img, bg_rect)
    difficulty_surface = render_text_with_outline(texts[language]["select_difficulty"], font_medium, white, brown)
    screen.blit(difficulty_surface, difficulty_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 200)))
    
    # AJUSTE PARA DIFICULTAD: El texto ahora estará centrado (0, 0)
    draw_button_with_text_3_state(beginner_button_rect, texts[language]["beginner"], font_small, mouse_pos, button_pressed, "beginner", normal_button_img_1, normal_button_img_3, normal_button_img_2, text_adjust_x=-40, text_adjust_y=-4)
    draw_button_with_text_3_state(advanced_button_rect, texts[language]["advanced"], font_small, mouse_pos, button_pressed, "advanced", avanzado_button_img_1, avanzado_button_img_3, avanzado_button_img_2, text_adjust_x=-41, text_adjust_y=-4)
    
    # Botón Regresar (btn_back)
    draw_3_state_button(back_button_rect_difficulty, back_button_img_1, back_button_img_3, back_button_img_2, mouse_pos, button_pressed, "back_difficulty")
    
    if show_coming_soon:
        coming_soon_text = render_text_with_outline(texts[language]["coming_soon"], font_medium, red, white)
        text_rect = coming_soon_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(coming_soon_text, text_rect)

def draw_character_selection(char1_button_rect, char2_button_rect, back_button_rect_character, mouse_pos, button_pressed):
    
    # Fondo Dinámico y ESCUELA SECUNDARIA
    screen.blit(sky_background, [0, 0])
    for cloud in clouds:
        cloud.draw(screen)
    balloon.draw(screen)
    screen.blit(school_secondary_img, school_secondary_rect) 
    
    # Título
    bg_rect = text_background_img.get_rect(center=(size[0] // 2, size[1] // 2 - 200))
    screen.blit(text_background_img, bg_rect)
    select_surface = render_text_with_outline(texts[language]["select_character"], font_medium, white, brown)
    screen.blit(select_surface, select_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 200)))
    
    # Botones Personaje (btn_boy/btn_girl) - SIN TEXTO
    draw_3_state_button(char1_button_rect, boy_button_img_1, boy_button_img_3, boy_button_img_2, mouse_pos, button_pressed, "char_boy")
    draw_3_state_button(char2_button_rect, girl_button_img_1, girl_button_img_3, girl_button_img_2, mouse_pos, button_pressed, "char_girl")
    
    # Botón Regresar (btn_back) - SIN TEXTO
    draw_3_state_button(back_button_rect_character, back_button_img_1, back_button_img_3, back_button_img_2, mouse_pos, button_pressed, "back_character")

def draw_level_selection(level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect_level, mouse_pos, button_pressed):
    
    # Fondo Dinámico y ESCUELA SECUNDARIA
    screen.blit(sky_background, [0, 0])
    for cloud in clouds:
        cloud.draw(screen)
    balloon.draw(screen)
    screen.blit(school_secondary_img, school_secondary_rect) 
    
    # Título
    bg_rect = text_background_img.get_rect(center=(size[0] // 2, size[1] // 2 - 200))
    screen.blit(text_background_img, bg_rect)
    level_surface = render_text_with_outline(texts[language]["select_level"], font_medium, white, brown)
    screen.blit(level_surface, level_surface.get_rect(center=(size[0] // 2, size[1] // 2 - 200)))
    
    # Botones Nivel con texto y 3 estados de imagen (btn_normal)
    # AJUSTE PARA NIVELES: El texto ahora estará centrado (0, 0)
    draw_button_with_text_3_state(level1_button_rect, texts[language]["level1_name"], font_small, mouse_pos, button_pressed, "lvl1", level1_button_img_1, level1_button_img_3, level1_button_img_2, text_adjust_x=-41, text_adjust_y=-4)
    draw_button_with_text_3_state(level2_button_rect, texts[language]["level2_name"], font_small, mouse_pos, button_pressed, "lvl2", level2_button_img_1, level2_button_img_3, level2_button_img_2, text_adjust_x=-41, text_adjust_y=-4)
    draw_button_with_text_3_state(level3_button_rect, texts[language]["level3_name"], font_small, mouse_pos, button_pressed, "lvl3", level3_button_img_1, level3_button_img_3, level3_button_img_2, text_adjust_x=-41, text_adjust_y=-4)
    # Botón Regresar (btn_back) - SIN TEXTO
    draw_3_state_button(back_button_rect_level, back_button_img_1, back_button_img_3, back_button_img_2, mouse_pos, button_pressed, "back_level")
    
    if show_coming_soon:
        coming_soon_text = render_text_with_outline(texts[language]["coming_soon"], font_medium, red, white)
        text_rect = coming_soon_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(coming_soon_text, text_rect)

def draw_config_menu(back_button_rect_config, mouse_pos, button_pressed, dragging_volume):
    
    # Fondo Dinámico y ESCUELA SECUNDARIA
    screen.blit(sky_background, [0, 0])
    for cloud in clouds:
        cloud.draw(screen)
    balloon.draw(screen)
    screen.blit(school_secondary_img, school_secondary_rect) 
    
    center_x = size[0] // 2
    
    # Título
    bg_rect = text_background_img.get_rect(center=(center_x, 120))
    screen.blit(text_background_img, bg_rect)
    title_surface = render_text_with_outline(texts[language]["title_config"], font_medium, white, brown)
    screen.blit(title_surface, title_surface.get_rect(center=(center_x, 120)))
    
    # --- IDIOMA ---
    lang_y = 220
    lang_label = render_text_with_outline(f"{texts[language]['language']}:", font_medium, white, brown)
    screen.blit(lang_label, lang_label.get_rect(center=(center_x, lang_y)))
    
    flag_button_width, flag_button_height = 140, 70
    flag_spacing = 30
    global language_es_rect, language_en_rect
    
    # Botón Español (btn_spanish)
    language_es_rect = pygame.Rect(0, 0, flag_button_width, flag_button_height)
    language_es_rect.center = (center_x - flag_button_width//2 - flag_spacing, lang_y + 50)
    
    # Lógica de dibujo para ESPAÑOL: Usa img_2 si 'language' es "es" (o si está haciendo clic)
    if language == "es":
        es_image = spanish_button_img_2
    elif button_pressed == "lang_es": # Mantiene el estado de clic momentáneo
        es_image = spanish_button_img_2
    elif language_es_rect.collidepoint(mouse_pos):
        es_image = spanish_button_img_3
    else:
        es_image = spanish_button_img_1
    draw_button(es_image, language_es_rect) # Dibuja el botón con la imagen determinada
    
    # Botón Inglés (btn_english)
    language_en_rect = pygame.Rect(0, 0, flag_button_width, flag_button_height)
    language_en_rect.center = (center_x + flag_button_width//2 + flag_spacing, lang_y + 50)

    # Lógica de dibujo para INGLÉS: Usa img_2 si 'language' es "en" (o si está haciendo clic)
    if language == "en":
        en_image = english_button_img_2
    elif button_pressed == "lang_en": # Mantiene el estado de clic momentáneo
        en_image = english_button_img_2
    elif language_en_rect.collidepoint(mouse_pos):
        en_image = english_button_img_3
    else:
        en_image = english_button_img_1
    draw_button(en_image, language_en_rect) # Dibuja el botón con la imagen determinada
    
    # --- VOLUMEN ---
    vol_y = 220 + 140
    vol_label = render_text_with_outline(f"{texts[language]['volume']}: {int(volume_level * 100)}%", font_medium, white, brown)
    screen.blit(vol_label, vol_label.get_rect(center=(center_x, vol_y)))
    
    slider_width, slider_height = 400, 20
    global volume_slider_rect, volume_down_rect, volume_up_rect
    
    # Slider con thumb de imagen
    volume_slider_rect = draw_volume_slider(center_x - slider_width//2, vol_y + 40, slider_width, slider_height, volume_level, volume_thumb_img_1, volume_thumb_img_3, volume_thumb_img_2, mouse_pos, dragging_volume)
    
    vol_button_width, vol_button_height = 85, 55
    vol_button_spacing = 250
    
    # Botón Menos (btn_menos)
    volume_down_rect = pygame.Rect(0, 0, vol_button_width, vol_button_height)
    volume_down_rect.center = (center_x - vol_button_spacing//2, vol_y + 100)
    draw_3_state_button(volume_down_rect, volume_down_img_1, volume_down_img_3, volume_down_img_2, mouse_pos, button_pressed, "vol_down")
    
    # Botón Más (btn_mas)
    volume_up_rect = pygame.Rect(0, 0, vol_button_width, vol_button_height)
    volume_up_rect.center = (center_x + vol_button_spacing//2, vol_y + 100)
    draw_3_state_button(volume_up_rect, volume_up_img_1, volume_up_img_3, volume_up_img_2, mouse_pos, button_pressed, "vol_up")
    
    # Botón Regresar (btn_back) - SIN TEXTO
    back_button_rect_config.center = (center_x, size[1] - 100)
    draw_3_state_button(back_button_rect_config, back_button_img_1, back_button_img_3, back_button_img_2, mouse_pos, button_pressed, "back_config")

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
button_pressed = None 

while running:
    mouse_pos = pygame.mouse.get_pos() 

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
            continue 
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            # --- Lógica de Botones REGRESAR (Ajuste para estado 'clicked') ---
            if game_state == SELECT_DIFFICULTY and back_button_rect_difficulty.collidepoint(event.pos):
                button_pressed = "back_difficulty"
            elif game_state == SELECT_CHARACTER and back_button_rect_character.collidepoint(event.pos):
                button_pressed = "back_character"
            elif game_state == SELECT_LEVEL and back_button_rect_level.collidepoint(event.pos):
                button_pressed = "back_level"
            elif game_state == CONFIG_MENU and back_button_rect_config.collidepoint(event.pos):
                button_pressed = "back_config"
            
            # --- Lógica de botones de MENÚ (Establecer estado 'clicked') ---
            elif game_state == MENU:
                if play_button_rect.collidepoint(event.pos): button_pressed = "play"
                elif quit_button_rect.collidepoint(event.pos): button_pressed = "quit"
                elif config_button_rect.collidepoint(event.pos): button_pressed = "config"
            
            # --- Lógica de botones de CONFIGURACIÓN (Establecer estado 'clicked') ---
            elif game_state == CONFIG_MENU:
                if language_es_rect and language_es_rect.collidepoint(event.pos):
                    button_pressed = "lang_es"
                elif language_en_rect and language_en_rect.collidepoint(event.pos):
                    button_pressed = "lang_en"
                elif volume_down_rect and volume_down_rect.collidepoint(event.pos):
                    button_pressed = "vol_down"
                elif volume_up_rect and volume_up_rect.collidepoint(event.pos):
                    button_pressed = "vol_up"
                elif volume_slider_rect and volume_slider_rect.collidepoint(event.pos):
                    # Solo iniciar arrastre si hace click en el slider
                    dragging_volume = True
            
            # --- Lógica de botones de DIFICULTAD (Establecer estado 'clicked') ---
            elif game_state == SELECT_DIFFICULTY:
                if beginner_button_rect.collidepoint(event.pos):
                    button_pressed = "beginner"
                elif advanced_button_rect.collidepoint(event.pos):
                    button_pressed = "advanced"
            
            # --- Lógica de botones de PERSONAJE (Establecer estado 'clicked') ---
            elif game_state == SELECT_CHARACTER:
                if char1_button_rect.collidepoint(event.pos):
                    button_pressed = "char_boy"
                elif char2_button_rect.collidepoint(event.pos):
                    button_pressed = "char_girl"
            
            # --- Lógica de botones de SELECCIÓN DE NIVEL (Establecer estado 'clicked') ---
            elif game_state == SELECT_LEVEL:
                if level1_button_rect.collidepoint(event.pos): button_pressed = "lvl1"
                elif level2_button_rect.collidepoint(event.pos): button_pressed = "lvl2"
                elif level3_button_rect.collidepoint(event.pos): button_pressed = "lvl3"
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            
            # --- Ejecutar la acción al soltar el botón (solo si estaba 'clicked' y el mouse sigue encima) ---
            
            # Lógica de REGRESAR
            if button_pressed and "back_" in button_pressed and eval(button_pressed.replace('back_', 'back_button_rect_')).collidepoint(event.pos):
                if len(state_history) > 1: state_history.pop(); game_state = state_history[-1]; show_coming_soon = False

            # Lógica de MENU
            elif button_pressed == "play" and play_button_rect.collidepoint(event.pos):
                game_state = SELECT_DIFFICULTY; state_history.append(game_state)
            elif button_pressed == "quit" and quit_button_rect.collidepoint(event.pos):
                running = False
            elif button_pressed == "config" and config_button_rect.collidepoint(event.pos):
                game_state = CONFIG_MENU; state_history.append(game_state)
            
            # Lógica de DIFICULTAD
            elif button_pressed == "beginner" and beginner_button_rect.collidepoint(event.pos):
                is_advanced = False
                game_state = SELECT_CHARACTER; state_history.append(game_state); show_coming_soon = False
            elif button_pressed == "advanced" and advanced_button_rect.collidepoint(event.pos):
                if not show_coming_soon:
                    show_coming_soon = True
                    coming_soon_timer = pygame.time.get_ticks()
                    
            # Lógica de PERSONAJE
            elif button_pressed == "char_boy" and char1_button_rect.collidepoint(event.pos):
                selected_character = "boy"
                game_state = SELECT_LEVEL; state_history.append(game_state)
            elif button_pressed == "char_girl" and char2_button_rect.collidepoint(event.pos):
                selected_character = "girl"
                game_state = SELECT_LEVEL; state_history.append(game_state)
                
            # Lógica de NIVELES (Esta parte es la que abre el nivel, y es la misma que ya tenías)
            elif button_pressed == "lvl1" and level1_button_rect.collidepoint(event.pos):
                game_state = GAME_LEVEL_1
                level_instance = Level1F.Level1(screen, size, font_small, selected_character)
                show_coming_soon = False
            elif button_pressed == "lvl2" and level2_button_rect.collidepoint(event.pos):
                game_state = GAME_LEVEL_1
                level_instance = Level2F.Level2(screen, size, font_small, selected_character)
                show_coming_soon = False
            elif button_pressed == "lvl3" and level3_button_rect.collidepoint(event.pos):
                game_state = GAME_LEVEL_1
                level_instance = Level3F.Level3(screen, size, font_small, selected_character) 
                show_coming_soon = False

            # Lógica de CONFIGURACIÓN
            elif button_pressed == "lang_es" and language_es_rect.collidepoint(event.pos):
                language = "es"
            elif button_pressed == "lang_en" and language_en_rect.collidepoint(event.pos):
                language = "en"
            elif button_pressed == "vol_down" and volume_down_rect.collidepoint(event.pos):
                volume_level = max(0.0, volume_level - 0.1); pygame.mixer.music.set_volume(volume_level)
            elif button_pressed == "vol_up" and volume_up_rect.collidepoint(event.pos):
                volume_level = min(1.0, volume_level + 0.1); pygame.mixer.music.set_volume(volume_level)
                
            dragging_volume = False
            button_pressed = None # Limpiar el estado 'clicked'
            
        elif event.type == pygame.MOUSEMOTION and dragging_volume:
            if volume_slider_rect:
                relative_x = event.pos[0] - volume_slider_rect.left
                volume_level = max(0.0, min(1.0, relative_x / volume_slider_rect.width))
                pygame.mixer.music.set_volume(volume_level)

    # ACTUALIZACIÓN DEL MOVIMIENTO DINÁMICO (en todas las pantallas de menú)
    if game_state == MENU or game_state == SELECT_DIFFICULTY or game_state == SELECT_CHARACTER or game_state == SELECT_LEVEL or game_state == CONFIG_MENU:
        for cloud in clouds:
            cloud.move()
        balloon.move()

    # -------------------- DIBUJAR --------------------
    if game_state == MENU:
        draw_menu(play_button_rect, quit_button_rect, config_button_rect, mouse_pos, button_pressed)
    elif game_state == SELECT_DIFFICULTY:
        draw_difficulty_selection(beginner_button_rect, advanced_button_rect, back_button_rect_difficulty, mouse_pos, button_pressed)
    elif game_state == SELECT_CHARACTER:
        draw_character_selection(char1_button_rect, char2_button_rect, back_button_rect_character, mouse_pos, button_pressed)
    elif game_state == SELECT_LEVEL:
        draw_level_selection(level1_button_rect, level2_button_rect, level3_button_rect, back_button_rect_level, mouse_pos, button_pressed)
    elif game_state == CONFIG_MENU:
        draw_config_menu(back_button_rect_config, mouse_pos, button_pressed, dragging_volume)
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
