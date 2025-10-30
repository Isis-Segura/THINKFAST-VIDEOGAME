import pygame
import os

class FloorQuiz_KeyAndCarry:
    def __init__(self, size, questions, font_question, dialog_box_img=None, dialog_box_rect=None, dialog_img_loaded=False):
        self.size = size
        self.questions = questions
        self.font_question = font_question # Se usará para las opciones y la pregunta
        self.current_question_index = 0
        self.max_questions = len(questions)
        self.finished = False
        self.choice_rects = []
        self.highlighted_choice_index = -1
        self.carried_choice_index = -1
        self.player_is_near_npc = False
        self.is_answered = False
        self.answer_result = None

        # Elementos de diálogo pasados desde Level2 para la pregunta y el objeto cargado
        self.dialog_box_img_template = dialog_box_img # La imagen completa de la caja de diálogo
        self.dialog_box_rect_template = dialog_box_rect # El rect de la caja de diálogo de Level2
        self._dialog_img_loaded = dialog_img_loaded

        # Propiedades para la caja de la pregunta
        self.question_box_img = None
        self.question_box_rect = None
        self._setup_question_box_display() # Configura la caja de diálogo para la pregunta

        # Propiedades para la opción cargada (un pequeño recuadro)
        self.carried_choice_box_img = None
        self.carried_choice_box_rect = pygame.Rect(0, 0, 150, 40) # Un tamaño base, se ajustará el texto

        # Configuración visual de las opciones en el suelo
        self.choice_colors = [(255, 255, 255), (200, 200, 200), (150, 150, 150), (100, 100, 100)]
        self.highlight_color = (255, 255, 0)
        self.choice_font_color = (0, 0, 0)
        self.question_font_color = (255, 255, 255) # Para el texto de la pregunta

        self._setup_question_layout() # Elimina la carga de la imagen de la pregunta aquí

    def _setup_question_box_display(self):
        # Crear una caja de diálogo para la pregunta, más pequeña que la principal
        if self._dialog_img_loaded and self.dialog_box_img_template:
            # Usar una porción o escalar la imagen de diálogo existente
            # Si la imagen es muy grande, podríamos recortar una parte central o escalar
            # Para simplificar, escalaremos una copia de la imagen base a un tamaño de pregunta más adecuado.
            desired_width = 600
            desired_height = 80
            self.question_box_img = pygame.transform.scale(self.dialog_box_img_template, (desired_width, desired_height))
            self.question_box_rect = self.question_box_img.get_rect(center=(self.size[0] // 2, 80))
        else:
            # Cuadro de texto de fallback si no hay imagen
            self.question_box_img = pygame.Surface((600, 80), pygame.SRCALPHA)
            self.question_box_img.fill((20, 30, 80, 180)) # Color con transparencia
            pygame.draw.rect(self.question_box_img, (255, 200, 0), self.question_box_img.get_rect(), 3, border_radius=10)
            self.question_box_rect = self.question_box_img.get_rect(center=(self.size[0] // 2, 80))

    # Eliminamos _load_question_image ya que no usaremos la imagen de la pregunta

    def _setup_question_layout(self):
        self.choice_rects = []
        current_q = self.questions[self.current_question_index]
        choices = current_q["choices"]
        
        start_y = self.size[1] - 150
        max_choice_width = 0

        # Primero renderizamos todas las opciones para calcular el ancho máximo
        choice_text_surfaces = [self.font_question.render(choice, True, self.choice_font_color) for choice in choices]
        for surf in choice_text_surfaces:
            max_choice_width = max(max_choice_width, surf.get_width())

        choice_box_width = max_choice_width + 40 # Padding
        
        # Calcular ancho total para centrar
        total_width = len(choices) * choice_box_width + (len(choices) - 1) * 20 
        x_start = (self.size[0] - total_width) // 2

        for i in range(len(choices)):
            x = x_start + i * (choice_box_width + 20)
            y = start_y
            rect = pygame.Rect(x, y, choice_box_width, 40)
            self.choice_rects.append(rect)
        
        self.highlighted_choice_index = -1
        self.carried_choice_index = -1
        self.is_answered = False
        self.answer_result = None

    def check_player_collision(self, player_rect):
        if self.is_answered or self.carried_choice_index != -1:
            self.highlighted_choice_index = -1
            return
            
        near_index = -1
        for i, rect in enumerate(self.choice_rects):
            if player_rect.colliderect(rect.inflate(20, 20)):
                near_index = i
                break
        self.highlighted_choice_index = near_index
        
    def next_question(self):
        if self.current_question_index < self.max_questions - 1:
            self.current_question_index += 1
            # self._load_question_image() # Ya no es necesario
            self._setup_question_layout()
        else:
            self.finished = True
        
    def update_carried_choice_position(self, player_center_x, player_top_y):
        # Actualizamos la posición del recuadro de la opción cargada
        self.carried_choice_box_rect.centerx = player_center_x + self.carried_choice_box_rect.width // 2 + 10 # Derecha del jugador
        self.carried_choice_box_rect.centery = player_top_y + (self.carried_choice_box_rect.height // 2) + 20 # Un poco más abajo que la cabeza
        
    def handle_interaction_input(self, player_rect, npc_rect):
        if self.finished or self.is_answered:
            return None

        # 1. ENTREGA (DROP)
        if self.carried_choice_index != -1:
            drop_zone = npc_rect.inflate(40, 40)
            if player_rect.colliderect(drop_zone):
                
                is_correct = (self.carried_choice_index == self.questions[self.current_question_index]["correct_answer"])
                self.is_answered = True
                self.answer_result = "correct" if is_correct else "incorrect"
                self.carried_choice_index = -1
                self.highlighted_choice_index = -1

                if self.current_question_index == self.max_questions - 1:
                    return "finished"
                else:
                    return self.answer_result

        # 2. RECOGER (PICK UP)
        elif self.highlighted_choice_index != -1:
            self.carried_choice_index = self.highlighted_choice_index
            self.highlighted_choice_index = -1
            return "picked_up"
            
        return None

    def draw(self, surface, player_rect):
        # 1. DIBUJAR CAJA DE LA PREGUNTA
        question_text = self.questions[self.current_question_index]["question"]
        
        # Dibujar la imagen de la caja de la pregunta
        if self.question_box_img and self.question_box_rect:
            surface.blit(self.question_box_img, self.question_box_rect.topleft)
            
            # Dibujar el texto de la pregunta centrado en la caja
            text_surface = self.font_question.render(question_text, True, self.question_font_color)
            text_rect = text_surface.get_rect(center=self.question_box_rect.center)
            surface.blit(text_surface, text_rect)
        else:
            # Fallback si no hay imagen de caja (ya configurado en _setup_question_box_display)
            pass 

        # 2. DIBUJAR OPCIONES EN EL SUELO
        if self.carried_choice_index == -1: # Solo se dibujan si no estamos llevando una
            for i, rect in enumerate(self.choice_rects):
                choice_text = self.questions[self.current_question_index]["choices"][i]
                color = self.choice_colors[i]
                
                if i == self.highlighted_choice_index:
                    pygame.draw.rect(surface, self.highlight_color, rect.inflate(10, 10), border_radius=5)
                    
                pygame.draw.rect(surface, color, rect, border_radius=5)
                
                text_surface = self.font_question.render(choice_text, True, self.choice_font_color)
                text_rect = text_surface.get_rect(center=rect.center)
                surface.blit(text_surface, text_rect)
                
                if i == self.highlighted_choice_index and not self.is_answered:
                    prompt_text = "Presiona ESPACIO/ENTER para RECOGER."
                    prompt_surface = self.font_question.render(prompt_text, True, (255, 255, 255))
                    prompt_rect = prompt_surface.get_rect(center=(rect.centerx, rect.top - 20))
                    surface.blit(prompt_surface, prompt_rect)

        # 3. DIBUJAR RESULTADO TEMPORAL
        if self.is_answered:
            if self.answer_result == "correct":
                message = "¡CORRECTO! Pulsa ESPACIO para seguir."
                msg_color = (0, 255, 0)
            else:
                message = "INCORRECTO. Pulsa ESPACIO para seguir."
                msg_color = (255, 0, 0)
            
            msg_surface = self.font_question.render(message, True, msg_color)
            msg_rect = msg_surface.get_rect(center=(self.size[0] // 2, self.size[1] - 70))
            surface.blit(msg_surface, msg_rect)

        # 4. DIBUJAR OPCIÓN CARGADA (ESTILO SUTIL SIGUIENDO AL JUGADOR)
        if self.carried_choice_index != -1 and not self.is_answered:
            choice_index = self.carried_choice_index
            choice_text = self.questions[self.current_question_index]["choices"][choice_index]
            
            # Ajustar el tamaño del recuadro según el texto
            temp_text_surface = self.font_question.render(choice_text, True, (0,0,0)) # Renderizar para medir
            current_box_width = temp_text_surface.get_width() + 20 # Padding
            current_box_height = temp_text_surface.get_height() + 10 # Padding
            
            # Crear o redimensionar el Surface para la caja del carried choice
            carried_box_surface = pygame.Surface((current_box_width, current_box_height), pygame.SRCALPHA)
            carried_box_surface.fill((30, 30, 100, 180)) # Un azul oscuro semi-transparente
            pygame.draw.rect(carried_box_surface, (255, 255, 0), carried_box_surface.get_rect(), 2, border_radius=5) # Borde amarillo
            
            # Dibujar el texto centrado en este nuevo Surface
            text_surface = self.font_question.render(choice_text, True, (255, 255, 255)) # Texto blanco
            text_rect = text_surface.get_rect(center=(carried_box_surface.get_width() // 2, carried_box_surface.get_height() // 2))
            carried_box_surface.blit(text_surface, text_rect)
            
            # Dibujar el surface del recuadro en la pantalla, en la posición del jugador
            carried_box_rect_on_screen = carried_box_surface.get_rect(center=(self.carried_choice_box_rect.centerx, self.carried_choice_box_rect.centery))
            surface.blit(carried_box_surface, carried_box_rect_on_screen)