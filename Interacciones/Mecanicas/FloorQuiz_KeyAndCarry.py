import pygame
import random
import os

class FloorQuiz_KeyAndCarry:
    def __init__(self, size, questions, font):
        self.size = size
        self.questions_data = questions
        self.font = font
        self.current_question_index = 0
        self.answered_questions_count = 0
        self.finished = False
        self.is_answered = False
        self.answer_result = None
        self.carried_choice_index = -1 
        self.carried_choice_rect = None 
        self.highlighted_choice_index = -1 # NUEVA: Opción resaltada por colisión
        self.original_choice_rects = [] 
        self.choice_rects = []
        self.quiz_image = None
        self.load_question()

    def load_question(self):
        if self.current_question_index >= len(self.questions_data):
            self.finished = True
            return

        q_data = self.questions_data[self.current_question_index]
        self.question = q_data["question"]
        self.choices = q_data["choices"]
        self.correct_answer_index = q_data["correct_answer"]
        self.is_answered = False
        self.answer_result = None
        self.carried_choice_index = -1
        self.carried_choice_rect = None
        self.highlighted_choice_index = -1
        self.quiz_image = None
            
        self.setup_choice_rects()

    def setup_choice_rects(self):
        num_choices = len(self.choices)
        choice_w = 180
        choice_h = 50
        total_width = num_choices * choice_w + (num_choices - 1) * 30 
        x_start = (self.size[0] - total_width) // 2
        y_start = self.size[1] - 180 
        
        self.choice_rects = []
        self.original_choice_rects = []
        for i in range(num_choices):
            x = x_start + i * (choice_w + 30)
            rect = pygame.Rect(x, y_start, choice_w, choice_h)
            self.choice_rects.append(rect)
            self.original_choice_rects.append(rect.copy())

    def next_question(self):
        if self.is_answered:
            self.current_question_index += 1
            self.answered_questions_count += 1
            self.load_question()
        
    def check_player_collision(self, player_rect):
        # RESALTA la opción sobre la que está el jugador
        if self.is_answered or self.carried_choice_index != -1:
            self.highlighted_choice_index = -1
            return
            
        self.highlighted_choice_index = -1
        for i, rect in enumerate(self.choice_rects):
            if player_rect.colliderect(rect.inflate(10, 10)):
                if not (rect.width == 0 and rect.height == 0): # Asegura que no está ya recogida
                    self.highlighted_choice_index = i
                    break

    def handle_interaction(self, player_rect, keys, prefecta_rect):
        # 1. Lógica de RECOGER (Si está sobre una opción y presiona tecla)
        if self.carried_choice_index == -1 and not self.is_answered:
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                if self.highlighted_choice_index != -1:
                    self.carried_choice_index = self.highlighted_choice_index
                    
                    # La opción desaparece del suelo
                    self.choice_rects[self.carried_choice_index] = pygame.Rect(0,0,0,0)
                    self.carried_choice_rect = pygame.Rect(0,0,0,0)
                    self.highlighted_choice_index = -1
                    return "picked_up"
        
        # 2. Lógica de ENTREGAR (Si lleva algo, está cerca de la prefecta y presiona tecla)
        elif self.carried_choice_index != -1 and not self.is_answered:
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                if player_rect.colliderect(prefecta_rect.inflate(20, 20)):
                    is_correct = (self.carried_choice_index == self.correct_answer_index)
                    return self.process_delivery(is_correct)
        
        return None


    def update_carried_choice_position(self, player_center_x, player_top_y):
        if self.carried_choice_index != -1 and self.carried_choice_rect:
            choice_w = 180
            choice_h = 50
            self.carried_choice_rect.width = choice_w
            self.carried_choice_rect.height = choice_h
            self.carried_choice_rect.centerx = player_center_x
            self.carried_choice_rect.centery = player_top_y - choice_h // 2 - 10

    def process_delivery(self, is_correct):
        if self.is_answered:
            return 
        
        self.is_answered = True
        self.answer_result = "correct" if is_correct else "incorrect"
        
        self.carried_choice_index = -1
        self.carried_choice_rect = None
        
        # Si fue incorrecta, vuelve al suelo (todas las opciones vuelven)
        if not is_correct: 
            for i in range(len(self.original_choice_rects)):
                self.choice_rects[i] = self.original_choice_rects[i].copy()
        else: # Si fue correcta, desaparecen todas
            for i in range(len(self.choice_rects)):
                self.choice_rects[i] = pygame.Rect(0,0,0,0)
        
        if self.answered_questions_count + 1 == len(self.questions_data):
            return "finished"
        
        return self.answer_result
        
    def draw(self, surface, player_rect):
        if self.finished:
            return

        self._draw_text_centered(surface, self.question, self.font, (255, 255, 255), (self.size[0] // 2, 100))

        for i, rect in enumerate(self.choice_rects):
            if not (rect.width == 0 and rect.height == 0):
                color = (20, 50, 100)
                
                if i == self.highlighted_choice_index:
                    color = (255, 200, 0) # Opción resaltada lista para ser recogida
                elif self.is_answered and i == self.correct_answer_index:
                    color = (0, 100, 0)
                    
                pygame.draw.rect(surface, color, rect, border_radius=10)
                pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=10)
                self._draw_text_centered(surface, self.choices[i], self.font, (0,0,0) if i == self.highlighted_choice_index else (255, 255, 255), rect.center)
            
        if self.carried_choice_index != -1 and self.carried_choice_rect:
            color = (255, 200, 0) 
            pygame.draw.rect(surface, color, self.carried_choice_rect, border_radius=10)
            pygame.draw.rect(surface, (255, 255, 255), self.carried_choice_rect, 2, border_radius=10)
            self._draw_text_centered(surface, self.choices[self.carried_choice_index], self.font, (0, 0, 0), self.carried_choice_rect.center)
            

        if self.is_answered:
            feedback_text = ""
            if self.answer_result == "correct":
                feedback_text = "¡CORRECTO! Presiona ESPACIO para la siguiente pregunta."
            elif self.answer_result == "incorrect":
                feedback_text = "¡INCORRECTO! Presiona ESPACIO para la siguiente pregunta."
            
            if self.answered_questions_count == len(self.questions_data):
                 feedback_text = "¡QUIZ COMPLETO! Presiona ESPACIO para hablar con la Prefecta."

            self._draw_text_centered(surface, feedback_text, self.font, (255, 255, 255), (self.size[0] // 2, self.size[1] - 100))
            
        elif self.highlighted_choice_index != -1:
             pick_up_text = "Presiona ESPACIO/ENTER para RECOGER."
             self._draw_text_centered(surface, pick_up_text, self.font, (255, 200, 0), (self.size[0] // 2, self.size[1] - 100))


    def _draw_text_centered(self, surface, text, font, color, center_pos):
        lines = text.split('\n')
        line_height = font.get_height()
        y_offset = center_pos[1] - (len(lines) * line_height) // 2
        
        for line in lines:
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(center_pos[0], y_offset))
            surface.blit(text_surface, text_rect)
            y_offset += line_height