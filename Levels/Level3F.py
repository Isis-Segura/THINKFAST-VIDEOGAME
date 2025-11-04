import pygame
import random
from Personajes.boy import Characterb
from Personajes.girl import Characterg
from Personajes.Prefect import Characternpcp 
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Controldeobjetos.timer import Timer
from Interacciones.FloorQuiz import FloorQuiz 
from Interacciones.Controldeobjetos.AnswerPickup import AnswerPickup 

# Inicializa el mezclador de audio (para música y sonidos)
try:
    pygame.mixer.init()
except pygame.error:
    # Ignora el error si el mezclador no se puede inicializar
    pass

# CLASE CONFETTI: (Efecto visual de victoria)
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


# CLASE LEVEL3: implementa la mecánica de agarrar y entregar (renombrada de Level2)
class Level3:
    def __init__(self, screen, size, font, character_choice):
        self.flash_color = None
        self.flash_alpha = 0
        self.flash_timer = 0
        self.screen = screen
        self.size = size
        self.font = font
        self.character_choice = character_choice

        # Pantalla de controles
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
        self.Guardia = Characternpcp(470, 330, 'Materials/Pictures/Characters/NPCs/Prefecta/Prefect.png')

        # Define área de colisión del guardia
        guardia_width = self.Guardia.rect.width
        guardia_height = self.Guardia.rect.height
        COL_WIDTH_FACTOR = 0.5
        COL_HEIGHT_PIXELS = 5
        new_width = int(guardia_width * COL_WIDTH_FACTOR)
        new_height = COL_HEIGHT_PIXELS
        new_x = self.Guardia.rect.x + int((guardia_width - new_width) / 2)
        new_y = self.Guardia.rect.y + guardia_height - new_height
        self.guardia_collision_rect = pygame.Rect(new_x, new_y, new_width, new_height)

        # Fondos
        try:
            self.background_image_game = pygame.image.load('Materials/Pictures/Assets/fondon3.png').convert() 
            self.background_image_game = pygame.transform.scale(self.background_image_game, self.size)
        except pygame.error:
            self.background_image_game = pygame.Surface(self.size)
            self.background_image_game.fill((50, 50, 50))
        self.background_image = self.background_image_game

        try:
            self.background_image_open = pygame.image.load('Materials/Pictures/Assets/fondon2.jpg').convert() 
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
        self.quiz_timer = Timer(10) # Tiempo para responder cada pregunta

        # Cuadros de respuestas
        self.answer_results = []
        self.max_questions = 4 
        self.current_question_index = 0 # <-- Índice para controlar el flujo
        
        # Carga imágenes para marcos y símbolos
        try:
            self.marco_img = pygame.image.load("Materials/Pictures/Assets/marco.png").convert_alpha()
            self.palomita_img = pygame.image.load("Materials/Pictures/Assets/palomita.png").convert_alpha()
            self.tache_img = pygame.image.load("Materials/Pictures/Assets/tache.png").convert_alpha()
        except Exception:
            # Imágenes de respaldo (fallback)
            self.marco_img = pygame.Surface((48, 48), pygame.SRCALPHA)
            pygame.draw.rect(self.marco_img, (255, 255, 255), self.marco_img.get_rect(), 3, border_radius=6)
            self.palomita_img = pygame.Surface((36, 36), pygame.SRCALPHA)
            self.tache_img = pygame.Surface((36, 36), pygame.SRCALPHA)
            pygame.draw.line(self.palomita_img, (0, 200, 0), (4, 18), (14, 30), 4)
            pygame.draw.line(self.palomita_img, (0, 200, 0), (14, 30), (30, 6), 4)
            pygame.draw.line(self.tache_img, (200, 0, 0), (6, 6), (30, 30), 4)
            pygame.draw.line(self.tache_img, (200, 0, 0), (30, 6), (6, 30), 4)
            
        # Escalar imágenes para UI
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
        try:
            self.controls_music = pygame.mixer.Sound('Materials/Music/controls.wav')
            pygame.mixer.music.load('Materials/Music/Level3.wav') # <--- MÚSICA CAMBIADA A LEVEL 3
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
        self.dialogo_text = "Bienvenidos al nivel 3. Esta vez, tendras que\ntraerme la respuesta correcta para pasar." # <--- DIÁLOGO ACTUALIZADO
        self.typewriter = None
        self.dialogo_active = False

        # Control del quiz y diálogos posteriores
        self.quiz_game = None # Usaremos FloorQuiz solo para manejar la pregunta actual
        self.post_quiz_dialogs = []
        self.current_dialog_index = 0
        self.guard_interacted = False

        # Estados de música y efectos
        self.game_over_music_played = False
        self.win_music_played = False

        # Confeti (efecto de victoria)
        self.confetti = Confetti(self.size[0], self.size[1])

        # NUEVOS ELEMENTOS para la mecánica de AGARRAR Y ENTREGAR
        self.held_answer = None # Respuesta actualmente sostenida por el jugador
        self.answer_pickups = pygame.sprite.Group() # Grupo de respuestas en el suelo
        
        # Preguntas del minijuego (Deja las preguntas del Nivel 2, si quieres cambiarlas, hazlo aquí)
        self.questions = [
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "¿Qué lenguaje de programación es 'padre' de Python?", "choices": ["Java", "ABC", "C", "Haskell"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "¿Cuánto es $2^5$?", "choices": ["64", "32", "16", "25"], "correct_answer": 1 }, 
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "¿Cuál es la capital de Australia?", "choices": ["Sídney", "Melbourne", "Canberra", "Perth"], "correct_answer": 2 }, 
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "¿Cuál es la formula química del agua?", "choices": ["CO2", "H2O", "O3", "N2"], "correct_answer": 1 }
        ]

        # Zona de victoria (puerta)
        self.win_zone = pygame.Rect(420, 280, 65, 65)

        # Fuentes del texto
        self.font_base = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 18)
        self.font_dialog = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 15)
        self.font_question = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 13)
        self.font_title = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 15)
        self.font_timer = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 24)
        self.font_control_title = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 36)
    
    # FUNCIONES AUXILIARES
    
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
        self.held_answer = None # Asegurar que el jugador no sostiene nada
        
        # En el caso de Level3, la generación depende de current_question_index
        current_q_index = self.current_question_index 
        if current_q_index >= len(self.questions):
            return 
            
        q_data = self.questions[current_q_index]
        
        # Posiciones en el suelo para las opciones de respuesta
        positions = [(180, 500), (350, 500), (520, 500), (690, 500)] 
        
        # Asegurarse de que el número de opciones no exceda las posiciones
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
        
        # Registrar resultado
        if len(self.answer_results) < self.max_questions:
            result_string = "correct" if is_correct else "incorrect"
            self.answer_results.append(result_string)
            
            # Reproducir sonidos
            if is_correct:
                if self.correct_sound: self.correct_sound.play()
            else:
                if self.incorrect_sound: self.incorrect_sound.play()

            # Desaparecer la respuesta entregada
            answer_pickup.visible = False
            answer_pickup.is_held = False
            self.held_answer = None
            
            # Revisar condición de derrota (3 respuestas incorrectas)
            if self.answer_results.count("incorrect") >= 3:
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                if self.loss_sound: self.loss_sound.play()
                return

        # Pasar a la siguiente pregunta (si no se perdió y no ha terminado)
        if len(self.answer_results) < self.max_questions:
            self.current_question_index += 1 # <-- Avance de pregunta manual
            if self.current_question_index < self.max_questions:
                # Si hay quiz_game, actualizar su índice
                if self.quiz_game and hasattr(self.quiz_game, 'current_question_index'):
                    self.quiz_game.current_question_index = self.current_question_index
                
                self._generate_answer_pickups() # Generar nuevas opciones
                self.quiz_timer = Timer(10)
                self.quiz_timer.start()
            else:
                # Si llegamos aquí, hemos respondido la última pregunta.
                if self.quiz_game and hasattr(self.quiz_game, 'finished'):
                    self.quiz_game.finished = True
        else:
            # Quiz terminado (si el contador de respuestas ya llegó al máximo)
            if self.quiz_game and hasattr(self.quiz_game, 'finished'):
                self.quiz_game.finished = True
    
    # MANEJO DE EVENTOS
    def handle_events(self, event):
        # Reinicio o salida desde pantalla final
        if self.state in ["game_over", "loss_sound_state", "win_state"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.stop()
                    # Reiniciar la instancia de Level3
                    self.__init__(self.screen, self.size, self.font, self.character_choice)
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    return "menu"
            return None

        # Pantalla de controles
        if self.state == "controls_screen" and not self.is_fading:
            if event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN]):
                self.is_fading = True
                self.target_state = "game"
                self.fade_alpha = 0
                if self.controls_music:
                    self.controls_music.stop()
            return None

        # Teclas de interacción (Espacio/Enter)
        if event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_RETURN]):
            keys = pygame.key.get_pressed() 
            
            # Lógica de Diálogo
            if self.dialogo_active and self.typewriter:
                if not self.typewriter.finished():
                    self.typewriter.complete_text()
                elif self.state == "dialog":
                    # Inicia el quiz
                    self.timer.start()
                    self.quiz_timer = Timer(10)
                    self.quiz_timer.start()
                    self.state = "quiz_floor"
                    self.dialogo_active = False
                    self.typewriter = None
                    
                    # Se instancia FloorQuiz
                    self.quiz_game = FloorQuiz(self.size, self.questions, self.font_question)
                    
                    # Se inicializa el índice de la pregunta en FloorQuiz
                    if self.quiz_game and hasattr(self.quiz_game, 'current_question_index'):
                        self.quiz_game.current_question_index = self.current_question_index

                    self._generate_answer_pickups() # Generar los objetos de respuesta
                    
                elif self.state == "quiz_complete_dialog":
                    # Avanza diálogos post-quiz
                    self.current_dialog_index += 1
                    if self.current_dialog_index < len(self.post_quiz_dialogs):
                        next_text = self.post_quiz_dialogs[self.current_dialog_index]
                        self.typewriter = TypewriterText(next_text, self.font_dialog, (255,255,255), speed=25)
                        self.dialogo_active = True
                    else:
                        self.dialogo_active = False
                        self.typewriter = None

            # Lógica de Recoger / Entregar (solo en estado QUIZ)
            elif self.state == "quiz_floor":
                if not self.held_answer:
                    # 1. Intentar RECOGER una respuesta
                    for answer_pickup in self.answer_pickups:
                        if answer_pickup.visible and self.player.rect.colliderect(answer_pickup.rect.inflate(10, 10)):
                            self.held_answer = answer_pickup
                            self.held_answer.is_held = True
                            self.quiz_timer.pause() # Pausar el tiempo mientras la tiene
                            return None
                        
                elif self.held_answer:
                    # 2. Intentar ENTREGAR al guardia
                    if self.player.rect.colliderect(self.guardia_collision_rect.inflate(20, 20)):
                        self._submit_answer(self.held_answer)
                        return None
                            
        return None

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
                if not pygame.mixer.get_busy() or self.controls_music.get_num_channels() == 0:
                    self.controls_music.play(-1)
            return self.state

        # Estados de juego y quiz
        if self.state in ["game", "quiz_floor"]:
            if self.timer.is_running():
                self.timer.update() # <--- CORRECCIÓN 1: Se asegura la llamada completa
            
            # Actualizar posición del objeto sostenido (sigue al jugador)
            if self.held_answer:
                self.held_answer.update_position(self.player.rect)
                barrier = None # Sin barrera si el jugador tiene la respuesta
            else:
                # Barrera del guardia activa hasta que se resuelva el quiz
                barrier = self.guardia_collision_rect if not self.guard_interacted else None
            
            self.player.move(keys, self.size[0], self.size[1], barrier)

            # Condición de tiempo general agotado
            if self.timer.finished and self.state not in ["loss_sound_state", "game_over", "win_state"]:
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                if self.loss_sound: self.loss_sound.play()
                return self.state

        # Interacción con el guardia
        if self.state == "game":
            # Condición de victoria (alcanza la zona de la puerta tras interactuar con el guardia)
            if self.guard_interacted and self.player.rect.colliderect(self.win_zone):
                pygame.mixer.music.stop()
                self.state = "win_state"
                self.confetti.reset()
                if self.win_music and not self.win_music_played:
                    self.win_music.play()
                    self.win_music_played = True

            # Iniciar el diálogo/quiz
            if not self.is_fading and self.player.rect.colliderect(self.guardia_collision_rect.inflate(20,20)) and (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and not self.guard_interacted:
                self.state = "dialog"
                self.dialogo_active = True
                self.typewriter = TypewriterText(self.dialogo_text, self.font_dialog, (255,255,255), speed=25)

        # Estado del quiz (temporizador y avance)
        elif self.state == "quiz_floor":
            # Si el jugador no tiene la respuesta, el quiz timer avanza
            if self.quiz_timer.is_running() and not self.held_answer:
                self.quiz_timer.update()
                
            if self.quiz_timer.finished:
                # Tiempo agotado: Respuesta incorrecta
                if len(self.answer_results) < self.max_questions:
                    if self.incorrect_sound: self.incorrect_sound.play()
                    self.answer_results.append("incorrect")
                    
                # Limpiar opciones del suelo
                for answer in self.answer_pickups: answer.visible = False
                if self.held_answer:
                    self.held_answer.visible = False
                    self.held_answer.is_held = False
                    self.held_answer = None

                # Condición de derrota
                if self.answer_results.count("incorrect") >= 3:
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    if self.loss_sound: self.loss_sound.play()
                    return self.state
                
                # Pasar a la siguiente pregunta si aún quedan
                if len(self.answer_results) < self.max_questions:
                    self.current_question_index += 1 # <-- Avance de pregunta manual
                    if self.current_question_index < self.max_questions:
                        if self.quiz_game and hasattr(self.quiz_game, 'current_question_index'):
                            self.quiz_game.current_question_index = self.current_question_index
                        self._generate_answer_pickups() # Generar nuevas opciones
                        self.quiz_timer = Timer(10)
                        self.quiz_timer.start()
                    else:
                        if self.quiz_game and hasattr(self.quiz_game, 'finished'):
                            self.quiz_game.finished = True 
                else:
                    if self.quiz_game and hasattr(self.quiz_game, 'finished'):
                        self.quiz_game.finished = True 

            # Si termina el quiz, muestra diálogo final
            if self.quiz_game and (hasattr(self.quiz_game, 'finished') and self.quiz_game.finished):
                self.state = "quiz_complete_dialog"
                self.dialogo_active = True
                score = self.answer_results.count("correct")
                total = len(self.questions)

                # Determina mensaje según puntaje
                if score == total:
                    dialog_text = "¡Muy bien hecho! Has demostrado tener una buena\n calidad de estudio."
                elif score >= 2: # Se cambió de 3 a 2 para una victoria más probable
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
                self.quiz_game = None # Se elimina el objeto quiz
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
                self.Guardia.rect.y = 330
                self.player.rect.x = 450
                self.player.rect.y = 570
                self.guard_interacted = True
                if not self.background_changed:
                    self.background_image = self.background_image_open
                    self.background_changed = True
                self.state = "game"

        # Estado de derrota (sonido)
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
    
    # DIBUJO
    def draw(self):
        # Pantalla de controles
        if self.state == "controls_screen":
            # Lógica de dibujo de la pantalla de controles
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
                
                try:
                    text_to_render_title = "CONTROLES"
                    center_x_title = self.size[0] // 2
                    center_y_title = 40 
                    self._draw_text_with_border(self.screen, text_to_render_title, self.font_control_title, (0, 0, 0), (255, 128, 0), (center_x_title, center_y_title), border_size=4)
                except Exception:
                    pass
                
                font_to_use = self.font_dialog
                try:
                    text_to_render = "Presiona ESPACIO o ENTER para comenzar el Nivel 3"
                    center_x = self.size[0] // 2
                    center_y = self.size[1] - 30
                    self._draw_text_with_border(self.screen, text_to_render, font_to_use, (0, 0, 0), (255, 128, 0), (center_x, center_y), border_size=2)
                except Exception:
                    pass
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
            self.Guardia.draw(self.screen)
            
            # DIBUJAR RESPUESTAS EN EL PISO
            for answer in self.answer_pickups:
                if answer.visible and not answer.is_held:
                    answer.draw(self.screen)
            
            self.player.draw(self.screen)
            
            # DIBUJAR RESPUESTA SOSTENIDA (encima del jugador)
            if self.held_answer:
                self.held_answer.draw(self.screen)
            
            # DIBUJAR TEMPORIZADOR GENERAL Y MARCADOR DE RESULTADOS
            # El dibujo del temporizador general debe ir aquí
            if self.timer.is_running() or self.timer.paused:
                self.timer.draw(self.screen, self.font_timer) 
                
            # DIBUJAR MARCADOR DE RESULTADOS
            x_start = self.size[0] - (self.max_questions * 60) - 20
            y_pos = 20
            
            for i in range(self.max_questions):
                x = x_start + i * 60
                
                # Dibujar el marco
                marco_rect = self.marco_img.get_rect(topleft=(x, y_pos))
                self.screen.blit(self.marco_img, marco_rect)

                # Dibujar el símbolo (palomita/tache)
                if i < len(self.answer_results):
                    symbol = self.palomita_img if self.answer_results[i] == "correct" else self.tache_img
                    symbol_rect = symbol.get_rect(center=marco_rect.center)
                    self.screen.blit(symbol, symbol_rect)

            # DIBUJAR UI de QUIZ (pregunta y temporizador)
            if self.state == "quiz_floor" and self.quiz_game:
                self.quiz_game.draw(self.screen)
                
                # Dibujar temporizador del QUIZ (en la posición de la pregunta)
                # NOTA: El temporizador del quiz se dibujará si no está pausado
                if self.quiz_timer.is_running() or self.quiz_timer.paused:
                    # Lo dibujo centrado encima de la pregunta
                    self.quiz_timer.draw(self.screen, self.font_timer, is_quiz_timer=True, position=(self.size[0] // 2 - 80, 150))


            # DIBUJAR DIÁLOGO (si está activo)
            if self.dialogo_active and self.typewriter:
                # Dibujar la caja de diálogo
                if self._dialog_img_loaded:
                    self.screen.blit(self.dialog_box_img, self.dialog_box_rect)
                else:
                    pygame.draw.rect(self.screen, (0, 0, 0), self.dialog_box_rect)
                    pygame.draw.rect(self.screen, (200, 200, 200), self.dialog_box_rect.inflate(-4, -4))

                # Dibujar el texto
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
