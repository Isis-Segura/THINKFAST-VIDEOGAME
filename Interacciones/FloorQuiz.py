import pygame 
import random # <--- ¡IMPORTACIÓN NECESARIA PARA ALEATORIEDAD! 

class FloorQuiz: 
    """ 
    Gestiona la lógica y el dibujo del minijuego de preguntas en el suelo. 
    Las opciones de respuesta tienen posiciones y colores aleatorios por partida. 
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

        # --- Dimensiones y Posiciones (Fijas) --- 
        self.PIXEL_RADIUS = 10  
        self.QUESTION_BOX_WIDTH = 800 
        self.QUESTION_BOX_HEIGHT = 100 
        self.QUESTION_BOX_RADIUS = 10 
        
        self.start_x = (size[0] - self.QUESTION_BOX_WIDTH) // 2 
        self.start_y = size[1] - self.QUESTION_BOX_HEIGHT - 20 
        self.box_width = self.QUESTION_BOX_WIDTH 
        self.box_height = self.QUESTION_BOX_HEIGHT 

        # 1. Definir las 4 posiciones (rectángulos) posibles de la cuadrícula 
        CHOICE_WIDTH = 150 
        CHOICE_HEIGHT = 60 
        
        POS_0_X = 150 
        POS_0_Y = 370  
        POS_1_X = size[0] - 150 - CHOICE_WIDTH 
        POS_1_Y = 370 
        POS_2_X = 150 
        POS_2_Y = size[1] - 180 
        POS_3_X = size[0] - 150 - CHOICE_WIDTH 
        POS_3_Y = size[1] - 180 
        
        choice_rects_template = [ 
            pygame.Rect(POS_0_X, POS_0_Y, CHOICE_WIDTH, CHOICE_HEIGHT),  
            pygame.Rect(POS_1_X, POS_1_Y, CHOICE_WIDTH, CHOICE_HEIGHT), 
            pygame.Rect(POS_2_X, POS_2_Y, CHOICE_WIDTH, CHOICE_HEIGHT),  
            pygame.Rect(POS_3_X, POS_3_Y, CHOICE_WIDTH, CHOICE_HEIGHT) 
        ] 

        # 2. Definir los 4 colores (fijos) 
        self.NEON_COLORS = [ 
            (0, 255, 0),
            (255, 255, 0), 
            (0, 100, 255), 
            (255, 0, 0), 
        ] 
        
        # 3. ¡ALEATORIZAR LAS POSICIONES Y COLORES AL INICIO! 
        self.choice_rects = choice_rects_template 
        self.vivid_colors = self.NEON_COLORS  

        random.shuffle(self.choice_rects) 
        random.shuffle(self.vivid_colors) 
        
        # 4. Modificar las preguntas para que sus opciones también se mezclen 
        self._shuffle_questions_choices() 


        # --- Colores de estado --- 
        self.QUESTION_BOX_BACKGROUND = (20, 30, 80)  
        self.QUESTION_BOX_BORDER = (255, 200, 0)  
        self.option_text_color = (0, 0, 0)
        self.selected_color = (255, 255, 255) 
        self.correct_color = (0, 255, 0)  
        self.incorrect_color = (255, 0, 0)  
        self.ALPHA_SELECTED = 150 

    def _shuffle_questions_choices(self): 
        """ 
        Mezcla las opciones (choices) de cada pregunta y actualiza el  
        índice de la respuesta correcta (correct_answer) para que coincida. 
        """ 
        for q in self.questions: 
            choices = q["choices"] 
            correct_index = q["correct_answer"] 
            
            # 1. Crear una lista de pares (opción, es_correcta) 
            shufflable_items = [] 
            for i, choice in enumerate(choices): 
                is_correct = (i == correct_index) 
                shufflable_items.append((choice, is_correct)) 
            
            # 2. Mezclar la lista de pares 
            random.shuffle(shufflable_items) 
            
            # 3. Reasignar las opciones mezcladas y encontrar el nuevo índice correcto 
            new_choices = [] 
            new_correct_index = -1 
            
            for i, (choice, is_correct) in enumerate(shufflable_items): 
                new_choices.append(choice) 
                if is_correct: 
                    new_correct_index = i 
            
            # 4. Actualizar la pregunta 
            q["choices"] = new_choices 
            q["correct_answer"] = new_correct_index 
            
    def _create_choice_rects_from_positions(self): 
        # NOTA: Este método se deja vacío en esta versión porque choice_rects se construye 
        # directamente en __init__ a partir de choice_rects_template 
        pass 
        
    def check_player_collision(self, player_rect): 
        """ 
        Verifica si el rectángulo COMPLETO del jugador colisiona con el 
        rectángulo COMPLETO de la opción de respuesta. 
        """ 
        if self.is_answered or self.finished: 
            self.selected_choice_index = -1  
            return 

        for i, rect in enumerate(self.choice_rects): 
            if player_rect.colliderect(rect): 
                self.selected_choice_index = i 
                return 

        self.selected_choice_index = -1 

    def handle_event(self, event): 
        """Maneja los eventos (solo la tecla ESPACIO/ENTER para responder o avanzar).""" 
        if self.finished: 
            return None 
            
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN): 
            if self.is_answered: 
                return self.advance_question() 
            elif self.selected_choice_index != -1: 
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

    def advance_question(self): 
        """Avanza al siguiente estado del quiz o lo finaliza.""" 
        self.current_question_index += 1 
        
        if self.current_question_index >= len(self.questions): 
            self.finished = True 
            return "finished" 
        else: 
            self.is_answered = False 
            self.selected_choice_index = -1 
            self.answer_result = None 
            return "advanced" 

    def draw(self, screen): 
        """Dibuja la pregunta, las opciones y el estado del quiz.""" 
        if self.finished: 
            return 

        current_q = self.questions[self.current_question_index] 
        question_text = current_q["question"].replace('\n', ' ')  
        choices = current_q["choices"] # Las opciones ya están mezcladas 
        correct_index = current_q["correct_answer"] 
        
        # --- 1. Dibujo de la caja de pregunta inferior (Opaca) --- 
        question_box_rect = pygame.Rect(self.start_x, self.start_y, self.box_width, self.box_height) 
        
        pygame.draw.rect(screen, self.QUESTION_BOX_BACKGROUND, question_box_rect, border_radius=self.QUESTION_BOX_RADIUS) 
        pygame.draw.rect(screen, self.QUESTION_BOX_BORDER, question_box_rect, 5, border_radius=self.QUESTION_BOX_RADIUS)  
        
        # Dibujar pregunta: Centrado (Texto blanco) 
        try: 
            text_surface = self.font.render(question_text, True, (255, 255, 255)) 
        except: 
            text_surface = self.font.render("Error de Texto", True, (255, 0, 0)) 

        text_rect = text_surface.get_rect(center=question_box_rect.center) 
        screen.blit(text_surface, text_rect.topleft) 
        
        # --- 2. Dibujo de las opciones (Rectángulos Neón en 2x2) --- 
        for i, choice in enumerate(choices): 
            # El índice 'i' aquí corresponde a la posición en la lista ya aleatoria 
            rect = self.choice_rects[i] # El rectángulo aleatorio 
            base_color = self.vivid_colors[i] # El color aleatorio 
            
            border_thickness = 0 
            border_color = base_color 
            draw_color = base_color  
            
            is_currently_selected = (i == self.selected_choice_index) 
            
            if self.is_answered: 
                # Post-respuesta: Muestra Correcto/Incorrecto 
                if i == correct_index: 
                    draw_color = self.correct_color  
                    border_color = (255, 255, 255) 
                    border_thickness = 5 
                elif i == self.selected_choice_index: 
                    draw_color = self.incorrect_color  
                    border_color = (255, 255, 255) 
                    border_thickness = 5 
                    
                # Dibujar el cuadro con el color final (opaco) 
                pygame.draw.rect(screen, draw_color, rect, border_radius=self.PIXEL_RADIUS) 

            elif is_currently_selected: 
                # Efecto de transparencia en la selección 
                
                # 1. Crear una Surface temporal con canal alfa 
                surface = pygame.Surface(rect.size, pygame.SRCALPHA) 
                
                # 2. Dibujar el fondo redondeado y transparente 
                fill_color_with_alpha = base_color + (self.ALPHA_SELECTED,) 
                pygame.draw.rect(surface, fill_color_with_alpha, (0, 0, rect.width, rect.height), border_radius=self.PIXEL_RADIUS) 
                
                # 3. Dibujar el borde blanco redondeado SOBRE esa misma superficie 
                border_color = self.selected_color  
                border_thickness = 5 
                pygame.draw.rect(surface, border_color, (0, 0, rect.width, rect.height), border_thickness, border_radius=self.PIXEL_RADIUS) 

                # 4. Blit la Surface transparente a la pantalla 
                screen.blit(surface, rect.topleft) 
                
            else: 
                # Opción no seleccionada (opaca) 
                pygame.draw.rect(screen, draw_color, rect, border_radius=self.PIXEL_RADIUS) 
            
            # Si no está seleccionada y no se ha contestado, dibujar el borde opaco. 
            if not self.is_answered and not is_currently_selected: 
                    pygame.draw.rect(screen, border_color, rect, border_thickness, border_radius=self.PIXEL_RADIUS) 


            # Dibujo de texto de opción (centrado, color negro) 
            choice_surface = self.font.render(choice.replace('\n', ' '), True, self.option_text_color)  
            choice_rect = choice_surface.get_rect(center=rect.center) 
            screen.blit(choice_surface, choice_rect) 
            
        # --- 3. Mensajes de estado (inferior derecho) --- 
        if self.is_answered: 
            if self.answer_result == "correct": 
                msg = "¡Correcto! (Presiona ESPACIO para avanzar)" 
                color = self.correct_color 
            else: 
                correct_choice = choices[correct_index].replace('\n', ' ') 
                # Mensaje acortado  
                msg = f"¡Mal! La correcta era: {correct_choice} (ESPACIO para avanzar)" 
                color = self.incorrect_color 
            
            msg_surface = self.font.render(msg, True, color) 
            msg_rect = msg_surface.get_rect(bottomright=(question_box_rect.right - 10, question_box_rect.bottom - 10)) 
            screen.blit(msg_surface, msg_rect) 
            
        elif self.selected_choice_index != -1: 
            msg = "Presiona ESPACIO para contestar." 
            msg_surface = self.font.render(msg, True, self.selected_color) 
            msg_rect = msg_surface.get_rect(bottomright=(question_box_rect.right - 10, question_box_rect.bottom - 10)) 
            screen.blit(msg_surface, msg_rect)