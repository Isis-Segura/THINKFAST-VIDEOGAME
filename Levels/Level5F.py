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
        self.animation_speed = 0.15 # Velocidad de cambio de frame (0.15s por frame)
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_update = pygame.time.get_ticks()
        self.active = False # Inicialmente inactivo

    def start(self):
        self.active = True

    def stop(self):
        self.active = False
        
    def update(self):
        if not self.active:
            return

        now = pygame.time.get_ticks()
        # Control de animación basado en tiempo
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

    def draw(self, surface):
        if self.active:
            surface.blit(self.image, self.rect.topleft)


class Level5:
    def __init__(self, screen, size, font, character_choice, language):
        global MIXER_INITIALIZED
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
        self.tuto_image_3 = None # <--- TUTO 3 (Solo lado Izquierdo)
        
        # === AÑADIDO PARA TUTO 4 ===
        self.tuto_image_4 = None
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
        self.tuto_pending_index = 0 # <--- AÑADIDO: Indice del Tuto esperando a que el anterior se desvanezca.

        # Control del tutorial actual (1 = tuto1, 2 = tuto2, 3 = tuto3, 0 = finalizado)
        self.current_tuto_index = 1 
        self.tuto_2_active = False 

        self.tuto_target_x = 20  # Posición X final (cerca de la esquina izquierda)
        # Posición X inicial/final de salida (fuera de la pantalla a la izquierda)
        self.tuto_exit_x = -250 
        self.tuto_current_x = self.tuto_exit_x # Inicializa fuera de pantalla
        # === CAMBIO SOLICITADO AQUÍ: Ajustar la posición Y de 20 a 80 ===
        self.tuto_y = 80 # Posición Y fija cerca de la parte superior (Originalmente 20)
        # ================================================================

        try:
            # 1. Cargar y redimensionar la imagen de tutorial 1 (Movimiento)
            img1 = pygame.image.load('Materials/Pictures/Assets/tuto5.jpg').convert_alpha()
            self.tuto_image = pygame.transform.scale(img1, (250, 180)) 
            self.tuto_rect = self.tuto_image.get_rect(topleft=(self.tuto_current_x, self.tuto_y)) 
            
            # 2. Cargar y redimensionar la imagen de tutorial 2 (Espacio/Enter)
            img2 = pygame.image.load('Materials/Pictures/Assets/tuto6.jpg').convert_alpha()
            self.tuto_image_2 = pygame.transform.scale(img2, (250, 180))
            
            # 3. Cargar y redimensionar la imagen de tutorial 3 (Diálogo/Quiz)
            img3 = pygame.image.load('Materials/Pictures/Assets/tuto3.jpg').convert_alpha()
            self.tuto_image_3 = pygame.transform.scale(img3, (250, 180))
            
            # 4. Cargar y redimensionar la imagen de tutorial 4 (Puerta/Victoria)
            img4 = pygame.image.load('Materials/Pictures/Assets/tuto7.jpg').convert_alpha() 
            self.tuto_image_4 = pygame.transform.scale(img4, (250, 180)) 
            
        except pygame.error as e:
            self.tuto_image = None
            self.tuto_image_2 = None
            self.tuto_image_3 = None
            self.tuto_image_4 = None
            self.current_tuto_index = 0
            print(f"Error cargando imágenes de tutorial: {e}. El tutorial no se mostrará.")

        try:
            self.control_image = pygame.image.load('Materials/Pictures/Assets/Control2.jpg').convert()
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
            img = pygame.image.load('Materials/Pictures/Assets/perdiste2.png').convert()
            self.game_over_image = pygame.transform.scale(img, self.size)
        except pygame.error:
            self.game_over_image = None

        try:
            img = pygame.image.load('Materials/Pictures/Assets/ganaste2.png').convert()
            self.win_image = pygame.transform.scale(img, self.size)
        except pygame.error:
            self.win_image = None

        self.timer = Timer(5000)
        self.quiz_timer = Timer(60)

        self.answer_results = []
        self.max_questions = 7

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
        
        # Reproduce la música de control al iniciar la pantalla de controles
        if self.state == "controls_screen" and self.controls_music:
            self.controls_music.play(-1) # El -1 indica reproducción en bucle
            print("DEBUG PLAY: Música de control (controls.wav) iniciada en bucle.")
        # ---------------------------------------------------------------------------------------------
        if language == 'es':
            self.dialogo_text = "Si quieres pasar, tendras que responder estas\npreguntas!!"
        else:
            self.dialogo_text = "If you want to pass, you will have to answer\nthese questions!!"
        self.typewriter = None
        self.dialogo_active = False

        self.quiz_game = None
        self.post_quiz_dialogs = []
        self.current_dialog_index = 0
        self.guard_interacted = False

        self.game_over_music_played = False
        self.win_music_played = False

        self.confetti = Confetti(self.size[0], self.size[1])

        # --- Temporizador y Bandera para la Pantalla de Controles (10s) ---
        self.control_timer = Timer(10) # 10 segundos
        self.control_timer_started = False
        self.can_skip_controls = False
        # -------------------------------------------------------------------------

        # -------------------- ESTRUCTURA DE PREGUNTAS --------------------
        if language == "es":
            self.questions = [
                { "question": "¿Cómo se llama el planeta donde vivimos?", "choices": [
                    { "text": "Marte", "image": "Materials/Pictures/Assets/marte.jpg" }, 
                    { "text": "Tierra", "image": "Materials/Pictures/Assets/tierra.jpg" }, 
                    { "text": "Saturno", "image": "Materials/Pictures/Assets/saturno.jpg" }, 
                    { "text": "Venus", "image": "Materials/Pictures/Assets/venus.jpg" }
                ], "correct_answer": 1 },
                { "question": "¿Qué usamos para ver dónde están los países y mares?", "choices": [
                    { "text": "Un mapa", "image": "Materials/Pictures/Assets/mapa.jpg" }, 
                    { "text": "Un reloj", "image": "Materials/Pictures/Assets/reloj.jpg" }, 
                    { "text": "Una lupa", "image": "Materials/Pictures/Assets/lupa.jpg" }, 
                    { "text": "Un termómetro", "image": "Materials/Pictures/Assets/termometro.jpg" }
                ], "correct_answer": 0 },
                { "question": "¿Cuál de estos no es un país del continente americano?", "choices": [
                    { "text": "Japón", "image": "Materials/Pictures/Assets/japon.jpg" }, 
                    { "text": "Venezuela", "image": "Materials/Pictures/Assets/venezuela.jpg" }, 
                    { "text": "Peru", "image": "Materials/Pictures/Assets/peru.jpg" }, 
                    { "text": "México", "image": "Materials/Pictures/Assets/mexico.jpg" }
                ], "correct_answer": 0 },
                { "question": "¿Cómo se llama al lugar donde hay mucha arena y casi no llueve?", "choices": [
                    { "text": "Montañas", "image": "Materials/Pictures/Assets/montaña.jpg" }, 
                    { "text": "Ciudad", "image": "Materials/Pictures/Assets/ciudad.jpg" }, 
                    { "text": "Desierto", "image": "Materials/Pictures/Assets/desierto.jpg" }, 
                    { "text": "Selva", "image": "Materials/Pictures/Assets/selva.jpg" }
                ], "correct_answer": 2 },
                { "question": "¿Qué línea imaginaria divide la Tierra en norte y sur?", "choices": [
                    { "text": "Polo norte", "image": "Materials/Pictures/Assets/polo.jpg" }, 
                    { "text": "Oceano", "image": "Materials/Pictures/Assets/oceano.jpg" }, 
                    { "text": "Meridiano", "image": "Materials/Pictures/Assets/meridiano.jpg" }, 
                    { "text": "Ecuador", "image": "Materials/Pictures/Assets/ecuador.jpg" }
                ], "correct_answer": 3 },
                { "question": "¿Cómo se llama el país más grande del mundo?", "choices": [
                    { "text": "México", "image": "Materials/Pictures/Assets/mexico.jpg" }, 
                    { "text": "Rusia", "image": "Materials/Pictures/Assets/rusia.jpg" }, 
                    { "text": "China", "image": "Materials/Pictures/Assets/china.jpg" }, 
                    { "text": "Canadá", "image": "Materials/Pictures/Assets/canada.jpg" }
                ], "correct_answer": 1 },
                { "question": "¿Cómo se llama a la masa de agua más pequeña y estancada?", "choices": [
                    { "text": "Desierto", "image": "Materials/Pictures/Assets/desierto.jpg" }, 
                    { "text": "Océano", "image": "Materials/Pictures/Assets/oceano.jpg" }, 
                    { "text": "Lago", "image": "Materials/Pictures/Assets/lago.jpg" }, 
                    { "text": "Glaciar", "image": "Materials/Pictures/Assets/glaciar.jpg" }
                ], "correct_answer": 2 }
            ]
        else:
            self.questions = [
                { "question": "What is the name of the planet we live on?", "choices": [
                    { "text": "Mars", "image": "Materials/Pictures/Assets/marte.jpg" }, 
                    { "text": "Earth", "image": "Materials/Pictures/Assets/tierra.jpg" }, 
                    { "text": "Saturn", "image": "Materials/Pictures/Assets/saturno.jpg" }, 
                    { "text": "Venus", "image": "Materials/Pictures/Assets/venus.jpg" }
                ], "correct_answer": 1 },
                { "question": "What do we use to see where countries and seas are located?", "choices": [
                    { "text": "A map", "image": "Materials/Pictures/Assets/mapa.jpg" }, 
                    { "text": "A clock", "image": "Materials/Pictures/Assets/reloj.jpg" }, 
                    { "text": "A magnifying glass", "image": "Materials/Pictures/Assets/lupa.jpg" }, 
                    { "text": "A thermometer", "image": "Materials/Pictures/Assets/termometro.jpg" }
                ], "correct_answer": 0 },
                { "question": "Which of these is not a country on the American continent?", "choices": [
                    { "text": "Japan", "image": "Materials/Pictures/Assets/japon.jpg" }, 
                    { "text": "Venezuela", "image": "Materials/Pictures/Assets/venezuela.jpg" }, 
                    { "text": "Peru", "image": "Materials/Pictures/Assets/peru.jpg" }, 
                    { "text": "Mexico", "image": "Materials/Pictures/Assets/mexico.jpg" }
                ], "correct_answer": 0 },
                { "question": "What is the name of the place where there is a lot of sand and it hardly ever rains?", "choices": [
                    { "text": "Mountains", "image": "Materials/Pictures/Assets/montaña.jpg" }, 
                    { "text": "City", "image": "Materials/Pictures/Assets/ciudad.jpg" }, 
                    { "text": "Desert", "image": "Materials/Pictures/Assets/desierto.jpg" }, 
                    { "text": "Jungle", "image": "Materials/Pictures/Assets/selva.jpg" }
                ], "correct_answer": 2 },
                { "question": "What is the name of the imaginary line that divides the Earth into North and South?", "choices": [
                    { "text": "North Pole", "image": "Materials/Pictures/Assets/polo.jpg" }, 
                    { "text": "Ocean", "image": "Materials/Pictures/Assets/oceano.jpg" }, 
                    { "text": "Meridian", "image": "Materials/Pictures/Assets/meridiano.jpg" }, 
                    { "text": "Equator", "image": "Materials/Pictures/Assets/ecuador.jpg" }
                ], "correct_answer": 3 },
                { "question": "What is the name of the largest country in the world?", "choices": [
                    { "text": "Mexico", "image": "Materials/Pictures/Assets/mexico.jpg" }, 
                    { "text": "Russia", "image": "Materials/Pictures/Assets/rusia.jpg" }, 
                    { "text": "China", "image": "Materials/Pictures/Assets/china.jpg" }, 
                    { "text": "Canada", "image": "Materials/Pictures/Assets/canada.jpg" }
                ], "correct_answer": 1 },
                { "question": "What is the name for the smallest and stagnant body of water?", "choices": [
                    { "text": "Desert", "image": "Materials/Pictures/Assets/desierto.jpg" }, 
                    { "text": "Ocean", "image": "Materials/Pictures/Assets/oceano.jpg" }, 
                    { "text": "Lake", "image": "Materials/Pictures/Assets/lago.jpg" }, 
                    { "text": "Glacier", "image": "Materials/Pictures/Assets/glaciar.jpg" }
                ], "correct_answer": 2 }
            ]
        # ----------------------------------------------------------------------------------------------------------------------

        self.win_zone = pygame.Rect(420, 280, 65, 65)

        if os.path.exists("Materials/Fonts/PressStart2P-Regular.ttf"):
            font_path = "Materials/Fonts/PressStart2P-Regular.ttf"
        else:
            font_path = None 
        
        self.font_base = pygame.font.Font(font_path, 18)
        self.font_dialog = pygame.font.Font(font_path, 15)
        self.font_question = pygame.font.Font(font_path, 14)
        self.font_title = pygame.font.Font(font_path, 15)
        self.font_timer = pygame.font.Font(font_path, 24)
        self.font_control_title = pygame.font.Font(font_path, 36)
        self.font_control_text = pygame.font.Font(font_path, 18) 
        
        # --- Sprite de la flecha animada ---
        self.arrow_sprite = ArrowSprite(self.win_zone.centerx + 22, self.win_zone.centery ) 


    def _process_quiz_result(self, quiz_result):
        if quiz_result == "finished":
            # Esta rama ya no debería ser necesaria con la nueva lógica de FloorQuiz_KeyAndCarry.py, 
            # pero se mantiene para robustez.
            result_string = self.quiz_game.answer_result
        else:
            result_string = quiz_result
        
        # Pausa el temporizador de 20s durante el delay de 2s
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

        if self.answer_results.count("incorrect") >= 4: # <-- CONDICIÓN DE GAME OVER
            self.state = "loss_sound_state"
            pygame.mixer.music.stop()
            if self.loss_sound:
                self.loss_sound.play()
                
        if quiz_result in ["correct", "incorrect"]:
            self.player.rect.x -= 20 
        
        return self.state


    def handle_events(self, event,language):
        if self.state in ["game_over", "loss_sound_state", "win_state"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.stop()
                    # Utilizar la reinicialización con __init__ para mantener la lógica de reinicio del juego.
                    new_level = Level5(self.screen, self.size, self.font, self.character_choice, language)
                    self.__dict__.update(new_level.__dict__)
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    return "menu"
            return None

        if self.state == "controls_screen" and not self.is_fading:
            # Solo permite saltar si la bandera self.can_skip_controls es True (después de 10 segundos)
            if self.can_skip_controls and event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN]):
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
                    self.quiz_timer = Timer(60)
                    self.quiz_timer.start()
                    self.state = "quiz_floor"
                    self.dialogo_active = False
                    self.typewriter = None
                    self.quiz_game = FloorQuiz_KeyAndCarry(self.size, self.questions, self.font_question, self.dialog_box_img, self.dialog_box_rect, self._dialog_img_loaded)
                    
                    # === [MODIFICACIÓN] LÓGICA DE DESAPARICIÓN DE TUTO 3 (Inicio de Quiz) ===
                    # Tuto 3 desaparece para que el jugador se concentre en el quiz
                    if self.current_tuto_index == 3 and not self.tuto_fade_out_started:
                        self.tuto_fade_out_started = True
                    # =========================================================
                    return None
                
                elif self.state == "quiz_complete_dialog":
                    self.current_dialog_index += 1
                    if self.current_dialog_index < len(self.post_quiz_dialogs):
                        next_text = self.post_quiz_dialogs[self.current_dialog_index]
                        self.typewriter = TypewriterText(next_text, self.font_dialog, (0, 0, 0), speed=25)
                        self.dialogo_active = True
                    else:
                        self.dialogo_active = False
                        self.typewriter = None
                        
            elif self.state == "game" and not self.dialogo_active and not self.guard_interacted:
                if self.player.rect.colliderect(self.guardia_collision_rect.inflate(20,20)):
                    self.state = "dialog"
                    self.dialogo_active = True
                    self.typewriter = TypewriterText(self.dialogo_text, self.font_dialog, (0, 0, 0), speed=25)
                    
                    # === ACTIVACIÓN INMEDIATA DEL TUTO 3 (Solo Izquierdo) ===
                    if self.tuto_image_3: 
                        self.current_tuto_index = 3         
                        self.tuto_fade_out_started = False  
                        self.tuto_fade_in_started = True    
                        self.tuto_current_x = self.tuto_exit_x 
                        self.tuto_alpha = 0                 
                        self.tuto_visible_timer.reset()     
                        self.tuto_3_has_appeared = True     
                    # ============================================
                    
                    return None

            elif self.state == "quiz_floor" and self.quiz_game:
                if self.quiz_game.is_answered and not self.quiz_game.finished and self.state != "loss_sound_state":
                    return None 
                    
                if not self.quiz_game.is_answered:
                    quiz_result = self.quiz_game.handle_interaction_input(self.player.rect, self.Guardia.rect)
                    
                    if quiz_result == "picked_up":
                        return None
                    elif quiz_result in ["correct", "incorrect", "finished"]:
                        return self._process_quiz_result(quiz_result)
        
        return None

    def update(self,is_paused,language):
        keys = pygame.key.get_pressed()
        if is_paused:
                    # NO EJECUTAR LA LÓGICA DEL JUEGO si está en pausa
                    return "running"

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
                        print("DEBUG PLAY: Música de fondo de Level 2 iniciada.")
            return self.state

        if self.state == "controls_screen":
            # --- Actualizar el temporizador y habilitar el salto ---
            if self.control_timer_started and self.control_timer.is_running():
                self.control_timer.update()
            
            if self.control_timer.finished and not self.can_skip_controls:
                self.can_skip_controls = True
                print("DEBUG TIEMPO: Han pasado 10 segundos. El jugador puede saltar la pantalla de controles.")
            # -----------------------------------------------------------------
            return self.state

        # =======================================================
        # CONTROL DE ANIMACIÓN Y ESTADO DEL TUTORIAL (TUTO 1-4)
        # =======================================================
        if self.state != "controls_screen" and self.fade_alpha == 0 and not self.is_fading and self.current_tuto_index > 0:
            
            # --- Lógica de Transiciones Automáticas (Solo Tuto 1 y Tuto 4) ---
            if (self.current_tuto_index == 1 or self.current_tuto_index == 4) and not self.tuto_fade_out_started:
                self.tuto_visible_timer.update()
                if self.tuto_visible_timer.finished and not self.tuto_fade_out_started:
                    self.tuto_fade_out_started = True

            # --- Lógica de Transiciones por Proximidad (Tuto 1 y Tuto 2) ---
            is_near_guard = self.player.rect.colliderect(self.guardia_collision_rect.inflate(100, 100))
            
            if self.current_tuto_index == 1 and is_near_guard and not self.tuto_fade_out_started and not self.guard_interacted:
                self.tuto_fade_out_started = True
            
            elif self.current_tuto_index == 2 and not is_near_guard and not self.tuto_fade_out_started and not self.guard_interacted:
                self.tuto_fade_out_started = True
            
            # --- CONTROL DE ANIMACIÓN (Fade In / Slide In) ---
            if not self.tuto_fade_out_started:
                # 1. Slide In
                if self.tuto_current_x < self.tuto_target_x:
                    self.tuto_current_x = min(self.tuto_target_x, self.tuto_current_x + self.tuto_slide_speed)
                
                # 2. Fade In
                if self.tuto_alpha < self.tuto_max_alpha:
                    self.tuto_alpha = min(self.tuto_max_alpha, self.tuto_alpha + self.tuto_fade_speed * 3)

            # --- CONTROL DE ANIMACIÓN (Fade Out / Slide Out) ---
            else: # self.tuto_fade_out_started == True
                # 1. Slide Out
                if self.tuto_current_x > self.tuto_exit_x:
                    self.tuto_current_x = max(self.tuto_exit_x, self.tuto_current_x - self.tuto_slide_speed)
                
                # 2. Fade Out
                if self.tuto_alpha > 0:
                    self.tuto_alpha = max(0, self.tuto_alpha - self.tuto_fade_speed)
                
                # --- Lógica de Transición al COMPLETAR Slide Out ---
                if self.tuto_current_x <= self.tuto_exit_x and self.tuto_alpha == 0:
                    # Resetear banderas
                    self.tuto_fade_out_started = False
                    self.tuto_visible_timer.reset()
                    
                    # === TRANSICIÓN DE ÍNDICE PENDIENTE ===
                    if self.tuto_pending_index != 0:
                        self.current_tuto_index = self.tuto_pending_index
                        self.tuto_pending_index = 0
                        
                        # Marcamos Tuto 3 como aparecido si es el que se está cargando
                        if self.current_tuto_index == 3:
                            self.tuto_3_has_appeared = True
                        
                        # === ACTIVACIÓN DE TUTO 4 ===
                        if self.current_tuto_index == 4:
                            self.tuto_4_active = True
                            
                    # ==================================================
                    
                    # Lógica de transición de Tuto 1
                    if self.current_tuto_index == 1:
                        if is_near_guard and not self.guard_interacted:
                            # Transición Tuto 1 -> Tuto 2 (por proximidad)
                            self.current_tuto_index = 2
                            self.tuto_current_x = self.tuto_exit_x # Reinicia posición para Slide In
                        else:
                            # Finaliza Tuto 1 (por tiempo)
                            self.current_tuto_index = 0
                            self.tuto_finished = True
                            
                    elif self.current_tuto_index == 2:
                        if self.guard_interacted:
                            # Tuto 2 finaliza por interacción 
                            self.current_tuto_index = 0
                        else:
                            # Transición Tuto 2 -> Tuto 1 (por alejamiento)
                            self.current_tuto_index = 1
                            self.tuto_current_x = self.tuto_exit_x # Reinicia posición para Slide In
                            
                    elif self.current_tuto_index == 3:
                        # Tuto 3 desapareció por inicio de quiz
                        self.current_tuto_index = 0
                            
                    elif self.current_tuto_index == 4: # Tuto 4 desapareció (por tiempo o por entrar a la zona)
                        self.tuto_4_active = False
                        self.current_tuto_index = 0
                        
                    # Esto asegura que el Tuto que se active entre con Fade In / Slide In
                    self.tuto_fade_in_started = True 
                    
            # --- Lógica de Inicio de Tuto 1 ---
            # Si el control terminó y no hay otro tutorial corriendo, iniciar Tuto 1
            if self.state == "game" and not self.is_fading and self.fade_alpha == 0 and self.current_tuto_index == 1 and not self.tuto_fade_in_started and not self.tuto_finished:
                self.tuto_fade_in_started = True
                self.tuto_visible_timer.start()
                self.tuto_current_x = self.tuto_exit_x # Asegura que esté fuera para empezar a deslizar
            
            # --- Lógica de Finalización de Tuto 4 por entrada a Win Zone ---
            if self.current_tuto_index == 4 and self.player.rect.colliderect(self.win_zone) and not self.tuto_fade_out_started:
                self.tuto_fade_out_started = True
                self.tuto_visible_timer.pause()
            
            # =======================================================
            # FIN DEL CONTROL DE ANIMACIÓN DEL TUTORIAL
            # =======================================================

        if self.state in ["game", "quiz_floor"]:
            
            # --- Actualización de la flecha ---
            self.arrow_sprite.update() 
            
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
            # CRÍTICO: Llama a update() para manejar el avance automático de 2 segundos.
            if self.quiz_game:
                self.quiz_game.update() 
            
            # === Reiniciar el temporizador para la nueva pregunta ===
            if (self.quiz_game and 
                not self.quiz_game.finished and 
                not self.quiz_game.is_answered and 
                self.quiz_timer.paused): 
                
                self.quiz_timer.reset() # Lo pone de nuevo a 20 segundos
                self.quiz_timer.start() # Lo inicia

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

                if self.answer_results.count("incorrect") >= 4: # <-- CONDICIÓN DE GAME OVER
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    if self.loss_sound:
                        self.loss_sound.play()

            # === LÓGICA DE TRANSICIÓN AL DIÁLOGO FINAL (Versión limpia) ===
            if self.quiz_game and self.quiz_game.finished: 
                
                # === INICIO DE TUTO 3 PARA EL DIÁLOGO POST-QUIZ (Solo Izquierdo) ===
                if self.tuto_image_3:
                    self.current_tuto_index = 3 
                    self.tuto_fade_out_started = False 
                    self.tuto_fade_in_started = True 
                    self.tuto_current_x = self.tuto_exit_x 
                    self.tuto_3_has_appeared = True 
                    self.tuto_visible_timer.reset() 
                # ==============================================================
                
                self.confetti.stop() 
                
                self.state = "quiz_complete_dialog"
                self.dialogo_active = True
                score = self.answer_results.count("correct")
                total = len(self.questions)
                if language == "es":
                    if score == total:
                        dialog_text = "Muy bien hecho! Has demostrado tener una buena\ncalidad de estudio."
                    elif score >= 4: # <-- CONDICIÓN DE VICTORIA
                        dialog_text = "Buen trabajo. Te has esforzado bastante, sigue\npracticando."
                    else:
                        dialog_text = "Puedes mejorar, nunca dejes de estudiar."

                    self.post_quiz_dialogs = [
                        f"Has respondido correctamente {score} de {total} preguntas.",
                        dialog_text,
                        "Ahora te abro el paso. Buena suerte en tu camino!"
                    ]
                else:
                    if score == total:
                        dialog_text = "Well done! You have shown good\nstudy skills."
                    elif score >= 4: # <-- VICTORY CONDITION
                        dialog_text = "Good job. You have worked hard, keep\npracticing."
                    else:
                        dialog_text = "You can improve, never stop studying."

                    self.post_quiz_dialogs = [
                        f"You answered {score} out of {total} questions correctly.",
                        dialog_text,
                        "Now I will open the way for you. Good luck on\nyour journey!"
                    ]
                self.current_dialog_index = 0
                self.typewriter = TypewriterText(self.post_quiz_dialogs[self.current_dialog_index], self.font_dialog, (0, 0, 0), speed=25)
                self.quiz_game = None
                self.timer.pause()
                self.quiz_timer.reset()
                if score >= 4: # <-- CONDICIÓN DE VICTORIA
                    self.confetti.start() 
        
        elif self.state == "quiz_complete_dialog":
            if not self.dialogo_active and self.current_dialog_index >= len(self.post_quiz_dialogs):
                
                score = self.answer_results.count("correct")
                
                # Detener las animaciones de Tuto 3 (para Tuto 4)
                self.tuto_fade_out_started = True
                self.tuto_visible_timer.pause()
                self.tuto_pending_index = 0

                # Lógica de movimiento de la Prefecta y reseteo de jugador
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
                
                # Cambio de fondo
                if not self.background_changed:
                    self.background_image = self.background_image_open
                    self.background_changed = True
                
                if score >= 4: 
                    # === ACTIVACIÓN INMEDIATA DE TUTO 4 (si ganó) ===
                    self.arrow_sprite.start()
                    self.confetti.start() 
                    
                    self.current_tuto_index = 4
                    self.tuto_4_active = True 
                    self.tuto_fade_out_started = False
                    self.tuto_fade_in_started = True
                    self.tuto_current_x = self.tuto_exit_x
                    self.tuto_visible_timer.start() 
                else:
                    # Si perdió, limpiar la escena
                    self.arrow_sprite.stop() 
                    self.confetti.stop()
                    self.current_tuto_index = 0

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


    def draw(self, language):
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
                if language == "es":
                    font_to_use_title = self.font_control_title
                    text_to_render_title = "CONTROLES"
                    center_x_title = self.size[0] // 2
                    center_y_title = 40 
                    # ESTILO UNIFICADO: Texto negro (0, 0, 0), Borde naranja (255, 128, 0)
                    self._draw_text_with_border(self.screen, text_to_render_title, font_to_use_title, (0, 0, 0), (255, 128, 0), (center_x_title, center_y_title), border_size=4 )
                    
                    # --- Lógica para mostrar el temporizador con estilo unificado ---
                    BORDER_SIZE = 3
                    COLOR_BORDER = (255, 128, 0) # Naranja (Borde)
                    COLOR_TEXT = (0, 0, 0) # Negro (Texto)
                    
                    font_to_use = self.font_control_text
                    center_x = self.size[0] // 2
                    center_y = self.size[1] - 35
                    
                    if self.can_skip_controls:
                        # ✅ TEXTO LISTO PARA EMPEZAR
                        text_to_render = "Presiona ESPACIO o ENTER para comenzar el Nivel 2"
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
                    
                    # Dibuja el texto con borde
                    self._draw_text_with_border(self.screen, text_to_render, font_to_use, 
                                                COLOR_TEXT, COLOR_BORDER, 
                                                (center_x, center_y), border_size=BORDER_SIZE)
                else:
                    font_to_use_title = self.font_control_title
                    text_to_render_title = "CONTROLS"
                    center_x_title = self.size[0] // 2
                    center_y_title = 40 
                    # UNIFIED STYLE: Black text (0, 0, 0), Orange border (255, 128, 0)
                    self._draw_text_with_border(self.screen, text_to_render_title, font_to_use_title, (0, 0, 0), (255, 128, 0), (center_x_title, center_y_title), border_size=4 )
                    
                    # --- Logic to display the timer with unified style ---
                    BORDER_SIZE = 3
                    COLOR_BORDER = (255, 128, 0) # Orange (Border)
                    COLOR_TEXT = (0, 0, 0) # Black (Text)
                    
                    font_to_use = self.font_control_text
                    center_x = self.size[0] // 2
                    center_y = self.size[1] - 35
                    
                    if self.can_skip_controls:
                        # ✅ READY TO START TEXT
                        text_to_render = "Press SPACE or ENTER to start Level 2"
                    elif self.control_timer_started:
                        # 🕒 TIMER TEXT
                        remaining_time_ms = getattr(self.control_timer, 'time_remaining', 0)
                        remaining_time = max(0, int(remaining_time_ms // 1000))
                        
                        if remaining_time == 0 and self.control_timer.is_running():
                            text_to_render = "Please wait..."
                        else:
                            text_to_render = f"Waiting {remaining_time} seconds..."
                    else:
                        # ⏳ LOADING TEXT
                        text_to_render = "Loading..."
                    
                    # Draw the text with border
                    self._draw_text_with_border(self.screen, text_to_render, font_to_use, 
                                                COLOR_TEXT, COLOR_BORDER, 
                                                (center_x, center_y), border_size=BORDER_SIZE)
                # -----------------------------------------------------------------------------
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
            
            # --- DIBUJAR SOMBRAS DETALLADAS ---
            shadow_surface = pygame.Surface(self.size, pygame.SRCALPHA)
            SHADOW_COLOR_RGBA = (30, 30, 30, 100)
            OFFSET_Y = 4
            
            # 1. Sombra del Jugador
            shadow_w_player = self.player.rect.width * 0.7 
            shadow_h_player = self.player.rect.height * 0.15
            shadow_rect_player = pygame.Rect(0, 0, shadow_w_player, shadow_h_player)
            shadow_rect_player.midtop = (self.player.rect.centerx, self.player.rect.bottom - OFFSET_Y - 5) 
            pygame.draw.ellipse(shadow_surface, SHADOW_COLOR_RGBA, shadow_rect_player)
            
            # 2. Sombra de la Prefecta (NPC)
            shadow_w_guardia = self.Guardia.rect.width * 0.8  
            shadow_h_guardia = self.Guardia.rect.height * 0.18
            shadow_rect_guardia = pygame.Rect(0, 0, shadow_w_guardia, shadow_h_guardia)
            shadow_rect_guardia.midtop = (self.Guardia.rect.centerx , self.Guardia.rect.bottom - OFFSET_Y - 10)
            pygame.draw.ellipse(shadow_surface, SHADOW_COLOR_RGBA, shadow_rect_guardia)
            self.screen.blit(shadow_surface, (0, 0))
            # -----------------------------------------------------------
            
            self.Guardia.draw(self.screen)
            self.player.draw(self.screen)

            # --- DIBUJO DE RECUADROS DE RESULTADO (Puntos) ---
            spacing = 18
            marco_w, marco_h = self.marco_img.get_size()
            
            total_width = self.max_questions * marco_w + (self.max_questions - 1) * spacing
            
            # === Desplazar 50 píxeles a la izquierda ===
            OFFSET_LEFT = 50 
            x_start = ((self.size[0] - total_width) // 2) - OFFSET_LEFT 
            # =================================================================
            
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
            
            # --- Dibuja la flecha ---
            self.arrow_sprite.draw(self.screen)

            # =======================================================
            # DIBUJO DE IMÁGENES DE TUTORIAL (TUTO 1-4, solo IZQUIERDO)
            # =======================================================
            if self.current_tuto_index > 0:
                current_image = None
                
                if self.current_tuto_index == 1 and self.tuto_image:
                    current_image = self.tuto_image
                elif self.current_tuto_index == 2 and self.tuto_image_2:
                    current_image = self.tuto_image_2
                elif self.current_tuto_index == 3 and self.tuto_image_3: 
                    current_image = self.tuto_image_3
                elif self.current_tuto_index == 4 and self.tuto_image_4 and self.tuto_4_active: 
                    current_image = self.tuto_image_4
                
                # Dibuja si hay una imagen seleccionada y está visible/saliendo
                if current_image and (self.tuto_alpha > 0 or self.tuto_current_x > self.tuto_exit_x):
                    current_image.set_alpha(self.tuto_alpha) # Aplica opacidad
                    self.tuto_rect.topleft = (self.tuto_current_x, self.tuto_y) # Aplica posición
                    self.screen.blit(current_image, self.tuto_rect.topleft) # Dibuja
            # =======================================================


            # --- DIBUJO DEL TEMPORIZADOR ---
            if self.state == "quiz_floor":
                self.quiz_timer.draw(self.screen, self.font_timer, is_quiz_timer=True, position=(680, 10))
            elif self.timer.is_running():
                self.timer.draw(self.screen, self.font_timer, position=(680, 10))

            if self.state == "quiz_floor" and self.quiz_game:
                self.quiz_game.draw(self.screen, self.player.rect, language)
                if language == "es":
                    if self.quiz_game.carried_choice_index != -1:
                        drop_text = "Presiona ESPACIO/ENTER para ENTREGAR a la Prefecta."
                        center_pos = (self.size[0] // 2, self.Guardia.rect.top - 40)
                        self._draw_text_with_border(self.screen, drop_text, self.font_question, (255, 255, 255), (0, 0, 0), center_pos, border_size=2)
                    # =========================================================================================
                    # MODIFICACIÓN SOLICITADA:
                    # 1. Se añade la condición 'self.quiz_game._answers_visible' para que solo aparezca cuando el fade-in haya terminado.
                    # 2. Se cambia el texto a la frase que indicó el usuario: "¡Muevete hacia la respuesta!"
                    elif not self.quiz_game.is_answered and self.quiz_game.highlighted_choice_index == -1 and self.quiz_game._answers_visible:
                        drop_text = "¡MUEVETE CERCA DE UNA RESPUESTA PARA RESPONDERLA!"
                        center_pos = (self.size[0] // 2, self.size[1] - 150)
                        self._draw_text_with_border(self.screen, drop_text, self.font_question, (255, 255, 255), (0, 0, 0), center_pos, border_size=2)
                else:
                    if self.quiz_game.carried_choice_index != -1:
                        drop_text = "Press SPACE/ENTER to DELIVER to the Prefect."
                        center_pos = (self.size[0] // 2, self.Guardia.rect.top - 40)
                        self._draw_text_with_border(self.screen, drop_text, self.font_question, (255, 255, 255), (0, 0, 0), center_pos, border_size=2)
                    # =========================================================================================
                    # REQUESTED MODIFICATION:
                    # 1. The condition 'self.quiz_game._answers_visible' is added so that it only appears when the fade-in has finished.
                    # 2. The text is changed to the phrase indicated by the user: "Move towards the answer!"
                    elif not self.quiz_game.is_answered and self.quiz_game.highlighted_choice_index == -1 and self.quiz_game._answers_visible:
                        drop_text = "MOVE CLOSE TO AN ANSWER TO RESPOND!"
                        center_pos = (self.size[0] // 2, self.size[1] - 150)
                        self._draw_text_with_border(self.screen, drop_text, self.font_question, (255, 255, 255), (0, 0, 0), center_pos, border_size=2)
                # =========================================================================================


            if self.dialogo_active:
                if self._dialog_img_loaded and self.dialog_box_img:
                    self.screen.blit(self.dialog_box_img, self.dialog_box_rect.topleft)
                    pygame.draw.rect(self.screen, (255, 200, 0), self.dialog_box_rect, width=5, border_radius=20)
                    self.typewriter.draw(self.screen, (self.dialog_box_rect.x + 20, self.dialog_box_rect.y + 35))
                else:
                    box_rect = pygame.Rect(50, 550, 800, 100)
                    pygame.draw.rect(self.screen, (255, 255, 255), box_rect, border_radius=10)
                    pygame.draw.rect(self.screen, (139, 69, 19), box_rect, 5, border_radius=10)
                    self.typewriter.draw(self.screen, (box_rect.x + 20, box_rect.y + 35))
        if language == "es":
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
        else:
            if self.state == "game_over":
                self.screen.fill((0, 0, 0))
                if self.game_over_image:
                    self.screen.blit(self.game_over_image, (0, 0))
                font_to_use = self.font_title
                text_restart = "Press 'R' to Restart"
                text_menu = "Press 'ESC' to return to Menu"
                self._draw_text_with_border(self.screen, text_restart, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-80), border_size=3)
                self._draw_text_with_border(self.screen, text_menu, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-30), border_size=3)

            elif self.state == "win_state":
                self.screen.fill((0, 0, 0))
                if self.win_image:
                    self.screen.blit(self.win_image, (0, 0))
                self.confetti.draw(self.screen)
                text_restart = "Press 'R' to Restart"
                text_menu = "Press 'ESC' to return to Menu"
                font_to_use = self.font_title
                self._draw_text_with_border(self.screen, text_restart, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-80), border_size=3)
                self._draw_text_with_border(self.screen, text_menu, font_to_use, (255,255,255), (0,0,0), (self.size[0]//2, self.size[1]-30), border_size=3)