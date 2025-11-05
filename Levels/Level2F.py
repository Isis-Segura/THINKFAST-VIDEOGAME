import pygame
import random
import os
from Personajes.boy import Characterb
from Personajes.girl import Characterg
from Personajes.Prefect import Characternpcp
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Controldeobjetos.timer import Timer
from Interacciones.Mecanicas.FloorQuiz_KeyAndCarry import FloorQuiz_KeyAndCarry

# -------------------- INICIALIZACIÓN Y DEBUGGING --------------------
MIXER_INITIALIZED = False
try:
    pygame.mixer.init()
    MIXER_INITIALIZED = True
    print("DEBUG INICIO: pygame.mixer inicializado correctamente.")
except pygame.error as e:
    print(f"ADVERTENCIA CRÍTICA: No se pudo inicializar pygame.mixer. El juego no tendrá sonido. Error: {e}")
# --------------------------------------------------------------------


class Confetti:
    def __init__(self, screen_width, screen_height):
        self.flash_color = None
        self.flash_alpha = 0
        self.flash_timer = 0
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

    def reset(self):
        self.particles = []
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
        for p in self.particles:
            x, y, dx, dy, color, life, size = p
            shadow_radius = int(size * 1.4)
            pygame.draw.circle(surface, (30, 30, 30), (int(x + 2), int(y + 3)), shadow_radius)
            pygame.draw.circle(surface, color, (int(x), int(y)), size)

class Level2:
    def __init__(self, screen, size, font, character_choice):
        global MIXER_INITIALIZED
        self.flash_color = None
        self.flash_alpha = 0
        self.flash_timer = 0
        self.screen = screen
        self.size = size
        self.font = font
        self.character_choice = character_choice

        try:
            self.control_image = pygame.image.load('Materials/Pictures/Assets/Control.jpg').convert()
        except pygame.error:
            self.control_image = None

        self.fade_alpha = 255 if self.control_image else 0
        self.fade_in_speed = 5
        self.fade_out_speed = 10
        self.is_fading = True
        self.target_state = None

        if self.control_image:
            self.state = "controls_screen"
        else:
            self.state = "game"
            self.is_fading = True
            self.fade_alpha = 255

        if self.character_choice == "boy":
            self.player = Characterb(440, 600, 2)
        else:
            self.player = Characterg(440, 600, 2)

        self.Guardia = Characternpcp(470, 330, 'Materials/Pictures/Characters/NPCs/Prefecta/Prefect.png')

        guardia_width = self.Guardia.rect.width
        guardia_height = self.Guardia.rect.height
        COL_WIDTH_FACTOR = 0.5
        COL_HEIGHT_PIXELS = 5
        new_width = int(guardia_width * COL_WIDTH_FACTOR)
        new_height = COL_HEIGHT_PIXELS
        new_x = self.Guardia.rect.x + int((guardia_width - new_width) / 2)
        new_y = self.Guardia.rect.y + guardia_height - new_height
        self.guardia_collision_rect = pygame.Rect(new_x, new_y, new_width, new_height)
        
        self.prefecta_drop_zone = self.guardia_collision_rect.inflate(20, 20)
        self.is_holding_answer = False
        self.held_answer_info = None

        try:
            self.background_image_game = pygame.image.load('Materials/Pictures/Assets/fondon3.png').convert()
            self.background_image_game = pygame.transform.scale(self.background_image_game, self.size)
        except pygame.error:
            self.background_image_game = pygame.Surface(self.size)
            self.background_image_game.fill((0, 0, 0))
        self.background_image = self.background_image_game

        try:
            self.background_image_open = pygame.image.load('Materials/Pictures/Assets/fondon2.png').convert()
            self.background_image_open = pygame.transform.scale(self.background_image_open, self.size)
        except pygame.error:
            self.background_image_open = self.background_image_game
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

        try:
            img = pygame.image.load('Materials/Pictures/Assets/perdiste.png').convert()
            self.game_over_image = pygame.transform.scale(img, self.size)
        except pygame.error:
            self.game_over_image = None

        try:
            img = pygame.image.load('Materials/Pictures/Assets/ganaste.png').convert()
            self.win_image = pygame.transform.scale(img, self.size)
        except pygame.error:
            self.win_image = None

        self.timer = Timer(120)
        self.quiz_timer = Timer(10)

        self.answer_results = []
        self.max_questions = 4

        try:
            self.marco_img = pygame.image.load("Materials/Pictures/Assets/marco.png").convert_alpha()
            self.palomita_img = pygame.image.load("Materials/Pictures/Assets/palomita.png").convert_alpha()
            self.tache_img = pygame.image.load("Materials/Pictures/Assets/tache.png").convert_alpha()
        except Exception:
            self.marco_img = pygame.Surface((48, 48), pygame.SRCALPHA)
            pygame.draw.rect(self.marco_img, (255, 255, 255), self.marco_img.get_rect(), 3, border_radius=6)
            self.palomita_img = pygame.Surface((36, 36), pygame.SRCALPHA)
            self.tache_img = pygame.Surface((36, 36), pygame.SRCALPHA)
            pygame.draw.line(self.palomita_img, (0, 200, 0), (4, 18), (14, 30), 4)
            pygame.draw.line(self.palomita_img, (0, 200, 0), (14, 30), (30, 6), 4)
            pygame.draw.line(self.tache_img, (200, 0, 0), (6, 6), (30, 30), 4)
            pygame.draw.line(self.tache_img, (200, 0, 0), (30, 6), (6, 30), 4)

        marco_w = 56
        marco_h = 56
        symbol_w = 40
        symbol_h = 40
        self.marco_img = pygame.transform.scale(self.marco_img, (marco_w, marco_h))
        self.palomita_img = pygame.transform.scale(self.palomita_img, (symbol_w, symbol_h))
        self.tache_img = pygame.transform.scale(self.tache_img, (symbol_w, symbol_h))

        # -------------------- CARGA DE SONIDOS CONDICIONAL Y CON DEBUG --------------------
        self.level_music_loaded = False
        self.controls_music = None
        self.loss_sound = None
        self.game_over_music = None
        self.win_music = None
        self.correct_sound = None
        self.incorrect_sound = None

        if MIXER_INITIALIZED:
            try:
                # Intenta cargar la música de fondo del nivel
                pygame.mixer.music.load('Materials/Music/Level2.wav')
                self.level_music_loaded = True
                print("DEBUG CARGA: Música de Level2.wav cargada con éxito.")

                # Intenta cargar los efectos y otras músicas
                self.controls_music = pygame.mixer.Sound('Materials/Music/controls.wav')
                self.loss_sound = pygame.mixer.Sound('Materials/Music/antesover.wav')
                self.game_over_music = pygame.mixer.Sound('Materials/Music/GameOver.wav')
                self.win_music = pygame.mixer.Sound('Materials/Music/Ganar.wav')
                self.correct_sound = pygame.mixer.Sound('Materials/Music/PreguntaB.wav')
                self.incorrect_sound = pygame.mixer.Sound('Materials/Music/PreguntaM.wav')
                print("DEBUG CARGA: Todos los efectos de sonido cargados con éxito.")

            except pygame.error as e:
                self.level_music_loaded = False
                print("---------------------------------------------------------------")
                print(f"!!! ERROR FATAL DE CARGA DE AUDIO !!!")
                print(f"El juego NO PUDO encontrar uno o más archivos de audio, o el formato es incorrecto.")
                print(f"Verifica que los archivos .wav estén en la ruta: 'Materials/Music/'")
                print(f"Error detallado: {e}")
                print("---------------------------------------------------------------")
        # ---------------------------------------------------------------------------------------------
        
        # -------------------- SOLUCIÓN FALTANTE: REPRODUCCIÓN DE MÚSICA DE CONTROL --------------------
        # Reproduce la música de control al iniciar la pantalla de controles
        if self.state == "controls_screen" and self.controls_music:
            self.controls_music.play(-1) # El -1 indica reproducción en bucle
            print("DEBUG PLAY: Música de control (controls.wav) iniciada en bucle.")
        # ---------------------------------------------------------------------------------------------

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
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "Como se llama nuestro pais?", "choices": ["Espana", "Mexico", "Roma", "Berlin"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "Cuanto es 6 + 2?", "choices": ["7", "8", "9", "10"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "Cual es el animal mas grande del mundo?", "choices": ["Ballena azul", "Elefante", "Tiburon", "Jirafa"], "correct_answer": 0 },
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "Cual es el oceano mas grande?", "choices": ["Atlantico", "Indico", "Pacifico", "Artico"], "correct_answer": 2 }
        ]

        self.win_zone = pygame.Rect(420, 280, 65, 65)

        if os.path.exists("Materials/Fonts/PressStart2P-Regular.ttf"):
            font_path = "Materials/Fonts/PressStart2P-Regular.ttf"
        else:
            font_path = None 
        
        self.font_base = pygame.font.Font(font_path, 18)
        self.font_dialog = pygame.font.Font(font_path, 15)
        self.font_question = pygame.font.Font(font_path, 13)
        self.font_title = pygame.font.Font(font_path, 15)
        self.font_timer = pygame.font.Font(font_path, 24)
        self.font_control_title = pygame.font.Font(font_path, 36)

    def _process_quiz_result(self, quiz_result):
        if quiz_result == "finished":
            result_string = self.quiz_game.answer_result
        else:
            result_string = quiz_result
        
        self.quiz_timer.pause() 
        
        if len(self.answer_results) < self.max_questions:
            if result_string == "correct":
                if self.correct_sound:
                    self.correct_sound.play()
                self.answer_results.append("correct")
            else:
                if self.incorrect_sound:
                    self.incorrect_sound.play()
                self.answer_results.append("incorrect")

        if self.answer_results.count("incorrect") >= 3:
            self.state = "loss_sound_state"
            pygame.mixer.music.stop()
            if self.loss_sound:
                self.loss_sound.play()
                
        if quiz_result in ["correct", "incorrect"]:
            self.player.rect.x -= 20 
        
        return self.state


    def handle_events(self, event):
        if self.state in ["game_over", "loss_sound_state", "win_state"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.stop()
                    self.__init__(self.screen, self.size, self.font, self.character_choice)
                    self.answer_results.clear()
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    return "menu"
            return None

        if self.state == "controls_screen" and not self.is_fading:
            if event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN]):
                self.is_fading = True
                self.target_state = "game"
                self.fade_alpha = 0
                if self.controls_music:
                    self.controls_music.stop() # Detiene la música de control al pasar al juego
            return None

        if event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_RETURN]):
            
            if self.dialogo_active and self.typewriter:
                if not self.typewriter.finished():
                    self.typewriter.complete_text()
                    return None
                
                if self.state == "dialog":
                    self.timer.start()
                    self.quiz_timer = Timer(10)
                    self.quiz_timer.start()
                    self.state = "quiz_floor"
                    self.dialogo_active = False
                    self.typewriter = None
                    self.quiz_game = FloorQuiz_KeyAndCarry(self.size, self.questions, self.font_question, self.dialog_box_img, self.dialog_box_rect, self._dialog_img_loaded)
                    return None
                
                elif self.state == "quiz_complete_dialog":
                    self.current_dialog_index += 1
                    if self.current_dialog_index < len(self.post_quiz_dialogs):
                        next_text = self.post_quiz_dialogs[self.current_dialog_index]
                        self.typewriter = TypewriterText(next_text, self.font_dialog, (255,255,255), speed=25)
                        self.dialogo_active = True
                    else:
                        self.dialogo_active = False
                        self.typewriter = None
                        
            elif self.state == "game" and not self.dialogo_active and not self.guard_interacted:
                if self.player.rect.colliderect(self.guardia_collision_rect.inflate(20,20)):
                    self.state = "dialog"
                    self.dialogo_active = True
                    self.typewriter = TypewriterText(self.dialogo_text, self.font_dialog, (255,255,255), speed=25)
                    return None

            elif self.state == "quiz_floor" and self.quiz_game:
                if self.quiz_game.is_answered and not self.quiz_game.finished and self.state != "loss_sound_state":
                    self.quiz_timer = Timer(10)
                    self.quiz_timer.start()
                    self.quiz_game.next_question()
                    return None
                
                if not self.quiz_game.is_answered:
                    quiz_result = self.quiz_game.handle_interaction_input(self.player.rect, self.Guardia.rect)
                    
                    if quiz_result == "picked_up":
                        return None
                    elif quiz_result in ["correct", "incorrect", "finished"]:
                        return self._process_quiz_result(quiz_result)
        
        return None

    def update(self):
        keys = pygame.key.get_pressed()

        if self.is_fading:
            if self.state == "controls_screen":
                if self.target_state is None:
                    self.fade_alpha = max(0, self.fade_alpha - self.fade_in_speed)
                    if self.fade_alpha == 0:
                        self.is_fading = False
                elif self.target_state == "game":
                    self.fade_alpha = min(255, self.fade_alpha + self.fade_out_speed)
                    if self.fade_alpha == 255:
                        self.state = self.target_state
                        self.target_state = None
                        self.is_fading = True
            elif self.state == "game" and self.target_state is None:
                self.fade_alpha = max(0, self.fade_alpha - self.fade_in_speed)
                if self.fade_alpha == 0:
                    self.is_fading = False
                    if self.level_music_loaded and not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play(-1)
                        print("DEBUG PLAY: Música de fondo de Level 2 iniciada.")
            return self.state

        if self.state == "controls_screen":
            return self.state

        if self.state in ["game", "quiz_floor"]:
            if self.timer.is_running():
                self.timer.update()
            
            barrier = self.guardia_collision_rect
            
            if not self.dialogo_active:
                self.player.move(keys, self.size[0], self.size[1], barrier)
            else:
                self.player.move_animation_only()
            
            if self.quiz_game and self.quiz_game.carried_choice_index != -1:
                self.quiz_game.update_carried_choice_position(self.player.rect.centerx, self.player.rect.top)

            if self.quiz_game and self.state == "quiz_floor":
                self.quiz_game.check_player_collision(self.player.rect)

            if self.timer.finished and self.state not in ["loss_sound_state", "game_over", "win_state"]:
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                if self.loss_sound:
                    self.loss_sound.play()
                return self.state

        if self.state == "game":
            if self.guard_interacted and self.player.rect.colliderect(self.win_zone):
                pygame.mixer.music.stop()
                self.state = "win_state"
                self.confetti.reset()
                if self.win_music and not self.win_music_played:
                    self.win_music.play()
                    self.win_music_played = True
            
        elif self.state == "quiz_floor":
            if not self.quiz_timer.paused and not getattr(self.quiz_game, "is_answered", False):
                self.quiz_timer.update()

            if self.quiz_timer.finished and not getattr(self.quiz_game, "is_answered", False):
                if self.incorrect_sound:
                    self.incorrect_sound.play()
                if len(self.answer_results) < self.max_questions:
                    self.answer_results.append("incorrect")

                self.quiz_game.is_answered = True
                self.quiz_game.answer_result = "incorrect"
                self.quiz_game.carried_choice_index = -1
                self.quiz_timer.pause()
                
                if hasattr(self.quiz_timer, 'time_remaining'):
                    self.quiz_timer.time_remaining = 10 

                if self.answer_results.count("incorrect") >= 3:
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    if self.loss_sound:
                        self.loss_sound.play()

            if self.quiz_game and self.quiz_game.finished and getattr(self.quiz_game, 'is_answered', False):
                self.state = "quiz_complete_dialog"
                self.dialogo_active = True
                score = self.answer_results.count("correct")
                total = len(self.questions)

                if score == total:
                    dialog_text = "Muy bien hecho! Has demostrado tener una buena\n calidad de estudio."
                elif score >= 2:
                    dialog_text = "Buen trabajo. Tienes un buen nivel, sigue \npracticando."
                else:
                    dialog_text = "Puedes mejorar, sigue estudiando."

                self.post_quiz_dialogs = [
                    f"Has respondido correctamente {score} de {total} preguntas.",
                    dialog_text,
                    "Ahora te abro el paso. Buena suerte en tu camino!"
                ]
                self.current_dialog_index = 0
                self.typewriter = TypewriterText(self.post_quiz_dialogs[self.current_dialog_index], self.font_dialog, (255,255,255), speed=25)
                self.quiz_game = None
                self.timer.pause()
                self.quiz_timer.reset()
                if score >= 2:
                    self.confetti.start()
        
        elif self.state == "quiz_complete_dialog":
            if not self.dialogo_active and self.current_dialog_index >= len(self.post_quiz_dialogs):
                self.Guardia.rect.x -= 130
                guardia_width = self.Guardia.rect.width
                new_width = self.guardia_collision_rect.width
                new_height = self.guardia_collision_rect.height
                self.guardia_collision_rect = pygame.Rect(
                    self.Guardia.rect.x + int((guardia_width - new_width) / 2), 
                    self.Guardia.rect.y + self.Guardia.rect.height - new_height, 
                    new_width, 
                    new_height
                )
                self.player.rect.x = 450
                self.player.rect.y = 570
                self.guard_interacted = True
                if not self.background_changed:
                    self.background_image = self.background_image_open
                    self.background_changed = True
                self.state = "game"

        elif self.state == "loss_sound_state":
            if not self.loss_sound or not pygame.mixer.get_busy() or (self.loss_sound and self.loss_sound.get_num_channels() == 0):
                self.state = "game_over"
                if self.game_over_music and not self.game_over_music_played:
                    self.game_over_music.play(-1)
                    self.game_over_music_played = True

        if self.dialogo_active and self.typewriter:
            self.typewriter.update()
        self.confetti.update()
        return self.state
    
    def _draw_text_with_border(self, surface, text, font, text_color, border_color, center_pos, border_size=2):
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=center_pos)
        
        for dx in range(-border_size, border_size + 1):
            for dy in range(-border_size, border_size + 1):
                if dx != 0 or dy != 0:
                    border_rect = text_surface.get_rect(center=(center_pos[0] + dx, center_pos[1] + dy))
                    border_surface = font.render(text, True, border_color)
                    surface.blit(border_surface, border_rect)
        
        surface.blit(text_surface, text_rect)


    def draw(self):
        if self.state == "controls_screen":
            if self.control_image:
                screen_width, screen_height = self.size
                image_orig_width, image_orig_height = self.control_image.get_size()
                image_aspect = image_orig_width / image_orig_height
                scale_factor_w = screen_width / image_orig_width
                scale_factor_h = screen_height / image_orig_height
                if scale_factor_w < scale_factor_h:
                    new_width = screen_width
                    new_height = int(new_width / image_aspect)
                else:
                    new_height = screen_height
                    new_width = int(new_height * image_aspect)
                scaled_image = pygame.transform.scale(self.control_image, (new_width, new_height))
                target_rect = scaled_image.get_rect(center=(screen_width // 2, screen_height // 2))
                self.screen.fill((255, 255, 255))
                self.screen.blit(scaled_image, target_rect.topleft)
                
                font_to_use = self.font_control_title
                text_to_render_title = "CONTROLES"
                center_x_title = self.size[0] // 2
                center_y_title = 40 
                self._draw_text_with_border(self.screen, text_to_render_title, font_to_use, (0, 0, 0), (255, 128, 0), (center_x_title, center_y_title), border_size=4 )
                
                font_to_use = self.font_dialog
                text_to_render = "Presiona ESPACIO o ENTER para comenzar el Nivel 1"
                center_x = self.size[0] // 2
                center_y = self.size[1] - 30
                self._draw_text_with_border(self.screen, text_to_render, font_to_use, (0, 0, 0), (255, 128, 0), (center_x, center_y), border_size=2)
            else:
                self.screen.fill((255, 255, 255))
                font_to_use = self.font_dialog
                text1 = font_to_use.render("Error cargando Controles. Presiona ESPACIO.", True, (0, 0, 0))
                self.screen.blit(text1, text1.get_rect(center=(self.size[0] // 2, self.size[1] // 2)))

            if self.is_fading or self.fade_alpha > 0:
                fade_surface = pygame.Surface(self.size).convert_alpha()
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(fade_surface, (0, 0))
            return

        if self.state in ["game", "dialog", "quiz_complete_dialog", "quiz_floor", "loss_sound_state"]:
            self.screen.blit(self.background_image, (0, 0))
            self.Guardia.draw(self.screen)
            self.player.draw(self.screen)

            spacing = 18
            marco_w, marco_h = self.marco_img.get_size()
            total_width = self.max_questions * marco_w + (self.max_questions - 1) * spacing
            x_start = (self.size[0] - total_width) // 2
            y = 18

            for i in range(self.max_questions):
                x = x_start + i * (marco_w + spacing)
                self.screen.blit(self.marco_img, (x, y))

                if i < len(self.answer_results):
                    res = self.answer_results[i]
                    symbol_img = self.palomita_img if res == "correct" else self.tache_img
                    sx, sy = symbol_img.get_size()
                    sym_x = x + (marco_w - sx) // 2
                    sym_y = y + (marco_h - sy) // 2
                    self.screen.blit(symbol_img, (sym_x, sym_y))

            self.confetti.draw(self.screen)

            if self.state == "quiz_floor":
                self.quiz_timer.draw(self.screen, self.font_timer, is_quiz_timer=True, position=(680, 10))
            elif self.timer.is_running():
                self.timer.draw(self.screen, self.font_timer, position=(680, 10))

            if self.state == "quiz_floor" and self.quiz_game:
                self.quiz_game.draw(self.screen, self.player.rect)
                
                if self.quiz_game.carried_choice_index != -1:
                    drop_text = "Presiona ESPACIO/ENTER para ENTREGAR a la Prefecta."
                    text_surface = self.font_question.render(drop_text, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(self.size[0] // 2, self.Guardia.rect.top - 20))
                    self.screen.blit(text_surface, text_rect)
                elif not self.quiz_game.is_answered and self.quiz_game.highlighted_choice_index == -1:
                    drop_text = "MUEVETE CERCA DE UNA RESPUESTA para RECOGERLA."
                    text_surface = self.font_question.render(drop_text, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(self.size[0] // 2, self.size[1] - 250))
                    self.screen.blit(text_surface, text_rect)


            if self.dialogo_active:
                if self._dialog_img_loaded and self.dialog_box_img:
                    self.screen.blit(self.dialog_box_img, self.dialog_box_rect.topleft)
                    pygame.draw.rect(self.screen, (255, 200, 0), self.dialog_box_rect, width=5, border_radius=20)
                    self.typewriter.draw(self.screen, (self.dialog_box_rect.x + 20, self.dialog_box_rect.y + 35))
                else:
                    box_rect = pygame.Rect(50, 550, 800, 100)
                    pygame.draw.rect(self.screen, (20, 30, 80), box_rect, border_radius=10)
                    pygame.draw.rect(self.screen, (255, 200, 0), box_rect, 5, border_radius=10)
                    self.typewriter.draw(self.screen, (box_rect.x + 20, box_rect.y + 35))

        if self.state == "game_over":
            self.screen.fill((0, 0, 0))
            if self.game_over_image:
                self.screen.blit(self.game_over_image, (0, 0))
            font_to_use = self.font_title
            text_restart = "Presiona 'R' para Reiniciar"
            text_menu = "Presiona 'ESC' para volver al Menu"
            self._draw_text_with_border(self.screen, text_restart, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-80), border_size=3)
            self._draw_text_with_border(self.screen, text_menu, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-30), border_size=3)

        elif self.state == "win_state":
            self.screen.fill((0, 0, 0))
            if self.win_image:
                self.screen.blit(self.win_image, (0, 0))
            self.confetti.draw(self.screen)
            text_restart = "Presiona 'R' para Reiniciar"
            text_menu = "Presiona 'ESC' para volver al Menu"
            font_to_use = self.font_title
            self._draw_text_with_border(self.screen, text_restart, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-80), border_size=3)
            self._draw_text_with_border(self.screen, text_menu, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-30), border_size=3)