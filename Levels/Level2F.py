import pygame
import random
import os

# Importa las clases de los personajes y controladores del juego
from Personajes.boy import Characterb
from Personajes.girl import Characterg
from Personajes.Guardian import Characternpcg 
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Controldeobjetos.timer import Timer
# from Interacciones.FloorQuiz import FloorQuiz # Clase ya no usada para la nueva mecánica

# ------------------------------------------------------------------
# CRÍTICO: DEFINICIÓN DE COLORES GLOBALES 
# ------------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0) 
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255) 

# Inicializa el mezclador de audio 
try:
    pygame.mixer.init()
except pygame.error:
    pass

# ============================================================
# CLASE CONFETTI 
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
# CLASE LEVEL2: controla todo el funcionamiento del nivel
# ============================================================
class Level2:
    def __init__(self, screen, size, font, character_choice):
        self.screen = screen
        self.size = size
        self.font = font
        self.character_choice = character_choice

        # ------------------------------------------------------------------
        # ESTADOS Y CONTROL INICIAL 
        # ------------------------------------------------------------------
        self.state = "game"
        self.fade_alpha = 255
        self.fade_in_speed = 5
        self.is_fading = True
        self.target_state = None
        self.answer_item = None # Objeto de respuesta que lleva el jugador: (valor_respuesta, rect_dibujo)
        self.answer_zone_rects = [] # Rectángulos de las respuestas en el piso
        self.current_correct_answer = -1 # Índice de la respuesta correcta de la pregunta actual

        if self.character_choice == "boy":
            self.player = Characterb(440, 600, 2)
        else:
            self.player = Characterg(440, 600, 2)

        self.Guardia = Characternpcg(470, 330, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')

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
        
        # Zona de entrega frente al guardia
        self.deliver_zone_rect = self.guardia_collision_rect.inflate(10, 10)


        # ------------------------------------------------------------------
        # CARGA DE IMÁGENES Y MÚSICA 
        # ------------------------------------------------------------------
        try:
            # Reemplazando 'fondon2.jpg' por los nombres corregidos
            self.background_image_game = pygame.image.load('Materials/Pictures/Assets/fondon2.jpg').convert() 
            self.background_image_game = pygame.transform.scale(self.background_image_game, self.size)
        except pygame.error:
            self.background_image_game = pygame.Surface(self.size)
            self.background_image_game.fill(BLACK)
        self.background_image = self.background_image_game

        try:
            self.background_image_open = pygame.image.load('Materials/Pictures/Assets/fondon2.jpg').convert() 
            self.background_image_open = pygame.transform.scale(self.background_image_open, self.size)
        except pygame.error:
            self.background_image_open = self.background_image_game 
        self.background_changed = False
        
        # (Resto de la carga de imágenes y sonidos se mantiene igual)
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
            
        self.level_music_loaded = False
        try:
            pygame.mixer.music.load('Materials/Music/Level2.wav') 
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

        self.game_over_music_played = False
        self.win_music_played = False
        
        # ------------------------------------------------------------------
        # LÓGICA DEL JUEGO
        # ------------------------------------------------------------------
        self.timer = Timer(180)      
        self.quiz_timer = Timer(20)  

        self.answer_results = []
        self.max_questions = 4 

        self.dialogo_text = "Bienvenido al Nivel 2. Si quieres pasar, tendras que\n responder estas preguntas mas dificiles!"
        self.typewriter = None
        self.dialogo_active = False

        self.quiz_game = None
        self.post_quiz_dialogs = []
        self.current_dialog_index = 0
        self.guard_interacted = False

        self.confetti = Confetti(self.size[0], self.size[1])

        # Preguntas del Nivel 2
        self.questions = [
            { "image": "Materials/Pictures/Assets/imagen2_1.jpg", "question": "Cuantos huesos tiene el cuerpo humano adulto?", "choices": ["206", "190", "250", "300"], "correct_answer": 0 },
            { "image": "Materials/Pictures/Assets/imagen2_2.jpg", "question": "Cual es el pais mas poblado del mundo?", "choices": ["India", "China", "Estados Unidos", "Indonesia"], "correct_answer": 0 },
            { "image": "Materials/Pictures/Assets/imagen2_3.jpg", "question": "Que elemento quimico representa la letra K?", "choices": ["Fosforo", "Potasio", "Calcio", "Sodio"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen2_4.jpg", "question": "Quien pinto la Mona Lisa?", "choices": ["Michelangelo", "Raphael", "Donatello", "Leonardo da Vinci"], "correct_answer": 3 }
        ]

        # Posiciones de los rectángulos en el piso (ajusta estas coordenadas a tu mapa)
        self.ANSWER_RECT_POSITIONS = [
            pygame.Rect(100, 500, 150, 50),
            pygame.Rect(270, 500, 150, 50),
            pygame.Rect(440, 500, 150, 50),
            pygame.Rect(610, 500, 150, 50)
        ]

        # Zona de victoria (puerta)
        self.win_zone = pygame.Rect(420, 280, 65, 65)

        # Fuentes del texto
        if os.path.exists("Materials/Fonts/PressStart2P-Regular.ttf"):
            font_path = "Materials/Fonts/PressStart2P-Regular.ttf"
        else:
            font_path = None 
        
        self.font_base = pygame.font.Font(font_path, 18)
        self.font_dialog = pygame.font.Font(font_path, 15)
        self.font_question = pygame.font.Font(font_path, 13)
        self.font_title = pygame.font.Font(font_path, 15)
        self.font_timer = pygame.font.Font(font_path, 24)
        
        # Fuente para los iconos de resultado
        self.font_results = pygame.font.Font(None, 40) # Fuente simple para iconos

    # Función auxiliar para dibujar texto con borde
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

    # ------------------------------------------------------------
    # NUEVO MÉTODO: INICIALIZAR OBJETOS DE RESPUESTA EN EL PISO
    # ------------------------------------------------------------
    def _setup_answer_objects(self):
        """Asigna las respuestas de la pregunta actual a los rectángulos del piso."""
        q_index = len(self.answer_results)
        if q_index >= len(self.questions):
            return

        current_q = self.questions[q_index]
        self.current_correct_answer = current_q["correct_answer"]
        self.answer_zone_rects = []
        
        # Asigna cada opción a un rectángulo en el piso
        for i, rect_pos in enumerate(self.ANSWER_RECT_POSITIONS):
            # El valor del objeto será el índice de la respuesta (0, 1, 2, 3)
            text_value = current_q["choices"][i]
            
            # Almacena el rect, el índice de la respuesta y el texto para dibujarlo
            self.answer_zone_rects.append({
                "rect": rect_pos,
                "answer_index": i,
                "text": text_value
            })
        
        # Si estamos listos para la pregunta, iniciamos el Quiz Timer
        self.quiz_timer = Timer(20) 
        self.quiz_timer.start()

    # ============================================================
    # Maneja los eventos del teclado y las interacciones del jugador
    # ============================================================
    def handle_events(self, event):
        # Reinicio o salida desde pantalla final 
        if self.state in ["game_over", "loss_sound_state", "win_state"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # CRÍTICO: Aseguramos la detención de la música antes de reiniciar
                    pygame.mixer.stop()
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    return "menu"
            return None

        keys = pygame.key.get_pressed()

        # Interacción principal con ESPACIO/ENTER
        if event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_RETURN]):
            
            # Lógica de avance en diálogos (sin quiz activo o post-quiz)
            if self.dialogo_active and self.typewriter:
                if not self.typewriter.finished():
                    self.typewriter.complete_text()
                elif self.state == "dialog":
                    # Si ya completamos el quiz, volvemos a 'game' para movernos
                    if len(self.answer_results) == self.max_questions or len(self.answer_results) >= self.max_questions:
                        self.state = "game"
                        self.dialogo_active = False
                        self.typewriter = None
                    else:
                        # Empezamos la siguiente pregunta (PICKUP)
                        self.timer.start()
                        self.state = "quiz_pickup" # Nuevo estado
                        self.dialogo_active = False
                        self.typewriter = None
                        self._setup_answer_objects() 

                elif self.state == "quiz_complete_dialog":
                    self.current_dialog_index += 1
                    if self.current_dialog_index < len(self.post_quiz_dialogs):
                        next_text = self.post_quiz_dialogs[self.current_dialog_index]
                        self.typewriter = TypewriterText(next_text, self.font_dialog, WHITE, speed=25)
                        self.dialogo_active = True
                    else:
                        self.dialogo_active = False
                        self.typewriter = None
            
            # LÓGICA DE RECOLECCIÓN (Estado: quiz_pickup)
            elif self.state == "quiz_pickup" and not self.answer_item:
                for item in self.answer_zone_rects:
                    # Colisión expandida para que sea más fácil recoger
                    if self.player.rect.colliderect(item["rect"].inflate(10, 10)):
                        # Recoge el objeto (guarda el índice de la respuesta)
                        self.answer_item = {"answer_index": item["answer_index"], "text": item["text"]}
                        self.answer_zone_rects = [] # Vacía el piso
                        self.state = "quiz_delivery"
                        break

            # LÓGICA DE ENTREGA (Estado: quiz_delivery)
            elif self.state == "quiz_delivery" and self.answer_item:
                if self.player.rect.colliderect(self.deliver_zone_rect):
                    
                    selected_index = self.answer_item["answer_index"]
                    
                    # Comprueba si la respuesta entregada es la correcta
                    is_correct = (selected_index == self.current_correct_answer)

                    self.quiz_timer.pause()
                    self.answer_item = None # Suelta/entrega el objeto
                    
                    # Manejo del resultado y sonido
                    if is_correct:
                        result = "correct"
                        if self.correct_sound:
                            self.correct_sound.play()
                    else:
                        result = "incorrect"
                        if self.incorrect_sound:
                            self.incorrect_sound.play()

                    self.answer_results.append(result)

                    # CRÍTICO: Transición a la siguiente pregunta o final
                    if len(self.answer_results) >= self.max_questions:
                        # Si es la última pregunta, el update manejará la transición a quiz_complete_dialog
                        pass
                    else:
                        # Prepara el diálogo para la siguiente pregunta
                        self.state = "dialog" 
                        self.dialogo_text = f"Respuesta {result.upper()}! Presiona ESPACIO para la siguiente pregunta."
                        self.typewriter = TypewriterText(self.dialogo_text, self.font_dialog, WHITE, speed=25)
                        self.dialogo_active = True

        return None 

    # ============================================================
    # Actualiza la lógica del juego según el estado actual
    # ============================================================
    def update(self):
        keys = pygame.key.get_pressed()

        # ... (La lógica de fade in/out y el timer general se mantiene igual)
        if self.is_fading:
            if self.state == "game" and self.target_state is None:
                self.fade_alpha = max(0, self.fade_alpha - self.fade_in_speed)
                if self.fade_alpha == 0:
                    self.is_fading = False
                    if self.level_music_loaded and not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play(-1) 

        # Movimiento del jugador
        if self.state in ["game", "quiz_pickup", "quiz_delivery"]:
            if self.timer.is_running():
                self.timer.update()
            
            # Bloquea al jugador con el guardia solo si no ha terminado el quiz
            barrier = self.guardia_collision_rect if not self.guard_interacted else None
            self.player.move(keys, self.size[0], self.size[1], barrier)

            # CRÍTICO: Derrota por tiempo (global)
            if self.timer.finished and self.state not in ["loss_sound_state", "game_over", "win_state"]:
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                if self.loss_sound:
                    self.loss_sound.play()
                return self.state

        # Interacción con el guardia (inicio del quiz)
        if self.state == "game":
             # Lógica de Victoria (al final del nivel)
            if self.guard_interacted and self.player.rect.colliderect(self.win_zone):
                pygame.mixer.music.stop()
                self.state = "win_state" 
                self.confetti.reset()
                if self.win_music and not self.win_music_played:
                    self.win_music.play()
                    self.win_music_played = True 
                return self.state

            # Interacción con el guardia (inicio del quiz)
            if not self.is_fading and self.player.rect.colliderect(self.guardia_collision_rect.inflate(20,20)) and (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and not self.guard_interacted and len(self.answer_results) == 0:
                self.state = "dialog"
                self.dialogo_active = True
                self.typewriter = TypewriterText(self.dialogo_text, self.font_dialog, WHITE, speed=25)


        # Estados de quiz (Pickup/Delivery)
        elif self.state in ["quiz_pickup", "quiz_delivery"]:
            # Timer de la pregunta
            if self.quiz_timer.is_running():
                self.quiz_timer.update()

            # Tiempo agotado para la pregunta (se registra fallo)
            if self.quiz_timer.finished:
                if self.incorrect_sound:
                    self.incorrect_sound.play()
                
                # Se registra un fallo forzado por tiempo
                if len(self.answer_results) < self.max_questions:
                    self.answer_results.append("incorrect")
                
                self.answer_item = None # El objeto desaparece
                self.answer_zone_rects = []
                self.quiz_timer.pause()
                
                # Transición (fallo por tiempo)
                if len(self.answer_results) >= self.max_questions:
                    self.state = "quiz_complete_dialog"
                else:
                    # Prepara el diálogo de fallo por tiempo antes de la siguiente pregunta
                    self.state = "dialog" 
                    self.dialogo_text = "¡Tiempo agotado! Presiona ESPACIO para la siguiente pregunta."
                    self.typewriter = TypewriterText(self.dialogo_text, self.font_dialog, WHITE, speed=25)
                    self.dialogo_active = True

        # Lógica de 3 fallos y victoria/finalización del quiz
        if self.state not in ["game", "dialog", "quiz_complete_dialog", "game_over", "loss_sound_state", "win_state"] or (self.state == "dialog" and len(self.answer_results) > 0 and self.dialogo_active == False):
            # Lógica de derrota por 3 fallos (se chequea después de cada entrega o timeout)
            if self.answer_results.count("incorrect") >= 3:
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                if self.loss_sound:
                    self.loss_sound.play()
                return self.state

        # Lógica de finalización del quiz (se chequea después de la última respuesta/timeout)
        if len(self.answer_results) == self.max_questions and self.state not in ["quiz_complete_dialog", "loss_sound_state", "game_over", "win_state"]:
            self.state = "quiz_complete_dialog"
            self.dialogo_active = True
            score = self.answer_results.count("correct")
            total = len(self.questions)
            
            # Configuración del diálogo final (CRÍTICO: El guardia habla)
            if score == total:
                dialog_text = "Fantastico! Tienes un gran conocimiento."
            elif score >= 2:
                dialog_text = "Buen trabajo, pero el Nivel 3 sera mas dificil!"
            else:
                dialog_text = "Debes estudiar mas para el Nivel 3."

            self.post_quiz_dialogs = [
                f"Has respondido correctamente {score} de {total} preguntas.",
                dialog_text,
                "Puedes seguir. Buena suerte en tu camino!"
            ]
            self.current_dialog_index = 0
            self.typewriter = TypewriterText(self.post_quiz_dialogs[self.current_dialog_index], self.font_dialog, WHITE, speed=25)
            self.timer.pause()
            self.quiz_timer.reset()
            if score >= 2:
                self.confetti.start()
        
        # Diálogo final tras el quiz
        elif self.state == "quiz_complete_dialog":
            if not self.dialogo_active and self.current_dialog_index >= len(self.post_quiz_dialogs):
                # Mueve al guardia y abre la puerta
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
                
        # Estado de derrota (maneja la música de Game Over)
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
    
    # ============================================================
    # Dibuja todos los elementos en pantalla según el estado
    # ============================================================
    def draw(self):
        # Dibujo principal del juego
        if self.state in ["game", "dialog", "quiz_complete_dialog", "quiz_pickup", "quiz_delivery", "loss_sound_state"]:
            self.screen.blit(self.background_image, (0, 0))
            self.Guardia.draw(self.screen)
            self.player.draw(self.screen)

            # --- DIBUJO DE OBJETOS DE RESPUESTA EN EL PISO ---
            if self.state == "quiz_pickup" and self.answer_zone_rects:
                for item in self.answer_zone_rects:
                    rect = item["rect"]
                    text_val = item["text"]
                    
                    # Dibuja el rectángulo de la respuesta en el piso
                    # CRÍTICO: DIBUJO VISIBLE
                    pygame.draw.rect(self.screen, BLACK, rect, border_radius=5)
                    pygame.draw.rect(self.screen, YELLOW, rect, 3, border_radius=5)
                    
                    # Dibuja el texto de la respuesta sobre el rectángulo
                    text_surface = self.font_question.render(text_val, True, WHITE)
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)

            # --- DIBUJO DEL OBJETO EN MANO ---
            if self.state == "quiz_delivery" and self.answer_item:
                # Dibuja el objeto cerca del jugador
                item_rect = pygame.Rect(self.player.rect.x + 20, self.player.rect.y - 10, 15, 15)
                pygame.draw.circle(self.screen, BLUE, item_rect.center, 10)
                # Dibuja el texto de la respuesta que lleva el jugador
                item_text = self.font_dialog.render(self.answer_item["text"], True, BLACK)
                self.screen.blit(item_text, (item_rect.x + 15, item_rect.y - 5))

            # --- DIBUJO DE RESULTADOS DE LAS PREGUNTAS ---
            # Dibuja iconos de 👍 o 👎
            result_y = 50
            for i, result in enumerate(self.answer_results):
                icon = "👍" if result == "correct" else "👎"
                color = GREEN if result == "correct" else RED
                result_text = self.font_results.render(icon, True, color)
                # Coloca los resultados en la esquina superior izquierda
                self.screen.blit(result_text, (20, result_y + i * 40))
                
            # Dibuja confetti
            self.confetti.draw(self.screen)

            # Dibuja timers
            if self.state in ["quiz_pickup", "quiz_delivery"]:
                self.quiz_timer.draw(self.screen, self.font_timer, is_quiz_timer=True, position=(680, 10))
            elif self.timer.is_running():
                self.timer.draw(self.screen, self.font_timer, position=(680, 10))

            # Dibuja cuadro de diálogo (se mantiene igual)
            if self.dialogo_active:
                if self._dialog_img_loaded and self.dialog_box_img:
                    self.screen.blit(self.dialog_box_img, self.dialog_box_rect.topleft)
                    pygame.draw.rect(self.screen, YELLOW, self.dialog_box_rect, width=5, border_radius=20)
                    self.typewriter.draw(self.screen, (self.dialog_box_rect.x + 20, self.dialog_box_rect.y + 35))
                else:
                    box_rect = pygame.Rect(50, 550, 800, 100)
                    pygame.draw.rect(self.screen, (20, 30, 80), box_rect, border_radius=10)
                    pygame.draw.rect(self.screen, YELLOW, box_rect, 5, border_radius=10)
                    self.typewriter.draw(self.screen, (box_rect.x + 20, box_rect.y + 35))


        # Pantalla de derrota y victoria (se mantienen igual)
        if self.state == "game_over":
            self.screen.fill(BLACK)
            if self.game_over_image:
                self.screen.blit(self.game_over_image, (0, 0))
            font_to_use = self.font_title
            text_restart = "Presiona 'R' para Reiniciar"
            text_menu = "Presiona 'ESC' para volver al Menu"
            self._draw_text_with_border(self.screen, text_restart, font_to_use, WHITE, BLACK, (self.size[0]//2, self.size[1]-80), border_size=3)
            self._draw_text_with_border(self.screen, text_menu, font_to_use, WHITE, BLACK, (self.size[0]//2, self.size[1]-30), border_size=3)

        elif self.state == "win_state":
            self.screen.fill(BLACK)
            if self.win_image:
                self.screen.blit(self.win_image, (0, 0))
            self.confetti.draw(self.screen)
            text_restart = "Presiona 'R' para Reiniciar"
            text_menu = "Presiona 'ESC' para volver al Menu"
            font_to_use = self.font_title
            self._draw_text_with_border(self.screen, text_restart, font_to_use, WHITE, BLACK, (self.size[0]//2, self.size[1]-80), border_size=3)
            self._draw_text_with_border(self.screen, text_menu, font_to_use, WHITE, BLACK, (self.size[0]//2, self.size[1]-30), border_size=3)

        # Dibuja efecto fundido
        if self.is_fading or self.fade_alpha > 0:
            fade_surface = pygame.Surface(self.size).convert_alpha()
            fade_surface.fill(BLACK)
            fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(fade_surface, (0, 0))