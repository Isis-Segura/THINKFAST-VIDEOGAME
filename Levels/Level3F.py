import pygame
import random
import time
import math
from Personajes.boy import Characterb
from Personajes.girl import Characterg
from Personajes.Prefect import Characternpcp 
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Controldeobjetos.timer import Timer
from Interacciones.Mecanicas.FloorQuiz import FloorQuiz 
from Interacciones.Controldeobjetos.AnswerPickup import AnswerPickup 
from Interacciones.Mecanicas.question_board import show_question_board

# Inicializa el mezclador de audio (para música y sonidos)
try:
    pygame.mixer.init()
except pygame.error:
    pass

# CLASE CONFETTI:
class Confetti:
    def __init__(self, screen_width, screen_height):
        # Inicialización de partículas y colores
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
            # Lógica para generar confeti desde los lados
            for _ in range(self.spawn_rate):
                side = random.choice(["left", "right"])
                x = 0 if side == "left" else self.screen_width
                y = random.randint(0, self.screen_height // 3)
                dx = random.uniform(-3, 3)
                
                # Asegura que el movimiento sea hacia el centro
                if side == "right" and dx > -0.5:
                    dx = random.uniform(-3, -0.8)
                if side == "left" and dx < 0.5:
                    dx = random.uniform(0.8, 3)
                
                dy = random.uniform(1.5, 4.0)
                color = random.choice(self.colors)
                life = random.randint(int(self._max_life*0.6), self._max_life)
                size = random.randint(4, 7)
                self.particles.append([x, y, dx, dy, color, life, size])

        # Actualiza posición y vida
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[5] -= 1
        self.particles = [p for p in self.particles if p[5] > 0 and p[1] < self.screen_height + 50]

    def draw(self, surface):
        # Dibuja el confeti
        for p in self.particles:
            x, y, dx, dy, color, life, size = p
            shadow_radius = int(size * 1.4)
            pygame.draw.circle(surface, (30, 30, 30), (int(x + 2), int(y + 3)), shadow_radius)
            pygame.draw.circle(surface, color, (int(x), int(y)), size)

# CLASE MENSAJE FLOTANTE
class FloatingMessage:
    def __init__(self, text, font, duration=5):
        self.text = text
        self.font = font
        self.duration = duration
        self.start_time = time.time()
        self.active = True
        
    def update(self):
        if time.time() - self.start_time > self.duration:
            self.active = False
            
    def draw(self, surface, position):
        if not self.active:
            return
            
        # Colores para el mensaje
        LIGHT_BROWN = (160, 120, 80)  # Madera clara
        BROWN = (139, 69, 19)         # Café para el marco
        BLACK = (0, 0, 0)
        
        # Crear superficie para el mensaje con efecto de madera
        text_surface = self.font.render(self.text, True, BLACK)
        padding = 15  # Reducido de 20 a 15
        rect_width = text_surface.get_width() + padding * 2
        rect_height = text_surface.get_height() + padding * 2
        
        # Crear superficie para el mensaje
        message_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        
        # Dibujar fondo de madera
        pygame.draw.rect(message_surface, LIGHT_BROWN, (0, 0, rect_width, rect_height), border_radius=12)  # Reducido de 15 a 12
        pygame.draw.rect(message_surface, BROWN, (0, 0, rect_width, rect_height), 2, border_radius=12)  # Reducido grosor de 3 a 2
        
        # Añadir textura de madera (rayas)
        for i in range(0, rect_width, 3):  # Reducido de 4 a 3
            pygame.draw.line(message_surface, (120, 80, 40), (i, 0), (i, rect_height), 1)
        
        # Dibujar texto
        text_rect = text_surface.get_rect(center=(rect_width // 2, rect_height // 2))
        message_surface.blit(text_surface, text_rect)
        
        # Dibujar en la posición especificada
        surface.blit(message_surface, position)


# CLASE LEVEL3: implementa la mecánica de agarrar y entregar
class Level3:
    def __init__(self, screen, size, font, character_choice):

        # Parametrización de hitboxes y trigger (ajustables)
        self.HITBOX_SHRINK_X = 20   # píxeles a quitar del ancho de la colisión
        self.HITBOX_SHRINK_Y = 10   # píxeles a quitar de la altura de la colisión
        self.TEACHER_TRIGGER_MARGIN = 40  # margen alrededor del profesor para activar interacción

        self.flash_color = None
        self.flash_alpha = 0
        self.flash_timer = 0
        self.screen = screen
        self.size = size
        self.font = font
        self.character_choice = character_choice

        # Controla qué mecánica usar (True = quiz con temporizador, False = pizarra de relaciones)
        self.use_quiz_timer = True

        # Mensaje flotante
        self.show_initial_message = True
        self.message_start_time = time.time()
        self.message_font = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 12)  # Reducido de 16 a 12
        self.floating_message = FloatingMessage("Presiona ENTER o ESPACIO para interactuar con el profesor", self.message_font, 5)

        # Pantalla de controles
        try:
            self.control_image = pygame.image.load('Materials/Pictures/Assets/Control3.jpg').convert()
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

        # Crea maestro
        self.maestro = Characternpcp(500, 250, 'Materials/Pictures/Characters/MAESTRO_NIVEL_3.png')

        # DEFINE ÁREA DE COLISIÓN DEL MAESTRO USANDO PARÁMETROS (pequeña y ajustable)
        maestro_width = self.maestro.rect.width
        maestro_height = self.maestro.rect.height
        
        COL_WIDTH_FACTOR = 0.10
        COL_HEIGHT_PIXELS = 4
        
        new_width = int(maestro_width * COL_WIDTH_FACTOR)
        new_height = COL_HEIGHT_PIXELS
        new_x = self.maestro.rect.x + int((maestro_width - new_width) / 2)
        new_y = self.maestro.rect.y + maestro_height - new_height
        
        self.maestro_collision_rect = pygame.Rect(new_x, new_y, new_width, new_height)
        self.maestro_drop_zone = self.maestro_collision_rect.inflate(30, 30)

        # NUEVO: Definir colisiones del entorno (obstáculos)
        self.obstacles = [
            # Bordes de la pantalla
            pygame.Rect(0, 0, self.size[0], 0),  # Borde superior
            pygame.Rect(0, 0, 10, self.size[1]),  # Borde izquierdo
            pygame.Rect(self.size[0]-10, 0, 5, self.size[1]),  # Borde derecho
            pygame.Rect(0, self.size[1]-10, self.size[0], 10),  # Borde inferior 
        ]

        # Fondos
        try:
            self.background_image_game = pygame.image.load('Materials/Pictures/Assets/fondo_nivel_3.png').convert() 
            self.background_image_game = pygame.transform.scale(self.background_image_game, self.size)
        except pygame.error:
            self.background_image_game = pygame.Surface(self.size)
            self.background_image_game.fill((50, 50, 50))
        self.background_image = self.background_image_game

        try:
            self.background_image_open = pygame.image.load('Materials/Pictures/Assets/fondo_nivel_3.png').convert() 
            self.background_image_open = pygame.transform.scale(self.background_image_open, self.size)
        except pygame.error:
            self.background_image_open = self.background_image_game
        self.background_changed = False

        # Cuadro de diálogo inferior (imagen)
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
        self.timer = Timer(150)  # Tiempo general del nivel
        
        # --- Temporizador y Bandera para la Pantalla de Controles (10s) ---
        self.control_timer = Timer(10) # 10 segundos
        self.control_timer_started = False
        self.can_skip_controls = False
        # -------------------------------------------------------------------------

        # Carga sonidos y música
        self.controls_music = None
        self.level_music_loaded = False
        try:
            # Música de controles unificada
            self.controls_music = pygame.mixer.Sound('Materials/Music/controls.wav')
            # Música de nivel unificada
            pygame.mixer.music.load('Materials/Music/Level3.wav')
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
        self.dialogo_text = "Bienvenidos al nivel 3. Esta vez, tendras que\ntraerme la respuesta correcta para pasar."
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

        # NUEVOS ELEMENTOS para la mecánica de AGARRAR Y ENTREGAR
        self.held_answer = None
        self.answer_pickups = pygame.sprite.Group()
        
        # Preguntas del minijuego (ya no se usan para el quiz con temporizador)
        self.questions = [
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "Relaciona cada lenguaje con su familia (ejemplo):", "choices": ["Python", "Java", "C", "Haskell"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "Relaciona cada número con su potencia de 2:", "choices": ["32", "64", "16", "8"], "correct_answer": 1 }, 
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "Relaciona cada ciudad con su país:", "choices": ["Sídney", "Melbourne", "Canberra", "Perth"], "correct_answer": 2 }, 
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "Relaciona cada fórmula con su compuesto:", "choices": ["CO2", "H2O", "O3", "N2"], "correct_answer": 1 }
        ]

        # Zona de victoria (puerta)
        self.win_zone = pygame.Rect(420, 280, 65, 65)

        # Fuentes del texto
        font_path = "Materials/Fonts/PressStart2P-Regular.ttf"
        
        self.font_base = pygame.font.Font(font_path, 18)
        self.font_dialog = pygame.font.Font(font_path, 15)
        self.font_question = pygame.font.Font(font_path, 13)
        self.font_title = pygame.font.Font(font_path, 15)
        self.font_timer = pygame.font.Font(font_path, 24)
        self.font_control_title = pygame.font.Font(font_path, 36)
        self.font_control_text = pygame.font.Font(font_path, 18) 
    
    # FUNCIONES AUXILIARES
    
    def get_hitbox(self, rect: pygame.Rect):
        """Devuelve un rect reducido (hitbox) a partir del rect original del sprite."""
        try:
            return rect.inflate(-self.HITBOX_SHRINK_X, -self.HITBOX_SHRINK_Y)
        except Exception:
            return rect

    def teacher_trigger_rect(self):
        """Área alrededor del profesor donde se permite activar la pizarra."""
        return pygame.Rect(
            self.maestro.rect.x - self.TEACHER_TRIGGER_MARGIN,
            self.maestro.rect.y - self.TEACHER_TRIGGER_MARGIN,
            self.maestro.rect.width + self.TEACHER_TRIGGER_MARGIN * 2,
            self.maestro.rect.height + self.TEACHER_TRIGGER_MARGIN * 2
        )

    def both_at_teacher(self):
        """
        Revisa si el jugador y (si existe) el monito están dentro del área de trigger del maestro.
        """
        trigger = self.teacher_trigger_rect()
        player_hit = self.get_hitbox(self.player.rect)
        player_inside = trigger.colliderect(player_hit)
        if hasattr(self, 'monkey') and self.monkey is not None:
            monkey_hit = self.get_hitbox(self.monkey.rect)
            monkey_inside = trigger.colliderect(monkey_hit)
            return player_inside and monkey_inside
        else:
            return player_inside

    def _draw_text_with_border(self, surface, text, font, text_color, border_color, center_pos, border_size=2):
        # Helper para dibujar texto con un borde (shadow-like)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=center_pos)
        
        for dx in range(-border_size, border_size + 1):
            for dy in range(-border_size, border_size + 1):
                if dx != 0 or dy != 0:
                    border_rect = text_surface.get_rect(center=(center_pos[0] + dx, center_pos[1] + dy))
                    border_surface = font.render(text, True, border_color)
                    surface.blit(border_surface, border_rect)
        
        surface.blit(text_surface, text_rect)

    def _generate_answer_pickups(self):
        """Genera los objetos AnswerPickup para la pregunta actual en el suelo."""
        self.answer_pickups.empty()
        self.held_answer = None
        
        current_q_index = self.current_question_index 
        if current_q_index >= len(self.questions):
            return 
            
        q_data = self.questions[current_q_index]
        
        positions = [(180, 500), (350, 500), (520, 500), (690, 500)] 
        
        num_options = min(len(q_data["choices"]), len(positions))
        
        for i, choice in enumerate(q_data["choices"][:num_options]):
            is_correct = (i == q_data["correct_answer"])
            answer = AnswerPickup(
                *positions[i], 
                choice, 
                self.font_question, 
                is_correct, 
                current_q_index
            )
            self.answer_pickups.add(answer)

    def _submit_answer(self, answer_pickup):
        """Verifica la respuesta entregada, registra el resultado y avanza la pregunta."""
        is_correct = answer_pickup.is_correct
        
        if len(self.answer_results) < self.max_questions:
            result_string = "correct" if is_correct else "incorrect"
            self.answer_results.append(result_string)
            
            if is_correct:
                if self.correct_sound: self.correct_sound.play()
            else:
                if self.incorrect_sound: self.incorrect_sound.play()

            answer_pickup.visible = False
            answer_pickup.is_held = False
            self.held_answer = None
            
            if self.answer_results.count("incorrect") >= 3:
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                if self.loss_sound: self.loss_sound.play()
                return

        if len(self.answer_results) < self.max_questions:
            self.current_question_index += 1
            if self.current_question_index < self.max_questions:
                if self.quiz_game and hasattr(self.quiz_game, 'current_question_index'):
                    self.quiz_game.current_question_index = self.current_question_index
                
                self._generate_answer_pickups()
                self.quiz_timer = Timer(10)
                self.quiz_timer.start()
            else:
                if self.quiz_game and hasattr(self.quiz_game, 'finished'):
                    self.quiz_game.finished = True
        else:
            if self.quiz_game and hasattr(self.quiz_game, 'finished'):
                self.quiz_game.finished = True
    
    def _check_collision_with_obstacles(self, new_rect):
        """Verifica si un rectángulo colisiona con algún obstáculo"""
        for obstacle in self.obstacles:
            if new_rect.colliderect(obstacle):
                return True
        return False
    
    # MANEJO DE EVENTOS
    def handle_events(self, event):
        # Reinicio o salida desde pantalla final
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

        # Pantalla de controles
        if self.state == "controls_screen" and not self.is_fading:
            if self.can_skip_controls and event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN]):
                self.is_fading = True
                self.target_state = "game"
                self.fade_alpha = 0
                if self.controls_music:
                    self.controls_music.stop()
            return None

        # Teclas de interacción (Espacio/Enter)
        if event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_RETURN]):
            # Ocultar mensaje inicial al interactuar
            self.show_initial_message = False
            
            # Si estamos en el juego y estamos en la zona del maestro, abrimos la mecánica seleccionada
            if self.state == "game" and not self.guard_interacted and self.both_at_teacher():
                
                if self.use_quiz_timer:
                    # USAR EL QUIZ CON TEMPORIZADOR
                    try:
                        from Interacciones.Mecanicas.quiz_timer_relaciones import run_quiz_with_timer
                        passed = run_quiz_with_timer(self.screen, "Materials/Pictures/Assets/fondo_nivel_3.png")
                        
                        # Procesar resultado del quiz (ahora usa el return del quiz_timer_relaciones)
                        if passed:
                            if self.correct_sound: 
                                self.correct_sound.play()
                            # Mover al maestro y liberar el paso
                            self.maestro.rect.x -= 130
                            maestro_width = self.maestro.rect.width
                            new_width = self.maestro_collision_rect.width
                            self.maestro_collision_rect.x = self.maestro.rect.x + int((maestro_width - new_width) / 2)
                            self.maestro.rect.y = 330
                            self.player.rect.x = 450
                            self.player.rect.y = 570
                            self.guard_interacted = True
                            if not self.background_changed:
                                self.background_image = self.background_image_open
                                self.background_changed = True
                            self.confetti.start()
                        else:
                            # Respuesta incorrecta - mostrar pantalla de derrota
                            if self.incorrect_sound: 
                                self.incorrect_sound.play()
                            self.state = "game_over"
                            pygame.mixer.music.stop()
                    except ImportError:
                        # Fallback a la pizarra de relaciones si no se encuentra el quiz
                        self._use_relation_board()
                
                else:
                    # USAR LA PIZARRA DE RELACIONES
                    self._use_relation_board()
                
                return None

            # Lógica de Diálogo (existente)
            keys = pygame.key.get_pressed() 
            if self.dialogo_active and self.typewriter:
                if not self.typewriter.finished():
                    self.typewriter.complete_text()
                elif self.state == "dialog":
                    self.timer.start()
                    self.state = "game"
                    self.dialogo_active = False
                    self.typewriter = None
                    
                elif self.state == "quiz_complete_dialog":
                    self.current_dialog_index += 1
                    if self.current_dialog_index < len(self.post_quiz_dialogs):
                        next_text = self.post_quiz_dialogs[self.current_dialog_index]
                        self.typewriter = TypewriterText(next_text, self.font_dialog, (255,255,255), speed=25)
                        self.dialogo_active = True
                    else:
                        self.dialogo_active = False
                        self.typewriter = None

        # Ocultar mensaje inicial al hacer clic
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.show_initial_message = False

        return None

    def _use_relation_board(self):
        """Método auxiliar para usar la pizarra de relaciones"""
        q_idx = self.current_question_index if self.current_question_index < len(self.questions) else 0
        q_data = self.questions[q_idx]
        left = list(q_data.get("choices", []))
        right = left.copy()
        random.shuffle(right)
        question_data = {
            "question": q_data.get("question", "Relaciona las opciones:"),
            "left": left,
            "right": right
        }

        result = show_question_board(self.screen, question_data, font=self.font_question)
        if not result or result.get("cancelled", False):
            return

        pairs = result.get("pairs", {})
        all_ok = True
        for li, ri in pairs.items():
            try:
                if right[ri] != left[li]:
                    all_ok = False
                    break
            except Exception:
                all_ok = False
                break

        if all_ok and len(pairs) == len(left):
            if self.correct_sound: 
                self.correct_sound.play()
            self.maestro.rect.x -= 130
            maestro_width = self.maestro.rect.width
            new_width = self.maestro_collision_rect.width
            self.maestro_collision_rect.x = self.maestro.rect.x + int((maestro_width - new_width) / 2)
            self.maestro.rect.y = 330
            self.player.rect.x = 450
            self.player.rect.y = 570
            self.guard_interacted = True
            if not self.background_changed:
                self.background_image = self.background_image_open
                self.background_changed = True
            self.confetti.start()
        else:
            if self.incorrect_sound: 
                self.incorrect_sound.play()
            self.state = "game_over"
            pygame.mixer.music.stop()

    # LÓGICA DE ACTUALIZACIÓN
    def update(self):
        keys = pygame.key.get_pressed()

        # Transiciones de fundido (fade in/out)
        if self.is_fading:
            if self.state == "controls_screen":
                if self.target_state is None:
                    self.fade_alpha = max(0, self.fade_alpha - self.fade_in_speed)
                    if self.fade_alpha == 0:
                        self.is_fading = False
                        # --- Iniciar el temporizador solo si no se ha iniciado ---
                        if not self.control_timer_started:
                            self.control_timer.start()
                            self.control_timer_started = True
                        # ---------------------------------------------------------------------
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
            return self.state

        # Pantalla de controles
        if self.state == "controls_screen":
            if not self.is_fading and self.controls_music:
                # CORRECCIÓN DE MÚSICA DE CONTROL: 
                # 1. DETENER la música de fondo (menú/nivel) para evitar interferencia.
                pygame.mixer.music.stop() 
                # 2. Verifica si la música de control no está sonando para reproducirla en bucle.
                if self.controls_music.get_num_channels() == 0:
                    self.controls_music.play(-1)
            
            # Actualizar el temporizador y habilitar el salto
            if self.control_timer_started and self.control_timer.is_running():
                self.control_timer.update()
            
            if self.control_timer.finished and not self.can_skip_controls:
                self.can_skip_controls = True

            return self.state

        # Estados de juego y quiz
        if self.state in ["game", "quiz_floor"]:
            if self.timer.is_running():
                self.timer.update()
            
            if self.held_answer:
                self.held_answer.update_position(self.player.rect)
                barrier = None
            else:
                barrier = self.maestro_collision_rect if not self.guard_interacted else None
            
            # 🟢 CORRECCIÓN CLAVE: Se pasa '3' como el sexto argumento posicional para 'level_id'.
            self.player.move(keys, self.size[0], self.size[1], barrier, self.obstacles, 3) # Se elimina 'level_id='

            if self.timer.finished and self.state not in ["loss_sound_state", "game_over", "win_state"]:
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                if self.loss_sound: self.loss_sound.play()
                return self.state

        # Interacción con el maestro y condiciones de victoria
        if self.state == "game":
            if self.guard_interacted and self.player.rect.colliderect(self.win_zone):
                pygame.mixer.music.stop()
                self.state = "win_state"
                self.confetti.reset()
                if self.win_music and not self.win_music_played:
                    self.win_music.play()
                    self.win_music_played = True

        # Estado de derrota (sonido)
        elif self.state == "loss_sound_state":
            if not pygame.mixer.get_busy() or (self.loss_sound and self.loss_sound.get_num_channels() == 0):
                self.state = "game_over"
                if self.game_over_music and not self.game_over_music_played:
                    self.game_over_music.play(-1)
                    self.game_over_music_played = True

        # Actualizar mensaje flotante
        if self.show_initial_message:
            self.floating_message.update()
            # Ocultar mensaje después de 5 segundos
            if time.time() - self.message_start_time > 5:
                self.show_initial_message = False

        # Actualiza texto y confeti
        if self.dialogo_active and self.typewriter:
            self.typewriter.update()
        self.confetti.update()
        return self.state
    
    # DIBUJO
    def draw(self):
        # Pantalla de controles
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
                
                # TITULO DE CONTROLES
                font_to_use_title = self.font_control_title
                text_to_render_title = "CONTROLES"
                center_x_title = self.size[0] // 2
                center_y_title = 40 
                # ESTILO UNIFICADO: Texto negro (0, 0, 0), Borde naranja (255, 128, 0)
                self._draw_text_with_border(self.screen, text_to_render_title, font_to_use_title, (0, 0, 0), (255, 128, 0), (center_x_title, center_y_title), border_size=4)
                
                # Lógica para mostrar el temporizador con estilo unificado
                BORDER_SIZE = 3
                COLOR_BORDER = (255, 128, 0) # Naranja (Borde)
                COLOR_TEXT = (0, 0, 0) # Negro (Texto)
                
                font_to_use = self.font_control_text
                center_x = self.size[0] // 2
                center_y = self.size[1] - 35
                
                if self.can_skip_controls:
                    # ✅ TEXTO LISTO PARA EMPEZAR
                    text_to_render = "Presiona ESPACIO o ENTER para comenzar el Nivel 3"
                elif self.control_timer_started:
                    # 🕒 TEXTO DEL TEMPORIZADOR
                    # Intenta acceder al atributo 'time_remaining'. Si falla, usa 0
                    remaining_time_ms = getattr(self.control_timer, 'time_remaining', 0)
                    remaining_time = max(0, int(remaining_time_ms // 1000))
                    
                    if remaining_time == 0 and self.control_timer.is_running():
                        text_to_render = "Espera un momento..."
                    else:
                        text_to_render = f"Esperando {remaining_time} segundos..."
                else:
                    # ⏳ TEXTO DE CARGA
                    text_to_render = "Cargando..."
                
                # Dibuja el texto con borde
                self._draw_text_with_border(self.screen, text_to_render, font_to_use, 
                                            COLOR_TEXT, COLOR_BORDER, 
                                            (center_x, center_y), border_size=BORDER_SIZE)
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

        # Dibujo principal del juego
        if self.state in ["game", "dialog", "quiz_complete_dialog", "quiz_floor", "loss_sound_state"]:
            self.screen.blit(self.background_image, (0, 0))
            self.maestro.draw(self.screen)
            self.player.draw(self.screen)
            
            # DIBUJAR RESPUESTAS EN EL PISO
            for answer in self.answer_pickups:
                if answer.visible and not answer.is_held:
                    answer.draw(self.screen)
            
            # DIBUJAR RESPUESTA SOSTENIDA (encima del jugador)
            if self.held_answer:
                self.held_answer.draw(self.screen)
            
            # DIBUJAR TEMPORIZADOR GENERAL
            if self.timer.is_running() or self.timer.paused:
                self.timer.draw(self.screen, self.font_timer) 
                
            # DIBUJAR MENSAJE FLOTANTE (si está activo) - MODIFICADO: esquina inferior derecha
            if self.show_initial_message and self.state == "game":
                # Calcular posición en esquina inferior derecha
                message_width = self.message_font.size("Presiona ENTER o ESPACIO para interactuar con el profesor")[0] + 30  # + padding
                message_height = self.message_font.get_height() + 30  # + padding
                message_x = self.size[0] - message_width - 20  # 20px del borde derecho
                message_y = self.size[1] - message_height - 20  # 20px del borde inferior
                self.floating_message.draw(self.screen, (message_x, message_y))

            # DIBUJAR DIÁLOGO (si está activo)
            if self.dialogo_active and self.typewriter:
                if self._dialog_img_loaded:
                    self.screen.blit(self.dialog_box_img, self.dialog_box_rect)
                else:
                    pygame.draw.rect(self.screen, (0, 0, 0), self.dialog_box_rect)
                    pygame.draw.rect(self.screen, (200, 200, 200), self.dialog_box_rect.inflate(-4, -4))

                text_x = self.dialog_box_rect.x + 30
                text_y = self.dialog_box_rect.y + 20
                self.typewriter.draw(self.screen, (text_x, text_y))
            
            # DIBUJAR CONFETI (si está activo)
            self.confetti.draw(self.screen)
            
            # DIBUJAR FUNDIDO (fade in/out)
            if self.is_fading or self.fade_alpha > 0:
                fade_surface = pygame.Surface(self.size).convert_alpha()
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(fade_surface, (0, 0))

        # Pantallas finales
        elif self.state == "game_over":
            if self.game_over_image:
                self.screen.blit(self.game_over_image, (0, 0))
            else:
                self.screen.fill((255, 0, 0))
                self._draw_text_with_border(self.screen, "GAME OVER", self.font_title, (255, 255, 255), (0, 0, 0), (self.size[0] // 2, self.size[1] // 2))
            
            self._draw_text_with_border(self.screen, "Presiona R para Reiniciar / ESC para Menu", self.font_dialog, (255, 255, 255), (0, 0, 0), (self.size[0] // 2, self.size[1] - 40))

        elif self.state == "win_state":
            if self.win_image:
                self.screen.blit(self.win_image, (0, 0))
            else:
                self.screen.fill((0, 255, 0))
                self._draw_text_with_border(self.screen, "¡GANASTE!", self.font_title, (255, 255, 255), (0, 0, 0), (self.size[0] // 2, self.size[1] // 2))
            
            self.confetti.draw(self.screen)
            self._draw_text_with_border(self.screen, "Presiona R para Reiniciar / ESC para Menu", self.font_dialog, (255, 255, 255), (0, 0, 0), (self.size[0] // 2, self.size[1] - 40))

        pygame.display.flip()