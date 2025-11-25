import pygame 
import random 
import os
from Interacciones.Controldeobjetos.timer import Timer

# Definiciones de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255) 

DARK_GREEN = (0, 100, 0) 

def _darken_color(color, factor=80):
    return (max(0, color[0] - factor), 
            max(0, color[1] - factor), 
            max(0, color[2] - factor))

def _draw_text_outline(surface, text, font, color, outline_color, x, y, outline_thickness=2):
    for dx, dy in [(-outline_thickness, 0), (outline_thickness, 0), (0, -outline_thickness), (0, outline_thickness)]:
        outline_surface = font.render(text, True, outline_color)
        surface.blit(outline_surface, (x + dx, y + dy))
    
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))


class FloorQuiz: 
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
        
        # Temporizador para retrasar la aparición de las opciones
        self.options_reveal_timer = Timer(1.5) 
        self.options_reveal_timer.start() 

        # --- Variables para la animación de fade-in de las opciones ---
        self.choice_alpha = 0              
        self.fade_in_speed = 15            
        self.fade_in_finished = False      

        # --- Dimensiones y Posiciones --- 
        self.choice_corner_radius = 20 # <--- Mantenemos el valor para redondeado
        self.choice_border_thickness = 0 

        self.PIXEL_RADIUS = 10  
        self.QUESTION_BOX_WIDTH = 800 
        self.QUESTION_BOX_HEIGHT = 100 
        self.QUESTION_BOX_RADIUS = 10 
        
        self.CHOICE_WIDTH = 160 
        self.IMAGE_HEIGHT = 80  
        self.CHOICE_HEIGHT = 160 
        
        self.start_x = (size[0] - self.QUESTION_BOX_WIDTH) // 2 
        self.start_y = size[1] - self.QUESTION_BOX_HEIGHT - 490  
        self.box_width = self.QUESTION_BOX_WIDTH 
        self.box_height = self.QUESTION_BOX_HEIGHT

    
        POS_0_X = 150 
        POS_0_Y = 290  
        POS_1_X = size[0] - 150 - self.CHOICE_WIDTH 
        POS_1_Y = 290  
        POS_2_X = 150 
        POS_2_Y = size[1] - 200  
        POS_3_X = size[0] - 150 - self.CHOICE_WIDTH 
        POS_3_Y = size[1] - 200 
        
        choice_rects_template = [ 
            pygame.Rect(POS_0_X, POS_0_Y, self.CHOICE_WIDTH, self.CHOICE_HEIGHT),  
            pygame.Rect(POS_1_X, POS_1_Y, self.CHOICE_WIDTH, self.CHOICE_HEIGHT), 
            pygame.Rect(POS_2_X, POS_2_Y, self.CHOICE_WIDTH, self.CHOICE_HEIGHT),  
            pygame.Rect(POS_3_X, POS_3_Y, self.CHOICE_WIDTH, self.CHOICE_HEIGHT) 
        ]

        self.NEON_COLORS = [ 
            (255, 255, 255), 
            (255, 255, 255), 
            (255, 255, 255), 
            (255, 255, 255),  
        ] 
        
        self.choice_rects = choice_rects_template 
        self.vivid_colors = self.NEON_COLORS  

        random.shuffle(self.choice_rects) 
        random.shuffle(self.vivid_colors) 
        
        # --- Colores de estado --- 
        self.QUESTION_BOX_BACKGROUND = (255, 255, 255)  
        self.QUESTION_BOX_BORDER = (71, 52, 41)  
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
                    img_path = choice["image"] if isinstance(choice, dict) and "image" in choice else "Materials/Pictures/Assets/imagen1.jpg"
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (self.CHOICE_WIDTH - 10, self.IMAGE_HEIGHT))
                    question_images.append(img)
                except Exception:
                    fallback = pygame.Surface((self.CHOICE_WIDTH - 10, self.IMAGE_HEIGHT), pygame.SRCALPHA)
                    fallback.fill((100, 100, 100))
                    question_images.append(fallback)
            self.choice_images.append(question_images)
        self._choice_image_cache = {}
        
        self._shuffle_questions_choices() 


    def _shuffle_questions_choices(self): 
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
        new_choice_images = []
        
        for q_index, q in enumerate(self.questions):
            question_images = []
            for choice in q["choices"]:
                try:
                    img_path = choice["image"] if isinstance(choice, dict) and "image" in choice else "Materials/Pictures/Assets/imagen1.jpg"
                    
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (self.CHOICE_WIDTH - 10, self.IMAGE_HEIGHT))
                    question_images.append(img)

                except Exception:
                    fallback = pygame.Surface((self.CHOICE_WIDTH - 10, self.IMAGE_HEIGHT), pygame.SRCALPHA)
                    fallback.fill((100, 100, 100))
                    question_images.append(fallback)
            new_choice_images.append(question_images)

        self.choice_images = new_choice_images


    def next_question(self): 
        if self.current_question_index < len(self.questions) - 1: 
            self.current_question_index += 1 
            self.is_answered = False 
            self.selected_choice_index = -1 
            self.answer_result = None 
            
            # Reinicia el temporizador de revelado y el estado de fade-in para la nueva pregunta
            self.options_reveal_timer.reset()
            self.options_reveal_timer.start()
            self.choice_alpha = 0
            self.fade_in_finished = False
        else: 
            self.finished = True 

    def update(self):
        # Actualiza el temporizador de retraso
        if self.options_reveal_timer.is_running():
            self.options_reveal_timer.update()
        
        # --- Lógica de Fade-in ---
        # Solo ejecuta el fade-in si el retraso terminó, el quiz NO ha sido respondido, 
        # y la animación aún no ha terminado.
        if self.options_reveal_timer.finished and not self.is_answered and not self.fade_in_finished:
            self.choice_alpha += self.fade_in_speed
            if self.choice_alpha >= 255:
                self.choice_alpha = 255
                self.fade_in_finished = True 
        
        # Solo reseteamos la opacidad si el retraso NO ha terminado, es decir, antes de que aparezcan por primera vez.
        if not self.options_reveal_timer.finished:
            self.choice_alpha = 0
            self.fade_in_finished = False


    def check_player_collision(self, player_rect): 
        # Solo permite la colisión si las opciones ya fueron reveladas Y el fade-in terminó
        if self.is_answered or not self.fade_in_finished:
            return 

        current_selected = -1 
        for i, rect in enumerate(self.choice_rects): 
            if rect.colliderect(player_rect): 
                current_selected = i 
                break 
        
        if current_selected != self.selected_choice_index: 
            self.selected_choice_index = current_selected 


    def handle_event(self, event): 
        # Solo permite responder si las opciones ya fueron reveladas Y el fade-in terminó
        if self.finished or self.is_answered or not self.fade_in_finished:
            return None 

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN): 
            if self.selected_choice_index != -1: 
                return self.submit_answer() 
        return None 

    def submit_answer(self): 
        self.is_answered = True 
        current_q = self.questions[self.current_question_index] 
        correct_index = current_q["correct_answer"] 
        
        # Al contestar, forzamos la opacidad al máximo (255) para asegurar el feedback
        self.choice_alpha = 255 
        
        if self.selected_choice_index == correct_index: 
            self.correct_answers += 1 
            self.answer_result = "correct" 
            return "correct" 
        else: 
            self.answer_result = "incorrect" 
            return "incorrect" 

    def draw(self, screen): 
        if self.finished: 
            return 

        current_q = self.questions[self.current_question_index] 
        question_text = current_q["question"].replace('\n', ' ') 
        choices = current_q["choices"] 
        
        correct_index = current_q["correct_answer"] 
        current_images = self.choice_images[self.current_question_index]

        # --- 1. Dibujo de la caja de pregunta inferior --- 
        question_box_rect = pygame.Rect(self.start_x, self.start_y, self.box_width, self.box_height) 
        pygame.draw.rect(screen, self.QUESTION_BOX_BACKGROUND, question_box_rect, border_radius=self.QUESTION_BOX_RADIUS) 
        pygame.draw.rect(screen, self.QUESTION_BOX_BORDER, question_box_rect, 5, border_radius=self.QUESTION_BOX_RADIUS) 

        try:
            text_surface = self.font.render(question_text, True, BLACK) 
            text_rect = text_surface.get_rect(center=(question_box_rect.centerx, question_box_rect.centery)) 
            screen.blit(text_surface, text_rect) 
        except:
            pass

        # --- 2. Dibujo de las 4 opciones de respuesta (en el suelo) con FADE-IN --- 
        if self.choice_alpha > 0 or self.is_answered:
            
            for i, rect in enumerate(self.choice_rects): 
                choice_dict = choices[i] 
                choice_text = choice_dict["text"].replace('\n', ' ') 

                # Inicialización: Fondo BLANCO, Borde NEGRO sutil
                # fill_color se usará como el color de relleno del rectángulo (blanco)
                fill_color = WHITE               
                border_color = BLACK             
                border_thickness = 1             
                
                # --- LÓGICA DE COLOR DE ESTADO (feedback) ---
                if self.is_answered: 
                    border_thickness = 5 
                    
                    if i == correct_index: 
                        border_color = self.correct_color_highlight 
                    else:
                        border_color = self.NEON_RED_ERROR 
                        
                # --- LÓGICA DE COLOR NORMAL/HOVER (ANTES DE RESPONDER) ---
                else: 
                    if i == self.selected_choice_index: 
                        border_color = YELLOW  
                        border_thickness = 5 
                    else:
                        border_color = BLACK 
                        border_thickness = 1 
                        
                # Crea una superficie temporal para la opción y aplica la opacidad
                option_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                
                # PASO 1: Dibujar el relleno blanco redondeado (grosor 0). 
                # Esto asegura que todo el área de la opción sea blanca y se recorte correctamente.
                pygame.draw.rect(option_surface, WHITE, (0, 0, rect.width, rect.height), 0, border_radius=self.choice_corner_radius) 
                
                # PASO 2: Dibujar el borde redondeado encima del relleno. 
                # Pygame respeta el área definida por el radio de la esquina.
                if border_thickness > 0:
                     pygame.draw.rect(option_surface, border_color, (0, 0, rect.width, rect.height), border_thickness, border_radius=self.choice_corner_radius) 
                
                # --- DIBUJAR TEXTO DE LA OPCIÓN (siempre negro) ---
                choice_text_surface = self.font.render(choice_text, True, self.option_text_color_default) 
                choice_text_rect = choice_text_surface.get_rect(center=(rect.width // 2, 30)) 
                option_surface.blit(choice_text_surface, choice_text_rect.topleft) 
                
                # --- DIBUJAR IMAGEN DEBAJO DEL TEXTO ---
                image_rect_pos = current_images[i].get_rect()
                image_rect_pos.center = (rect.width // 2, 30 + self.IMAGE_HEIGHT // 2 + 10) 
                try:
                    option_surface.blit(current_images[i], image_rect_pos.topleft) 
                except:
                    pass
                
                # Aplica la opacidad
                option_surface.set_alpha(self.choice_alpha)
                
                # Dibuja la superficie temporal en la pantalla
                screen.blit(option_surface, rect.topleft) 
            
        # --- 3. Mensajes de estado (inferior derecho) --- 
        status_msg = None
        status_color = None
        
        outline_color = BLACK
        
        status_font = self.font
        try:
            status_font_size = int(self.font.get_height() * 5.0) 
            font_path = self.font.get_path()
            if font_path:
                status_font = pygame.font.Font(font_path, status_font_size)
            else:
                status_font = pygame.font.Font(None, status_font_size)
                
        except Exception:
            pass 
        
        if self.is_answered: 
            if self.answer_result == "correct": 
                status_msg = "¡Correcto!" 
                status_color = self.correct_color_highlight 
                outline_color = DARK_GREEN 
            else: 
                correct_choice_text = choices[correct_index]["text"] if isinstance(choices[correct_index], dict) else choices[correct_index]
                correct_choice = correct_choice_text.replace('\n', ' ') 
                status_msg = f"¡Mal! La correcta era: {correct_choice}" 
                status_color = self.NEON_RED_ERROR 
                outline_color = WHITE
        
            if status_msg and status_color:
                temp_surface = status_font.render(status_msg, True, status_color) 
                msg_rect = temp_surface.get_rect(bottomright=(question_box_rect.right - 10, question_box_rect.bottom - 10)) 
                
                _draw_text_outline(
                    screen, 
                    status_msg, 
                    status_font, 
                    status_color, 
                    outline_color, 
                    msg_rect.x, 
                    msg_rect.y, 
                    outline_thickness=2 
                )
        
        elif self.selected_choice_index != -1 and self.fade_in_finished: 
            msg = "Presiona ESPACIO para contestar." 
            msg_surface = self.font.render(msg, True, WHITE)
            msg_rect = msg_surface.get_rect(bottomright=(question_box_rect.right - 10, question_box_rect.bottom - 10))
            screen.blit(msg_surface, msg_rect)