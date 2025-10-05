import pygame
import random
import math
# Asumiendo que estas importaciones están en tu entorno
from Personajes.boy import Characterb
from Personajes.girl import Characterg
from Personajes.Guardian import Characternpc 
from Interacciones.Controldeobjetos.velotex import TypewriterText 
from Interacciones.Controldeobjetos.timer import Timer 
from Interacciones.Controldeobjetos.corazones import LifeManager
from Interacciones.FloorQuiz import FloorQuiz 

# =================================================================
# CLASE CONFETTI (SIN CAMBIOS)
# =================================================================

class Confetti:
    def __init__(self, screen_width, screen_height):
        self.particles = []
        self.colors = [
            (255, 0, 0), (0, 255, 0), (0, 150, 255),
            (255, 255, 0), (255, 0, 255), (255,128,0), (128,0,255)
        ]
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.spawn_rate = 5
        self._max_life = 140

    def start(self):
        self.active = True
        self.particles = []

    def stop(self):
        self.active = False

    def update(self):
        if self.active:
            for _ in range(self.spawn_rate):
                side = random.choice(["left", "right"])
                x = 0 if side == "left" else self.screen_width
                y = random.randint(0, self.screen_height // 3)
                dx = random.uniform(-3, 3)
                if side == "right" and dx > -0.5:
                    dx = random.uniform(-3, -0.8)
                if side == "left" and dx < 0.5:
                    dx = random.uniform(0.8, 3)
                dy = random.uniform(1.5, 4.0)
                color = random.choice(self.colors)
                life = random.randint(int(self._max_life*0.6), self._max_life)
                size = random.randint(4, 7)
                self.particles.append([x, y, dx, dy, color, life, size])

        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[5] -= 1

        self.particles = [p for p in self.particles if p[5] > 0 and p[1] < self.screen_height + 50]

    def draw(self, surface):
        if not self.particles:
            return
        for p in self.particles:
            x, y, dx, dy, color, life, size = p
            shadow_radius = int(size * 1.4)
            pygame.draw.circle(surface, (30, 30, 30), (int(x + 2), int(y + 3)), shadow_radius)
            pygame.draw.circle(surface, color, (int(x), int(y)), size)

# =================================================================
# CLASE LEVEL 1 (MODIFICADA)
# =================================================================

class Level1:
    def __init__(self, screen, size, font, character_choice):
        self.screen = screen
        self.size = size
        self.font = font
        self.character_choice = character_choice
        
        # 1. Cargar la imagen de control (Control.jpg)
        self.control_image = None
        try:
            img = pygame.image.load('Materials/Pictures/Assets/Control.jpg').convert() 
            self.control_image = img
            print("[Level1] Control image loaded successfully.")
        except pygame.error as e:
            print(f"[Level1] Warning: Could not load Control image (Control.jpg). Error: {e}")
        
        # --- Variables de Animación de Fundido ---
        self.fade_alpha = 255 if self.control_image else 0 
        self.fade_in_speed = 5    
        self.fade_out_speed = 10  
        self.is_fading = True
        self.target_state = None 
        # ----------------------------------------------------

        # 2. Establecer el estado inicial a la pantalla de control
        if self.control_image:
            self.state = "controls_screen" 
        else:
            self.state = "game"
            self.is_fading = False 

        if self.character_choice == "boy":
            self.player = Characterb(440, 600, 2)
        else:
            self.player = Characterg(440, 600, 2)

        self.Guardia = Characternpc(470, 330, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')

        guardia_width = self.Guardia.rect.width
        guardia_height = self.Guardia.rect.height
        COL_WIDTH_FACTOR = 0.5
        COL_HEIGHT_PIXELS = 5
        new_width = int(guardia_width * COL_WIDTH_FACTOR)
        new_height = COL_HEIGHT_PIXELS
        new_x = self.Guardia.rect.x + int((guardia_width - new_width) / 2)
        new_y = self.Guardia.rect.y + guardia_height - new_height
        self.guardia_collision_rect = pygame.Rect(new_x, new_y, new_width, new_height)

        # Carga del fondo del juego (Image 2)
        self.background_image_game = pygame.image.load('Materials/Pictures/Assets/fondo_CloseDoor.jpeg').convert()
        self.background_image_game = pygame.transform.scale(self.background_image_game, self.size)
        self.background_image = self.background_image_game 

        try:
            self.background_image_open = pygame.image.load('Materials/Pictures/Assets/fondo_OpenDoor.jpeg').convert() 
            self.background_image_open = pygame.transform.scale(self.background_image_open, self.size)
        except pygame.error:
            self.background_image_open = self.background_image_game 
            print("[Level1] Warning: 'fondo_OpenDoor.jpeg' not found. Using main game background as fallback.")
            
        self.background_changed = False 
        
        try:
            img = pygame.image.load("Materials/Pictures/Assets/dialog_box.png").convert_alpha()
            self.dialog_box_img = pygame.transform.scale(img, (800, 120))
            self.dialog_box_rect = self.dialog_box_img.get_rect()
            self.dialog_box_rect.center = (self.size[0] // 2, self.size[1] - 70)
            self._dialog_img_loaded = True
        except Exception:
            self._dialog_img_loaded = False
            self.dialog_box_img = None
            self.dialog_box_rect = pygame.Rect(50, self.size[1] - 150, 800, 100)

        # Carga de la imagen de Game Over (Image 1)
        self.game_over_image = None
        try:
            img = pygame.image.load('Materials/Pictures/Assets/perdiste.png').convert() 
            self.game_over_image = pygame.transform.scale(img, self.size)
        except pygame.error as e:
            print(f"[Level1] Warning: Could not load Game Over image. Error: {e}")
            self.game_over_image = None

        # Carga de la imagen de Ganaste (Image 3)
        self.win_image = None
        try:
            img = pygame.image.load('Materials/Pictures/Assets/ganaste.png').convert() 
            self.win_image = pygame.transform.scale(img, self.size)
        except pygame.error as e:
            print(f"[Level1] Warning: Could not load Win image. Error: {e}")
            self.win_image = None

        self.timer = Timer(120)
        self.quiz_timer = Timer(10)
        
        self.life_manager = LifeManager(3, 'Materials/Pictures/Assets/corazones.png')

        # --- Carga de audio ---
        self.controls_music = None
        try:
            self.controls_music = pygame.mixer.Sound('Materials/Music/controls.wav')
            pygame.mixer.music.load('Materials/Music/Level1.wav')
            self.loss_sound = pygame.mixer.Sound('Materials/Music/antesover.wav')
            self.game_over_music = pygame.mixer.Sound('Materials/Music/GameOver.wav')
            self.win_music = pygame.mixer.Sound('Materials/Music/Ganar.wav')
            self.correct_sound = pygame.mixer.Sound('Materials/Music/PreguntaB.wav')
            self.incorrect_sound = pygame.mixer.Sound('Materials/Music/PreguntaM.wav')
        except Exception as e:
            print(f"[Level1] error cargando audio: {e}")
            self.loss_sound = None
            self.game_over_music = None
            self.win_music = None
            self.correct_sound = None
            self.incorrect_sound = None
        
        # Iniciar la música de control inmediatamente si estamos en ese estado
        if self.state == "controls_screen" and self.controls_music:
            try:
                self.controls_music.play(-1) # Reproducir en loop
            except Exception as e:
                print(f"[Level1] error playing controls music: {e}")


        self.dialogo_text = "Si quieres pasar, tendras que responder estas\n preguntas!!" 
        self.typewriter = None
        self.dialogo_active = False
        self.quiz_game = None
        self.post_quiz_dialogs = []
        self.current_dialog_index = 0
        self.guard_interacted = False
        self.game_over_music_played = False
        self.win_music_played = False

        self.confetti = Confetti(self.size[0], self.size[1])

        self.questions = [
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cómo se llama nuestro país?", "choices": ["España", "México", "Roma", "Berlín"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuánto es 6 + 2?", "choices": ["7", "8", "9", "10"], "correct_answer": 1 }, 
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuál es el animal más grande del mundo?", "choices": ["Ballena azul", "Elefante", "Tiburón", "Jirafa"], "correct_answer": 0 }, 
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuál es el océano más grande?", "choices": ["Atlántico", "Índico", "Pacífico", "Ártico"], "correct_answer": 2 }
        ]
        self.win_zone = pygame.Rect(420, 280, 65, 65)
        
        self.font_base = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 18) 
        self.font_dialog = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 15) 
        self.font_question = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 13) 
        self.font_title = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 15)
        self.font_timer = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 24)
        
        # --- Fuente para el título "CONTROLES" ---
        self.font_control_title = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 36)

    def _make_font(self, spec, default_size):
        if spec is None:
            return pygame.font.Font(None, default_size)
        if isinstance(spec, pygame.font.Font):
            return spec
        if isinstance(spec, int):
            return pygame.font.Font(None, spec)
        if isinstance(spec, tuple) and len(spec) == 2:
            path, size = spec
            try:
                return pygame.font.Font(path, size)
            except Exception:
                return pygame.font.Font(None, default_size)
        return pygame.font.Font(None, default_size)

    def set_fonts(self, dialog_font=None, question_font=None, title_font=None, timer_font=None):
        self.font_dialog = self._make_font(dialog_font, 28)
        self.font_question = self._make_font(question_font, 32)
        self.font_title = self._make_font(title_font, 48)
        self.font_timer = self._make_font(timer_font, 26)

    def handle_events(self, event):
        # Manejo de eventos de reinicio/menú para estados finales
        if self.state in ["game_over", "loss_sound_state", "win_state"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.stop()
                    self.__init__(self.screen, self.size, self.font, self.character_choice)
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    return "menu"
            return None

        # Lógica para la pantalla de control (MODIFICADO para incluir K_RETURN)
        if self.state == "controls_screen" and not self.is_fading:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN):
                # Iniciar el Fade Out en lugar de cambiar de estado inmediatamente
                self.is_fading = True
                self.target_state = "game"
                self.fade_alpha = 0 # Empezar a aumentar la opacidad para fade out (oscurecer)
                
                # Detener la música de control aquí, el cambio de estado real ocurre en update()
                if self.controls_music:
                    self.controls_music.stop()
                return None
            return None 

        # Lógica para interactuar con el diálogo/avanzar el texto (MODIFICADO para incluir K_RETURN)
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
            if self.dialogo_active and self.typewriter:
                if not self.typewriter.finished():
                    self.typewriter.complete_text()
                elif self.state == "dialog":
                    self.state = "quiz_floor"
                    self.dialogo_active = False
                    self.typewriter = None
                    self.quiz_timer = Timer(10)
                    self.quiz_game = FloorQuiz(self.size, self.questions, self.font_question) 
                    self.quiz_timer.start()
                    return
                elif self.state == "quiz_complete_dialog":
                    self.current_dialog_index += 1
                    if self.current_dialog_index < len(self.post_quiz_dialogs):
                        next_text = self.post_quiz_dialogs[self.current_dialog_index]
                        self.typewriter = TypewriterText(next_text, self.font_dialog, (255,255,255), speed=25)
                        self.dialogo_active = True
                    else:
                        self.dialogo_active = False
                        self.typewriter = None

        if self.state == "quiz_floor" and self.quiz_game:
            result = self.quiz_game.handle_event(event)
            
            if result in ["correct", "incorrect"]:
                if result == "correct":
                    if self.correct_sound: self.correct_sound.play()
                else:
                    if self.incorrect_sound: self.incorrect_sound.play()
                    self.life_manager.lose_life()
                
                self.quiz_timer.pause()
                
                if self.life_manager.is_dead():
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    if self.loss_sound: self.loss_sound.play()
                    return
            
            elif result == "advanced":
                if not self.quiz_game.finished: 
                    self.quiz_timer = Timer(10) 
                    self.quiz_timer.start()
                
            
            elif result == "finished":
                self.quiz_timer.pause() 
                     
        return None

    def update(self):
        keys = pygame.key.get_pressed()

        # --- Lógica de Fundido ---
        if self.is_fading:
            if self.state == "controls_screen": # Fade In (de 255 a 0) o Fade Out (de 0 a 255)
                if self.target_state is None: # Fade In
                    self.fade_alpha = max(0, self.fade_alpha - self.fade_in_speed)
                    if self.fade_alpha == 0:
                        self.is_fading = False
                elif self.target_state == "game": # Fade Out
                    self.fade_alpha = min(255, self.fade_alpha + self.fade_out_speed)
                    if self.fade_alpha == 255:
                        self.state = self.target_state
                        self.target_state = None
                        self.fade_alpha = 255 # Para el Fade In del juego

                        # Iniciar la música de nivel y el timer
                        try:
                            pygame.mixer.music.play(-1)
                        except Exception as e:
                            print(f"[Level1] error playing Level1 music: {e}")
                        self.quiz_timer.start()
                        
                        self.is_fading = True
            
            elif self.state == "game" and self.target_state is None:
                     # Fade In para la entrada del nivel (de 255 a 0)
                self.fade_alpha = max(0, self.fade_alpha - self.fade_in_speed)
                if self.fade_alpha == 0:
                    self.is_fading = False
        # -------------------------

        if self.state == "controls_screen":
            if not self.is_fading and self.controls_music:
                if not pygame.mixer.get_busy() or self.controls_music.get_num_channels() == 0:
                    try:
                         self.controls_music.play(-1)
                    except Exception:
                         pass
            return self.state

        if self.state in ["game", "quiz_floor"]:
            barrier = self.guardia_collision_rect if not self.guard_interacted else None
            self.player.move(keys, self.size[0], self.size[1], barrier)

        if self.state == "game":
            if self.guard_interacted:
                if self.player.rect.colliderect(self.win_zone):
                    pygame.mixer.music.stop()
                    self.state = "win_state"
                    if self.win_music and not self.win_music_played:
                        self.win_music.play()
                        self.win_music_played = True
            # Lógica para interactuar con el guardia (MODIFICADO para incluir K_RETURN)
            elif self.player.rect.colliderect(self.guardia_collision_rect.inflate(20,20)) and (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and not self.guard_interacted:
                self.state = "dialog"
                self.dialogo_active = True
                self.typewriter = TypewriterText(self.dialogo_text, self.font_dialog, (255,255,255), speed=25) 

        elif self.state == "quiz_floor":
            if not self.quiz_timer.paused:
                self.quiz_timer.update()

            if self.quiz_timer.finished and not getattr(self.quiz_game, "is_answered", False):
                if self.incorrect_sound: self.incorrect_sound.play()
                self.life_manager.lose_life()
                
                self.quiz_game.is_answered = True
                self.quiz_game.answer_result = "incorrect"
                self.quiz_game.selected_choice_index = -1
                
                self.quiz_timer.pause()
                
                if self.life_manager.is_dead():
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    if self.loss_sound: self.loss_sound.play()
                    return

            self.quiz_game.check_player_collision(self.player.rect)

            if self.quiz_game.finished:
                self.state = "quiz_complete_dialog"
                self.dialogo_active = True
                score = self.quiz_game.correct_answers
                total = len(self.questions)

                if score == total:
                    dialog_text = "¡Muy bien hecho! Has demostrado tener una buena\n calidad de estudio." 
                elif score >= 3:
                    dialog_text = "Buen trabajo. Tienes un buen nivel, sigue \npracticando. El aprendizaje son oportunidades que\nnunca se deben desaprovechar."
                else:
                    dialog_text = "Puedes mejorar, solo aquellos que estudian pueden \nsuperar cualquier obstaculo que se le presente.!"

                self.post_quiz_dialogs = [
                    f"Has respondido correctamente {score} de {total} preguntas.",
                    dialog_text,
                    "Ahora te abro el paso. ¡Buena suerte en tu camino!"
                ]

                self.current_dialog_index = 0
                self.typewriter = TypewriterText(self.post_quiz_dialogs[self.current_dialog_index], self.font_dialog, (255,255,255), speed=25)
                self.quiz_game = None
                self.timer.reset()

                if score >= 2:
                    self.confetti.start()

        elif self.state == "quiz_complete_dialog":
            if not self.dialogo_active and self.current_dialog_index >= len(self.post_quiz_dialogs):
                self.Guardia.rect.x -= 130
                guardia_width = self.Guardia.rect.width
                new_width = self.guardia_collision_rect.width
                self.guardia_collision_rect.x = self.Guardia.rect.x + int((guardia_width - new_width) / 2)
                
                self.player.rect.x = 450
                self.player.rect.y = 570
                
                self.guard_interacted = True
                
                if not self.background_changed:
                    self.background_image = self.background_image_open 
                    self.background_changed = True
                
                self.state = "game"

        elif self.state == "loss_sound_state":
            if not pygame.mixer.get_busy():
                self.state = "game_over" 
                
                if self.game_over_music and not self.game_over_music_played:
                    try:
                        self.game_over_music.play(-1)
                        self.game_over_music_played = True
                    except pygame.error:
                        pass

        if self.dialogo_active and self.typewriter:
            self.typewriter.update()

        self.confetti.update()
        return self.state
    
    # Función auxiliar para dibujar texto con un borde simple
    def _draw_text_with_border(self, surface, text, font, text_color, border_color, center_pos, border_size=2):
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=center_pos)
        
        # Dibuja el borde (offset)
        for dx in range(-border_size, border_size + 1):
            for dy in range(-border_size, border_size + 1):
                if dx != 0 or dy != 0:
                    border_rect = text_surface.get_rect(center=(center_pos[0] + dx, center_pos[1] + dy))
                    border_surface = font.render(text, True, border_color)
                    surface.blit(border_surface, border_rect)
        
        # Dibuja el texto principal
        surface.blit(text_surface, text_rect)


    def draw(self):
        # Dibuja la pantalla de control (estado inicial)
        if self.state == "controls_screen":
            if self.control_image:
                screen_width, screen_height = self.size
                image_orig_width, image_orig_height = self.control_image.get_size()
                
                image_aspect = image_orig_width / image_orig_height

                scale_factor_w = screen_width / image_orig_width
                scale_factor_h = screen_height / image_orig_height

                # Determinar el escalado para mantener el aspecto (sin distorsión)
                if scale_factor_w < scale_factor_h:
                    new_width = screen_width
                    new_height = int(new_width / image_aspect)
                else:
                    new_height = screen_height
                    new_width = int(new_height * image_aspect)
                
                # Escalar y centrar la imagen
                scaled_image = pygame.transform.scale(self.control_image, (new_width, new_height))
                target_rect = scaled_image.get_rect(center=(screen_width // 2, screen_height // 2))

                # --- FONDO BLANCO ---
                self.screen.fill((255, 255, 255)) 
                self.screen.blit(scaled_image, target_rect.topleft)
                
                # --- AÑADIR TÍTULO "CONTROLES" (NUEVO) ---
                try:
                    text_to_render_title = "CONTROLES"
                    center_x_title = self.size[0] // 2
                    center_y_title = 40 # Cerca de la parte superior
                    
                    self._draw_text_with_border(
                        self.screen, 
                        text_to_render_title, 
                        self.font_control_title, 
                        (0, 0, 0),       # Color del texto: Negro
                        (255, 128, 0),     # Color del borde: NARANJA
                        (center_x_title, center_y_title),
                        border_size=4 # Borde un poco más grande para el título
                    )
                except Exception:
                    pass
                # ----------------------------------------
                
                # Añadir texto "Presiona ESPACIO..." con borde NARANJA
                font_to_use = self.font_dialog if hasattr(self, 'font_dialog') else self.font
                try:
                    text_to_render = "Presiona ESPACIO o ENTER para comenzar el Nivel 1"
                    center_x = self.size[0] // 2
                    center_y = self.size[1] - 30
                    
                    self._draw_text_with_border(
                        self.screen, 
                        text_to_render, 
                        font_to_use, 
                        (0, 0, 0),       # Color del texto: Negro
                        (255, 128, 0),     # Color del borde: NARANJA
                        (center_x, center_y),
                        border_size=2
                    )
                except Exception:
                    pass
            else:
                self.screen.fill((255, 255, 255))
                font_to_use = self.font_dialog if hasattr(self, 'font_dialog') else self.font
                try:
                    text1 = font_to_use.render("Error cargando Controles. Presiona ESPACIO.", True, (0, 0, 0))
                    self.screen.blit(text1, text1.get_rect(center=(self.size[0] // 2, self.size[1] // 2)))
                except Exception:
                    pass
            
            # --- DIBUJAR CAPA DE FUNDIDO ---
            if self.is_fading or self.fade_alpha > 0:
                fade_surface = pygame.Surface(self.size).convert_alpha()
                
                if self.target_state == "game" and self.state == "controls_screen":
                    # Fade Out (Oscurecer a negro para la transición)
                    fade_surface.fill((0, 0, 0)) 
                    fade_surface.set_alpha(self.fade_alpha)
                elif self.state == "controls_screen":
                    # Fade In (Aclarar desde blanco)
                    fade_surface.fill((255, 255, 255))
                    fade_surface.set_alpha(self.fade_alpha)
                
                self.screen.blit(fade_surface, (0, 0))
            # -----------------------------------------------

            return 
            
        # Dibuja el juego normal si el estado es otro
        
        if self.state in ["game", "dialog", "quiz_complete_dialog", "quiz_floor", "loss_sound_state"]:
            self.screen.blit(self.background_image, (0, 0)) # Dibuja el fondo del juego (Image 2)

            shadow_offset = 5
            try:
                px = self.player.rect.x-5
                py = self.player.rect.y+5
                ph = self.player.rect.height
                shadow_surface = pygame.Surface((self.player.rect.width, 8), pygame.SRCALPHA)
                pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, self.player.rect.width, 8))
                self.screen.blit(shadow_surface, (px + shadow_offset, py + ph - 10))
                
                gx = self.Guardia.rect.x+25
                gy = self.Guardia.rect.y
                gh = self.Guardia.rect.height-2
                pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, self.Guardia.rect.width, 8))
                self.screen.blit(shadow_surface, (gx + shadow_offset, gy + gh - 10))
            except Exception:
                pass

            self.player.draw(self.screen)
            self.Guardia.draw(self.screen)

            font_to_use = self.font_timer if hasattr(self, 'font_timer') else self.font
            if self.state == "quiz_floor":
                self.quiz_timer.draw(self.screen, font_to_use, is_quiz_timer=True, position=(680, 10))
            else:
                self.timer.draw(self.screen, font_to_use, position=(680, 10))

            self.life_manager.draw(self.screen)
            self.confetti.draw(self.screen)

            if self.state == "quiz_floor" and self.quiz_game:
                self.quiz_game.draw(self.screen)

            if self.dialogo_active:
                if self._dialog_img_loaded and self.dialog_box_img:
                    self.screen.blit(self.dialog_box_img, self.dialog_box_rect.topleft)
                    
                    pygame.draw.rect(self.screen, (255, 200, 0), self.dialog_box_rect, 
                                            width=5, border_radius=20)
                    
                    self.typewriter.draw(self.screen, (self.dialog_box_rect.x + 20, self.dialog_box_rect.y + 35))

                else:
                    box_rect = pygame.Rect(50, 550, 800, 100)
                    PIXEL_RADIUS = 10 
                    
                    BACKGROUND_COLOR = (20, 30, 80) 
                    pygame.draw.rect(self.screen, BACKGROUND_COLOR, box_rect, border_radius=PIXEL_RADIUS) 
                    
                    BORDER_COLOR = (255, 200, 0) 
                    pygame.draw.rect(self.screen, BORDER_COLOR, box_rect, 5, border_radius=PIXEL_RADIUS)
                    
                    self.typewriter.draw(self.screen, (box_rect.x + 20, box_rect.y + 35))

            # --- DIBUJAR CAPA DE FUNDIDO PARA LA ENTRADA AL JUEGO ---
            if self.state == "game" and self.is_fading and self.fade_alpha > 0:
                fade_surface = pygame.Surface(self.size).convert_alpha()
                fade_surface.fill((0, 0, 0)) 
                fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(fade_surface, (0, 0))
            # ----------------------------------------------------------------------


        elif self.state == "win_state":
            if self.win_image:
                self.screen.blit(self.win_image, (0, 0)) # Dibuja la imagen de Ganaste (Image 3)
            else:
                self.screen.fill((0, 0, 0))
                font_title_to_use = self.font_title if hasattr(self, 'font_title') else self.font
                try:
                    text1 = font_title_to_use.render("¡HAS GANADO!", True, (0, 255, 0))
                    self.screen.blit(text1, text1.get_rect(center=(self.size[0] // 2, self.size[1] // 2 - 40)))
                except Exception:
                    pass 
            
            font_to_use = self.font_dialog if hasattr(self, 'font_dialog') else self.font
            try:
                text_to_render = "Presiona R para reiniciar o ESC para ir al menú"
                center_x = self.size[0] // 2
                center_y = self.size[1] - 50
                
                self._draw_text_with_border(
                    self.screen, 
                    text_to_render, 
                    font_to_use, 
                    (255, 255, 255), 
                    (255, 140, 0),
                    (center_x, center_y),
                    border_size=2 
                )

            except Exception:
                try:
                    text2 = font_to_use.render("Presiona R para reiniciar o ESC para ir al menú", True, (255, 255, 255))
                    self.screen.blit(text2, text2.get_rect(center=(self.size[0] // 2, self.size[1] - 50)))
                except Exception:
                    pass

        elif self.state == "game_over":
            if self.game_over_image:
                self.screen.blit(self.game_over_image, (0, 0)) 
            else:
                self.screen.fill((0, 0, 0))
                font_title_to_use = self.font_title if hasattr(self, 'font_title') else self.font
                try:
                    text1 = font_title_to_use.render("GAME OVER", True, (255, 0, 0))
                    self.screen.blit(text1, text1.get_rect(center=(self.size[0] // 2, self.size[1] // 2 - 40)))
                except Exception:
                    pass