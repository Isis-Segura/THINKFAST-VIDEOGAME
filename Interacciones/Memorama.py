import pygame
import math
import random # Agregamos random para barajar las preguntas

class QuizCards:
    def __init__(self, size, questions):
        self.size = size
        self.questions = list(questions) # Usamos una copia para no modificar el original
        random.shuffle(self.questions) # Barajamos las preguntas al crear el objeto
        self.current_question = 0
        self.answered = False
        self.finished = False
        self.correct_answers = 0
        self.wrong_answers = 0
        self.answer_rects = []
        
        self.font = pygame.font.Font(None, 36)
        
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (150, 150, 150)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        
        self.flipping = False
        self.flip_angle = 0
        self.flip_speed = 10 
        self.wait_time_after_answer = 2000
        self.answered_time = 0
        self.selected_answer_index = -1
        
        self.show_answers = True
        self.preview_timer = pygame.time.get_ticks()
        self.preview_time_limit = 2000

    def handle_event(self, event):
        if self.finished or self.flipping or self.answered or self.show_answers:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.answer_rects):
                if rect.collidepoint(event.pos):
                    self.answered = True
                    self.selected_answer_index = i
                    self.answered_time = pygame.time.get_ticks()

                    if i == self.questions[self.current_question]["correct_answer"]:
                        self.correct_answers += 1
                        return "correct"
                    else:
                        self.wrong_answers += 1
                        return "incorrect"
        return None

    def update(self):
        if self.show_answers and pygame.time.get_ticks() - self.preview_timer > self.preview_time_limit:
            self.show_answers = False

        if self.answered and not self.flipping:
            if pygame.time.get_ticks() - self.answered_time > self.wait_time_after_answer:
                self.flipping = True
                self.flip_angle = 0
        
        if self.flipping:
            self.flip_angle += self.flip_speed
            if self.flip_angle >= 180:
                self.flip_angle = 0
                self.flipping = False
                self.answered = False
                self.selected_answer_index = -1
                self.current_question += 1
                self.show_answers = True
                self.preview_timer = pygame.time.get_ticks()
                if self.current_question >= len(self.questions):
                    self.finished = True
                
    def draw(self, screen):
        quiz_rect = pygame.Rect(self.size[0] // 2 - 300, self.size[1] // 2 - 250, 600, 500)
        
        pygame.draw.rect(screen, self.gray, quiz_rect)
        pygame.draw.rect(screen, self.black, quiz_rect, 5)

        if self.finished or self.current_question >= len(self.questions):
            return
            
        current_q = self.questions[self.current_question]
        
        image_path = current_q["image"]
        try:
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (200, 150))
            image_rect_temp = image.get_rect(center=(quiz_rect.centerx, quiz_rect.top + 100))
            screen.blit(image, image_rect_temp)
        except pygame.error as e:
            print(f"No se pudo cargar la imagen: {e}")
        
        question_text = self.font.render(current_q["question"], True, self.black)
        question_rect_temp = question_text.get_rect(center=(quiz_rect.centerx, quiz_rect.top + 250))
        screen.blit(question_text, question_rect_temp)
        
        self.answer_rects = []
        for i, choice in enumerate(current_q["choices"]):
            y_pos = quiz_rect.top + 300 + i * 50
            choice_rect = pygame.Rect(quiz_rect.left + 50, y_pos, 500, 40)
            self.answer_rects.append(choice_rect)
            
            if self.flipping and i == self.selected_answer_index:
                cos_val = math.cos(math.radians(self.flip_angle))
                width = 500 * abs(cos_val)
                height = 40
                
                card_surface = pygame.Surface((500, 40))
                
                if self.flip_angle < 90:
                    card_surface.fill(self.white)
                    pygame.draw.rect(card_surface, self.black, card_surface.get_rect(), 2)
                    dot_surface = self.font.render("?", True, self.black)
                    dot_rect = dot_surface.get_rect(center=(250, 20))
                    card_surface.blit(dot_surface, dot_rect)
                else:
                    card_surface.fill(self.white)
                    pygame.draw.rect(card_surface, self.black, card_surface.get_rect(), 2)
                    choice_text = self.font.render(choice, True, self.black)
                    card_surface.blit(choice_text, (10, 5))

                scaled_card = pygame.transform.scale(card_surface, (int(width), height))
                scaled_rect = scaled_card.get_rect(center=choice_rect.center)
                screen.blit(scaled_card, scaled_rect)
            
            elif self.show_answers or self.answered:
                pygame.draw.rect(screen, self.white, choice_rect)
                pygame.draw.rect(screen, self.black, choice_rect, 2)
                choice_text = self.font.render(choice, True, self.black)
                screen.blit(choice_text, (choice_rect.x + 10, choice_rect.y + 5))
            
            else:
                pygame.draw.rect(screen, self.white, choice_rect)
                pygame.draw.rect(screen, self.black, choice_rect, 2)
                dot_surface = self.font.render("?", True, self.black)
                dot_rect = dot_surface.get_rect(center=choice_rect.center)
                screen.blit(dot_surface, dot_rect)
        
        if self.answered:
            color = self.green if self.selected_answer_index == self.questions[self.current_question]["correct_answer"] else self.red
            result_text = "¡Correcto!" if color == self.green else "Incorrecto."
            result_surface = self.font.render(result_text, True, color)
            result_rect = result_surface.get_rect(center=(quiz_rect.centerx, quiz_rect.bottom - 40))
            screen.blit(result_surface, result_rect)