import pygame, sys
import random
from Personajes.boy import Characterb
from Personajes.girl import Characterg
from Personajes.Guardian import Characternpc
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Controldeobjetos.timer import Timer
from Interacciones.Controldeobjetos.corazones import LifeManager
from Interacciones.Memorama import QuizCards

class Level1:
    def __init__(self, screen, size, font, character_choice):
        self.screen = screen
        self.size = size
        self.font = font
        self.character_choice = character_choice
        
        if self.character_choice == "boy":
            self.player = Characterb(450, 750, 2)
        else:
            self.player = Characterg(350, 470, 2)
        
        self.Guardia = Characternpc(450, 350, 'Materials/Pictures/Characters/NPCs/Guardia/Guar_down1.png')
        self.background_image = pygame.image.load('Materials/Pictures/Assets/fondo_CloseDoor.jpg')
        self.background_image = pygame.transform.scale(self.background_image, self.size)
        self.timer = Timer(120)
        self.life_manager = LifeManager(3, 'Materials/Pictures/Assets/corazones.png')
        
        try:
            pygame.mixer.music.load('Materials/Music/Level1.wav')
            pygame.mixer.music.play(-1)
            self.loss_sound = pygame.mixer.Sound('Materials/Music/antesover.wav')
            self.game_over_music = pygame.mixer.Sound('Materials/Music/GameOver.wav')
            self.win_music = pygame.mixer.Sound('Materials/Music/Ganar.wav') # Nuevo audio para la victoria
            self.correct_sound = pygame.mixer.Sound('Materials/Music/PreguntaB.wav')
            self.incorrect_sound = pygame.mixer.Sound('Materials/Music/PreguntaM.wav')
        except pygame.error as e:
            print(f"No se pudo cargar la música: {e}")

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
        
        self.questions = [
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cómo se llama nuestro país?", "choices": ["España", "México", "Roma", "Berlín"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuánto es 2 + 2?", "choices": ["3", "4", "5", "6"], "correct_answer": 1 },
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuál es el animal más grande del mundo?", "choices": ["Ballena azul", "Elefante", "Tiburón blanco", "Jirafa"], "correct_answer": 0 },
            { "image": "Materials/Pictures/Assets/imagen1.jpg", "question": "¿Cuál es el océano más grande?", "choices": ["Atlántico", "Índico", "Pacífico", "Ártico"], "correct_answer": 2 }
        ]
        
        # Define la zona de victoria (las coordenadas de la zona blanca en el fondo)
        self.win_zone = pygame.Rect(350, 240, 200, 10)

    def handle_events(self, event):
        """Maneja los eventos del nivel."""
        if self.state in ["game_over", "loss_sound_state", "win_state"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.stop()
                    self.__init__(self.screen, self.size, self.font, self.character_choice)
                    return "restart"
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    return "menu"
        
        # ... (El resto de la lógica de handle_events es la misma) ...
        if self.state == "dialog" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.typewriter and self.typewriter.finished():
                self.state = "quiz_cards"
                self.dialogo_active = False
                self.typewriter = None
                self.quiz_game = QuizCards(self.size, self.questions)
        
        elif self.state == "quiz_complete_dialog" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.typewriter and self.typewriter.finished():
                self.current_dialog_index += 1
                if self.current_dialog_index < len(self.post_quiz_dialogs):
                    self.dialogo_active = True
                    self.typewriter = TypewriterText(self.post_quiz_dialogs[self.current_dialog_index], self.font, (255,255,255), speed=25)
                else:
                    self.state = "game"
                    self.dialogo_active = False
                    self.typewriter = None
                    self.Guardia.rect.x -= 130
                    self.player.rect.x = 450
                    self.player.rect.y = 570
        
        if self.state == "quiz_cards" and self.quiz_game:
            result = self.quiz_game.handle_event(event)
            if result == "correct":
                self.correct_sound.play()
            elif result == "incorrect":
                self.incorrect_sound.play()
                self.life_manager.lose_life()
                if self.life_manager.is_dead():
                    self.state = "loss_sound_state"
                    pygame.mixer.music.stop()
                    self.loss_sound.play()
        
        return None

    def update(self):
        """Actualiza la lógica del nivel."""
        if self.state == "game":
            keys = pygame.key.get_pressed()
            self.player.move(keys, self.size[0], self.size[1], self.Guardia.rect)
            
            # Condición de victoria: si el jugador colisiona con la zona de victoria
            if self.player.rect.colliderect(self.win_zone):
                pygame.mixer.music.stop()
                self.state = "win_state"
                if not self.win_music_played:
                    self.win_music.play()
                    self.win_music_played = True

            elif self.player.rect.colliderect(self.Guardia.rect.inflate(20,20)) and keys[pygame.K_SPACE] and not self.guard_interacted:
                self.state = "dialog"
                self.dialogo_active = True
                self.typewriter = TypewriterText(self.dialogo_text, self.font, (255,255,255), speed=25)
                self.guard_interacted = True
        
        # ... (El resto de la lógica de update es la misma) ...
        elif self.state == "quiz_cards":
            if not self.quiz_game.finished:
                self.quiz_game.update()
            else:
                self.state = "quiz_complete_dialog"
                self.dialogo_active = True
                score = self.quiz_game.correct_answers
                total = len(self.questions) 
                
                if score == total:
                    dialog_text = "¡Muy bien hecho! Has demostrado tener una buena calidad de estudio."
                elif score >= 3:
                    dialog_text = "El aprendizaje siempre esta para aquellos que lo necesitan.\n Sigue practicando."
                else:
                    dialog_text = "El aprendizaje son oportunidades que nunca se deben desaprovechar\n ¡Practica para la proxima vez!"
                
                self.post_quiz_dialogs = [
                    f"Has respondido correctamente {score} de {total} preguntas.",
                    dialog_text,
                    "Ahora puedes pasar. ¡Buena suerte en tu camino!"
                ]
                self.current_dialog_index = 0
                self.typewriter = TypewriterText(self.post_quiz_dialogs[self.current_dialog_index], self.font, (255,255,255), speed=25)
                self.quiz_game = None
                self.timer.reset()
        
        elif self.state == "loss_sound_state":
            if not pygame.mixer.get_busy():
                self.state = "game_over"
                if not self.game_over_music_played:
                    self.game_over_music.play(-1)
                    self.game_over_music_played = True

        if self.dialogo_active and self.typewriter:
            self.typewriter.update()

        return self.state

    def draw(self):
        """Dibuja los elementos en la pantalla."""
        if self.state in ["game", "dialog", "quiz_complete_dialog", "quiz_cards", "loss_sound_state"]:
            self.screen.blit(self.background_image, (0, 0))
            self.player.draw(self.screen)
            self.Guardia.draw(self.screen)
            self.timer.draw(self.screen, self.font)
            self.life_manager.draw(self.screen)
            
            # Dibujar la zona de victoria para depuración (opcional)
            # pygame.draw.rect(self.screen, (255, 0, 0), self.win_zone, 2)

            if self.dialogo_active:
                box_rect = pygame.Rect(50, 550, 800, 100)
                pygame.draw.rect(self.screen, (0, 0, 0), box_rect)
                pygame.draw.rect(self.screen, (255, 255, 255), box_rect, 3)
                self.typewriter.draw(self.screen, (box_rect.x + 20, box_rect.y + 30))

            if self.state == "quiz_cards":
                self.quiz_game.draw(self.screen)
        
        elif self.state == "win_state":
            self.screen.fill((0, 0, 0))
            win_text = self.font.render("¡HAS GANADO!", True, (0, 255, 0))
            retry_text = self.font.render("Presiona R para reiniciar o ESC para ir al menú", True, (255, 255, 255))
            self.screen.blit(win_text, win_text.get_rect(center=(self.size[0] // 2, self.size[1] // 2 - 40)))
            self.screen.blit(retry_text, retry_text.get_rect(center=(self.size[0] // 2, self.size[1] // 2 + 20)))

        elif self.state == "game_over":
            self.screen.fill((0, 0, 0))
            game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            retry_text = self.font.render("Presiona R para reiniciar o ESC para ir al menú", True, (255, 255, 255))
            self.screen.blit(game_over_text, game_over_text.get_rect(center=(self.size[0] // 2, self.size[1] // 2 - 40)))
            self.screen.blit(retry_text, retry_text.get_rect(center=(self.size[0] // 2, self.size[1] // 2 + 20)))