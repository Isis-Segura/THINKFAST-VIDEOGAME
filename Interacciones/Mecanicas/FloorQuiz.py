import pygame 
import random 
import os
# Definiciones de colores para usar en el dibujo
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255) # Azul Neón

# =======================================================
# FUNCIÓN AUXILIAR PARA OSCURECER COLORES (NUEVA)
# =======================================================
def _darken_color(color, factor=80):
    """Oscurece un color RGB dado un factor (0-255)."""
    return (max(0, color[0] - factor), 
            max(0, color[1] - factor), 
            max(0, color[2] - factor))

class FloorQuiz: 
    """ 
    Gestiona la lógica y el dibujo del minijuego de preguntas en el suelo. 
    """ 
    def __init__(self, size, questions, font): 
        self.size = size 
        self.questions = questions 
        self.font = font 
        self.current_question_index = 0 
        self.correct_answers = 0 
        self.finished = False 
        self.is_answered = False 
        self.selected_choice_index = -1 
        self.answer_result = None 

        # --- Dimensiones y Posiciones (Atributos de Instancia - CORREGIDOS) --- 
        
        self.PIXEL_RADIUS = 10  
        self.QUESTION_BOX_WIDTH = 800 
        self.QUESTION_BOX_HEIGHT = 100 
        self.QUESTION_BOX_RADIUS = 10 
        
        # Dimensiones de las opciones de respuesta (DEFINIDAS ANTES DEL SHUFFLE)
        self.CHOICE_WIDTH = 160 # AHORA ES UN ATRIBUTO de INSTANCIA
        self.IMAGE_HEIGHT = 80  # Altura dedicada a la imagen
        # Altura total de la caja de opción 
        self.CHOICE_HEIGHT = 160 
        
        self.start_x = (size[0] - self.QUESTION_BOX_WIDTH) // 2 
        # Posición de la caja de pregunta (ajustada a -490)
        self.start_y = size[1] - self.QUESTION_BOX_HEIGHT - 490  
        self.box_width = self.QUESTION_BOX_WIDTH 
        self.box_height = self.QUESTION_BOX_HEIGHT

    
        # 1. Definir las 4 posiciones (rectángulos) posibles de la cuadrícula 
        
        POS_0_X = 150 
        POS_0_Y = 290  
        POS_1_X = size[0] - 150 - self.CHOICE_WIDTH 
        POS_1_Y = 290  
        POS_2_X = 150 
        POS_2_Y = size[1] - 200  
        POS_3_X = size[0] - 150 - self.CHOICE_WIDTH 
        POS_3_Y = size[1] - 200 
        
        # Usamos los atributos de instancia self.CHOICE_WIDTH y self.CHOICE_HEIGHT
        choice_rects_template = [ 
            pygame.Rect(POS_0_X, POS_0_Y, self.CHOICE_WIDTH, self.CHOICE_HEIGHT),  
            pygame.Rect(POS_1_X, POS_1_Y, self.CHOICE_WIDTH, self.CHOICE_HEIGHT), 
            pygame.Rect(POS_2_X, POS_2_Y, self.CHOICE_WIDTH, self.CHOICE_HEIGHT),  
            pygame.Rect(POS_3_X, POS_3_Y, self.CHOICE_WIDTH, self.CHOICE_HEIGHT) 
        ]

        # 2. Definir los 4 colores (fijos)
        self.NEON_COLORS = [ 
            (0, 255, 0), # Verde Neón
            (255, 255, 0), # Amarillo Neón
            (0, 100, 255), # Azul Neón
            (255, 51, 255),  # Rosa Neón
        ] 
        
        # 3. ¡ALEATORIZAR LAS POSICIONES Y COLORES AL INICIO! 
        self.choice_rects = choice_rects_template 
        self.vivid_colors = self.NEON_COLORS  

        random.shuffle(self.choice_rects) 
        random.shuffle(self.vivid_colors) 
        
        # --- Colores de estado --- 
     
        self.QUESTION_BOX_BACKGROUND = (20, 30, 80)  
        self.QUESTION_BOX_BORDER = (255, 200, 0)  
        self.option_text_color_default = BLACK 
        self.selected_color = WHITE 
        self.correct_color_highlight = (0, 255, 0) 
        self.NEON_RED_ERROR = (255, 0, 0) 
        self.DIM_COLOR = (100, 30, 30) 
        
        
        # Cargar imágenes de las opciones
        self.choice_images = []
        for q in questions:
            question_images = []
            for choice in q["choices"]:
                try:
                    img_path = choice["image"] if isinstance(choice, dict) else "Materials/Pictures/Assets/imagen1.jpg"
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (self.CHOICE_WIDTH - 10, self.IMAGE_HEIGHT))
                    question_images.append(img)
                except:
                    fallback = pygame.Surface((self.CHOICE_WIDTH - 10, self.IMAGE_HEIGHT), pygame.SRCALPHA)
                    fallback.fill((100, 100, 100))
                    question_images.append(fallback)
            self.choice_images.append(question_images)
        self._choice_image_cache = {}
        
        self._shuffle_questions_choices() 


    def _shuffle_questions_choices(self): 
        """ 
        Mezcla las opciones (choices) de cada pregunta y actualiza el  
        índice de la respuesta correcta (correct_answer) para que coincida.
        """ 
        for q in self.questions: 
            choices = q["choices"] 
            correct_index = q["correct_answer"] 
            
            shufflable_items = [] 
            for i, choice in enumerate(choices): 
                is_correct = (i == correct_index) 
                shufflable_items.append((choice, is_correct)) 
            
            random.shuffle(shufflable_items) 
         
            new_choices = []
            new_correct_index = -1
            for i, (choice, is_correct) in enumerate(shufflable_items):
                new_choices.append(choice)
                if is_correct:
                    new_correct_index = i

            q["choices"] = new_choices
            q["correct_answer"] = new_correct_index

        self._reorder_choice_images()

    def _reorder_choice_images(self):
        """Reordena las imágenes cargadas para que coincida con el orden aleatorio de las opciones."""
        new_choice_images = []
        
        for q_index, q in enumerate(self.questions):
            question_images = []
            for choice in q["choices"]:
                try:
                    img_path = choice["image"] if isinstance(choice, dict) else "Materials/Pictures/Assets/imagen1.jpg"
                    
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (self.CHOICE_WIDTH - 10, self.IMAGE_HEIGHT))
                    question_images.append(img)

                except:
                    fallback = pygame.Surface((self.CHOICE_WIDTH - 10, self.IMAGE_HEIGHT), pygame.SRCALPHA)
                    fallback.fill((100, 100, 100))
                    question_images.append(fallback)
            new_choice_images.append(question_images)

        self.choice_images = new_choice_images


    def next_question(self): 
        """Avanza a la siguiente pregunta o finaliza el quiz.""" 
        if self.current_question_index < len(self.questions) - 1: 
            self.current_question_index += 1 
            self.is_answered = False 
            self.selected_choice_index = -1 
            self.answer_result = None 
        else: 
            self.finished = True 

    def check_player_collision(self, player_rect): 
        """ 
        Verifica si el jugador (player_rect) colisiona con alguna de las opciones 
        y actualiza la opción seleccionada. 
        """ 
        if self.is_answered: 
            return 

        current_selected = -1 
        for i, rect in enumerate(self.choice_rects): 
            if rect.colliderect(player_rect): 
                current_selected = i 
                break 
        
        if current_selected != self.selected_choice_index: 
            self.selected_choice_index = current_selected 


    def handle_event(self, event): 
        """ 
        Maneja el evento de contestar (tecla ESPACIO/ENTER). 
        """ 
        if self.finished or self.is_answered: 
            return None 

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN): 
            if self.selected_choice_index != -1: 
                return self.submit_answer() 
        return None 

    def submit_answer(self): 
        """Procesa la respuesta seleccionada.""" 
        self.is_answered = True 
        current_q = self.questions[self.current_question_index] 
        correct_index = current_q["correct_answer"] 
        
        if self.selected_choice_index == correct_index: 
            self.correct_answers += 1 
            self.answer_result = "correct" 
            return "correct" 
        else: 
            self.answer_result = "incorrect" 
            return "incorrect" 

    def draw(self, screen): 
        """Dibuja la pregunta, las opciones y el estado del quiz.""" 
        if self.finished: 
            return 

        current_q = self.questions[self.current_question_index] 
        question_text = current_q["question"].replace('\n', ' ') 
        choices = current_q["choices"] 
        correct_index = current_q["correct_answer"] 
        current_images = self.choice_images[self.current_question_index]


        # --- 1. Dibujo de la caja de pregunta inferior (Opaca) --- 
        question_box_rect = pygame.Rect(self.start_x, self.start_y, self.box_width, self.box_height) 
        pygame.draw.rect(screen, self.QUESTION_BOX_BACKGROUND, question_box_rect, border_radius=self.QUESTION_BOX_RADIUS) 
        pygame.draw.rect(screen, self.QUESTION_BOX_BORDER, question_box_rect, 5, border_radius=self.QUESTION_BOX_RADIUS) 

        # Dibujar pregunta: Centrado (Texto blanco) 
        try:
            text_surface = self.font.render(question_text, True, WHITE) 
            text_rect = text_surface.get_rect(center=(question_box_rect.centerx, question_box_rect.centery)) 
            screen.blit(text_surface, text_rect) 
        except:
            pass

        # --- 2. Dibujo de las 4 opciones de respuesta (en el suelo) --- 
        for i, rect in enumerate(self.choice_rects): 
            choice_dict = choices[i] 
            choice_text = choice_dict["text"].replace('\n', ' ') 

            # --- DIBUJO DE FONDO Y BORDE --- 
            draw_color = self.vivid_colors[i] 
            border_color = BLACK # Inicializar con valor por defecto
            border_thickness = 5 
            
            # --- LÓGICA DE COLOR DE ESTADO ---
            if self.is_answered: 
                if i == correct_index: 
                    # Respuesta correcta
                    draw_color = self.correct_color_highlight 
                    border_color = WHITE
                elif i == self.selected_choice_index and i != correct_index: 
                    # Respuesta seleccionada incorrecta 
                    draw_color = self.NEON_RED_ERROR 
                    border_color = WHITE
                else:
                    # Opciones incorrectas no seleccionadas (atenuar)
                    draw_color = self.DIM_COLOR
                    border_color = BLACK
            
            # --- LÓGICA DE COLOR NORMAL/HOVER (ANTES DE RESPONDER) ---
            else: 
                if i == self.selected_choice_index: 
                    # ESTADO SELECCIONADO (Hover)
                    # 1. Ajustar el color del fondo (más claro)
                    selected_draw_color = (min(255, draw_color[0] + 50), min(255, draw_color[1] + 50), min(255, draw_color[2] + 50))
                    # 2. El borde será del mismo color CLARO para un efecto sutil
                    border_color = selected_draw_color
                else:
                    # ESTADO NORMAL (No seleccionado)
                    # El borde será el color base, pero oscurecido
                    border_color = _darken_color(draw_color, factor=80) 
                    
            # Dibuja la caja de opción con el color de estado
            surface = pygame.Surface((rect.width, rect.height)) 
            
            # Rellenar con el color de fondo (usando el color más claro si está en hover)
            if i == self.selected_choice_index and not self.is_answered: 
                surface.fill(selected_draw_color) 
            else:
                surface.fill(draw_color) 
            
            # Dibuja el borde con el color dinámico
            pygame.draw.rect(surface, border_color, (0, 0, rect.width, rect.height), border_thickness, border_radius=self.PIXEL_RADIUS) 
            screen.blit(surface, rect.topleft) 
            
            # --- DIBUJAR TEXTO DE LA OPCIÓN (siempre negro) ---
            choice_text_surface = self.font.render(choice_text, True, self.option_text_color_default) 
            choice_text_rect = choice_text_surface.get_rect(center=(rect.centerx, rect.top + 30)) 
            screen.blit(choice_text_surface, choice_text_rect.topleft) 
            
            # --- DIBUJAR IMAGEN DEBAJO DEL TEXTO ---
            image_rect_pos = current_images[i].get_rect()
            image_rect_pos.center = (rect.centerx, rect.top + 30 + self.IMAGE_HEIGHT // 2 + 10) 
            try:
                screen.blit(current_images[i], image_rect_pos.topleft) 
            except:
                pass
            
        # --- 3. Mensajes de estado (inferior derecho) --- 
        if self.is_answered: 
            if self.answer_result == "correct": 
                msg = "¡Correcto! (Presiona ESPACIO para avanzar)" 
                color = self.correct_color_highlight 
            else: 
                correct_choice_text = choices[correct_index]["text"] if isinstance(choices[correct_index], dict) else choices[correct_index]
                correct_choice = correct_choice_text.replace('\n', ' ') 
                msg = f"¡Mal! La correcta era: {correct_choice} (ESPACIO para avanzar)" 
                color = self.NEON_RED_ERROR 
        
            msg_surface = self.font.render(msg, True, color) 
            msg_rect = msg_surface.get_rect(bottomright=(question_box_rect.right - 10, question_box_rect.bottom - 10)) 
            screen.blit(msg_surface, msg_rect) 
        
        elif self.selected_choice_index != -1: 
            msg = "Presiona ESPACIO para contestar." 
            msg_surface = self.font.render(msg, True, WHITE)
            msg_rect = msg_surface.get_rect(bottomright=(question_box_rect.right - 10, question_box_rect.bottom - 10))
            screen.blit(msg_surface, msg_rect)