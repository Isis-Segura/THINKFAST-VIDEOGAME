import pygame
import os

class FloorQuiz_KeyAndCarry:
    def __init__(self, size, questions, font_question, dialog_box_img=None, dialog_box_rect=None, dialog_img_loaded=False):
        self.size = size
        self.questions = questions
        self.font_question = font_question 
        self.current_question_index = 0
        self.max_questions = len(questions)
        self.finished = False
        self.choice_rects = []
        self.highlighted_choice_index = -1
        self.carried_choice_index = -1
        self.player_is_near_npc = False
        self.is_answered = False
        self.answer_result = None

        self.dialog_box_img_template = dialog_box_img
        self.dialog_box_rect_template = dialog_box_rect
        self._dialog_img_loaded = dialog_img_loaded

        # Propiedades para la caja de la pregunta
        self.question_box_img = None
        self.question_box_rect = None
        self._setup_question_box_display()

        # Propiedades para la opción cargada
        self.carried_choice_box_img = None
        self.carried_choice_box_rect = pygame.Rect(0, 0, 150, 40)

        # Configuración visual de las opciones en el suelo
        # ------------------- CAMBIO AQUÍ -------------------
        # Se define Blanco Puro (255, 255, 255) para las 4 opciones
        self.choice_colors = [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)]
        # ---------------------------------------------------
        self.highlight_color = (255, 255, 0)
        self.choice_font_color = (0, 0, 0) # El texto sigue siendo negro para contraste
        self.question_font_color = (255, 255, 255)

        self.choice_images = []
        self._load_choice_images()
        
        self._setup_question_layout() 

    def _load_choice_images(self):
        """Carga solo las imágenes de las opciones al inicio."""
        C_IMG_SIZE = (80, 80)
        self.choice_images = []

        for q_index, question_data in enumerate(self.questions):
            current_q_images = []
            for choice_data in question_data["choices"]:
                c_path = choice_data.get("image")
                loaded_img = None
                
                if c_path and os.path.exists(c_path):
                    try:
                        c_img = pygame.image.load(c_path).convert_alpha()
                        loaded_img = pygame.transform.scale(c_img, C_IMG_SIZE)
                    except pygame.error as e:
                        print(f"Error al cargar imagen de la opción '{c_path}': {e}")
                
                current_q_images.append(loaded_img)
            self.choice_images.append(current_q_images)

    def _setup_question_box_display(self):
        if self._dialog_img_loaded and self.dialog_box_img_template:
            desired_width = 600
            desired_height = 80
            self.question_box_img = pygame.transform.scale(self.dialog_box_img_template, (desired_width, desired_height))
            self.question_box_rect = self.question_box_img.get_rect(center=(self.size[0] // 2, 150))
        else:
            self.question_box_img = pygame.Surface((600, 80), pygame.SRCALPHA)
            self.question_box_img.fill((20, 30, 80, 180)) 
            pygame.draw.rect(self.question_box_img, (255, 200, 0), self.question_box_img.get_rect(), 3, border_radius=10)
            self.question_box_rect = self.question_box_img.get_rect(center=(self.size[0] // 2, 150))

    def _setup_question_layout(self):
        self.choice_rects = []
        current_q = self.questions[self.current_question_index]
        choices = current_q["choices"]
        
        start_y = self.size[1] - 130
        choice_box_height = 100
        
        max_choice_width = 0
        choice_text_surfaces = [self.font_question.render(choice["text"], True, self.choice_font_color) for choice in choices]
        for surf in choice_text_surfaces:
            max_choice_width = max(max_choice_width, surf.get_width(), 90)

        choice_box_width = max_choice_width + 40
        
        total_width = len(choices) * choice_box_width + (len(choices) - 1) * 20 
        x_start = (self.size[0] - total_width) // 2

        for i in range(len(choices)):
            x = x_start + i * (choice_box_width + 20)
            rect = pygame.Rect(x, start_y, choice_box_width, choice_box_height)
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
            self._setup_question_layout()
        else:
            self.finished = True
        
    def update_carried_choice_position(self, player_center_x, player_top_y):
        self.carried_choice_box_rect.centerx = player_center_x + self.carried_choice_box_rect.width // 2 + 10
        self.carried_choice_box_rect.centery = player_top_y + (self.carried_choice_box_rect.height // 2) + 20
        
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

    def _wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line: 
                    lines.append(' '.join(current_line))
                current_line = [word] 
        
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines

    def _draw_text_with_border(self, surface, text, font, text_color, outline_color, center_pos, border_offset=1):
        outline_surface = font.render(text, True, outline_color)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=center_pos)
        
        for dx in [-border_offset, 0, border_offset]:
            for dy in [-border_offset, 0, border_offset]:
                if dx != 0 or dy != 0: 
                    surface.blit(outline_surface, (text_rect.x + dx, text_rect.y + dy))

        surface.blit(text_surface, text_rect)


    def draw(self, surface, player_rect):
        
        # 1. DIBUJAR CAJA DE LA PREGUNTA
        question_text = self.questions[self.current_question_index]["question"]
        
        if self.question_box_img and self.question_box_rect:
            surface.blit(self.question_box_img, self.question_box_rect.topleft)
            
            padding_x = 20
            text_display_rect = self.question_box_rect.inflate(-padding_x * 2, 0)
            wrapped_lines = self._wrap_text(question_text, self.font_question, text_display_rect.width)
            line_height = self.font_question.get_height()
            total_text_height = len(wrapped_lines) * line_height
            start_y = self.question_box_rect.centery - (total_text_height // 2)
            
            current_y = start_y
            for line in wrapped_lines:
                text_surface = self.font_question.render(line, True, self.question_font_color)
                text_rect = text_surface.get_rect(centerx=self.question_box_rect.centerx, top=current_y)
                surface.blit(text_surface, text_rect)
                current_y += line_height

        # 2. DIBUJAR OPCIONES EN EL SUELO (Incluyendo imágenes)
        if self.carried_choice_index == -1: 
            current_choice_images = self.choice_images[self.current_question_index]
            
            for i, rect in enumerate(self.choice_rects):
                
                choice_text = self.questions[self.current_question_index]["choices"][i]["text"]
                
                # Se utiliza el color blanco definido en __init__
                color = self.choice_colors[i]
                
                # Resaltar (se mantiene amarillo)
                if i == self.highlighted_choice_index:
                    pygame.draw.rect(surface, self.highlight_color, rect.inflate(10, 10), border_radius=5)
                    
                # Dibujar recuadro de opción
                pygame.draw.rect(surface, color, rect, border_radius=5)
                
                # DIBUJAR IMAGEN DE OPCIÓN
                choice_img = current_choice_images[i]
                if choice_img:
                    img_rect = choice_img.get_rect(centerx=rect.centerx, top=rect.top + 5)
                    surface.blit(choice_img, img_rect.topleft)
                
                # DIBUJAR TEXTO DE OPCIÓN
                text_surface = self.font_question.render(choice_text, True, self.choice_font_color)
                text_rect = text_surface.get_rect(centerx=rect.centerx, bottom=rect.bottom - 5)
                surface.blit(text_surface, text_rect)
                
                # DIBUJAR MENSAJE DE RECOGER CON BORDE
                if i == self.highlighted_choice_index and not self.is_answered:
                    prompt_text = "Presiona ESPACIO/ENTER para RECOGER."
                    
                    prompt_center_pos = (rect.centerx, rect.top - 35) 
                    
                    self._draw_text_with_border(
                        surface, 
                        prompt_text, 
                        self.font_question, 
                        (255, 255, 255),  
                        (0, 0, 0),        
                        prompt_center_pos,
                        border_offset=1
                    )

        # 3. DIBUJAR RESULTADO TEMPORAL CON BORDE 
        if self.is_answered:
            if self.answer_result == "correct":
                message = "¡CORRECTO! Pulsa ESPACIO para seguir."
                msg_color = (0, 255, 0) 
            else:
                message = "INCORRECTO. Pulsa ESPACIO para seguir."
                msg_color = (255, 0, 0) 
            
            msg_center_pos = (self.size[0] // 2, self.size[1] - 150)
            
            self._draw_text_with_border(
                surface, 
                message, 
                self.font_question, 
                msg_color,        
                (0, 0, 0),        
                msg_center_pos,
                border_offset=1
            )


        # 4. DIBUJAR OPCIÓN CARGADA
        if self.carried_choice_index != -1 and not self.is_answered:
            choice_index = self.carried_choice_index
            choice_text = self.questions[self.current_question_index]["choices"][choice_index]["text"]
            
            temp_text_surface = self.font_question.render(choice_text, True, (0,0,0))
            current_box_width = temp_text_surface.get_width() + 20 
            current_box_height = temp_text_surface.get_height() + 10 
            
            carried_box_surface = pygame.Surface((current_box_width, current_box_height), pygame.SRCALPHA)
            carried_box_surface.fill((30, 30, 100, 180)) 
            pygame.draw.rect(carried_box_surface, (255, 255, 0), carried_box_surface.get_rect(), 2, border_radius=5) 
            
            text_surface = self.font_question.render(choice_text, True, (255, 255, 255)) 
            text_rect = text_surface.get_rect(center=(carried_box_surface.get_width() // 2, carried_box_surface.get_height() // 2))
            carried_box_surface.blit(text_surface, text_rect)
            
            carried_box_rect_on_screen = carried_box_surface.get_rect(center=(self.carried_choice_box_rect.centerx, self.carried_choice_box_rect.centery))
            surface.blit(carried_box_surface, carried_box_rect_on_screen)