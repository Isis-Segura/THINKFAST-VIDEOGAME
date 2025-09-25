import pygame
import random

class QuizCards:
    def __init__(self, screen_size, questions):
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.font = pygame.font.SysFont(None, 40)
        self.questions = questions
        self.current_question_index = 0
        self.correct_answers = 0
        self.finished = False

        self.cards = []
        self.card_size = (150, 200)
        
        self.state = "showing"
        self.showing_timer = pygame.time.get_ticks()
        self.showing_duration = 3000
        
        self.is_flipping = False
        self.flip_timer = 0
        self.flip_duration = 500
        self.flipping_card_index = -1
        
        if self.questions:
            self.setup_cards()

    def setup_cards(self):
        self.cards = []
        if self.current_question_index >= len(self.questions):
            self.finished = True
            return

        current_q = self.questions[self.current_question_index]
        choices = list(current_q["choices"])
        random.shuffle(choices)
        
        start_x = (self.screen_width - (len(choices) * (self.card_size[0] + 20))) / 2
        
        for i, text in enumerate(choices):
            card_rect = pygame.Rect(
                start_x + i * (self.card_size[0] + 20),
                self.screen_height / 2 + 100,
                self.card_size[0],
                self.card_size[1]
            )
            is_correct = (text == current_q["choices"][current_q["correct_answer"]])
            self.cards.append({
                "rect": card_rect,
                "text": text,
                "is_correct": is_correct,
                "is_flipped": False,
                "flip_progress": 0
            })
        
        self.state = "showing"
        self.showing_timer = pygame.time.get_ticks()

    def handle_event(self, event):
        if self.state != "playing":
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, card in enumerate(self.cards):
                if card["rect"].collidepoint(mouse_pos):
                    self.start_flip(i)
                    self.check_answer(i)
                    break
    
    def start_flip(self, index):
        self.is_flipping = True
        self.flipping_card_index = index
        self.state = "flipping"
        self.flip_timer = pygame.time.get_ticks()

    def check_answer(self, index):
        if self.cards[index]["is_correct"]:
            self.correct_answers += 1
            print("¡Correcto!")
        else:
            print("¡Incorrecto!")
        
    def update(self):
        if self.finished:
            return

        if self.state == "showing":
            if pygame.time.get_ticks() - self.showing_timer > self.showing_duration:
                self.state = "playing"
        
        if self.state == "flipping":
            elapsed = pygame.time.get_ticks() - self.flip_timer
            progress = min(1.0, elapsed / self.flip_duration)
            self.cards[self.flipping_card_index]["flip_progress"] = progress
            if progress >= 1.0:
                pygame.time.delay(500)
                self.next_question()

    def wrap_text(self, text, font, max_width):
        """Envuelve el texto en varias líneas si es muy largo."""
        words = text.split(' ')
        wrapped_lines = []
        current_line = ''
        
        for word in words:
            if font.size(current_line + ' ' + word)[0] < max_width:
                current_line += ' ' + word
            else:
                wrapped_lines.append(current_line.strip())
                current_line = word
        wrapped_lines.append(current_line.strip())
        
        return wrapped_lines

    def draw(self, surface):
        if self.finished:
            return

        current_q = self.questions[self.current_question_index]
        
        # Dibuja el recuadro para la pregunta
        question_surface = self.font.render(current_q["question"], True, (255, 255, 255))
        question_rect = question_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 150))
        bg_rect = question_rect.inflate(40, 20)
        
        pygame.draw.rect(surface, (0, 0, 0), bg_rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), bg_rect, 3, border_radius=10)
        
        surface.blit(question_surface, question_rect)
        

        for i, card in enumerate(self.cards):
            if self.state == "showing":
                pygame.draw.rect(surface, (255, 255, 255), card["rect"], border_radius=10)
                
                # Usa la función para envolver el texto y calcular la altura total
                lines = self.wrap_text(card["text"], self.font, card["rect"].width - 20)
                total_text_height = len(lines) * self.font.get_height()
                
                # Calcula la posición de inicio para centrar verticalmente el texto
                start_y = card["rect"].y + (card["rect"].height - total_text_height) / 2
                
                for line in lines:
                    text_surface = self.font.render(line, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(card["rect"].centerx, start_y))
                    surface.blit(text_surface, text_rect)
                    start_y += self.font.get_height()

            elif self.state == "playing":
                text_surface = self.font.render("?", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=card["rect"].center)
                pygame.draw.rect(surface, (100, 100, 200), card["rect"], border_radius=10)
                surface.blit(text_surface, text_rect)
            
            elif self.state == "flipping":
                progress = card["flip_progress"]
                
                if i == self.flipping_card_index:
                    current_width = self.card_size[0] * (1 - abs(progress - 0.5) * 2)
                    
                    if progress > 0.5:
                        pygame.draw.rect(surface, (255, 255, 255), card["rect"], border_radius=10)
                        
                        lines = self.wrap_text(card["text"], self.font, card["rect"].width - 20)
                        total_text_height = len(lines) * self.font.get_height()
                        start_y = card["rect"].y + (card["rect"].height - total_text_height) / 2

                        for line in lines:
                            text_surface = self.font.render(line, True, (0, 0, 0))
                            text_rect = text_surface.get_rect(center=(card["rect"].centerx, start_y))
                            surface.blit(text_surface, text_rect)
                            start_y += self.font.get_height()
                    else:
                        text_surface = self.font.render("?", True, (255, 255, 255))
                        text_rect = text_surface.get_rect(center=card["rect"].center)
                        pygame.draw.rect(surface, (100, 100, 200), card["rect"], border_radius=10)
                        surface.blit(text_surface, text_rect)
                else:
                    text_surface = self.font.render("?", True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=card["rect"].center)
                    pygame.draw.rect(surface, (100, 100, 200), card["rect"], border_radius=10)
                    surface.blit(text_surface, text_rect)

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index >= len(self.questions):
            self.finished = True
        else:
            self.setup_cards()
            self.state = "showing"