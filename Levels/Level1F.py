import pygame
import random
import math

# Importa las clases de los personajes y controladores del juego
from Personajes.boy import Characterb
from Personajes.girl import Characterg
from Personajes.Guardian import Characternpc 
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Controldeobjetos.timer import Timer

from Interacciones.FloorQuiz import FloorQuiz

# Inicializa el mezclador de audio (para música y sonidos)
try:
    pygame.mixer.init()
except pygame.error:
    pass


# ============================================================
# CLASE CONFETTI: controla el efecto visual al ganar el nivel
# ============================================================
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

    def reset(self):
        self.particles = []
        self.active = False

    def update(self):
        # Genera y actualiza partículas cuando está activo
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

        # Actualiza posición y elimina partículas muertas
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[5] -= 1
        self.particles = [p for p in self.particles if p[5] > 0 and p[1] < self.screen_height + 50]

    def draw(self, surface):
        # Dibuja cada partícula y su sombra
        for p in self.particles:
            x, y, dx, dy, color, life, size = p
            shadow_radius = int(size * 1.4)
            pygame.draw.circle(surface, (30, 30, 30), (int(x + 2), int(y + 3)), shadow_radius)
            pygame.draw.circle(surface, color, (int(x), int(y)), size)


# ============================================================
# CLASE LEVEL1: controla todo el funcionamiento del nivel
# ============================================================
class Level1:
    def __init__(self, screen, size, font, character_choice):
        self.screen = screen
        self.size = size
        self.font = font
        self.character_choice = character_choice

        # Pantalla de controles (se muestra al iniciar el nivel)
        try:
            self.control_image = pygame.image.load('Materials/Pictures/Assets/Control.jpg').convert()
        except pygame.error:
            self.control_image = None

        # Controla la animación de fundido (fade in/out)
        self.fade_alpha = 255 if self.control_image else 0
        self.fade_in_speed = 5
        self.fade_out_speed = 10
        self.is_fading = True
        self.target_state = None

        # Estado inicial del juego
        if self.control_image:
            self.state = "controls_screen"
        else:
            self.state = "game"
            self.is_fading = True
            self.fade_alpha = 255

        # Crea el jugador según la elección
        if self.character_choice == "boy":
            self.player = Characterb(440, 600, 2)
        else:
            self.player = Characterg(440, 600, 2)

        # Crea el guardia (NPC)
        self.Guardia = Characternpc(470, 330, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')

        # Define área de colisión del guardia (más pequeña que su sprite)
        guardia_width = self.Guardia.rect.width
        guardia_height = self.Guardia.rect.height
        COL_WIDTH_FACTOR = 0.5
        COL_HEIGHT_PIXELS = 5
        new_width = int(guardia_width * COL_WIDTH_FACTOR)
        new_height = COL_HEIGHT_PIXELS
        new_x = self.Guardia.rect.x + int((guardia_width - new_width) / 2)
        new_y = self.Guardia.rect.y + guardia_height - new_height
        self.guardia_collision_rect = pygame.Rect(new_x, new_y, new_width, new_height)

        # Fondo con puerta cerrada
        try:
            self.background_image_game = pygame.image.load('Materials/Pictures/Assets/fondo_CloseDoor.jpeg').convert()
            self.background_image_game = pygame.transform.scale(self.background_image_game, self.size)
        except pygame.error:
            self.background_image_game = pygame.Surface(self.size)
            self.background_image_game.fill((0, 0, 0))
        self.background_image = self.background_image_game

        # Fondo con puerta abierta
        try:
            self.background_image_open = pygame.image.load('Materials/Pictures/Assets/fondo_OpenDoor.jpeg').convert()
            self.background_image_open = pygame.transform.scale(self.background_image_open, self.size)
        except pygame.error:
            self.background_image_open = self.background_image_game
        self.background_changed = False

        # Cuadro de diálogo inferior (imagen)
        try:
            img = pygame.image.load("Materials/Pictures/Assets/dialog_box.png").convert_alpha()
            self.dialog_box_img = pygame.transform.scale(img, (800, 120))
            self.dialog_box_rect = self.dialog_box_img.get_rect()
            self.dialog_box_rect.center = (self.size[0] // 2, self.size[1] - 70)  # posición en pantalla
            self._dialog_img_loaded = True
        except Exception:
            # Cuadro alternativo dibujado con rectángulo si falla la carga
            self._dialog_img_loaded = False
            self.dialog_box_img = None
            self.dialog_box_rect = pygame.Rect(50, self.size[1] - 150, 800, 100)

        # Pantallas de victoria y derrota
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

        # Temporizadores
        self.timer = Timer(120)      # tiempo general del nivel
        self.quiz_timer = Timer(10)  # tiempo para responder cada pregunta

        # Gestor de vidas (corazones)
    
        # palomitas y taches
        self.answer_results = [] # guarda si la respuesta fue correcta o incorrecta
        self.max_questions = 3 # mostrara tres cuadros vacios
        

        # Carga sonidos y música
        self.controls_music = None
        self.level_music_loaded = False
        try:
            self.controls_music = pygame.mixer.Sound('Materials/Music/controls.wav')
            pygame.mixer.music.load('Materials/Music/Level1.wav')
            self.level_music_loaded = True
            self.loss_sound = pygame.mixer.Sound('Materials/Music/antesover.wav')
            self.game_over_music = pygame.mixer.Sound('Materials/Music/GameOver.wav')
            self.win_music = pygame.mixer.Sound('Materials/Music/Ganar.wav')
            self.correct_sound = pygame.mixer.Sound('Materials/Music/PreguntaB.wav')
            self.incorrect_sound = pygame.mixer.Sound('Materials/Music/PreguntaM.wav')
        except Exception:
            self.loss_sound = None
            self.game_over_music = None
            self.win_music = None
            self.correct_sound = None
            self.incorrect_sound = None

        # Texto inicial del guardia
        self.dialogo_text = "Si quieres pasar, tendras que responder estas\n preguntas!!"
        self.typewriter = None
        self.dialogo_active = False

        # Control del quiz y diálogos posteriores
        self.quiz_game = None
        self.post_quiz_dialogs = []
        self.current_dialog_index = 0
        self.guard_interacted = False

        # Estados de música y efectos
        self.game_over_music_played = False
        self.win_music_played = False

        # Confeti (efecto de victoria)
        self.confetti = Confetti(self.size[0], self.size[1])

        # Preguntas del minijuego
        self.questions = [
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cómo se llama nuestro país?", "choices": ["España", "México", "Roma", "Berlín"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuánto es 6 + 2?", "choices": ["7", "8", "9", "10"], "correct_answer": 1 }, 
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuál es el animal más grande del mundo?", "choices": ["Ballena azul", "Elefante", "Tiburón", "Jirafa"], "correct_answer": 0 }, 
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuál es el océano más grande?", "choices": ["Atlántico", "Índico", "Pacífico", "Ártico"], "correct_answer": 2 }
        ]

        # Zona de victoria (puerta)
        self.win_zone = pygame.Rect(420, 280, 65, 65)

        # Fuentes del texto (PressStart2P)
        self.font_base = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 18)
        self.font_dialog = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 15)
        self.font_question = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 13)
        self.font_title = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 15)
        self.font_timer = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 24)
        self.font_control_title = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 36)
# ============================================================
    # Maneja los eventos del teclado y las interacciones del jugador
    # ============================================================
    def handle_events(self, event):
        # Reinicio o salida desde pantalla final
        if self.state in ["game_over", "loss_sound_state", "win_state"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.stop()
                    self.__init__(self.screen, self.size, self.font, self.character_choice)
                    self.answer_results.clear() # reinicia los cuadros de respuestas
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    return "menu"
            return None

        # Pantalla de controles (presionar espacio para continuar)
        if self.state == "controls_screen" and not self.is_fading:
            if event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN]):
                self.is_fading = True
                self.target_state = "game"
                self.fade_alpha = 0
                if self.controls_music:
                    self.controls_music.stop()
            return None

        # Interacción con diálogos o quiz (espacio/enter)
        if event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_RETURN]):
            if self.dialogo_active and self.typewriter:
                if not self.typewriter.finished():
                    self.typewriter.complete_text()
                elif self.state == "dialog":
                    # Inicia el quiz cuando termina el diálogo del guardia
                    self.timer.start()
                    self.quiz_timer = Timer(10)
                    self.quiz_timer.start()
                    self.state = "quiz_floor"
                    self.dialogo_active = False
                    self.typewriter = None
                    self.quiz_game = FloorQuiz(self.size, self.questions, self.font_question)
                elif self.state == "quiz_complete_dialog":
                    # Avanza los diálogos después del quiz
                    self.current_dialog_index += 1
                    if self.current_dialog_index < len(self.post_quiz_dialogs):
                        next_text = self.post_quiz_dialogs[self.current_dialog_index]
                        self.typewriter = TypewriterText(next_text, self.font_dialog, (255,255,255), speed=25)
                        self.dialogo_active = True
                    else:
                        self.dialogo_active = False
                        self.typewriter = None

        # Manejo del quiz (respuestas correctas/incorrectas)
        if self.state == "quiz_floor" and self.quiz_game:
            result = self.quiz_game.handle_event(event)
            if result in ["correct", "incorrect"]:
                # guardar resultado
                if result == "correct":
                    if self.correct_sound:
                        self.correct_sound.play()
                    self.answer_results.append("correct")
                else:
                    if self.incorrect_sound:
                        self.incorrect_sound.play()
                    self.answer_results.append("incorrect")
                
                # limitar a 3 resultados
                if len(self.answer_results) > self.max_questions:
                    self.answer_results.pop(0)
                
                #pausar temporizador del quiz
                self.quiz_timer.pause()
                self.quiz_timer.pause()
                
                if self.answer_results.count("incorrect") >= 3:
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    if self.loss_sound:
                        self.loss_sound.play()
                # pasa a la siguiente pregunta
                self.quiz_timer = Timer(10)
                self.quiz_timer.start()
            elif result == "finished":
                self.quiz_timer.pause()
        return None

    # ============================================================
    # Actualiza la lógica del juego según el estado actual
    # ============================================================
    def update(self):
        keys = pygame.key.get_pressed()

        # Transiciones de fundido (fade in/out)
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
                    # Reproduce música del nivel
                    if self.level_music_loaded and not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play(-1)

        # Pantalla de controles
        if self.state == "controls_screen":
            if not self.is_fading and self.controls_music:
                if not pygame.mixer.get_busy() or self.controls_music.get_num_channels() == 0:
                    self.controls_music.play(-1)
            return self.state

        # Estados de juego y quiz
        if self.state in ["game", "quiz_floor"]:
            if self.timer.is_running():
                self.timer.update()
            barrier = self.guardia_collision_rect if not self.guard_interacted else None
            self.player.move(keys, self.size[0], self.size[1], barrier)

            # Si el tiempo se acaba, pierde
            if self.timer.finished and self.state not in ["loss_sound_state", "game_over", "win_state"]:
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                if self.loss_sound:
                    self.loss_sound.play()
                return self.state

        # Interacción con el guardia
        if self.state == "game":
            # Si ya pasó el guardia y toca la zona de victoria
            if self.guard_interacted and self.player.rect.colliderect(self.win_zone):
                pygame.mixer.music.stop()
                self.state = "win_state"
                self.confetti.reset()
                if self.win_music and not self.win_music_played:
                    self.win_music.play()
                    self.win_music_played = True

            # Cuando el jugador se acerca al guardia
            if not self.is_fading and self.player.rect.colliderect(self.guardia_collision_rect.inflate(20,20)) and (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and not self.guard_interacted:
                self.state = "dialog"
                self.dialogo_active = True
                self.typewriter = TypewriterText(self.dialogo_text, self.font_dialog, (255,255,255), speed=25)

        # Estado del quiz (temporizador y respuestas)
        elif self.state == "quiz_floor":
            if not self.quiz_timer.paused and not getattr(self.quiz_game, "is_answered", False):
                self.quiz_timer.update()
            if self.quiz_timer.finished and not getattr(self.quiz_game, "is_answered", False):
                # tiempo agotado = respuesta incorrecta
                if self.incorrect_sound:
                    self.incorrect_sound.play()
                # Registrar tache por tiempo agotado
                self.answer_results.append("incorrect")
                
                self.quiz_game.is_answered = True
                self.quiz_game.answer_result = "incorrect"
                self.quiz_game.selected_choice_index = -1
                self.quiz_timer.pause()
                
                # Condición para terminar el juego si hay 3 taches
                if self.answer_results.count("incorrect") >= 3:
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    if self.loss_sound:
                        self.loss_sound.play()
            # Verifica colisión del jugador con los cuadros del quiz
            self.quiz_game.check_player_collision(self.player.rect)

            # Si termina el quiz, muestra diálogo final
            if self.quiz_game.finished:
                self.state = "quiz_complete_dialog"
                self.dialogo_active = True
                score = self.quiz_game.correct_answers
                total = len(self.questions)

                # Determina mensaje según puntaje
                if score == total:
                    dialog_text = "¡Muy bien hecho! Has demostrado tener una buena\n calidad de estudio."
                elif score >= 3:
                    dialog_text = "Buen trabajo. Tienes un buen nivel, sigue \npracticando."
                else:
                    dialog_text = "Puedes mejorar, sigue estudiando."

                self.post_quiz_dialogs = [
                    f"Has respondido correctamente {score} de {total} preguntas.",
                    dialog_text,
                    "Ahora te abro el paso. ¡Buena suerte en tu camino!"
                ]
                self.current_dialog_index = 0
                self.typewriter = TypewriterText(self.post_quiz_dialogs[self.current_dialog_index], self.font_dialog, (255,255,255), speed=25)
                self.quiz_game = None
                self.timer.pause()
                self.quiz_timer.reset()
                if score >= 2:
                    self.confetti.start()

        # Diálogo final tras el quiz
        elif self.state == "quiz_complete_dialog":
            if not self.dialogo_active and self.current_dialog_index >= len(self.post_quiz_dialogs):
                # Mueve al guardia para liberar el paso
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

        # Estado de derrota (reproduce sonido y pasa a game_over)
        elif self.state == "loss_sound_state":
            if not pygame.mixer.get_busy() or (self.loss_sound and self.loss_sound.get_num_channels() == 0):
                self.state = "game_over"
                if self.game_over_music and not self.game_over_music_played:
                    self.game_over_music.play(-1)
                    self.game_over_music_played = True

        # Actualiza texto y confeti
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


    # ============================================================
    # Dibuja todos los elementos en pantalla según el estado
    # ============================================================
    def draw(self):
        # Pantalla de controles
        if self.state == "controls_screen":
            if self.control_image:
                # Escala imagen de controles al tamaño de la pantalla
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
                try:
                    text_to_render_title = "CONTROLES"
                    center_x_title = self.size[0] // 2
                    center_y_title = 40 
                    
                    self._draw_text_with_border(
                        self.screen, 
                        text_to_render_title, 
                        self.font_control_title, 
                        (0, 0, 0), 
                        (255, 128, 0), 
                        (center_x_title, center_y_title),
                        border_size=4 
                    )
                except Exception:
                    pass
                
                font_to_use = self.font_dialog if hasattr(self, 'font_dialog') else self.font
                try:
                    text_to_render = "Presiona ESPACIO o ENTER para comenzar el Nivel 1"
                    center_x = self.size[0] // 2
                    center_y = self.size[1] - 30
                    
                    self._draw_text_with_border(
                        self.screen, 
                        text_to_render, 
                        font_to_use, 
                        (0, 0, 0), 
                        (255, 128, 0), 
                        (center_x, center_y),
                        border_size=2
                    )
                except Exception:
                    pass
            else:
                # Si falla la carga muestra texto
                self.screen.fill((255, 255, 255))
                font_to_use = self.font_dialog
                text1 = font_to_use.render("Error cargando Controles. Presiona ESPACIO.", True, (0, 0, 0))
                self.screen.blit(text1, text1.get_rect(center=(self.size[0] // 2, self.size[1] // 2)))

            # Dibuja efecto de fundido
            if self.is_fading or self.fade_alpha > 0:
                fade_surface = pygame.Surface(self.size).convert_alpha()
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(fade_surface, (0, 0))
            return

        # Dibujo principal del juego
        if self.state in ["game", "dialog", "quiz_complete_dialog", "quiz_floor", "loss_sound_state"]:
            self.screen.blit(self.background_image, (0, 0))
            self.Guardia.draw(self.screen)
            self.player.draw(self.screen)
            # self.life_manager.draw(self.screen)
            square_size = 40
            spacing = 20
            start_x = 30
            y = 20

            for i in range(self.max_questions):
                x = start_x + i * (square_size + spacing)
                rect = pygame.Rect(x, y, square_size, square_size)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=5)

                # dibujar palomita o tache ya hay resultados
                if i < len(self.answer_results):
                    result = self.answer_results[i]
                    symbol = "✓" if result == "correct" else "✗"
                    color = (0, 255, 0) if result == "correct" else (255, 0, 0)
                    text_surface = self.font_timer.render(symbol, True, color)
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)
            self.confetti.draw(self.screen)

            # Dibuja timers
            if self.state == "quiz_floor":
                self.quiz_timer.draw(self.screen, self.font_timer, is_quiz_timer=True, position=(680, 10))
            elif self.timer.is_running():
                self.timer.draw(self.screen, self.font_timer, position=(680, 10))

            # Dibuja quiz si está activo
            if self.state == "quiz_floor" and self.quiz_game:
                self.quiz_game.draw(self.screen)

            # Dibuja cuadro de diálogo
            if self.dialogo_active:
                if self._dialog_img_loaded and self.dialog_box_img:
                    self.screen.blit(self.dialog_box_img, self.dialog_box_rect.topleft)
                    pygame.draw.rect(self.screen, (255, 200, 0), self.dialog_box_rect, width=5, border_radius=20)
                    self.typewriter.draw(self.screen, (self.dialog_box_rect.x + 20, self.dialog_box_rect.y + 35))
                else:
                    # Cuadro alternativo si no hay imagen
                    box_rect = pygame.Rect(50, 550, 800, 100)
                    pygame.draw.rect(self.screen, (20, 30, 80), box_rect, border_radius=10)
                    pygame.draw.rect(self.screen, (255, 200, 0), box_rect, 5, border_radius=10)
                    self.typewriter.draw(self.screen, (box_rect.x + 20, box_rect.y + 35))
        # Pantalla de derrota
        if self.state == "game_over":
            self.screen.fill((0, 0, 0))
            if self.game_over_image:
                self.screen.blit(self.game_over_image, (0, 0))
            font_to_use = self.font_title
            text_restart = "Presiona 'R' para Reiniciar"
            text_menu = "Presiona 'ESC' para volver al Menú"
            self._draw_text_with_border(self.screen, text_restart, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-80), border_size=3)
            self._draw_text_with_border(self.screen, text_menu, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-30), border_size=3)

        # Pantalla de victoria
        elif self.state == "win_state":
            self.screen.fill((0, 0, 0)) 
            if self.win_image:
                self.screen.blit(self.win_image, (0, 0))
            self.confetti.draw(self.screen)
            text_restart = "Presiona 'R' para Reiniciar"
            text_menu = "Presiona 'ESC' para volver al MenÃº"
            font_to_use = self.font_title 
            self._draw_text_with_border(self.screen, text_restart, font_to_use, (255, 255, 255), (0, 0, 0), (self.size[0] // 2, self.size[1] - 80), border_size=3)
            self._draw_text_with_border(self.screen, text_menu, font_to_use, (255, 255, 255), (0, 0, 0), (self.size[0] // 2, self.size[1] - 30), border_size=3)

        # Estado de perdida        
        elif self.state == "loss_sound_state":
            self.screen.blit(self.background_image, (0, 0)) 
            self.player.draw(self.screen)
            self.Guardia.draw(self.screen)
                