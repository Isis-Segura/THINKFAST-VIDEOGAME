import pygame, sys
import Level1

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
pygame.display.set_caption("Think Fast!")

# Fuentes
font_large = pygame.font.Font(None, 80)
font_medium = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 40)

# Carga de recursos del menú
titulo = pygame.image.load("Materials/Pictures/Assets/titulo.png").convert()
titulo.set_colorkey([0, 0, 0])
titulob = pygame.transform.scale(titulo, (sizetitulo))
background = pygame.image.load("Materials/Pictures/Assets/background.png").convert()
imageb = pygame.transform.scale(background, (size))
clock = pygame.time.Clock()

# ================================
# Carga de imágenes para los botones
# ================================
button_play_img = pygame.image.load("Materials/Pictures/Assets/botonplay.png").convert_alpha()
button_quit_img = pygame.image.load("Materials/Pictures/Assets/botonSmall.png").convert_alpha()
button_difficulty_img = pygame.image.load("Materials/Pictures/Assets/botonGrandeT.png").convert_alpha()
button_character_img = pygame.image.load("Materials/Pictures/Assets/botonSmall.png").convert_alpha()
button_level_img = pygame.image.load("Materials/Pictures/Assets/botonSmall.png").convert_alpha()
button_back_img = pygame.image.load("Materials/Pictures/Assets/botonSmall.png").convert_alpha()

# Función genérica para dibujar botones con imagen y texto
def draw_image_button(image, rect, text, font, text_color):
    img_scaled = pygame.transform.scale(image, (rect.width, rect.height))
    screen.blit(img_scaled, rect.topleft)
    text_surf = font.render(text, True, text_color)
    screen.blit(text_surf, text_surf.get_rect(center=rect.center))

# Estados del juego
MENU = 0
SELECT_DIFFICULTY = 1
SELECT_CHARACTER = 2
SELECT_LEVEL = 3
GAME_LEVEL_1 = 4

game_state = MENU
state_history = [MENU]
is_advanced = False

def draw_menu(titulob, play_button_rect, quit_button_rect, imageb):
    screen.blit(imageb, [7, 7])
    screen.blit(titulob, [80, -30])
    draw_image_button(button_play_img, play_button_rect, "", font_medium, black)
    draw_image_button(button_quit_img, quit_button_rect, "", font_medium, black)
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


def draw_difficulty_selection(difficulty_text, difficulty_text_rect, beginner_text, beginner_button_rect, advanced_text, advanced_button_rect, back_text, back_button_rect, imageb):
    screen.blit(imageb, [0, 0])
    screen.blit(difficulty_text, difficulty_text_rect)
    draw_image_button(button_difficulty_img, beginner_button_rect, "Principiante", font_medium, white)
    draw_image_button(button_difficulty_img, advanced_button_rect, "Avanzado", font_medium, white)
    draw_image_button(button_back_img, back_button_rect, "Regresar", font_small, white)

def draw_character_selection(select_text, select_text_rect, char1_text, char1_button_rect, char2_text, char2_button_rect, back_text, back_button_rect, imageb):
    screen.blit(imageb, [0, 0])
    screen.blit(select_text, select_text_rect)
    draw_image_button(button_character_img, char1_button_rect, "Niño", font_medium, white)
    draw_image_button(button_character_img, char2_button_rect, "Niña", font_medium, white)
    draw_image_button(button_back_img, back_button_rect, "Regresar", font_small, white)

def draw_level_selection(level_text, level_text_rect, level1_text, level1_button_rect, level2_text, level2_button_rect, level3_text, level3_button_rect, back_text, back_button_rect, imageb, is_advanced):
    screen.blit(imageb, [0, 0])
    screen.blit(level_text, level_text_rect)

    draw_image_button(button_level_img, level1_button_rect, f"Nivel 1 ({'Avanzado' if is_advanced else 'Principiante'})", font_medium, white)
    draw_image_button(button_level_img, level2_button_rect, f"Nivel 2 ({'Avanzado' if is_advanced else 'Principiante'})", font_medium, white)
    draw_image_button(button_level_img, level3_button_rect, f"Nivel 3 ({'Avanzado' if is_advanced else 'Principiante'})", font_medium, white)

    draw_image_button(button_back_img, back_button_rect, "Regresar", font_small, white)

# Menú principal centrado y grande
play_button_rect = pygame.Rect(0, 0, 900, 500)  # ancho 900, alto 500
play_button_rect.center = (size[0] // 2, size[1] // 2)  # centro horizontal y vertical

quit_button_rect = pygame.Rect(0, 0, 900, 500)
quit_button_rect.center = (size[0] // 2, size[1] // 2 + 550)  # ajusta 550 para separar abajo

# Selección de dificultad
beginner_button_rect = pygame.Rect(0, 0, 350, 80)
beginner_button_rect.center = (size[0] // 2, size[1] // 2)

advanced_button_rect = pygame.Rect(0, 0, 350, 80)
advanced_button_rect.center = (size[0] // 2, size[1] // 2 + 120)
# Selección de personaje
select_text = font_large.render("Selecciona tu personaje", True, white)
select_text_rect = select_text.get_rect(center=(size[0] // 2, size[1] // 2 - 150))

char1_button_rect = pygame.Rect(0, 0, 250, 60)
char1_button_rect.center = (size[0] // 2 - 150, size[1] // 2)

char2_button_rect = pygame.Rect(0, 0, 250, 60)
char2_button_rect.center = (size[0] // 2 + 150, size[1] // 2)

# Selección de nivel
level_text = font_large.render("Selecciona el nivel", True, white)
level_text_rect = level_text.get_rect(center=(size[0] // 2, size[1] // 2 - 150))

level1_button_rect = pygame.Rect(0, 0, 250, 60)
level1_button_rect.center = (size[0] // 2, size[1] // 2)

level2_button_rect = pygame.Rect(0, 0, 250, 60)
level2_button_rect.center = (size[0] // 2, size[1] // 2 + 80)

level3_button_rect = pygame.Rect(0, 0, 250, 60)
level3_button_rect.center = (size[0] // 2, size[1] // 2 + 160)

# Botón de regresar
back_button_rect = pygame.Rect(50, 600, 150, 50)

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == MENU:
        draw_menu(titulob, play_button_rect, quit_button_rect, imageb)
    elif game_state == SELECT_DIFFICULTY:
        draw_difficulty_selection(difficulty_text, difficulty_text_rect, beginner_text, beginner_button_rect,
                                  advanced_text, advanced_button_rect, back_text, back_button_rect, imageb)
    elif game_state == SELECT_CHARACTER:
        draw_character_selection(select_text, select_text_rect, char1_text, char1_button_rect, char2_text,
                                 char2_button_rect, back_text, back_button_rect, imageb)
    elif game_state == SELECT_LEVEL:
        draw_level_selection(level_text, level_text_rect, level1_text, level1_button_rect, level2_text,
                             level2_button_rect, level3_text, level3_button_rect, back_text, back_button_rect, imageb, is_advanced)

    pygame.display.flip()
    clock.tick(60)
  
pygame.quit()
sys.exit()