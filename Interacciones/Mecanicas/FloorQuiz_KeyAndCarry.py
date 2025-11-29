import pygame
import os
import random 

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

        # --- PROPIEDADES PARA EL TEMPORIZADOR DE AVANCE (2 SEGUNDOS) ---
        self.DELAY_DURATION = 2000 # 2 segundos en milisegundos
        self.delay_timer = 0       # Almacena el tiempo de inicio del retraso
        # -------------------------------------------------------------

        # Propiedades para la caja de la pregunta
        self.question_box_img = None
        self.question_box_rect = None
        self._setup_question_box_display()

        # --- NUEVOS PARÁMETROS PARA LA REVELACIÓN DE RESPUESTAS (Fade-in) ---
        self.ANSWER_REVEAL_DELAY = 1500  # 1.5 segundos de espera antes de la animación
        self._answer_reveal_timer = 0    # Tiempo de inicio de la revelación
        self._answers_visible = False    # Bandera para saber si ya se pueden dibujar
        self._current_reveal_alpha = 0   # Transparencia (0 a 255) para la animación fade-in
        self.REVEAL_DURATION = 500       # 0.5 segundos para el fade-in
        # ------------------------------------------------------------------

        # Propiedades para la opción cargada
        self.carried_choice_box_img = None
        self.carried_choice_box_rect = pygame.Rect(0, 0, 150, 40)

        # Configuración visual de las opciones en el suelo
        self.choice_colors = [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)]
        self.highlight_color = (255, 255, 0)
        self.choice_font_color = (0, 0, 0) 
        # Color de texto de la pregunta: Blanco/Tiza
        self.question_font_color = (0, 0, 0)
        
        # Nuevos colores para los bordes de retroalimentación
        self.CORRECT_COLOR = (0, 200, 0) # Verde
        self.INCORRECT_COLOR = (200, 0, 0) # Rojo

        self._load_choice_images()
        
        self._setup_question_layout() 

    def _load_choice_images(self):
        """Carga las imágenes de las opciones al inicio y las adjunta a los datos de la opción."""
        C_IMG_SIZE = (80, 80) 
        
        for q_index, question_data in enumerate(self.questions):
            for choice_data in question_data["choices"]:
                c_path = choice_data.get("image")
                loaded_img = None
                
                if c_path and os.path.exists(c_path):
                    try:
                        c_img = pygame.image.load(c_path).convert_alpha()
                        loaded_img = pygame.transform.scale(c_img, C_IMG_SIZE)
                    except pygame.error as e:
                        print(f"Error al cargar imagen de la opción '{c_path}': {e}")
                
                # Almacenar la imagen cargada directamente en el diccionario de la opción
                choice_data["loaded_image"] = loaded_img 

    def _setup_question_box_display(self):
        if self._dialog_img_loaded and self.dialog_box_img_template:
            desired_width = 600
            desired_height = 80
            self.question_box_img = pygame.transform.scale(self.dialog_box_img_template, (desired_width, desired_height))
            self.question_box_rect = self.question_box_img.get_rect(center=(self.size[0] // 2, 150))
        else:
            # --- CÓDIGO DE RECIBO ANTERIOR (Estilos) ---
            self.question_box_img = pygame.Surface((600, 80), 0) 
            self.question_box_img.set_colorkey((0, 0, 0))
            
            # Colores y parámetros
            BACKGROUND_COLOR = (255, 255, 255) 
            BORDER_COLOR = (101, 67, 33) 
            BORDER_THICKNESS = 7   
            BORDER_RADIUS = 20     
            
            # 1. DIBUJAR EL RELLENO VERDE CON BORDER_RADIUS 
            pygame.draw.rect(self.question_box_img, BACKGROUND_COLOR, self.question_box_img.get_rect(), 0, border_radius=BORDER_RADIUS)
            
            # 2. DIBUJAR EL BORDE MARRÓN CON MAYOR GROSOR
            pygame.draw.rect(self.question_box_img, BORDER_COLOR, self.question_box_img.get_rect(), BORDER_THICKNESS, border_radius=BORDER_RADIUS)
            
            self.question_box_rect = self.question_box_img.get_rect(center=(self.size[0] // 2, 150))
            # -----------------------------------------------------------------------

    def _setup_question_layout(self):
        self.choice_rects = []
        current_q = self.questions[self.current_question_index]
        choices = current_q["choices"]
        
        # --- LÓGICA PARA BARAJAR RESPUESTAS ---
        # 1. Obtener el objeto de la respuesta correcta antes de barajar
        correct_choice_data = choices[current_q["correct_answer"]]
        
        # 2. Barajar las opciones en su lugar (in-place)
        random.shuffle(choices) 
        
        # 3. Encontrar el nuevo índice de la respuesta correcta en la lista barajada
        try:
            new_correct_index = choices.index(correct_choice_data)
        except ValueError:
            new_correct_index = current_q["correct_answer"] 

        # 4. Actualizar la propiedad 'correct_answer' con el nuevo índice.
        current_q["correct_answer"] = new_correct_index
        # ---------------------------------------------
        
        # --- NUEVO: REINICIO DE ESTADOS DE REVELACIÓN ---
        self._answers_visible = False
        self._current_reveal_alpha = 0
        self._answer_reveal_timer = pygame.time.get_ticks() 
        # ------------------------------------------------
        
        start_y = self.size[1] - 130
        choice_box_height = 100
        
        # Se mantiene el ancho fijo para uniformidad
        C_BOX_UNIFORM_WIDTH = 180 
        choice_box_width = C_BOX_UNIFORM_WIDTH 
        

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
        self.delay_timer = 0 # Reiniciar el timer
        

    def check_player_collision(self, player_rect):
        # La colisión solo se comprueba si las respuestas son visibles
        if not self._answers_visible or self.is_answered or self.carried_choice_index != -1:
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
            # Aunque no se llama aquí en la nueva lógica, se mantiene
            self.finished = True 
        
    def update_carried_choice_position(self, player_center_x, player_top_y):
        self.carried_choice_box_rect.centerx = player_center_x + self.carried_choice_box_rect.width // 2 + 10
        self.carried_choice_box_rect.centery = player_top_y + (self.carried_choice_box_rect.height // 2) + 20

    def update(self):
        """Maneja la lógica de avance automático después de la respuesta y la animación de revelación."""
        current_time = pygame.time.get_ticks()

        # --- LÓGICA DE REVELACIÓN DE RESPUESTAS (Fade-in) ---
        if not self._answers_visible and self.carried_choice_index == -1 and not self.is_answered:
            elapsed = current_time - self._answer_reveal_timer
            
            if elapsed > self.ANSWER_REVEAL_DELAY:
                # 1. Ya pasó el retraso inicial, ahora hacemos el fade-in
                reveal_time = elapsed - self.ANSWER_REVEAL_DELAY
                
                # 2. Calcular el nuevo valor de alfa (transparencia)
                if reveal_time < self.REVEAL_DURATION:
                    # Cálculo de 0 a 255
                    self._current_reveal_alpha = int((reveal_time / self.REVEAL_DURATION) * 255)
                else:
                    # Fin de la animación
                    self._current_reveal_alpha = 255
                    self._answers_visible = True

        # --- Lógica de AVANCE AUTOMÁTICO (EXISTENTE) ---
        if self.is_answered and self.delay_timer > 0:
            if current_time - self.delay_timer >= self.DELAY_DURATION:
                # Si es la última pregunta
                if self.current_question_index == self.max_questions - 1:
                    self.finished = True 
                    self.is_answered = False 
                    self.delay_timer = 0
                else:
                    self.next_question() # Pasa a la siguiente pregunta
        
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
                
                # --- INICIAR EL TEMPORIZADOR AL RESPONDER (PARA TODAS LAS PREGUNTAS) ---
                self.delay_timer = pygame.time.get_ticks() 
                # ------------------------------------------

                # Se retorna el resultado, Level2F.py lo registra y espera que update() marque el final.
                return self.answer_result

        # 2. RECOGER (PICK UP)
        elif self.highlighted_choice_index != -1 and self._answers_visible: # Solo permite recoger si son visibles
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


    def draw(self, surface, player_rect,language):
        
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

        # 2. DIBUJAR OPCIONES EN EL SUELO 
        if self.carried_choice_index == -1: 
            current_q_data = self.questions[self.current_question_index]
            correct_index = current_q_data["correct_answer"]
            
            # --- NUEVO: DIBUJAR EN UNA SUPERFICIE TEMPORAL CON ALFA ---
            # Crear una superficie que abarque toda el área de dibujo para aplicar transparencia
            temp_surface = pygame.Surface(self.size, pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 0)) # Rellenar transparente
            
            if not self.is_answered:
                # Aplicar la transparencia calculada en update()
                temp_surface.set_alpha(self._current_reveal_alpha)
            else:
                # Si ya fue respondida, se dibuja opaca (alpha 255)
                temp_surface.set_alpha(255)
            # --------------------------------------------------------
            
            for i, rect in enumerate(self.choice_rects):
                
                current_choice_data = current_q_data["choices"][i]
                choice_text = current_choice_data["text"]
                
                # --- LÓGICA DE BORDE DE RETROALIMENTACIÓN ---
                border_color = None
                border_width = 3 # Grosor del borde
                
                if self.is_answered:
                    if i == correct_index:
                        border_color = self.CORRECT_COLOR  # Verde para la correcta
                    else:
                        border_color = self.INCORRECT_COLOR # Rojo para las incorrectas
                elif i == self.highlighted_choice_index:
                    border_color = self.highlight_color # Amarillo si está resaltada para recoger
                    border_width = 5 
                
                # --- DIBUJAR RECUADRO Y BORDE EN temp_surface ---
                pygame.draw.rect(temp_surface, self.choice_colors[i], rect, border_radius=5)
                
                if border_color:
                    pygame.draw.rect(temp_surface, border_color, rect, border_width, border_radius=5)

                
                # DIBUJAR IMAGEN DE OPCIÓN
                choice_img = current_choice_data.get("loaded_image") 
                if choice_img:
                    img_rect = choice_img.get_rect(centerx=rect.centerx, top=rect.top + 0) 
                    temp_surface.blit(choice_img, img_rect.topleft)
                
                # DIBUJAR TEXTO DE OPCIÓN
                text_surface = self.font_question.render(choice_text, True, self.choice_font_color)
                text_rect = text_surface.get_rect(centerx=rect.centerx, bottom=rect.bottom - 2) 
                temp_surface.blit(text_surface, text_rect)
                
                # DIBUJAR MENSAJE DE RECOGER (Solo si las respuestas están completamente visibles)
                if language == "es":
                    if self._answers_visible and i == self.highlighted_choice_index and not self.is_answered:
                        prompt_text = "Presiona ESPACIO/ENTER para RECOGER."
                        prompt_center_pos = (rect.centerx, rect.top - 40) 
                        
                        self._draw_text_with_border(
                            temp_surface, 
                            prompt_text, 
                            self.font_question, 
                            (255, 255, 255),  
                            (0, 0, 0),        
                            prompt_center_pos,
                            border_offset=1
                        )
                else: # language == "en"
                    if self._answers_visible and i == self.highlighted_choice_index and not self.is_answered:
                        prompt_text = "Press SPACE/ENTER to PICK UP."
                        prompt_center_pos = (rect.centerx, rect.top - 40) 
                        
                        self._draw_text_with_border(
                            temp_surface, 
                            prompt_text, 
                            self.font_question, 
                            (255, 255, 255),  
                            (0, 0, 0),        
                            prompt_center_pos,
                            border_offset=1
                        )
            
            # --- DIBUJAR LA SUPERFICIE TEMPORAL EN LA PANTALLA ---
            surface.blit(temp_surface, (0, 0))
            # -------------------------------------------------------------


        # 3. DIBUJAR RESULTADO TEMPORAL CON BORDE 
        if language == "es":
            if self.is_answered:
                # Ahora el mensaje de "CORRECTO/INCORRECTO" es uniforme para todas las preguntas
                if self.answer_result == "correct": 
                    message = "¡CORRECTO!"
                    msg_color = self.CORRECT_COLOR 
                else: # incorrect
                    message = "INCORRECTO."
                    msg_color = self.INCORRECT_COLOR

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
        else: # language == "en"
            if self.is_answered:
                # Ahora el mensaje de "CORRECTO/INCORRECTO" es uniforme para todas las preguntas
                if self.answer_result == "correct": 
                    message = "CORRECT!"
                    msg_color = self.CORRECT_COLOR 
                else: # incorrect
                    message = "INCORRECT."
                    msg_color = self.INCORRECT_COLOR

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
            carried_box_surface.fill((255, 255, 255)) 
            pygame.draw.rect(carried_box_surface, (255, 255, 0), carried_box_surface.get_rect(), 2, border_radius=5) 
            
            text_surface = self.font_question.render(choice_text, True, (0, 0, 0)) 
            text_rect = text_surface.get_rect(center=(carried_box_surface.get_width() // 2, carried_box_surface.get_height() // 2))
            carried_box_surface.blit(text_surface, text_rect)
            
            carried_box_rect_on_screen = carried_box_surface.get_rect(center=(self.carried_choice_box_rect.centerx, self.carried_choice_box_rect.centery))
            surface.blit(carried_box_surface, carried_box_rect_on_screen)