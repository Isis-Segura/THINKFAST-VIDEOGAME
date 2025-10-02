import pygame
import sys
from settings import *
import Levels.Level1F as Level1F

def run_menu(screen):
    clock = pygame.time.Clock()

    # Recursos
    titulo = pygame.image.load("Materials/Pictures/Assets/titulo.png").convert_alpha()
    titulob = pygame.transform.scale(titulo, TITLE_SIZE)
    background = pygame.image.load("Materials/Pictures/Assets/background.png").convert()
    imageb = pygame.transform.scale(background, SIZE)

    # Música del menú
    pygame.mixer.music.load("Materials/Music/Menu.wav")
    pygame.mixer.music.play(-1)

    # Estados
    MENU = 0
    SELECT_DIFFICULTY = 1
    SELECT_CHARACTER = 2
    SELECT_LEVEL = 3
    GAME_LEVEL_1 = 4

    game_state = MENU
    state_history = [MENU]
    is_advanced = False
    selected_character = "boy"
    level_instance = None

    # Botones
    play_text = FONT_MEDIUM.render("PLAY", True, BLACK)
    play_button_rect = pygame.Rect(0, 0, 200, 60)
    play_button_rect.center = (SIZE[0] // 2, SIZE[1] // 2)

    quit_text = FONT_MEDIUM.render("QUIT", True, BLACK)
    quit_button_rect = pygame.Rect(0, 0, 200, 60)
    quit_button_rect.center = (SIZE[0] // 2, SIZE[1] // 2 + 80)

    difficulty_text = FONT_LARGE.render("Selecciona la dificultad", True, WHITE)
    difficulty_text_rect = difficulty_text.get_rect(center=(SIZE[0] // 2, SIZE[1] // 2 - 150))

    beginner_text = FONT_MEDIUM.render("Principiante", True, WHITE)
    beginner_button_rect = pygame.Rect(0, 0, 300, 60)
    beginner_button_rect.center = (SIZE[0] // 2, SIZE[1] // 2)

    advanced_text = FONT_MEDIUM.render("Avanzado", True, WHITE)
    advanced_button_rect = pygame.Rect(0, 0, 300, 60)
    advanced_button_rect.center = (SIZE[0] // 2, SIZE[1] // 2 + 80)

    select_text = FONT_LARGE.render("Selecciona tu personaje", True, WHITE)
    select_text_rect = select_text.get_rect(center=(SIZE[0] // 2, SIZE[1] // 2 - 150))

    char1_text = FONT_MEDIUM.render("Niño", True, WHITE)
    char1_button_rect = pygame.Rect(0, 0, 250, 60)
    char1_button_rect.center = (SIZE[0] // 2 - 150, SIZE[1] // 2)

    char2_text = FONT_MEDIUM.render("Niña", True, WHITE)
    char2_button_rect = pygame.Rect(0, 0, 250, 60)
    char2_button_rect.center = (SIZE[0] // 2 + 150, SIZE[1] // 2)

    level_text = FONT_LARGE.render("Selecciona el nivel", True, WHITE)
    level_text_rect = level_text.get_rect(center=(SIZE[0] // 2, SIZE[1] // 2 - 150))

    level1_text = FONT_MEDIUM.render("Nivel 1", True, WHITE)
    level1_button_rect = pygame.Rect(0, 0, 250, 60)
    level1_button_rect.center = (SIZE[0] // 2, SIZE[1] // 2)

    back_text = FONT_SMALL.render("Regresar", True, WHITE)
    back_button_rect = pygame.Rect(50, 600, 150, 50)

    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == GAME_LEVEL_1 and level_instance:
                returned_state = level_instance.handle_events(event)
                if returned_state == "menu":
                    game_state = MENU
                    level_instance = None
                    pygame.mixer.music.load("Materials/Music/Menu.wav")
                    pygame.mixer.music.play(-1)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                        level_instance = Level1F.Level1(screen, SIZE, FONT_SMALL, selected_character)

        # Dibujar
        if game_state == MENU:
            screen.blit(imageb, [0, 0])
            screen.blit(titulob, [80, -50])
            pygame.draw.rect(screen, LIGHT_GRAY, play_button_rect, border_radius=10)
            pygame.draw.rect(screen, DARK_GRAY, play_button_rect, 4, border_radius=10)
            screen.blit(play_text, play_text.get_rect(center=play_button_rect.center))
            pygame.draw.rect(screen, LIGHT_GRAY, quit_button_rect, border_radius=10)
            pygame.draw.rect(screen, DARK_GRAY, quit_button_rect, 4, border_radius=10)
            screen.blit(quit_text, quit_text.get_rect(center=quit_button_rect.center))

        elif game_state == SELECT_DIFFICULTY:
            screen.blit(imageb, [0, 0])
            screen.blit(difficulty_text, difficulty_text_rect)
            pygame.draw.rect(screen, BLUE, beginner_button_rect, border_radius=10)
            screen.blit(beginner_text, beginner_text.get_rect(center=beginner_button_rect.center))
            pygame.draw.rect(screen, PINK, advanced_button_rect, border_radius=10)
            screen.blit(advanced_text, advanced_text.get_rect(center=advanced_button_rect.center))
            pygame.draw.rect(screen, DARK_GRAY, back_button_rect, border_radius=10)
            screen.blit(back_text, back_text.get_rect(center=back_button_rect.center))

        elif game_state == SELECT_CHARACTER:
            screen.blit(imageb, [0, 0])
            screen.blit(select_text, select_text_rect)
            pygame.draw.rect(screen, BLUE, char1_button_rect, border_radius=10)
            screen.blit(char1_text, char1_text.get_rect(center=char1_button_rect.center))
            pygame.draw.rect(screen, PINK, char2_button_rect, border_radius=10)
            screen.blit(char2_text, char2_text.get_rect(center=char2_button_rect.center))
            pygame.draw.rect(screen, DARK_GRAY, back_button_rect, border_radius=10)
            screen.blit(back_text, back_text.get_rect(center=back_button_rect.center))

        elif game_state == SELECT_LEVEL:
            screen.blit(imageb, [0, 0])
            screen.blit(level_text, level_text_rect)
            pygame.draw.rect(screen, GREEN, level1_button_rect, border_radius=10)
            screen.blit(level1_text, level1_text.get_rect(center=level1_button_rect.center))
            pygame.draw.rect(screen, DARK_GRAY, back_button_rect, border_radius=10)
            screen.blit(back_text, back_text.get_rect(center=back_button_rect.center))

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
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
