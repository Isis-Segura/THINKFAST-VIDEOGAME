import pygame

class FloorQuiz:
    def __init__(self, screen_size, questions, font):
        # ... (Mantener las inicializaciones existentes) ...
        self.screen_size = screen_size
        self.questions = questions
        self.font = font
        self.current_question_index = 0
        self.selected_choice_index = -1  # Cambiado a -1 (ninguna seleccionada)
        self.finished = False
        self.correct_answers = 0
        self.wrong_answers = 0
        self.is_answered = False 
        self.answer_result = None # Almacena "correct" o "incorrect" después de contestar
        
        # ... (Mantener las inicializaciones de color y posicionamiento) ...
        self.option_box_color = (0, 0, 128) 
        self.option_text_color = (255, 255, 255) 
        self.selected_color = (255, 165, 0) 
        self.correct_color = (0, 150, 0) 
        self.incorrect_color = (150, 0, 0) 
        
        self.box_width = int(screen_size[0] * 0.9)
        self.box_height = 80
        self.start_x = (screen_size[0] - self.box_width) // 2
        self.start_y = screen_size[1] - self.box_height - 30
        
        # Posiciones pre-calculadas para las 4 opciones (ejemplo de 4 opciones)
        self.choice_rects = []
        option_y = self.start_y - 120 
        option_margin = 10
        option_count = len(self.questions[0]["choices"])
        total_width = self.box_width
        choice_width = (total_width - (option_count - 1) * option_margin) // option_count
        
        for i in range(option_count):
            rect = pygame.Rect(
                self.start_x + i * (choice_width + option_margin),
                option_y,
                choice_width,
                50
            )
            self.choice_rects.append(rect)

    # --- NUEVO MÉTODO: Verificar colisión con el jugador ---
    def check_player_collision(self, player_rect):
        """
        Verifica si el rectángulo del jugador colisiona con alguna de las opciones 
        y actualiza el índice seleccionado.
        """
        if self.finished or self.is_answered:
            self.selected_choice_index = -1 # No se puede seleccionar si ya se respondió
            return -1
        
        for i, rect in enumerate(self.choice_rects):
            # Usamos colliderect para verificar si el jugador está "sobre" la opción
            if player_rect.colliderect(rect):
                self.selected_choice_index = i
                return i
                
        self.selected_choice_index = -1
        return -1

    # --- MÉTODO MODIFICADO: Solo manejar confirmación (Espacio) o avance ---
    def handle_event(self, event):
        """Maneja solo la confirmación de la respuesta con Espacio o el avance."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            
            if self.is_answered:
                 # Si ya se respondió, ESPACIO avanza a la siguiente pregunta
                 self.is_answered = False
                 return self.advance_question()
            
            elif self.selected_choice_index != -1 and not self.is_answered:
                # Si hay una opción seleccionada (personaje encima), se verifica la respuesta
                return self.check_answer()

        return None

    def check_answer(self):
        """Verifica la respuesta seleccionada."""
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
        """Avanza a la siguiente pregunta si ya se respondió la actual."""
        # Se llama desde handle_event si is_answered es True y se presiona ESPACIO
        self.selected_choice_index = -1 # Reinicia la selección
        self.answer_result = None
        self.current_question_index += 1

        if self.current_question_index >= len(self.questions):
            self.finished = True
        
        return "advanced"

    def draw(self, screen):
        """Dibuja la pregunta actual y las opciones."""
        if self.finished:
            return

        current_q = self.questions[self.current_question_index]
        question_text = current_q["question"]
        choices = current_q["choices"]
        correct_index = current_q["correct_answer"]
        
        # ... (Dibujar el cuadro de la pregunta - sin cambios) ...
        question_box_rect = pygame.Rect(self.start_x, self.start_y, self.box_width, self.box_height)
        pygame.draw.rect(screen, (0, 0, 0), question_box_rect) 
        pygame.draw.rect(screen, (255, 255, 255), question_box_rect, 3) 
        text_surface = self.font.render(question_text, True, self.option_text_color)
        text_rect = text_surface.get_rect(midleft=(question_box_rect.x + 20, question_box_rect.centery))
        screen.blit(text_surface, text_rect)
        
        # --- Dibujar las opciones (cambio en cómo se colorean) ---
        for i, choice in enumerate(choices):
            rect = self.choice_rects[i]
            color = self.option_box_color
            border_color = (255, 255, 255)
            
            if self.is_answered:
                # Mostrar resultado: Correcta en verde, seleccionada incorrecta en rojo.
                if i == correct_index:
                    color = self.correct_color
                elif i == self.selected_choice_index:
                    color = self.incorrect_color
            
            elif i == self.selected_choice_index:
                # No respondida: La opción que el personaje está tocando se resalta.
                border_color = self.selected_color
            
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, border_color, rect, 3)
            
            # Renderizar el texto de la opción
            choice_surface = self.font.render(choice, True, self.option_text_color)
            choice_rect = choice_surface.get_rect(center=rect.center)
            screen.blit(choice_surface, choice_rect)
            
        # Indicador de avance (solo si ya respondió)
        if self.is_answered:
             msg = "Presiona ESPACIO para continuar..."
             # Si fue incorrecta, muestra también la respuesta correcta para aprender
             if self.answer_result == "incorrect":
                 correct_choice = choices[correct_index]
                 msg = f"¡Mal! La correcta es: {correct_choice}. Presiona ESPACIO para continuar..."

             msg_surface = self.font.render(msg, True, (255, 255, 0))
             msg_rect = msg_surface.get_rect(bottomright=(question_box_rect.right - 10, question_box_rect.bottom - 10))
             screen.blit(msg_surface, msg_rect)
             
        # Indicador de selección (si no ha respondido)
        elif self.selected_choice_index != -1:
             msg = "Presiona ESPACIO para contestar."
             msg_surface = self.font.render(msg, True, self.selected_color)
             msg_rect = msg_surface.get_rect(bottomright=(question_box_rect.right - 10, question_box_rect.bottom - 10))
             screen.blit(msg_surface, msg_rect)