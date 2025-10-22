import pygame
import random
from Personajes.boy import Characterb
from Personajes.girl import Characterg
from Personajes.Prefect import Characternpcp 
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Controldeobjetos.timer import Timer
from Interacciones.FloorQuiz import FloorQuiz 
from Interacciones.Controldeobjetos.AnswerPickup import AnswerPickup 

# Inicialización de Pygame Mixer (para música y sonidos)
try:
    pygame.mixer.init()
except pygame.error:
    pass

# CLASE CONFETTI: (Efecto visual de victoria)
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
            pygame.draw.circle(surface, color, (int(x), int(y)), size)


# CLASE LEVEL2:
class Level2:
    def __init__(self, screen, size, font, character_choice):
        self.screen = screen
        self.size = size
        self.font = font
        self.character_choice = character_choice

        # --- Estado y Transiciones ---
        self.control_image = None
        self.fade_alpha = 255
        self.is_fading = True
        self.state = "game" 
        
        # Inicialización de variables de fundido (soluciona AttributeError: target_state)
        self.flash_color = None
        self.flash_alpha = 0
        self.flash_timer = 0
        self.target_state = None 

        # --- Personajes y Colisiones ---
        if self.character_choice == "boy":
            self.player = Characterb(440, 600, 2)
        else:
            self.player = Characterg(440, 600, 2)
        self.Guardia = Characternpcp(470, 330, 'Materials/Pictures/Characters/NPCs/Prefecta/Prefect.png')
        
        # Definición del rectángulo de colisión del guardia
        guardia_width = self.Guardia.rect.width
        guardia_height = self.Guardia.rect.height
        new_width = int(guardia_width * 0.5)
        new_x = self.Guardia.rect.x + int((guardia_width - new_width) / 2)
        new_y = self.Guardia.rect.y + guardia_height - 5
        self.guardia_collision_rect = pygame.Rect(new_x, new_y, new_width, 5)

        # --- Fondos y UI ---
        try:
            self.background_image_game = pygame.image.load('Materials/Pictures/Assets/fondon2.jpg').convert() 
            self.background_image_game = pygame.transform.scale(self.background_image_game, self.size)
        except pygame.error:
            self.background_image_game = pygame.Surface(self.size)
            self.background_image_game.fill((50, 50, 50))
        self.background_image = self.background_image_game
        self.background_changed = False
        
        self.dialog_box_img = None
        self.dialog_box_rect = pygame.Rect(50, self.size[1] - 150, 800, 100) 

        # CARGA DE IMÁGENES DE RESULTADOS (soluciona AttributeError: marco_img)
        try:
            self.marco_img = pygame.image.load("Materials/Pictures/Assets/marco.png").convert_alpha()
            self.palomita_img = pygame.image.load("Materials/Pictures/Assets/palomita.png").convert_alpha()
            self.tache_img = pygame.image.load("Materials/Pictures/Assets/tache.png").convert_alpha()
        except Exception:
            # Fallback si las imágenes no cargan
            self.marco_img = pygame.Surface((56, 56), pygame.SRCALPHA)
            pygame.draw.rect(self.marco_img, (255, 255, 255), self.marco_img.get_rect(), 3, border_radius=6)
            self.palomita_img = pygame.Surface((40, 40), pygame.SRCALPHA)
            self.tache_img = pygame.Surface((40, 40), pygame.SRCALPHA)
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


        # --- Mecánica de Juego y Temporizadores ---
        self.timer = Timer(150)         
        self.quiz_timer = Timer(10)     
        self.answer_results = []        
        self.max_questions = 4 
        self.current_question_index = 0
        
        # Respuestas y Preguntas
        self.held_answer = None         
        self.answer_pickups = pygame.sprite.Group() 
        self.questions = [
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "¿Qué lenguaje de programación es 'padre' de Python?", "choices": ["Java", "ABC", "C", "Haskell"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "¿Cuánto es $2^5$?", "choices": ["64", "32", "16", "25"], "correct_answer": 1 }, 
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "¿Cuál es la capital de Australia?", "choices": ["Sídney", "Melbourne", "Canberra", "Perth"], "correct_answer": 2 },
            { "image": "Materials/Pictures/Assets/imagen2.jpg", "question": "¿Cuál es la formula química del agua?", "choices": ["CO2", "H2O", "O3", "N2"], "correct_answer": 1 }
        ]

        # --- Diálogos y Control del Quiz ---
        self.dialogo_text = "Bienvenidos al nivel 2. Esta vez, tendras que\ntraerme la respuesta correcta para pasar."
        self.typewriter = None
        self.dialogo_active = False
        self.quiz_game = None 
        self.guard_interacted = False
        self.confetti = Confetti(self.size[0], self.size[1])

        # --- Fuentes ---
        self.font_dialog = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 15)
        self.font_question = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 13)
        self.font_timer = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 24)
        
        # Zona de victoria (Puerta)
        self.win_zone = pygame.Rect(420, 280, 65, 65)

    # --- FUNCIONES AUXILIARES ---
    
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

    def _draw_answer_results(self):
        start_x = self.size[0] // 2 - (self.max_questions * 60) // 2 
        start_y = 50
        spacing = 60
        
        for i in range(self.max_questions):
            x = start_x + i * spacing
            y = start_y
            self.screen.blit(self.marco_img, (x, y))
            
            if i < len(self.answer_results):
                result = self.answer_results[i]
                symbol_x = x + (self.marco_img.get_width() - self.palomita_img.get_width()) // 2
                symbol_y = y + (self.marco_img.get_height() - self.palomita_img.get_height()) // 2
                
                if result == "correct":
                    self.screen.blit(self.palomita_img, (symbol_x, symbol_y))
                elif result == "incorrect":
                    self.screen.blit(self.tache_img, (symbol_x, symbol_y))


    def _generate_answer_pickups(self):
        """Genera los objetos AnswerPickup para la pregunta actual en el suelo."""
        self.answer_pickups.empty()
        self.held_answer = None
        
        if not self.quiz_game or (hasattr(self.quiz_game, 'finished') and self.quiz_game.finished):
            return

        current_q_index = self.current_question_index 
        if current_q_index >= len(self.questions):
            return 
            
        q_data = self.questions[current_q_index]
        
        # Posiciones ajustadas a Y=600 para que sean visibles
        positions = [
            (250, 600), # 1. Izquierda 
            (400, 600), # 2. Centro izquierda 
            (550, 600), # 3. Centro derecha 
            (700, 600)  # 4. Derecha 
        ]

        num_choices = len(q_data["choices"])
        positions = positions[:num_choices]
        
        for i, choice in enumerate(q_data["choices"]):
            if i >= len(positions): break 
            
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
        
        # 1. Eliminar el objeto y soltarlo del jugador
        answer_pickup.kill() 
        self.held_answer = None 

        # 2. Registrar resultado y revisar derrota
        if len(self.answer_results) < self.max_questions:
            result_string = "correct" if is_correct else "incorrect"
            self.answer_results.append(result_string)
            
            # (Lógica de sonidos omitida)
            
            if self.answer_results.count("incorrect") >= 3:
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                return

        # 3. Avanzar a la siguiente pregunta
        if len(self.answer_results) < self.max_questions:
            self.current_question_index += 1
            
            if self.current_question_index < self.max_questions:
                if hasattr(self.quiz_game, 'current_question_index'):
                    self.quiz_game.current_question_index = self.current_question_index
                    
                self._generate_answer_pickups()
                self.quiz_timer.reset() 
                self.quiz_timer.start()
            else:
                if hasattr(self.quiz_game, 'finished'):
                    self.quiz_game.finished = True
        else:
            if hasattr(self.quiz_game, 'finished'):
                self.quiz_game.finished = True
    
    # --- MANEJO DE EVENTOS ---
    def handle_events(self, event):
        # (Lógica de estados finales y pantalla de controles omitida)

        # Teclas de interacción (Espacio/Enter)
        if event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_RETURN]):
            
            # Lógica de Diálogo: Avanzar texto o iniciar quiz
            if self.dialogo_active and self.typewriter:
                if not self.typewriter.finished():
                    self.typewriter.complete_text()
                elif self.state == "dialog":
                    # Inicia el quiz tras el diálogo inicial
                    self.timer.start()
                    self.quiz_timer.reset()
                    self.quiz_timer.start()
                    self.state = "quiz_floor"
                    self.dialogo_active = False # ¡Permite el movimiento del jugador!
                    self.typewriter = None
                    self.quiz_game = FloorQuiz(self.size, self.questions, self.font_question)
                    if hasattr(self.quiz_game, 'current_question_index'):
                        self.quiz_game.current_question_index = self.current_question_index
                    self._generate_answer_pickups()
                
                elif self.state == "quiz_complete_dialog":
                    # Avanza diálogos post-quiz
                    self.current_dialog_index += 1
                    if self.current_dialog_index < len(self.post_quiz_dialogs):
                        next_text = self.post_quiz_dialogs[self.current_dialog_index]
                        self.typewriter = TypewriterText(next_text, self.font_dialog, (255,255,255), speed=25)
                        self.dialogo_active = True
                    else:
                        self.dialogo_active = False # ¡Permite el movimiento del jugador!
                        self.typewriter = None

            # Lógica de Recoger / Entregar (solo en estado QUIZ)
            elif self.state == "quiz_floor":
                if not self.held_answer:
                    # 1. Intentar RECOGER una respuesta
                    for answer_pickup in self.answer_pickups:
                        if answer_pickup.visible and self.player.rect.colliderect(answer_pickup.rect.inflate(15, 15)):
                            self.held_answer = answer_pickup
                            self.held_answer.is_held = True
                            self.quiz_timer.pause() 
                            return None
                        
                elif self.held_answer:
                    # 2. Intentar ENTREGAR al guardia
                    if self.player.rect.colliderect(self.guardia_collision_rect.inflate(20, 20)):
                        self._submit_answer(self.held_answer)
                        return None
                            
        return None

    # --- LÓGICA DE ACTUALIZACIÓN ---
    def update(self):
        keys = pygame.key.get_pressed()

        # Lógica de fundido
        if self.is_fading:
            if self.state == "controls_screen":
                if self.target_state is None:
                    self.fade_alpha = max(0, self.fade_alpha - 5)
                    if self.fade_alpha == 0:
                        self.is_fading = False
                elif self.target_state == "game":
                    self.fade_alpha = min(255, self.fade_alpha + 10)
                    if self.fade_alpha == 255:
                        self.state = self.target_state
                        self.target_state = None
                        self.is_fading = True
            elif self.state == "game" and self.target_state is None:
                self.fade_alpha = max(0, self.fade_alpha - 5)
                if self.fade_alpha == 0:
                    self.is_fading = False
            return self.state

        # LÓGICA CORREGIDA DE MOVIMIENTO Y COLISIÓN
        if self.state in ["game", "quiz_floor", "dialog", "quiz_complete_dialog"]:
            
            # 1. Manejo del temporizador (solo si no estamos en diálogo)
            if self.timer.is_running() and not self.dialogo_active:
                self.timer.update()
            
            # 2. Lógica de Barrera: Solo la maestra actúa como barrera en estado "game" antes de interactuar.
            barrier = None 
            if self.state == "game" and not self.guard_interacted:
                barrier = self.guardia_collision_rect
            
            # 3. Lógica de Movimiento: Se permite mover solo si no hay diálogo activo.
            can_move = not self.dialogo_active 
            
            # Si tiene una respuesta, no hay barrera
            if self.held_answer:
                self.held_answer.update_position(self.player.rect)
                barrier = None 
            
            # Mueve al jugador (can_move detiene el movimiento si hay diálogo)
            self.player.move(keys, self.size[0], self.size[1], barrier, can_move=can_move)

            # Condición de tiempo general agotado
            if self.timer.finished and self.state not in ["loss_sound_state", "game_over", "win_state"]:
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                return self.state

        # Interacción con el guardia para iniciar el quiz
        if self.state == "game":
            # Lógica de victoria 
            if self.guard_interacted and hasattr(self, 'win_zone') and self.player.rect.colliderect(self.win_zone):
                pygame.mixer.music.stop()
                self.state = "win_state"
                self.confetti.start()
            
            if not self.is_fading and self.player.rect.colliderect(self.guardia_collision_rect.inflate(20,20)) and (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and not self.guard_interacted:
                self.state = "dialog"
                self.dialogo_active = True
                self.typewriter = TypewriterText(self.dialogo_text, self.font_dialog, (255,255,255), speed=25)

        # Estado del quiz
        elif self.state == "quiz_floor":
            if not self.quiz_timer.paused and not self.held_answer:
                self.quiz_timer.update()
                
            if self.quiz_timer.finished:
                # Tiempo agotado -> Respuesta incorrecta
                if len(self.answer_results) < self.max_questions:
                    self.answer_results.append("incorrect")
                    
                self.answer_pickups.empty()
                self.held_answer = None

                # Lógica de derrota 
                if self.answer_results.count("incorrect") >= 3:
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    return self.state
                
                # Avanzar al siguiente si quedan preguntas
                if len(self.answer_results) < self.max_questions:
                    self.current_question_index += 1
                    if self.current_question_index < self.max_questions:
                        if hasattr(self.quiz_game, 'current_question_index'):
                            self.quiz_game.current_question_index = self.current_question_index
                        self._generate_answer_pickups()
                        self.quiz_timer.reset()
                        self.quiz_timer.start()
                    else:
                        if hasattr(self.quiz_game, 'finished'):
                            self.quiz_game.finished = True 
                else:
                    if hasattr(self.quiz_game, 'finished'):
                        self.quiz_game.finished = True 

            # Transición a diálogo final
            if self.quiz_game and (hasattr(self.quiz_game, 'finished') and self.quiz_game.finished):
                self.state = "quiz_complete_dialog"
                score = self.answer_results.count("correct")
                total = len(self.questions)

                dialog_text = "¡Muy bien hecho! Has demostrado tener una buena\n calidad de estudio." if score == total else ("Buen trabajo. Tienes un buen nivel, sigue \npracticando." if score >= 2 else "Puedes mejorar, sigue estudiando.")

                self.post_quiz_dialogs = [
                    f"Has respondido correctamente {score} de {total} preguntas.",
                    dialog_text,
                    "Ahora te abro el paso. ¡Buena suerte en tu camino!"
                ]
                self.current_dialog_index = 0
                self.typewriter = TypewriterText(self.post_quiz_dialogs[self.current_dialog_index], self.font_dialog, (255,255,255), speed=25)
                self.dialogo_active = True
                self.quiz_game = None 
                self.timer.pause()
                self.quiz_timer.reset()

        # Diálogo final tras el quiz
        elif self.state == "quiz_complete_dialog":
            if not self.dialogo_active and self.current_dialog_index >= len(self.post_quiz_dialogs):
                # Mueve al guardia y abre el paso
                self.Guardia.rect.x = 250 
                self.guardia_collision_rect.x = self.Guardia.rect.x + int((self.Guardia.rect.width - self.guardia_collision_rect.width) / 2)
                self.Guardia.rect.y = 330
                self.guard_interacted = True
                self.background_changed = True
                self.state = "game" # Regresa al estado de movimiento libre

        if self.dialogo_active and self.typewriter:
            self.typewriter.update()
        self.confetti.update()
        return self.state
    
    # --- DIBUJO ---
    def draw(self):
        # (Dibujo de pantalla de controles omitido)

        # Dibujo principal del juego
        if self.state in ["game", "dialog", "quiz_complete_dialog", "quiz_floor", "loss_sound_state"]:
            self.screen.blit(self.background_image, (0, 0))
            self.Guardia.draw(self.screen)
            self.answer_pickups.draw(self.screen)
            self.player.draw(self.screen)

            # Dibuja la pregunta del quiz
            if self.state == "quiz_floor" and self.current_question_index < len(self.questions):
                current_q = self.questions[self.current_question_index]
                center_x = self.size[0] // 2
                start_y = 260
                box_w = 700
                box_h = 70
                question_rect = pygame.Rect(center_x - box_w // 2, start_y - 20, box_w, box_h)
                
                pygame.draw.rect(self.screen, (255, 200, 0), question_rect.inflate(8, 8), border_radius=10)
                pygame.draw.rect(self.screen, (20, 20, 100), question_rect, border_radius=8)

                text_lines = current_q["question"].split('\n')
                for i, line in enumerate(text_lines):
                    y_pos = start_y + i * 20 
                    self._draw_text_with_border(self.screen, line, self.font_question, (255, 255, 255), (0, 0, 0), (center_x, y_pos), border_size=1)
                
                self.quiz_timer.draw(self.screen, self.font_timer, (870, 100)) 

            self._draw_answer_results()

            # Dibuja el diálogo inferior
            if self.dialogo_active:
                if self.dialog_box_img:
                    self.screen.blit(self.dialog_box_img, self.dialog_box_rect)
                else:
                    pygame.draw.rect(self.screen, (50, 50, 50), self.dialog_box_rect)

                text_x = self.dialog_box_rect.x + 50 
                text_y = self.dialog_box_rect.y + 35
                text_to_show = None

                if self.typewriter and hasattr(self.typewriter, 'draw_text'):
                    self.typewriter.draw_text(self.screen, text_x, text_y)
                else:
                    try:
                        if self.typewriter and hasattr(self.typewriter, 'full_text'):
                            text_to_show = self.typewriter.full_text 
                        elif self.state == "dialog":
                            text_to_show = self.dialogo_text
                        elif self.state == "quiz_complete_dialog":
                             if self.current_dialog_index < len(self.post_quiz_dialogs):
                                  text_to_show = self.post_quiz_dialogs[self.current_dialog_index]
                        
                        if text_to_show:
                            text_lines = text_to_show.split('\n')
                            for i, line in enumerate(text_lines):
                                line_surface = self.font_dialog.render(line, True, (255, 255, 255))
                                self.screen.blit(line_surface, (text_x, text_y + i * self.font_dialog.get_height()))
                        else:
                            simple_error = self.font_dialog.render("Error: Text Not Found (99).", True, (255, 0, 0))
                            self.screen.blit(simple_error, (text_x, text_y))
                            
                    except Exception:
                        simple_error = self.font_dialog.render("Error: Rendering Failed (99).", True, (255, 0, 0))
                        self.screen.blit(simple_error, (text_x, text_y))

            
            self.confetti.draw(self.screen) 
        
        pygame.display.flip()