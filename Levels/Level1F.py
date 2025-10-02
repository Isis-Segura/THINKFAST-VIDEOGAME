import pygame
import random
from Personajes.boy import Characterb
from Personajes.girl import Characterg
from Personajes.Guardian import Characternpc 
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Controldeobjetos.timer import Timer
from Interacciones.Controldeobjetos.corazones import LifeManager
from Interacciones.FloorQuiz import FloorQuiz 

# -------------------------------------------------------------------------
# Confetti: partículas con sombra
# -------------------------------------------------------------------------
class Confetti:
    def __init__(self, screen_width, screen_height):
        self.particles = []               # lista de partículas [x,y,dx,dy,color,life]
        self.colors = [
            (255, 0, 0), (0, 255, 0), (0, 150, 255),
            (255, 255, 0), (255, 0, 255), (255,128,0), (128,0,255)
        ]
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.spawn_rate = 5   # cuántas se crean cada frame mientras active
        self._max_life = 140

    def start(self):
        """Activa el confeti (se resetean partículas)."""
        self.active = True
        self.particles = []

    def stop(self):
        """Desactiva el confeti (se deja que las partículas restantes se consuman)."""
        self.active = False

    def update(self):
        """Genera y actualiza partículas; llamar cada frame desde update() del nivel."""
        if self.active:
            for _ in range(self.spawn_rate):
                side = random.choice(["left", "right"])
                x = 0 if side == "left" else self.screen_width
                y = random.randint(0, self.screen_height // 3)
                dx = random.uniform(-3, 3)
                # si viene desde la derecha, forzar dx negativo moderado para atravesar la pantalla
                if side == "right" and dx > -0.5:
                    dx = random.uniform(-3, -0.8)
                if side == "left" and dx < 0.5:
                    dx = random.uniform(0.8, 3)
                dy = random.uniform(1.5, 4.0)
                color = random.choice(self.colors)
                life = random.randint(int(self._max_life*0.6), self._max_life)
                size = random.randint(4, 7)
                # almacena partícula: x,y,dx,dy,color,life,size
                self.particles.append([x, y, dx, dy, color, life, size])

        # actualizar movimiento y vida
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[5] -= 1

        # limpiar partículas muertas o fuera de pantalla
        self.particles = [p for p in self.particles if p[5] > 0 and p[1] < self.screen_height + 50]

    def draw(self, surface):
        """Dibuja partículas con sombra (shadow then color)."""
        if not self.particles:
            return
        for p in self.particles:
            x, y, dx, dy, color, life, size = p
            # sombra: ligeramente desplazada hacia abajo/derecha, dibujada más grande
            shadow_radius = int(size * 1.4)
            pygame.draw.circle(surface, (30, 30, 30), (int(x + 2), int(y + 3)), shadow_radius)
            # partícula principal
            pygame.draw.circle(surface, color, (int(x), int(y)), size)


# -------------------------------------------------------------------------
# Level1 (versión integrada con confetti, sombras y gestión de fuentes)
# -------------------------------------------------------------------------
class Level1:
    def __init__(self, screen, size, font, character_choice):
        """
        - screen: surface principal
        - size: (width, height)
        - font: objeto pygame.font.Font (usado por defecto)
        - character_choice: "boy" o "girl"
        """
        self.screen = screen
        self.size = size
        self.font = font  # fuente por defecto que te pasan (puede ser None)
        self.character_choice = character_choice

        # ----------------------------
        # Entidades
        # ----------------------------
        if self.character_choice == "boy":
            self.player = Characterb(440, 600, 2)
        else:
            self.player = Characterg(440, 600, 2)

        self.Guardia = Characternpc(470, 330, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')

        # Colisión ajustada para el guardia (banda baja)
        guardia_width = self.Guardia.rect.width
        guardia_height = self.Guardia.rect.height
        COL_WIDTH_FACTOR = 0.5
        COL_HEIGHT_PIXELS = 5
        new_width = int(guardia_width * COL_WIDTH_FACTOR)
        new_height = COL_HEIGHT_PIXELS
        new_x = self.Guardia.rect.x + int((guardia_width - new_width) / 2)
        new_y = self.Guardia.rect.y + guardia_height - new_height
        self.guardia_collision_rect = pygame.Rect(new_x, new_y, new_width, new_height)

        # ----------------------------
        # Recursos gráficos y HUD
        # ----------------------------
        self.background_image = pygame.image.load('Materials/Pictures/Assets/fondo_CloseDoor.jpg').convert()
        self.background_image = pygame.transform.scale(self.background_image, self.size)

        # dialog box image (si no existe, se usa un rect como fallback)
        try:
            img = pygame.image.load("Materials/Pictures/Assets/dialog_box.png").convert_alpha()
            self.dialog_box_img = pygame.transform.scale(img, (800, 120))
            self.dialog_box_rect = self.dialog_box_img.get_rect()
            self.dialog_box_rect.center = (self.size[0] // 2, self.size[1] - 70)
            self._dialog_img_loaded = True
        except Exception:
            # fallback: no image found
            self._dialog_img_loaded = False
            self.dialog_box_img = None
            self.dialog_box_rect = pygame.Rect(50, self.size[1] - 150, 800, 100)

        # ----------------------------
        # Timers y vida
        # ----------------------------
        self.timer = Timer(120)
        self.quiz_timer = Timer(10)
        self.quiz_timer.start()
        self.life_manager = LifeManager(3, 'Materials/Pictures/Assets/corazones.png')

        # ----------------------------
        # Sonidos
        # ----------------------------
        try:
            pygame.mixer.music.load('Materials/Music/Level1.wav')
            pygame.mixer.music.play(-1)
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

        # ----------------------------
        # Estado del juego
        # ----------------------------
        self.state = "game"
        self.dialogo_text = "¡Alto! Tienes que responder estas preguntas!!"
        self.typewriter = None
        self.dialogo_active = False
        self.quiz_game = None
        self.post_quiz_dialogs = []
        self.current_dialog_index = 0
        self.guard_interacted = False
        self.game_over_music_played = False
        self.win_music_played = False

        # ----------------------------
        # Confetti
        # ----------------------------
        self.confetti = Confetti(self.size[0], self.size[1])

        # ----------------------------
        # Preguntas
        # ----------------------------
        self.questions = [
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cómo se llama nuestro país?", "choices": ["España", "México", "Roma", "Berlín"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuánto es 2 + 2?", "choices": ["3", "4", "5", "6"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuál es el animal más grande del mundo?", "choices": ["Ballena azul", "Elefante", "Tiburón", "Jirafa"], "correct_answer": 0 },
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuál es el océano más grande?", "choices": ["Atlántico", "Índico", "Pacífico", "Ártico"], "correct_answer": 2 }
        ]
        self.win_zone = pygame.Rect(420, 280, 65, 65)
        # Fuentes 
        self.font_dialog = self.font if isinstance(self.font, pygame.font.Font) else pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 10)
        self.font_question = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 11)
        self.font_title = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 15)
        self.font_timer = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 20)

    # -------------------------------------------------------------------------
    # Helper para setear fuentes desde fuera
    # -------------------------------------------------------------------------
    def _make_font(self, spec, default_size):
        """
        spec puede ser:
         - None -> pygame.font.Font(None, default_size)
         - pygame.font.Font -> lo devuelve
         - int -> pygame.font.Font(None, int)
         - (ruta_str, tamaño_int) -> pygame.font.Font(ruta_str, tamaño_int)
        """
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
        """
        Llama a esto para cambiar las fuentes en tiempo de ejecución.
        Ejemplos de argumentos válidos:
          - pygame.font.Font objeto
          - entero (tamaño) -> creará Font(None, size)
          - ("ruta/a/archivo.ttf", tamaño)
          - None -> usa tamaño por defecto
        """
        self.font_dialog = self._make_font(dialog_font, 28)
        self.font_question = self._make_font(question_font, 32)
        self.font_title = self._make_font(title_font, 48)
        self.font_timer = self._make_font(timer_font, 26)

    # -------------------------------------------------------------------------
    # Manejo de eventos
    # -------------------------------------------------------------------------
    def handle_events(self, event):
        """Maneja eventos (teclado / mouse)."""
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

        # diálogos (typewriter)
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
            if self.dialogo_active and self.typewriter:
                if not self.typewriter.finished():
                    self.typewriter.complete_text()
                elif self.state == "dialog":
                    self.state = "quiz_floor"
                    self.dialogo_active = False
                    self.typewriter = None
                    # reiniciar timer de pregunta
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

        # eventos del quiz_floor (doble espacio: responder + avanzar)
        if self.state == "quiz_floor" and self.quiz_game:
            result = self.quiz_game.handle_event(event)
            # PRIMERA pulsación: resultado de la respuesta
            if result in ["correct", "incorrect"]:
                if result == "correct":
                    if self.correct_sound: self.correct_sound.play()
                else:
                    if self.incorrect_sound: self.incorrect_sound.play()
                    self.life_manager.lose_life()
                if self.life_manager.is_dead():
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    if self.loss_sound: self.loss_sound.play()
            # SEGUNDA pulsación: avanzar de pregunta
            elif result == "advanced":
                self.quiz_timer = Timer(10)
                self.quiz_timer.start()
            # otros resultados (finished) manejados en update()
        return None

    # -------------------------------------------------------------------------
    # Update - lógica por frame
    # -------------------------------------------------------------------------
    def update(self):
        keys = pygame.key.get_pressed()

        # movimiento con barrera
        if self.state in ["game", "quiz_floor"]:
            barrier = self.guardia_collision_rect if not self.guard_interacted else None
            self.player.move(keys, self.size[0], self.size[1], barrier)

        if self.state == "game":
            # si ya interactuamos, se habilita la zona de salida
            if self.guard_interacted:
                if self.player.rect.colliderect(self.win_zone):
                    pygame.mixer.music.stop()
                    self.state = "win_state"
                    if self.win_music and not self.win_music_played:
                        self.win_music.play()
                        self.win_music_played = True
            # si nos acercamos al guardia y no hemos interactuado: diálogo
            elif self.player.rect.colliderect(self.guardia_collision_rect.inflate(20,20)) and keys[pygame.K_SPACE] and not self.guard_interacted:
                self.state = "dialog"
                self.dialogo_active = True
                self.typewriter = TypewriterText(self.dialogo_text, self.font_dialog, (255,255,255), speed=25)

        elif self.state == "quiz_floor":
            # actualizar timer de pregunta
            self.quiz_timer.update()

            # si se acaba el tiempo y la pregunta no fue respondida
            if self.quiz_timer.finished and not getattr(self.quiz_game, "is_answered", False):
                if self.incorrect_sound: self.incorrect_sound.play()
                self.life_manager.lose_life()
                # marcar la pregunta como respondida (forzar estado)
                self.quiz_game.is_answered = True
                self.quiz_game.answer_result = "incorrect"
                self.quiz_game.selected_choice_index = -1
                advance_result = getattr(self.quiz_game, "advance_question", lambda: "finished")()
                if advance_result != "finished":
                    self.quiz_timer = Timer(10)
                    self.quiz_timer.start()

            # comprobar si se quedó sin vidas
            if self.life_manager.is_dead():
                self.state = "loss_sound_state"
                pygame.mixer.music.stop()
                if self.loss_sound: self.loss_sound.play()

            # colisiones de selección del quiz
            self.quiz_game.check_player_collision(self.player.rect)

            # si el quiz terminó: preparar diálogos post-quiz, reiniciar timer general
            if self.quiz_game.finished:
                self.state = "quiz_complete_dialog"
                self.dialogo_active = True
                score = self.quiz_game.correct_answers
                total = len(self.questions)

                if score == total:
                    dialog_text = "¡Muy bien hecho! Has demostrado tener una buena calidad de estudio."
                elif score >= 3:
                    dialog_text = "Buen trabajo. Tienes un buen nivel, sigue practicando.\n El aprendizaje son oportunidades que nunca se deben desaprovechar."
                else:
                    dialog_text = "Puedes mejorar, solo aquellos que estudian pueden cruzar\n superar cualquier obstaculo que se le presente.!"

                self.post_quiz_dialogs = [
                    f"Has respondido correctamente {score} de {total} preguntas.",
                    dialog_text,
                    "Ahora te abro el paso. ¡Buena suerte en tu camino!"
                ]

                self.current_dialog_index = 0
                self.typewriter = TypewriterText(self.post_quiz_dialogs[self.current_dialog_index], self.font_dialog, (255,255,255), speed=25)
                self.quiz_game = None
                self.timer.reset()

                # activar confeti cuando tenga 2 o más correctas
                if score >= 2:
                    self.confetti.start()

        elif self.state == "quiz_complete_dialog":
            # cuando terminan todos los diálogos post-quiz hacemos la transición a game
            if not self.dialogo_active and self.current_dialog_index >= len(self.post_quiz_dialogs):
                self.Guardia.rect.x -= 130
                guardia_width = self.Guardia.rect.width
                new_width = self.guardia_collision_rect.width
                self.guardia_collision_rect.x = self.Guardia.rect.x + int((guardia_width - new_width) / 2)
                self.player.rect.x = 450
                self.player.rect.y = 570
                self.guard_interacted = True
                self.state = "game"

        elif self.state == "loss_sound_state":
            if not pygame.mixer.get_busy():
                self.state = "game_over"
                if self.game_over_music and not self.game_over_music_played:
                    self.game_over_music.play(-1)
                    self.game_over_music_played = True

        # actualizar typewriter
        if self.dialogo_active and self.typewriter:
            self.typewriter.update()

        # actualizar confeti cada frame
        self.confetti.update()
        return self.state

    # -------------------------------------------------------------------------
    # Dibujo (draw)
    # -------------------------------------------------------------------------
    def draw(self):
        """Dibuja los elementos en la pantalla."""
        if self.state in ["game", "dialog", "quiz_complete_dialog", "quiz_floor", "loss_sound_state"]:
            # fondo
            self.screen.blit(self.background_image, (0, 0))

            # sombra de personaje
            shadow_offset = 6
            # jugador
            try:
                px = self.player.rect.x-5
                py = self.player.rect.y+5
                pw = self.player.rect.width+10
                ph = self.player.rect.height
                shadow_surface = pygame.Surface((self.player.rect.width, 8), pygame.SRCALPHA)
                pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, self.player.rect.width, 8))
                self.screen.blit(shadow_surface, (px + shadow_offset, py + ph - 10))
            except Exception:
                pass
            # guardia
            try:
                gx = self.Guardia.rect.x
                gy = self.Guardia.rect.y
                gw = self.Guardia.rect.width+10
                gh = self.Guardia.rect.height
                pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, self.player.rect.width, 8))
                self.screen.blit(shadow_surface, (gx + shadow_offset, gy + gh - 10))
            except Exception:
                pass

            # dibujar personajes
            self.player.draw(self.screen)
            self.Guardia.draw(self.screen)

            # dibujar timer (si es quiz, dibuja quiz_timer con fuente de timer)
            if self.state == "quiz_floor":
                # pasamos font de timer personalizado
                try:
                    self.quiz_timer.draw(self.screen, self.font_timer, is_quiz_timer=True, position=(680, 10))
                except Exception:
                    self.quiz_timer.draw(self.screen, self.font, is_quiz_timer=True, position=(680, 10))
            else:
                try:
                    self.timer.draw(self.screen, self.font_timer, position=(680, 10))
                except Exception:
                    self.timer.draw(self.screen, self.font, position=(680, 10))

            # vida
            self.life_manager.draw(self.screen)

            # confeti: dibujar antes del cuadro de diálogo para que quede detrás
            self.confetti.draw(self.screen)

            # quiz en el suelo
            if self.state == "quiz_floor" and self.quiz_game:
                self.quiz_game.draw(self.screen)

            # cuadro de diálogo
            if self.dialogo_active:
                if self._dialog_img_loaded and self.dialog_box_img:
                    # dibujar la imagen centrada
                    self.screen.blit(self.dialog_box_img, self.dialog_box_rect.topleft)
                    # borde opcional encima (puedes comentarlo si la imagen ya trae borde)
                    pygame.draw.rect(self.screen, (255,255,255), self.dialog_box_rect, 3, border_radius=10)
                    # dibujar texto con typewriter dentro de la caja (márgenes)
                    self.typewriter.draw(self.screen, (self.dialog_box_rect.x + 20, self.dialog_box_rect.y + 30))
                else:
                    # fallback: rect negro con borde blanco
                    box_rect = pygame.Rect(50, 550, 800, 100)
                    pygame.draw.rect(self.screen, (0, 0, 0), box_rect)
                    pygame.draw.rect(self.screen, (255, 255, 255), box_rect, 3)
                    self.typewriter.draw(self.screen, (box_rect.x + 20, box_rect.y + 30))

        # pantallas finales
        elif self.state == "win_state":
            self.screen.fill((0, 0, 0))
            try:
                text1 = self.font_title.render("¡HAS GANADO!", True, (0, 255, 0))
                text2 = self.font.render("Presiona R para reiniciar o ESC para ir al menú", True, (255, 255, 255))
                self.screen.blit(text1, text1.get_rect(center=(self.size[0] // 2, self.size[1] // 2 - 40)))
                self.screen.blit(text2, text2.get_rect(center=(self.size[0] // 2, self.size[1] // 2 + 20)))
            except Exception:
                win_text = self.font.render("¡HAS GANADO!", True, (0, 255, 0))
                retry_text = self.font.render("Presiona R para reiniciar o ESC para ir al menú", True, (255, 255, 255))
                self.screen.blit(win_text, win_text.get_rect(center=(self.size[0] // 2, self.size[1] // 2 - 40)))
                self.screen.blit(retry_text, retry_text.get_rect(center=(self.size[0] // 2, self.size[1] // 2 + 20)))

        elif self.state == "game_over":
            self.screen.fill((0, 0, 0))
            try:
                text1 = self.font_title.render("GAME OVER", True, (255, 0, 0))
                text2 = self.font.render("Presiona R para reiniciar o ESC para ir al menú", True, (255, 255, 255))
                self.screen.blit(text1, text1.get_rect(center=(self.size[0] // 2, self.size[1] // 2 - 40)))
                self.screen.blit(text2, text2.get_rect(center=(self.size[0] // 2, self.size[1] // 2 + 20)))
            except Exception:
                game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
                retry_text = self.font.render("Presiona R para reiniciar o ESC para ir al menú", True, (255, 255, 255))
                self.screen.blit(game_over_text, game_over_text.get_rect(center=(self.size[0] // 2, self.size[1] // 2 - 40)))
                self.screen.blit(retry_text, retry_text.get_rect(center=(self.size[0] // 2, self.size[1] // 2 + 20)))
