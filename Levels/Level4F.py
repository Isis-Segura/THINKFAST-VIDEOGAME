import pygame
import random
import os
from Personajes.boy import Characterb
from Personajes.girl import Characterg
from Personajes.Guardian import Characternpcg
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Controldeobjetos.timer import Timer
from Interacciones.Mecanicas.FloorQuiz import FloorQuiz 

# Inicializa el mezclador de audio (para música y sonidos)
MIXER_INITIALIZED = False
try:
    pygame.mixer.init()
    MIXER_INITIALIZED = True
except pygame.error:
    pass


# ============================================================
# CLASE CONFETTI: controla el efecto visual al ganar el nivel
# ============================================================
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


# ============================================================
# CLASE ARROWSPRITE: controla la animación de la flecha
# ============================================================
class ArrowSprite:
    def __init__(self, x, y):
        self.images = []
        for i in range(1, 5): # Carga flecha1.png, flecha2.png, flecha3.png, flecha4.png
            try:
                img = pygame.image.load(f'Materials/Pictures/Assets/flecha{i}.png').convert_alpha()
                # Redimensiona la flecha a un tamaño apropiado (ej: 80x80)
                img = pygame.transform.scale(img, (80, 80)) 
                self.images.append(img)
            except pygame.error:
                # Si las imágenes no cargan, usa un cuadrado rojo como fallback
                print(f"Error cargando flecha{i}.png. Usando fallback.")
                fallback = pygame.Surface((40, 40), pygame.SRCALPHA)
                fallback.fill((255, 0, 0, 150))
                self.images.append(fallback)

        self.current_frame = 0
        self.animation_speed = 0.15 # Velocidad de cambio de frame (más pequeño = más rápido)
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_update = pygame.time.get_ticks()
        self.active = False

    def start(self):
        self.active = True

    def update(self):
        if not self.active:
            return

        now = pygame.time.get_ticks()
        # Calcula el tiempo en milisegundos para el cambio de frame
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

    def draw(self, surface):
        if self.active:
            surface.blit(self.image, self.rect.topleft)


class Level4:
    def __init__(self, screen, size, font, character_choice):
        self.flash_color = None
        self.flash_alpha = 0
        self.flash_timer = 0
        self.screen = screen
        self.size = size
        self.font = font
        self.character_choice = character_choice

        # PANTALLA DE TUTORIAL
        self.tuto_image = None
        self.tuto_image_2 = None 
        self.tuto_image_3 = None # <--- NUEVA VARIABLE
        # === AÑADIDO PARA TUTO 4 ===
        self.tuto_image_4 = None # <--- NUEVA VARIABLE PARA TUTO 4
        self.tuto_4_active = False # Bandera de control para Tuto 4
        # ===========================
        self.tuto_alpha = 0  
        self.tuto_max_alpha = 255
        self.tuto_fade_speed = 8  
        self.tuto_slide_speed = 10 
        self.tuto_visible_timer = Timer(5) # 5 segundos de visibilidad (para el Tuto 1)
        self.tuto_fade_in_started = False
        self.tuto_fade_out_started = False
        self.tuto_finished = False # Indica si el Tuto 1 ha terminado su ciclo automático (se usa para bloqueo permanente)
        self.tuto_3_has_appeared = False # NUEVA BANDERA: Indica si Tuto 3 ya apareció alguna vez.

        # Control del tutorial actual (1 = tuto1, 2 = tuto2, 3 = tuto3, 0 = finalizado)
        self.current_tuto_index = 1 
        self.tuto_2_active = False 

        self.tuto_target_x = 20  # Posición X final (cerca de la esquina izquierda)
        # Posición X inicial/final de salida (fuera de la pantalla a la izquierda)
        self.tuto_exit_x = -250 
        self.tuto_current_x = self.tuto_exit_x # Inicializa fuera de pantalla
        self.tuto_y = 20 # Posición Y fija cerca de la parte superior

        try:
            # 1. Cargar y redimensionar la imagen de tutorial 1 (Movimiento)
            img1 = pygame.image.load('Materials/Pictures/Assets/tuto1.jpg').convert_alpha()
            self.tuto_image = pygame.transform.scale(img1, (250, 180)) 
            self.tuto_rect = self.tuto_image.get_rect(topleft=(self.tuto_current_x, self.tuto_y)) 
            
            # 2. Cargar y redimensionar la imagen de tutorial 2 (Espacio/Enter)
            img2 = pygame.image.load('Materials/Pictures/Assets/tuto2.jpg').convert_alpha()
            self.tuto_image_2 = pygame.transform.scale(img2, (250, 180))
            
            # 3. Cargar y redimensionar la imagen de tutorial 3 (Diálogo/Quiz) <--- NUEVO
            img3 = pygame.image.load('Materials/Pictures/Assets/tuto3.jpg').convert_alpha()
            self.tuto_image_3 = pygame.transform.scale(img3, (250, 180))
            
            # 4. Cargar y redimensionar la imagen de tutorial 4 (Puerta/Victoria) <--- NUEVO PARA TUTO 4
            img4 = pygame.image.load('Materials/Pictures/Assets/tuto4.jpg').convert_alpha() # <--- IMAGEN DE TUTO 4
            self.tuto_image_4 = pygame.transform.scale(img4, (250, 180)) # <--- TUTO 4
            
        except pygame.error as e:
            self.tuto_image = None
            self.tuto_image_2 = None
            self.tuto_image_3 = None # <--- Manejo de error para Tuto 3
            self.tuto_image_4 = None # <--- Manejo de error para Tuto 4
            self.current_tuto_index = 0
            print(f"Error cargando imágenes de tutorial: {e}. El tutorial no se mostrará.")

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
        self.Guardia = Characternpcg(470, 330, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')

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

        # Cuadro de diálogo inferior
        self.DIALOG_BOX_BACKGROUND = (247, 247, 247)
        self.DIALOG_BOX_BORDER = (89, 61, 46)
        self.DIALOG_BOX_RADIUS = 10
        self.DIALOG_BOX_WIDTH = 800
        self.DIALOG_BOX_HEIGHT = 100 
        
        dialog_width = self.DIALOG_BOX_WIDTH
        dialog_height = self.DIALOG_BOX_HEIGHT
        dialog_x = (self.size[0] - dialog_width) // 2
        dialog_y = self.size[1] - 130 
        
        self.dialog_box_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        self._dialog_img_loaded = False 
        self.dialog_box_img = None
        
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
        self.timer = Timer(5000)      # tiempo general del nivel
        self.quiz_timer = Timer(10)  # tiempo para responder cada pregunta
        # AÑADIDO: Temporizador para la pausa después de responder una pregunta (2 segundos)
        self.answer_pause_timer = Timer(2) 

        # palomitas y taches -> ahora con imágenes
        self.answer_results = []
        self.max_questions = 4

        # Carga imágenes para marcos y símbolos
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

        # Carga sonidos y música
        self.controls_music = None
        self.level_music_loaded = False
        if MIXER_INITIALIZED:
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

        # =======================================================
        # PREGUNTAS DEL MINIJUEGO (AHORA CON IMÁGENES POR OPCIÓN)
        # =======================================================
        self.questions = [
            {
                "image": "Materials/Pictures/Assets/imagen1.jpg",  # Imagen principal de la pregunta
                "question": "¿Qué órgano bombea sangre por el cuerpo?",
                "choices": [
                    {"text": "Cerebro", "image": "Materials/Pictures/Assets/cerebro.jpg"},
                    {"text": "Corazón", "image": "Materials/Pictures/Assets/cora.jpg"},
                    {"text": "Riñones", "image": "Materials/Pictures/Assets/rinones.jpg"},
                    {"text": "Pulmones", "image": "Materials/Pictures/Assets/pulmones.jpg"}
                ],
                "correct_answer": 1 # Índice 1 es 'Corazón'
            },
            {
                "image": "Materials/Pictures/Assets/imagen2.jpg",  # Imagen principal de la pregunta
                "question": "¿Qué animales comen solo plantas?",
                "choices": [
                    {"text": "Carnívoros", "image": "Materials/Pictures/Assets/carnivoros.jpg"},
                    {"text": "Herbívoros", "image": "Materials/Pictures/Assets/herbivoros.jpg"},
                    {"text": "Omnívoros", "image": "Materials/Pictures/Assets/omnivoros.jpg"},
                    {"text": "Detritívoros", "image": "Materials/Pictures/Assets/detritivoros.jpg"}
                ],
                "correct_answer": 1 # Índice 1 es 'Herbívoros'
            },
            {
                "image": "Materials/Pictures/Assets/imagen3.jpg",
                "question": "¿Cuál es el animal más grande del mundo?",
                "choices": [
                    {"text": "Ballena azul", "image": "Materials/Pictures/Assets/ballena_azul.jpg"},
                    {"text": "Elefante", "image": "Materials/Pictures/Assets/elefante.jpg"},
                    {"text": "Tiburón", "image": "Materials/Pictures/Assets/tiburon.jpg"},
                    {"text": "Jirafa", "image": "Materials/Pictures/Assets/jirafa.jpg"}
                ],
                "correct_answer": 0 # Índice 0 es 'Ballena azul'
            },
            {
                "image": "Materials/Pictures/Assets/imagen4.jpg",
                "question": "¿Qué animales nacen de huevos?",
                "choices": [
                    {"text": "Perros", "image": "Materials/Pictures/Assets/perros.jpg"},
                    {"text": "Gatos", "image": "Materials/Pictures/Assets/gatos.jpg"},
                    {"text": "Iguanas", "image": "Materials/Pictures/Assets/iguanas.jpg"},
                    {"text": "Vacas", "image": "Materials/Pictures/Assets/vacas.jpg"}
                ],
                "correct_answer": 2 # Índice 2 es 'Iguanas'
            }
        ]
        # =======================================================
        
        # Zona de victoria (puerta)
        self.win_zone = pygame.Rect(420, 280, 65, 65)
        
        # Sprite de la flecha animada
        self.arrow_sprite = ArrowSprite(self.win_zone.centerx + 22, self.win_zone.centery ) 
        # ------------------------------------------

        # Fuentes del texto
        if os.path.exists("Materials/Fonts/PressStart2P-Regular.ttf"):
            font_path = "Materials/Fonts/PressStart2P-Regular.ttf"
        else:
            font_path = None 
        
        self.font_base = pygame.font.Font(font_path, 18)
        self.font_dialog = pygame.font.Font(font_path, 17)
        self.font_question = pygame.font.Font(font_path, 13)
        self.font_title = pygame.font.Font(font_path, 15)
        self.font_timer = pygame.font.Font(font_path, 24)
        self.font_control_title = pygame.font.Font(font_path, 36)
        # Fuente para el texto inferior de controles
        self.font_control_text = pygame.font.Font(font_path, 18) 
        
        # --- CÓDIGO INTEGRADO DE LEVEL 2: Temporizador de Controles ---
        self.control_timer = Timer(5) # Ajustado a 5 segundos
        self.control_timer_started = False
        self.can_skip_controls = False
        # ------------------------------------------------------------


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
                    self.answer_results.clear()
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    return "menu"
            return None

        # Pantalla de controles (presionar espacio para continuar)
        if self.state == "controls_screen" and not self.is_fading:
            # --- CÓDIGO INTEGRADO DE LEVEL 2: Solo permite saltar si la espera de 5 segundos ha terminado ---
            if self.can_skip_controls and event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN]):
                self.is_fading = True
                self.target_state = "game"
                self.fade_alpha = 0
                if self.controls_music:
                    self.controls_music.stop() # Detiene la música de control al pasar al juego
            # ----------------------------------------------------------------------------------------------
            return None

        # Interacción con diálogos o quiz (espacio/enter)
        if event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_RETURN]):
            if self.dialogo_active and self.typewriter:
                if not self.typewriter.finished():
                    self.typewriter.complete_text()
                elif self.state == "dialog":
                    # Inicia el quiz
                    self.timer.start()
                    self.quiz_timer = Timer(60)
                    self.quiz_timer.start()
                    self.state = "quiz_floor"
                    self.dialogo_active = False
                    self.typewriter = None
                    self.quiz_game = FloorQuiz(self.size, self.questions, self.font_question) 
                    
                    # *** INICIO DE TUTO 3 (PRIMERA APARICIÓN) TERMINA SU SLIDE-OUT AQUÍ ***
                    # Lo forzamos a salir ya que el quiz cubre la pantalla.
                    if self.current_tuto_index == 3:
                        self.tuto_fade_out_started = True 
                        if hasattr(self.tuto_visible_timer, 'time_remaining'):
                            self.tuto_visible_timer.time_remaining = 0 
                    else:
                        # Finalizamos el tutorial si el flujo normal terminó
                        self.current_tuto_index = 0 
                        self.tuto_finished = True 
                        
                elif self.state == "quiz_complete_dialog":
                    # Avanza los diálogos después del quiz
                    self.current_dialog_index += 1
                    if self.current_dialog_index < len(self.post_quiz_dialogs):
                        next_text = self.post_quiz_dialogs[self.current_dialog_index]
                        self.typewriter = TypewriterText(next_text, self.font_dialog, 
                                                         (0, 0, 0), speed=25) 
                        self.dialogo_active = True
                    else:
                        # Diálogo post-quiz ha terminado
                        self.dialogo_active = False
                        self.typewriter = None
                        
                        # --- MODIFICACIÓN: Desactiva Tuto 3 al final del diálogo post-quiz (SEGUNDA APARICIÓN) ---
                        # Inicia el slide-out forzado de Tuto 3.
                        if self.current_tuto_index == 3:
                            self.tuto_fade_out_started = True 
                            if hasattr(self.tuto_visible_timer, 'time_remaining'):
                                self.tuto_visible_timer.time_remaining = 0 
                            # NO SE MARCA COMO 'tuto_finished = True' AQUÍ, ya que el tutorial 3 es el último
                            # y se marca como finalizado en el SLIDE-OUT de la función update.
                        # -------------------------------------------------------------------
            
        # Manejo del quiz
        if self.state == "quiz_floor" and self.quiz_game:
            result = self.quiz_game.handle_event(event)

            if result in ["correct", "incorrect"]:
                self.quiz_timer.pause()
                    
                if len(self.answer_results) < self.max_questions:
                    if result == "correct":
                        if self.correct_sound:
                            self.correct_sound.play()
                        self.answer_results.append("correct")
                    else:
                        if self.incorrect_sound:
                            self.incorrect_sound.play()
                        self.answer_results.append("incorrect")

                # AÑADIDO: Inicia el temporizador de pausa para el avance automático
                self.answer_pause_timer.reset()
                self.answer_pause_timer.start()

                if self.answer_results.count("incorrect") >= 3:
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    if self.loss_sound:
                        self.loss_sound.play()

        return None

    # ============================================================
    # Actualiza la lógica del juego según el estado actual
    # ============================================================
    def update(self,is_paused):
        keys = pygame.key.get_pressed()
        if is_paused:
                    # NO EJECUTAR LA LÓGICA DEL JUEGO si está en pausa
                    return "running"

        # Transiciones de fundido (fade in/out)
        if self.is_fading:
            # ... (código de fade-in/out para controls_screen)
            if self.state == "controls_screen":
                if self.target_state is None:
                    self.fade_alpha = max(0, self.fade_alpha - self.fade_in_speed)
                    if self.fade_alpha == 0:
                        self.is_fading = False
                        # --- INICIO DE LA MÚSICA DE CONTROLES (SOLUCIÓN AÑADIDA) ---
                        if self.controls_music and not self.controls_music.get_num_channels():
                            self.controls_music.play(-1) # -1 para reproducción en bucle
                        # -------------------------------------------------------------
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
                    # CAMBIO: Inicia el tutorial 1 si no ha terminado
                    if (self.tuto_image or self.tuto_image_2 or self.tuto_image_3) and self.current_tuto_index > 0 and not self.tuto_fade_in_started:
                        self.tuto_fade_in_started = True

        if self.state == "controls_screen" and not self.is_fading:
            # ... (código del temporizador de controles)
            if not self.control_timer_started:
                self.control_timer.start()
                self.control_timer_started = True

            if self.control_timer.is_running():
                self.control_timer.update()
                if self.control_timer.finished and not self.can_skip_controls:
                    self.can_skip_controls = True
            
            return self.state

        # Lógica de la animación del tutorial (MODIFICADA PARA ACTIVACIÓN DINÁMICA DE TUTO 2/3)
        # Se asegura de que si Tuto 4 está activo, los otros tutoriales no interfieran.
        if self.current_tuto_index > 0 and not self.tuto_4_active and (self.tuto_image or self.tuto_image_2 or self.tuto_image_3): 
            
            # Determinar si el jugador está cerca del guardia (AUMENTAR EL RECT DE COLISIÓN PARA CERCANÍA)
            is_near_guard = self.player.rect.colliderect(self.guardia_collision_rect.inflate(100, 100))
            
            # LÓGICA DE TRANSICIÓN POR PROXIMIDAD
            
            # TUTO 1 -> TUTO 2: Se activa al acercarse al guardia
            if self.current_tuto_index == 1 and is_near_guard and not self.tuto_fade_out_started:
                # Si estamos en Tuto 1 y nos acercamos al guardia, forzamos la salida de Tuto 1
                if hasattr(self.tuto_visible_timer, 'time_remaining'):
                    self.tuto_visible_timer.time_remaining = 0 # Fuerza el temporizador a terminar
                self.tuto_fade_out_started = True # Inicia el slide-out

            # TUTO 2 -> TUTO 1/FINAL: Se activa al alejarse (antes de la interacción)
            elif self.current_tuto_index == 2 and not is_near_guard and not self.tuto_fade_out_started and not self.guard_interacted:
                 # Si estamos en Tuto 2 y nos alejamos, forzamos la salida de Tuto 2
                 if hasattr(self.tuto_visible_timer, 'time_remaining'):
                    self.tuto_visible_timer.time_remaining = 0
                 self.tuto_fade_out_started = True


            # ---------------------------------------------------
            # Animation State 1: SLIDE-IN (tuto1 or tuto2 or tuto3)
            # ---------------------------------------------------
            if self.tuto_fade_in_started and not self.tuto_fade_out_started:
                # 1. Fade-in (Opacidad)
                if self.tuto_alpha < self.tuto_max_alpha:
                    self.tuto_alpha = min(self.tuto_max_alpha, self.tuto_alpha + self.tuto_fade_speed)

                # 2. Slide-in (Posición: de exit_x a target_x)
                if self.tuto_current_x < self.tuto_target_x:
                    self.tuto_current_x = min(self.tuto_target_x, self.tuto_current_x + self.tuto_slide_speed)
                
                self.tuto_rect.topleft = (self.tuto_current_x, self.tuto_y)

                # Check if slide-in is complete
                is_slide_finished = (self.tuto_current_x >= self.tuto_target_x)
                is_fade_in_finished = (self.tuto_alpha == self.tuto_max_alpha)

                # If slide-in is complete, start the timer for visibility (Solo para Tuto 1/2 si es necesario)
                if is_slide_finished and is_fade_in_finished and not self.tuto_visible_timer.is_running():
                    if self.current_tuto_index in [1, 2]:
                         self.tuto_visible_timer.start()
                    
                    # Tuto 1 solo debe iniciar su timer la primera vez
                    if self.current_tuto_index == 1 and not self.tuto_finished:
                        # La bandera tuto_finished ahora indica que ya corrió el ciclo de timer una vez (para controlar la repetición)
                        self.tuto_finished = True 

            # ---------------------------------------------------
            # Animation State 2: VISIBLE
            # ---------------------------------------------------
            if self.tuto_visible_timer.is_running():
                self.tuto_visible_timer.update()
                
                # Si el temporizador terminó, inicia la salida 
                if self.tuto_visible_timer.finished and not self.tuto_fade_out_started:
                    
                    if self.current_tuto_index == 1:
                         # Tuto 1: si termina el tiempo, inicia el fade-out.
                        self.tuto_fade_out_started = True 

                    elif self.current_tuto_index == 2:
                        # Tuto 2: solo debe desaparecer si me alejo o interactúo. Si el timer termina, se mantiene visible hasta que ocurra algo.
                        pass
                    
                    elif self.current_tuto_index == 3:
                        # Tuto 3: No tiene timer de desaparición automática.
                        pass


            # ---------------------------------------------------
            # Animation State 3: SLIDE-OUT (tuto1 or tuto2 or tuto3)
            # ---------------------------------------------------
            if self.tuto_fade_out_started and (self.tuto_alpha > 0 or self.tuto_current_x > self.tuto_exit_x):
                # 1. Fade-out (Opacidad)
                self.tuto_alpha = max(0, self.tuto_alpha - self.tuto_fade_speed)

                # 2. Slide-out (Posición: de target_x a exit_x)
                if self.tuto_current_x > self.tuto_exit_x:
                    self.tuto_current_x = max(self.tuto_exit_x, self.tuto_current_x - self.tuto_slide_speed)
                
                self.tuto_rect.topleft = (self.tuto_current_x, self.tuto_y)

                # Check if slide-out is complete
                is_slide_out_finished = (self.tuto_current_x <= self.tuto_exit_x)

                if is_slide_out_finished and self.tuto_alpha == 0:
                    
                    if self.current_tuto_index == 1:
                        # TUTO 1 FINISHED -> START TUTO 2 (ACTIVADO POR PROXIMIDAD) O REPETIR/FINALIZAR (por timer)
                        if is_near_guard: # Si salió por proximidad, vamos a Tuto 2
                            self.current_tuto_index = 2
                            self.tuto_fade_in_started = True
                            self.tuto_fade_out_started = False
                            self.tuto_visible_timer.reset() 
                            self.tuto_alpha = 0 
                            self.tuto_current_x = self.tuto_exit_x
                            self.tuto_finished = True # Si se acerca al guardia, ya no debe volver a Tuto 1 por tiempo.
                        else:
                            # Si salió por timer y no estaba cerca
                            if not self.tuto_finished:
                                # Primera vez que el timer termina: Repite Tuto 1 para la segunda aparición.
                                # La bandera tuto_finished ahora indica que ya corrió el ciclo de timer una vez.
                                self.tuto_finished = True 
                                self.current_tuto_index = 1 # Se queda en 1
                                self.tuto_fade_in_started = True
                                self.tuto_fade_out_started = False
                                self.tuto_visible_timer.reset() 
                                self.tuto_alpha = 0 
                                self.tuto_current_x = self.tuto_exit_x
                            else:
                                # Segunda vez que el timer termina: Finaliza permanentemente.
                                self.current_tuto_index = 0
                                # La bandera self.tuto_finished ya está en True
                                self.tuto_fade_in_started = False
                                self.tuto_fade_out_started = False
                                self.tuto_visible_timer.reset()
                        
                    elif self.current_tuto_index == 2:
                        # TUTO 2 FINISHED -> VUELVE A TUTO 1 o FINALIZA

                        # Si se aleja (y aún no ha interactuado), vuelve a Tuto 1 para permitir el re-trigger de Tuto 2
                        if not self.guard_interacted and not is_near_guard and self.tuto_image and self.tuto_finished: 
                            self.current_tuto_index = 1
                            self.tuto_fade_in_started = True
                            self.tuto_fade_out_started = False
                            self.tuto_visible_timer.reset() 
                            self.tuto_alpha = 0 
                            self.tuto_current_x = self.tuto_exit_x
                            self.tuto_finished = True # Mantiene el estado de "ya ha aparecido la primera vez"
                            
                        else:
                            # Finaliza la secuencia de tutoriales (solo si ya interactuó o si Tuto 1 terminó permanentemente)
                            self.current_tuto_index = 0
                            self.tuto_finished = True 
                            self.tuto_fade_in_started = False
                            self.tuto_fade_out_started = False
                            self.tuto_visible_timer.reset()
                            
                    elif self.current_tuto_index == 3: 
                        # TUTO 3 FINISHED -> Vuelve al estado de juego (Permite la re-aparición con Confeti si es la primera vez)
                        
                        # Si es la primera aparición (al iniciar el diálogo), no finalizamos la secuencia.
                        if not self.tuto_3_has_appeared:
                            self.tuto_3_has_appeared = True
                            self.current_tuto_index = 0 # Temporalmente 0 para no interferir con el quiz
                        else:
                            # Si es la segunda aparición (con el Confeti), finaliza la secuencia permanentemente.
                            self.current_tuto_index = 0
                            self.tuto_finished = True
                        
                        self.tuto_fade_in_started = False
                        self.tuto_fade_out_started = False
                        self.tuto_visible_timer.reset()
            # FIN CÓDIGO MODIFICADO PARA TUTO 1/2/3


        # LÓGICA DE ANIMACIÓN DE TUTO 4 (NUEVO)
        if self.tuto_4_active and self.tuto_image_4:
            # Estado 1: SLIDE-IN
            if self.tuto_fade_in_started and not self.tuto_fade_out_started:
                # 1. Fade-in (Opacidad)
                if self.tuto_alpha < self.tuto_max_alpha:
                    self.tuto_alpha = min(self.tuto_max_alpha, self.tuto_alpha + self.tuto_fade_speed)

                # 2. Slide-in (Posición: de exit_x a target_x)
                if self.tuto_current_x < self.tuto_target_x:
                    self.tuto_current_x = min(self.tuto_target_x, self.tuto_current_x + self.tuto_slide_speed)
                
                self.tuto_rect.topleft = (self.tuto_current_x, self.tuto_y)

                # Si el slide-in está completo, inicia el timer de visibilidad
                is_slide_finished = (self.tuto_current_x >= self.tuto_target_x)
                is_fade_in_finished = (self.tuto_alpha == self.tuto_max_alpha)

                if is_slide_finished and is_fade_in_finished and not self.tuto_visible_timer.is_running():
                    # === CORRECCIÓN DEL ERROR 'AttributeError: 'Timer' object has no attribute 'set_timer'' ===
                    # Se recrea el objeto Timer para asegurar su reseteo y ajuste a 8 segundos.
                    self.tuto_visible_timer = Timer(8) # Tuto 4 visible por 8 segundos
                    # =========================================================================================
                    self.tuto_visible_timer.start()

            # Estado 2: VISIBLE (Controlado por timer)
            if self.tuto_visible_timer.is_running():
                self.tuto_visible_timer.update()
                
                if self.tuto_visible_timer.finished and not self.tuto_fade_out_started:
                    self.tuto_fade_out_started = True # Inicia el fade-out

            # Estado 3: SLIDE-OUT
            if self.tuto_fade_out_started and (self.tuto_alpha > 0 or self.tuto_current_x > self.tuto_exit_x):
                # 1. Fade-out (Opacidad)
                self.tuto_alpha = max(0, self.tuto_alpha - self.tuto_fade_speed)

                # 2. Slide-out (Posición: de target_x a exit_x)
                if self.tuto_current_x > self.tuto_exit_x:
                    self.tuto_current_x = max(self.tuto_exit_x, self.tuto_current_x - self.tuto_slide_speed)
                
                self.tuto_rect.topleft = (self.tuto_current_x, self.tuto_y)

                # Check if slide-out is complete
                is_slide_out_finished = (self.tuto_current_x <= self.tuto_exit_x)

                if is_slide_out_finished and self.tuto_alpha == 0:
                    # TUTO 4 TERMINADO PERMANENTEMENTE
                    self.tuto_4_active = False 
                    self.tuto_fade_in_started = False
                    self.tuto_fade_out_started = False
                    self.tuto_visible_timer.reset()
                    self.tuto_finished = True # Asegura que la secuencia completa de tutoriales termine


        # Estados de juego y quiz
        if self.state in ["game", "dialog", "quiz_complete_dialog", "quiz_floor", "loss_sound_state"]: # Añadido "quiz_complete_dialog" para movimiento
            if self.timer.is_running():
                self.timer.update()
            
            # El jugador puede moverse durante el diálogo, pero el guardia sigue siendo barrera
            barrier = self.guardia_collision_rect if not self.guard_interacted else None
            self.player.move(keys, self.size[0], self.size[1], barrier)
            
            self.arrow_sprite.update() 

            # Si el tiempo se acaba, pierde
            if self.timer.finished and self.state not in ["loss_sound_state", "game_over", "win_state"]:
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                if self.loss_sound:
                    self.loss_sound.play()
                return self.state

        # Interacción con el guardia
        if self.state == "game":
            if self.guard_interacted and self.player.rect.colliderect(self.win_zone):
                pygame.mixer.music.stop()
                self.state = "win_state"
                self.confetti.reset()
                # --- MODIFICACIÓN: Desactiva Tuto 4 al entrar a la zona de victoria ---
                if self.tuto_4_active:
                    self.tuto_fade_out_started = True 
                    if hasattr(self.tuto_visible_timer, 'time_remaining'):
                        self.tuto_visible_timer.time_remaining = 0 
                # ---------------------------------------------------------------------
                if self.win_music and not self.win_music_played:
                    self.win_music.play()
                    self.win_music_played = True

            # Inicia el diálogo (y por ende el quiz)
            if not self.is_fading and self.player.rect.colliderect(self.guardia_collision_rect.inflate(20,20)) and (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and not self.guard_interacted:
                self.state = "dialog"
                self.dialogo_active = True
                self.typewriter = TypewriterText(self.dialogo_text, self.font_dialog, 
                                                 (0, 0, 0), speed=25)
                
                # *** MODIFICACIÓN: Lógica de PRIMERA APARICIÓN DE TUTO 3 ***
                # Tuto 2 termina y Tuto 3 empieza su fade-in/slide-in
                if self.tuto_image_3 and not self.tuto_3_has_appeared:
                    self.current_tuto_index = 3 
                    self.tuto_fade_in_started = True
                    self.tuto_fade_out_started = False
                    self.tuto_visible_timer.reset() 
                    self.tuto_alpha = 0 
                    self.tuto_current_x = self.tuto_exit_x
                else:
                    # Finalizamos la secuencia Tuto 1/2. Si ya apareció Tuto 3, no hacemos nada.
                    self.current_tuto_index = 0 
                    self.tuto_finished = True 
                
                # Aseguramos que la secuencia de Tuto 1/2 esté marcada como terminada si llegamos a interactuar
                self.tuto_finished = True


        # Estado del quiz (temporizador y respuestas)
        elif self.state == "quiz_floor":
            # AÑADIDO: Lógica de Avance Automático
            if getattr(self.quiz_game, 'is_answered', False) and not self.quiz_game.finished and self.answer_pause_timer.is_running():
                self.answer_pause_timer.update()
                
            # Si el temporizador de pausa terminó, avanza a la siguiente pregunta
            if getattr(self.quiz_game, 'is_answered', False) and not self.quiz_game.finished and self.answer_pause_timer.finished:
                if self.answer_results.count("incorrect") < 3:
                    # Resetea y arranca el timer del quiz.
                    self.quiz_timer.reset() 
                    self.quiz_timer.start()
                    self.quiz_game.next_question()
                
                # Si el quiz NO terminó, reseteamos el pause timer para evitar que se re-active
                if not self.quiz_game.finished:
                    self.answer_pause_timer.reset()
                    
            if not self.quiz_timer.paused and not getattr(self.quiz_game, "is_answered", False):
                self.quiz_timer.update()

            if self.quiz_timer.finished and not getattr(self.quiz_game, "is_answered", False):
                # ... (resto de lógica de finalización de tiempo en quiz)
                if self.incorrect_sound:
                    self.incorrect_sound.play()
                if len(self.answer_results) < self.max_questions:
                    self.answer_results.append("incorrect")

                self.quiz_game.is_answered = True
                self.quiz_game.answer_result = "incorrect"
                self.quiz_game.selected_choice_index = -1
                self.quiz_timer.pause()
                    
                # AÑADIDO: Inicia el temporizador de pausa
                self.answer_pause_timer.reset()
                self.answer_pause_timer.start()

                if self.answer_results.count("incorrect") >= 3:
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    if self.loss_sound:
                        self.loss_sound.play()

            if self.quiz_game:
                self.quiz_game.check_player_collision(self.player.rect)
            
            if self.quiz_game:
                self.quiz_game.update()

            # Si termina el quiz, muestra diálogo final
            if self.quiz_game and self.quiz_game.finished: 
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
                self.typewriter = TypewriterText(self.post_quiz_dialogs[self.current_dialog_index], self.font_dialog, 
                                                 (0, 0, 0), speed=25)
                self.quiz_game = None
                self.timer.pause()
                self.quiz_timer.reset()
                self.answer_pause_timer.reset() # AÑADIDO
                
                # --- MODIFICACIÓN: Inicia Confeti y Tuto 3 (SEGUNDA APARICIÓN) aquí ---
                if score >= 2:
                    self.confetti.start()
                    
                    # ACTIVA TUTO 3 PARA QUE APAREZCA CON EL CONFETI (AUNQUE HAYA APARECIDO ANTES)
                    if self.tuto_image_3:
                        self.current_tuto_index = 3 
                        self.tuto_fade_in_started = True
                        self.tuto_fade_out_started = False
                        self.tuto_visible_timer.reset()
                        self.tuto_alpha = 0 
                        self.tuto_current_x = self.tuto_exit_x
                    else:
                        self.current_tuto_index = 0
                        self.tuto_finished = True
                # --- FIN MODIFICACIÓN ---
        
        # Diálogo final tras el quiz
        elif self.state == "quiz_complete_dialog":
            if not self.dialogo_active and self.current_dialog_index >= len(self.post_quiz_dialogs):
                # Mueve al guardia para liberar el paso
                self.Guardia.rect.x -= 130
                guardia_width = self.Guardia.rect.width
                new_width = self.guardia_collision_rect.width
                new_x = self.Guardia.rect.x + int((guardia_width - new_width) / 2)
                self.guardia_collision_rect.x = new_x
                self.player.rect.x = 450
                self.player.rect.y = 570
                self.guard_interacted = True
                if not self.background_changed:
                    self.background_image = self.background_image_open
                    self.background_changed = True
                    self.arrow_sprite.start()
                    
                    # === INICIA LA APARICIÓN DE TUTO 4 AQUÍ ===
                    if self.tuto_image_4:
                        # Reinicia las banderas de animación para Tuto 4
                        self.tuto_4_active = True
                        self.tuto_fade_in_started = True
                        self.tuto_fade_out_started = False
                        # Es importante crear una nueva instancia de Timer o usar .reset()
                        # pero dado el cambio de duración (5s a 8s), lo más seguro es recrearlo
                        self.tuto_visible_timer = Timer(8)
                        self.tuto_alpha = 0 
                        self.tuto_current_x = self.tuto_exit_x
                    # ==========================================
                    
                self.state = "game"
                # El Tuto 3 ya fue marcado para desaparecer en handle_events

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
        # Función auxiliar para dibujar texto con borde (mejora la visibilidad)
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
            # ... (código de draw para controls_screen)
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
                self._draw_text_with_border(self.screen, text_to_render_title, font_to_use_title, (0, 0, 0), (255, 128, 0), (center_x_title, center_y_title), border_size=4 )
                
                # --- LÓGICA DE MENSAJE DE INICIO CON TEMPORIZADOR Y ESTILO UNIFICADO ---
                font_to_use = self.font_control_text
                center_x = self.size[0] // 2
                center_y = self.size[1] - 30 

                BORDER_SIZE = 3
                # Colores base unificados para el texto de abajo: Negro con Borde Naranja
                COLOR_BORDER = (255, 128, 0) # Naranja (Borde)
                COLOR_TEXT = (0, 0, 0) # Negro (Texto)

                if self.can_skip_controls:
                    # ✅ TEXTO LISTO PARA EMPEZAR
                    text_to_render = "Presiona ESPACIO o ENTER para comenzar el Nivel 1" 
                elif self.control_timer_started:
                    # 🕒 TEXTO DEL TEMPORIZADOR
                    remaining_time_ms = getattr(self.control_timer, 'time_remaining', 0)
                    remaining_time = max(0, int(remaining_time_ms // 1000))
                    
                    if remaining_time == 0 and self.control_timer.is_running():
                        text_to_render = "Espera un momento..."
                    else:
                        text_to_render = f"Esperando {remaining_time} segundos..."
                else:
                    # ⏳ TEXTO DE CARGA
                    text_to_render = "Cargando..."
                
                # Dibuja el texto con borde (utilizando los colores unificados)
                self._draw_text_with_border(self.screen, text_to_render, font_to_use, 
                                            COLOR_TEXT, COLOR_BORDER, 
                                            (center_x, center_y), border_size=BORDER_SIZE)

            else:
                self.screen.fill((0, 0, 0))
                font_to_use = self.font_control_text 
                text_to_render = "Error cargando Controles. Presiona ESPACIO."
                center_x = self.size[0] // 2
                center_y = self.size[1] // 2
                self._draw_text_with_border(self.screen, text_to_render, font_to_use, (255, 255, 255), (255, 128, 0), (center_x, center_y), border_size=3)

            # Dibuja efecto fundido
            if self.is_fading or self.fade_alpha > 0:
                fade_surface = pygame.Surface(self.size).convert_alpha()
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(fade_surface, (0, 0))
            return

        # Dibujo principal del juego
        if self.state in ["game", "dialog", "quiz_complete_dialog", "quiz_floor", "loss_sound_state"]:
            self.screen.blit(self.background_image, (0, 0))
            
            # DIBUJAR SOMBRAS
            # ... (código de sombras)
            shadow_surface = pygame.Surface(self.size, pygame.SRCALPHA)
            SHADOW_COLOR_RGBA = (30, 30, 30, 100)
            OFFSET_Y = 4
            
            # 1. Sombra del Jugador
            shadow_w_player = self.player.rect.width * 0.7 
            shadow_h_player = self.player.rect.height * 0.15
            shadow_rect_player = pygame.Rect(0, 0, shadow_w_player, shadow_h_player)
            shadow_rect_player.midtop = (self.player.rect.centerx, self.player.rect.bottom - OFFSET_Y - 5) 
            pygame.draw.ellipse(shadow_surface, SHADOW_COLOR_RGBA, shadow_rect_player)
            
            # 2. Sombra del Guardia (NPC)
            shadow_w_guardia = self.Guardia.rect.width * 0.8  
            shadow_h_guardia = self.Guardia.rect.height * 0.18
            shadow_rect_guardia = pygame.Rect(0, 0, shadow_w_guardia, shadow_h_guardia)
            shadow_rect_guardia.midtop = (self.Guardia.rect.centerx , self.Guardia.rect.bottom - OFFSET_Y - 10)
            pygame.draw.ellipse(shadow_surface, SHADOW_COLOR_RGBA, shadow_rect_guardia)
            self.screen.blit(shadow_surface, (0, 0))
            
            self.Guardia.draw(self.screen)
            self.player.draw(self.screen)

            # DIBUJAR MARCOS EN LA PARTE SUPERIOR
            # ... (código de marcadores de quiz)
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

            # Dibuja confetti
            self.confetti.draw(self.screen)
            
            # Dibuja la flecha
            self.arrow_sprite.draw(self.screen)
            
            # Dibuja timers
            if self.state == "quiz_floor":
                # Dibuja el timer del quiz. Si está en pausa, solo lo dibuja.
                self.quiz_timer.draw(self.screen, self.font_timer, is_quiz_timer=True, position=(680, 10))
            elif self.timer.is_running():
                self.timer.draw(self.screen, self.font_timer, position=(680, 10))

            # Dibuja quiz si está activo
            if self.state == "quiz_floor" and self.quiz_game:
                self.quiz_game.draw(self.screen)

            # Dibuja cuadro de diálogo con el estilo del quiz
            if self.dialogo_active:
                box_rect = self.dialog_box_rect
                # Dibuja el fondo y el borde con los colores del cuadro de pregunta
                pygame.draw.rect(self.screen, self.DIALOG_BOX_BACKGROUND, box_rect, border_radius=self.DIALOG_BOX_RADIUS)
                pygame.draw.rect(self.screen, self.DIALOG_BOX_BORDER, box_rect, 5, border_radius=self.DIALOG_BOX_RADIUS)
                
                # Dibuja el texto
                self.typewriter.draw(self.screen, (box_rect.x + 20, box_rect.y + 35))

            # DIBUJA LA IMAGEN DE TUTORIAL (TUTO 1, 2, 3)
            # Dibuja la imagen usando la posición y opacidad actuales
            if self.current_tuto_index > 0 and (self.tuto_alpha > 0 or self.tuto_current_x > self.tuto_exit_x) and not self.tuto_4_active:
                # Selecciona la imagen correcta
                current_image = self.tuto_image 
                if self.current_tuto_index == 2:
                    current_image = self.tuto_image_2
                elif self.current_tuto_index == 3: # <--- LÓGICA AÑADIDA PARA TUTO 3
                    current_image = self.tuto_image_3
                
                if current_image:
                    # Aplica la opacidad actual
                    current_image.set_alpha(self.tuto_alpha) 
                    
                    # Actualiza el rectángulo con la posición actual (slide)
                    self.tuto_rect.topleft = (self.tuto_current_x, self.tuto_y)
                    
                    # Dibuja
                    self.screen.blit(current_image, self.tuto_rect.topleft)

            # DIBUJA LA IMAGEN DE TUTORIAL 4 (NUEVO)
            if self.tuto_4_active and self.tuto_image_4 and (self.tuto_alpha > 0 or self.tuto_current_x > self.tuto_exit_x):
                # Selecciona la imagen de Tuto 4
                current_image = self.tuto_image_4
                
                # Aplica la opacidad actual
                current_image.set_alpha(self.tuto_alpha) 
                
                # Actualiza el rectángulo con la posición actual (slide)
                self.tuto_rect.topleft = (self.tuto_current_x, self.tuto_y)
                
                # Dibuja
                self.screen.blit(current_image, self.tuto_rect.topleft)


        # Pantalla de derrota
        if self.state == "game_over":
            # ... (código de draw para game_over)
            self.screen.fill((0, 0, 0))
            if self.game_over_image:
                self.screen.blit(self.game_over_image, (0, 0))
            font_to_use = self.font_title
            text_restart = "Presiona 'R' para Reiniciar"
            text_menu = "Presiona 'ESC' para volver al Menu"
            self._draw_text_with_border(self.screen, text_restart, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-80), border_size=3)
            self._draw_text_with_border(self.screen, text_menu, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-30), border_size=3)

        # Pantalla de victoria
        elif self.state == "win_state":
            # ... (código de draw para win_state)
            self.screen.fill((0, 0, 0))
            if self.win_image:
                self.screen.blit(self.win_image, (0, 0))
            self.confetti.draw(self.screen)
            text_restart = "Presiona 'R' para Reiniciar"
            text_menu = "Presiona 'ESC' para volver al Menu"
            font_to_use = self.font_title
            self._draw_text_with_border(self.screen, text_restart, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-0), border_size=3)
            self._draw_text_with_border(self.screen, text_menu, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-30), border_size=3)

        # Dibuja efecto fundido (si está activo)
        if self.is_fading or self.fade_alpha > 0:
            fade_surface = pygame.Surface(self.size).convert_alpha()
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(fade_surface, (0, 0))