import pygame, sys

pygame.init()

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
dark_gray = (50, 50, 50)
light_gray = (200, 200, 200)
green = (0, 200, 0)
blue = (0, 0, 200)

# Tamaños
size = (900, 700)
sizetitulo = (750, 350)

# Ejecución de la ventana
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mi Juego")

# Fuentes
font_large = pygame.font.Font(None, 80)
font_medium = pygame.font.Font(None, 60)

# Carga de recursos
titulo = pygame.image.load("titulo.png").convert()
titulo.set_colorkey([0, 0, 0])
titulob = pygame.transform.scale(titulo, (sizetitulo))
background = pygame.image.load("background.png").convert()
imageb = pygame.transform.scale(background, (size))
clock = pygame.time.Clock()

# --- Sistema de estados ---
# Define los estados posibles del juego
MENU = 0
SELECT_CHARACTER = 1

# Variable para rastrear el estado actual del juego
game_state = MENU

# --- Lógica de botones del menú ---
def create_menu_buttons():
    play_text = font_medium.render("PLAY", True, black)
    play_button_rect = pygame.Rect(0, 0, 200, 60)
    play_button_rect.center = (size[0] // 2, size[1] // 2)

    quit_text = font_medium.render("QUIT", True, black)
    quit_button_rect = pygame.Rect(0, 0, 200, 60)
    quit_button_rect.center = (size[0] // 2, size[1] // 2 + 80)
    
    return play_text, play_button_rect, quit_text, quit_button_rect

# --- Lógica de botones de selección de personaje ---
def create_character_buttons():
    # Texto para la pantalla de selección
    select_text = font_large.render("Selecciona tu personaje", True, white)
    select_text_rect = select_text.get_rect(center=(size[0] // 2, size[1] // 2 - 150))
    
    # Botón del personaje 1
    char1_text = font_medium.render("Personaje 1", True, white)
    char1_button_rect = pygame.Rect(0, 0, 250, 60)
    char1_button_rect.center = (size[0] // 2 - 150, size[1] // 2)

    # Botón del personaje 2
    char2_text = font_medium.render("Personaje 2", True, white)
    char2_button_rect = pygame.Rect(0, 0, 250, 60)
    char2_button_rect.center = (size[0] // 2 + 150, size[1] // 2)

    return select_text, select_text_rect, char1_text, char1_button_rect, char2_text, char2_button_rect

# Crear los elementos una vez
play_text, play_button_rect, quit_text, quit_button_rect = create_menu_buttons()
select_text, select_text_rect, char1_text, char1_button_rect, char2_text, char2_button_rect = create_character_buttons()

# --- Bucle principal del juego ---
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == MENU:
                if play_button_rect.collidepoint(event.pos):
                    game_state = SELECT_CHARACTER
                if quit_button_rect.collidepoint(event.pos):
                    running = False
            elif game_state == SELECT_CHARACTER:
                if char1_button_rect.collidepoint(event.pos):
                    print("¡Personaje 1 seleccionado!")
                    # Aquí puedes iniciar el juego con el Personaje 1
                    # Por ejemplo: game_state = IN_GAME
                if char2_button_rect.collidepoint(event.pos):
                    print("¡Personaje 2 seleccionado!")
                    # Aquí puedes iniciar el juego con el Personaje 2
                    # Por ejemplo: game_state = IN_GAME
                    
    # --- Dibujar en la pantalla basado en el estado del juego ---
    screen.blit(imageb, [0, 0])
    
    if game_state == MENU:
        screen.blit(titulob, [80, -50])
        # Dibujar botones del menú
        pygame.draw.rect(screen, light_gray, play_button_rect, border_radius=10)
        pygame.draw.rect(screen, dark_gray, play_button_rect, 4, border_radius=10)
        screen.blit(play_text, play_text.get_rect(center=play_button_rect.center))

        pygame.draw.rect(screen, light_gray, quit_button_rect, border_radius=10)
        pygame.draw.rect(screen, dark_gray, quit_button_rect, 4, border_radius=10)
        screen.blit(quit_text, quit_text.get_rect(center=quit_button_rect.center))

    elif game_state == SELECT_CHARACTER:
        # Dibujar elementos de la pantalla de selección
        screen.blit(select_text, select_text_rect)
        
        # Botones de personaje
        pygame.draw.rect(screen, green, char1_button_rect, border_radius=10)
        screen.blit(char1_text, char1_text.get_rect(center=char1_button_rect.center))
        
        pygame.draw.rect(screen, blue, char2_button_rect, border_radius=10)
        screen.blit(char2_text, char2_text.get_rect(center=char2_button_rect.center))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()