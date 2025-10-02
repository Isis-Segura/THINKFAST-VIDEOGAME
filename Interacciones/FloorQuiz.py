import pygame  # <--- ¡CORRECCIÓN CLAVE: Agregando la importación de pygame!
import math
# NOTA: Asegúrate de que este archivo no tiene la definición de la clase Timer, 
# ya que el error indicaba que FloorQuiz.py no tenía 'import pygame'.

class FloorQuiz:
    def __init__(self, screen_size, questions, font):
        self.screen_size = screen_size
        self.questions = questions
        self.font = font
        self.current_question_index = 0
        self.selected_choice_index = -1
        self.finished = False
        self.correct_answers = 0
        self.wrong_answers = 0
        self.is_answered = False 
        self.answer_result = None
        
        self.option_text_color = (0, 0, 0) 
        self.vivid_colors = [
             (255, 105, 180), (50, 200, 255), (255, 255, 0), (255, 140, 0), 
        ]
        self.selected_color = (0, 255, 0) 
        self.correct_color = (0, 180, 0) 
        self.incorrect_color = (180, 0, 0) 
        
        self.box_width = int(screen_size[0] * 0.9)
        self.box_height = 80
        self.start_x = (screen_size[0] - self.box_width) // 2
        self.start_y = screen_size[1] - self.box_height - 30
        
        CHOICE_WIDTH = 150 
        CHOICE_HEIGHT = 60 
        POS_0_X = 150
        POS_0_Y = 370
        POS_1_X = screen_size[0] - 150 - CHOICE_WIDTH
        POS_1_Y = 370
        POS_2_X = 150
        POS_2_Y = screen_size[1] - 180
        POS_3_X = screen_size[0] - 150 - CHOICE_WIDTH
        POS_3_Y = screen_size[1] - 180
        
        self.choice_positions = [
            (POS_0_X, POS_0_Y), (POS_1_X, POS_1_Y), 
            (POS_2_X, POS_2_Y), (POS_3_X, POS_3_Y)
        ]
        
        self.choice_rects = []
        for x, y in self.choice_positions:
            rect = pygame.Rect(x, y, CHOICE_WIDTH, CHOICE_HEIGHT)
            self.choice_rects.append(rect)

    def check_player_collision(self, player_rect):
        if self.finished or self.is_answered:
            self.selected_choice_index = -1
            return -1
        
        for i, rect in enumerate(self.choice_rects):
            if player_rect.colliderect(rect): 
                self.selected_choice_index = i
                return i
            
        self.selected_choice_index = -1
        return -1

    # CORRECCIÓN CLAVE: Permite el segundo ESPACIO para avanzar
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            
            # 1. Si NO está contestada, la contesta
            if not self.is_answered and self.selected_choice_index != -1:
                return self.check_answer() # Devuelve 'correct' o 'incorrect'
            
            # 2. Si YA está contestada, permite el avance a la siguiente pregunta
            elif self.is_answered: 
                return self.advance_question() # Devuelve 'advanced' o 'finished'
                
        return None

    def check_answer(self):
        current_q = self.questions[self.current_question_index]
        correct_index = current_q["correct_answer"]
        self.is_answered = True
        if self.selected_choice_index == correct_index:
            self.correct_answers += 1
            self.answer_result = "correct"
        else:
            self.wrong_answers += 1
            self.answer_result = "incorrect"
        return self.answer_result

    def advance_question(self):
        self.is_answered = False
        self.selected_choice_index = -1
        self.answer_result = None
        self.current_question_index += 1
        if self.current_question_index >= len(self.questions):
            self.finished = True
            return "finished"
        return "advanced"

    def draw(self, screen):
        if self.finished:
            return

        current_q = self.questions[self.current_question_index]
        question_text = current_q["question"]
        choices = current_q["choices"]
        correct_index = current_q["correct_answer"]
        
        question_box_rect = pygame.Rect(self.start_x, self.start_y, self.box_width, self.box_height)
        pygame.draw.rect(screen, (0, 0, 0), question_box_rect) 
        pygame.draw.rect(screen, (255, 255, 255), question_box_rect, 3) 
        text_surface = self.font.render(question_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(midleft=(question_box_rect.x + 20, question_box_rect.centery))
        screen.blit(text_surface, text_rect)
        
        for i, choice in enumerate(choices):
            rect = self.choice_rects[i]
            
            color_index = i % len(self.vivid_colors)
            color = self.vivid_colors[color_index]
            border_color = (20, 20, 20)
            border_thickness = 3
            
            if self.is_answered:
                if i == correct_index:
                    color = self.correct_color
                    border_color = (255, 255, 255)
                    border_thickness = 5
                elif i == self.selected_choice_index:
                    color = self.incorrect_color
                    border_color = (255, 255, 255)
                    border_thickness = 5
            elif i == self.selected_choice_index:
                border_color = self.selected_color
                border_thickness = 5
                
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, border_color, rect, border_thickness)
            
            choice_surface = self.font.render(choice, True, self.option_text_color) 
            choice_rect = choice_surface.get_rect(center=rect.center)
            screen.blit(choice_surface, choice_rect)
            
        if self.is_answered:
            # Texto para avisar que se presione ESPACIO para avanzar
            msg = "¡Correcto! (Presiona ESPACIO para avanzar)" if self.answer_result == "correct" else "¡Incorrecto! (Presiona ESPACIO para avanzar)"
            if self.answer_result == "incorrect":
                correct_choice = choices[correct_index]
                msg = f"¡Mal! La correcta era: {correct_choice} (Presiona ESPACIO para avanzar)"
            
            msg_surface = self.font.render(msg, True, (255, 255, 0))
            msg_rect = msg_surface.get_rect(bottomright=(question_box_rect.right - 10, question_box_rect.bottom - 10))
            screen.blit(msg_surface, msg_rect)
            
        elif self.selected_choice_index != -1:
            msg = "Presiona ESPACIO para contestar."
            msg_surface = self.font.render(msg, True, self.selected_color)
            msg_rect = msg_surface.get_rect(bottomright=(question_box_rect.right - 10, question_box_rect.bottom - 10))
            screen.blit(msg_surface, msg_rect)