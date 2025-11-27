import pygame
import sys
import os
import time
import math

pygame.init()

# --- COLORES ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)  # Verde obscuro para el botón principal
BROWN = (139, 69, 19)     # Café para el marco
LIGHT_BROWN = (160, 120, 80)  # Madera clara
RED = (200, 0, 0)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 180, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0 
        self.paused = False
        self.pause_time = 0
        self.finished = False
        self.elapsed_pause_time = 0

    def start(self):
        self.start_time = time.time() 
        self.finished = False
        self.paused = False
        self.elapsed_pause_time = 0

    def pause(self):
        if not self.paused:
            self.pause_time = time.time()
            self.paused = True

    def resume(self):
        if self.paused:
            self.elapsed_pause_time += time.time() - self.pause_time
            self.paused = False

    def update(self):
        if not self.paused and not self.finished:
            elapsed = time.time() - self.start_time - self.elapsed_pause_time
            if elapsed >= self.duration:
                self.finished = True

    def get_remaining_time(self):
        if self.paused:
            elapsed = self.pause_time - self.start_time - self.elapsed_pause_time
        else:
            elapsed = time.time() - self.start_time - self.elapsed_pause_time
        remaining = max(0, self.duration - elapsed)
        return remaining

    def is_running(self):
        return not self.paused and not self.finished

    def draw(self, surface, font, position):
        remaining = self.get_remaining_time()
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        time_text = f"{minutes:02d}:{seconds:02d}"
        
        # Cambiar color según el tiempo restante
        if remaining <= 5:
            color = RED
            bg_color = (150, 0, 0)  # Rojo oscuro
            clock_color = (255, 100, 100)  # Rojo claro para detalles
        elif remaining <= 10:
            color = ORANGE
            bg_color = (150, 80, 0)  # Naranja oscuro
            clock_color = (255, 200, 100)  # Naranja claro para detalles
        else:
            color = YELLOW
            bg_color = (0, 150, 0)  # Verde oscuro
            clock_color = (100, 255, 100)  # Verde claro para detalles
        
        # Dibujar el reloj circular (más grande y colorido para niños)
        clock_radius = 50  # Más grande
        clock_center = (position[0] + clock_radius, position[1] + clock_radius)
        
        # Dibujar círculo de fondo con efecto 3D
        pygame.draw.circle(surface, bg_color, clock_center, clock_radius)
        
        # Efecto de relieve
        pygame.draw.circle(surface, clock_color, clock_center, clock_radius - 5)
        pygame.draw.circle(surface, BLACK, clock_center, clock_radius, 3)
        
        # Dibujar manecilla del reloj (progreso del tiempo) - más gruesa
        progress = remaining / self.duration
        angle = 2 * math.pi * progress - math.pi / 2  # Empezar desde arriba
        
        end_x = clock_center[0] + (clock_radius - 10) * math.cos(angle)
        end_y = clock_center[1] + (clock_radius - 10) * math.sin(angle)
        
        pygame.draw.line(surface, color, clock_center, (end_x, end_y), 6)
        
        # Dibujar centro del reloj
        pygame.draw.circle(surface, color, clock_center, 8)
        
        # Dibujar marcas del reloj (más visibles)
        for i in range(12):
            mark_angle = 2 * math.pi * i / 12 - math.pi / 2
            inner_x = clock_center[0] + (clock_radius - 15) * math.cos(mark_angle)
            inner_y = clock_center[1] + (clock_radius - 15) * math.sin(mark_angle)
            outer_x = clock_center[0] + (clock_radius - 5) * math.cos(mark_angle)
            outer_y = clock_center[1] + (clock_radius - 5) * math.sin(mark_angle)
            pygame.draw.line(surface, BLACK, (inner_x, inner_y), (outer_x, outer_y), 2)
        
        # Dibujar el texto del tiempo DENTRO del reloj (más grande)
        time_font = pygame.font.Font(None, clock_radius)  # Fuente proporcional al tamaño del reloj
        text_surface = time_font.render(time_text, True, BLACK)
        text_rect = text_surface.get_rect(center=clock_center)
        surface.blit(text_surface, text_rect)

class RelationButton:
    def __init__(self, x, y, width, height, text, is_image=False, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_image = is_image
        self.image_path = image_path
        self.image = None
        self.selected = False
        self.matched = False
        
        if is_image and image_path:
            try:
                full_path = os.path.join("Materials", "Pictures", "Assets", image_path)
                if os.path.exists(full_path):
                    self.image = pygame.image.load(full_path).convert_alpha()
                    # Escalar imagen manteniendo proporciones - AUMENTAR EL TAMAÑO
                    img_ratio = self.image.get_width() / self.image.get_height()
                    
                    # AUMENTAR EL TAMAÑO DE LAS IMÁGENES - usar más espacio del botón
                    if img_ratio > 1:
                        # Imagen horizontal - usar 90% del ancho del botón
                        new_width = width * 0.9
                        new_height = new_width / img_ratio
                    else:
                        # Imagen vertical - usar 90% del alto del botón
                        new_height = height * 0.9
                        new_width = new_height * img_ratio
                    
                    # Asegurarse de que no sea más grande que el botón
                    if new_width > width * 0.95:
                        new_width = width * 0.95
                        new_height = new_width / img_ratio
                    if new_height > height * 0.95:
                        new_height = height * 0.95
                        new_width = new_height * img_ratio
                    
                    self.image = pygame.transform.scale(self.image, (int(new_width), int(new_height)))
                else:
                    print(f"Image not found: {full_path}")
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

    def draw(self, surface):
        # Dibujar botón con fondo blanco y marco café
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=8)
        pygame.draw.rect(surface, BROWN, self.rect, 3, border_radius=8)
        
        if self.is_image and self.image:
            # Centrar imagen en el botón
            img_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, img_rect)
        else:
            # Dibujar texto centrado
            font_size = max(30, self.rect.height // 3)
            text_font = pygame.font.Font(None, font_size)
            text_surf = text_font.render(self.text, True, BLACK)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def contains_point(self, point):
        return self.rect.collidepoint(point)

class FloatingMessage:
    def __init__(self, text, font, duration=5):
        self.text = text
        self.font = font
        self.duration = duration
        self.start_time = time.time()
        self.active = True
        
    def update(self):
        if time.time() - self.start_time > self.duration:
            self.active = False
            
    def draw(self, surface, position):
        if not self.active:
            return
            
        # Crear superficie para el mensaje con efecto de madera
        text_surface = self.font.render(self.text, True, BLACK)
        padding = 20
        rect_width = text_surface.get_width() + padding * 2
        rect_height = text_surface.get_height() + padding * 2
        
        # Crear superficie para el mensaje
        message_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        
        # Dibujar fondo de madera
        pygame.draw.rect(message_surface, LIGHT_BROWN, (0, 0, rect_width, rect_height), border_radius=15)
        pygame.draw.rect(message_surface, BROWN, (0, 0, rect_width, rect_height), 3, border_radius=15)
        
        # Añadir textura de madera (rayas)
        for i in range(0, rect_width, 4):
            pygame.draw.line(message_surface, (120, 80, 40), (i, 0), (i, rect_height), 1)
        
        # Dibujar texto
        text_rect = text_surface.get_rect(center=(rect_width // 2, rect_height // 2))
        message_surface.blit(text_surface, text_rect)
        
        # Dibujar en la posición especificada
        surface.blit(message_surface, position)

def run_quiz_with_timer(screen, fondo_path):
    # Obtener dimensiones reales de la pantalla
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    
    # Cargar y ajustar el fondo a toda la pantalla
    try:
        background = pygame.image.load(fondo_path).convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill((50, 100, 200))
    
    # Crear fuentes
    title_font = pygame.font.Font(None, SCREEN_HEIGHT // 20)
    medium_font = pygame.font.Font(None, SCREEN_HEIGHT // 25)
    small_font = pygame.font.Font(None, SCREEN_HEIGHT // 30)
    timer_font = pygame.font.Font(None, SCREEN_HEIGHT // 18)
    message_font = pygame.font.Font(None, SCREEN_HEIGHT // 30)
    large_font = pygame.font.Font(None, SCREEN_HEIGHT // 8)  # Fuente para el contador
    
    # --- DATOS DE LAS PREGUNTAS (6 PREGUNTAS EN TOTAL) ---
    questions_data = [
        {
            "question": "Si tienes 5 manzanas y comes 2\n¿cuántas te quedan?",
            "numbers": ["2", "3", "4", "6"],
            "images": ["3naranjas.png", "6 naranjas.png", "2naranjas.png", "4naranjas.png"],
            "correct_answer": "3",
            "correct_image": "3naranjas.png"
        },
        {
            "question": "¿Cuántas ruedas tiene un coche normal?",
            "numbers": ["1", "3", "4", "6"],
            "images": ["4llantas.png", "1llantas.png", "3llantas.png", "6llantas.png"],
            "correct_answer": "4",
            "correct_image": "4llantas.png"
        },
        {
            "question": "Si tienes 6 caramelos y das 1 a tu amigo\n¿cuántos te quedan?",
            "numbers": ["4", "5", "6", "7"],
            "images": ["4caramelos.png", "3caramelos.png", "7caramelos.png", "5carmelos.png"],
            "correct_answer": "5",
            "correct_image": "5carmelos.png"
        },
        {
            "question": "¿Cuántos son 2 mangos + 2 mangos + 2 mangos?",
            "numbers": ["3", "6", "2", "5"],  
            "images": ["3mangos.png", "6mangos.png", "2mangos.png", "5mangos.png"],
            "correct_answer": "6",
            "correct_image": "6mangos.png"
        },
        {
            "question": "¿Cuántas patitas tienen 1 gatito?\n",
                "numbers": ["1", "4", "2", "5"],
                "images": ["4patitas.png", "1patitas.png", "5patitas.png", "2patitas.png"],
                "correct_number": "12",
                "correct_image": "12patitas.png"
        },
        {
             "question": "María tiene 5 manzanas y compra 3 más\n¿cuántas tiene ahora?",
                "numbers": ["5", "8", "7", "6"],
                "images": ["5manzanas.png", "8manzanas.png", "7manzanas.png", "6manzanas.png"],
                "correct_number": "8",
                "correct_image": "8manzanas.png"
        }
    ]
    
    # Inicializar timer (35 segundos por pregunta)
    quiz_timer = Timer(35)
    
    score = 0
    question_index = 0
    total_questions = len(questions_data)
    running = True
    
    # Variables para mostrar resultados de cada pregunta
    answer_results = []
    
    # Variables para controlar la aparición de elementos
    show_mechanic_after_delay = False
    mechanic_delay_start =0
    mechanic_delay_duration =2 
    
    while running and question_index < total_questions:
        current_question = questions_data[question_index]
        
        # --- DEFINIR ÁREAS PRINCIPALES ---
        
        # Área de la pregunta (arriba) - Fondo blanco con marco café
        question_rect = pygame.Rect(
            SCREEN_WIDTH // 10,
            SCREEN_HEIGHT // 10,
            SCREEN_WIDTH * 0.8,
            SCREEN_HEIGHT // 6
        )
        
        # Área principal de la mecánica (verde obscuro con marco café)
        main_rect = pygame.Rect(
            SCREEN_WIDTH // 10,
            SCREEN_HEIGHT // 10 + SCREEN_HEIGHT // 6 + 20,
            SCREEN_WIDTH * 0.8,
            SCREEN_HEIGHT * 0.6
        )
        
        # AUMENTAR EL TAMAÑO DE LOS BOTONES PARA MEJOR VISIBILIDAD
        button_width = main_rect.width // 5  # Botones más anchos
        button_height = main_rect.height // 3  # Botones más altos
        
        # Crear botones para números (fila horizontal)
        number_buttons = []
        number_start_x = main_rect.left + (main_rect.width - (len(current_question["numbers"]) * button_width + 
                            (len(current_question["numbers"]) - 1) * 20)) // 2
        number_start_y = main_rect.top + main_rect.height // 4  # Subir un poco para dar más espacio a las imágenes
        
        for i, number in enumerate(current_question["numbers"]):
            x = number_start_x + i * (button_width + 20)
            y = number_start_y
            btn = RelationButton(x, y, button_width, button_height, number, False)
            number_buttons.append(btn)
        
        # Crear botones para imágenes (misma cantidad que números) - MÁS GRANDES
        image_buttons = []
        image_start_x = main_rect.left + (main_rect.width - (len(current_question["images"]) * button_width + 
                            (len(current_question["images"]) - 1) * 20)) // 2
        image_start_y = number_start_y + button_height + 30  # Menor separación para aprovechar espacio
        
        for i, image_name in enumerate(current_question["images"]):
            x = image_start_x + i * (button_width + 20)
            y = image_start_y
            btn = RelationButton(x, y, button_width, button_height, "", True, image_name)
            image_buttons.append(btn)
        
        # Variables para el emparejamiento
        selected_number = None
        selected_image = None
        current_pair = None
        
        question_finished = False
        answer_given = False
        
        # Reiniciar variables de control para nueva pregunta
        show_mechanic_after_delay = False
        mechanic_delay_start = time.time()  # Iniciar contador inmediatamente
        
        # Bucle principal de la pregunta actual
        while not question_finished and running:
            # Verificar si ya pasaron los 5 segundos para mostrar la mecánica automáticamente
            if not show_mechanic_after_delay and time.time() - mechanic_delay_start >= mechanic_delay_duration:
                show_mechanic_after_delay = True
                # Iniciar timer cuando aparece la mecánica
                quiz_timer = Timer(35)
                quiz_timer.start()
            
            # Actualizar timer solo si la mecánica está visible
            if show_mechanic_after_delay:
                quiz_timer.update()
            
            # Verificar si se acabó el tiempo
            if quiz_timer.finished and not answer_given and show_mechanic_after_delay:
                answer_results.append("incorrect")
                flash_color(screen, RED, SCREEN_WIDTH, SCREEN_HEIGHT)
                question_finished = True
                question_index += 1
                continue
            
            screen.blit(background, (0, 0))
            
            # --- DIBUJAR ÁREA DE PREGUNTA (fondo blanco, marco café) ---
            pygame.draw.rect(screen, WHITE, question_rect, border_radius=10)
            pygame.draw.rect(screen, BROWN, question_rect, 3, border_radius=10)
            
            # Dibujar pregunta
            question_lines = current_question["question"].split('\n')
            line_height = title_font.get_height()
            total_text_height = len(question_lines) * line_height
            start_y = question_rect.centery - total_text_height // 2
            
            for i, line in enumerate(question_lines):
                question_text = title_font.render(line, True, BLACK)
                text_rect = question_text.get_rect(center=(question_rect.centerx, start_y + i * line_height))
                screen.blit(question_text, text_rect)
            
            # --- CONTADOR O MECÁNICA SEGÚN EL TIEMPO ---
            if not show_mechanic_after_delay:
                # Mostrar solo el número del contador regresivo centrado
                remaining_time = max(0, mechanic_delay_duration - (time.time() - mechanic_delay_start))
                countdown_text = f"{int(remaining_time)}"  # Solo el número
                
                # Mostrar solo el número del contador, sin texto adicional
                countdown_surf = large_font.render(countdown_text, True, WHITE)  # Fuente más grande para el número
                countdown_rect = countdown_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(countdown_surf, countdown_rect)
            
            # --- MECÁNICA (aparece después de 5 segundos) ---
            else:
                # --- DIBUJAR ÁREA PRINCIPAL (verde obscuro con marco café) ---
                pygame.draw.rect(screen, DARK_GREEN, main_rect, border_radius=15)
                pygame.draw.rect(screen, BROWN, main_rect, 4, border_radius=15)
                
                # Dibujar etiquetas
                numbers_label = medium_font.render("SELECCIONA EL NÚMERO CORRECTO:", True, WHITE)
                images_label = medium_font.render("SELECCIONA LA IMAGEN CORRECTA:", True, WHITE)
                
                screen.blit(numbers_label, (number_start_x, number_start_y - 40))
                screen.blit(images_label, (image_start_x, image_start_y - 40))
                
                # Dibujar todos los botones (fondo blanco con marco café)
                for btn in number_buttons + image_buttons:
                    btn.draw(screen)
                
                # Dibujar línea de conexión si hay un par formado
                if current_pair is not None:
                    num_idx, img_idx = current_pair
                    if num_idx < len(number_buttons) and img_idx < len(image_buttons):
                        start_pos = number_buttons[num_idx].rect.midbottom
                        end_pos = image_buttons[img_idx].rect.midtop
                        pygame.draw.line(screen, GREEN, start_pos, end_pos, 6)
                
                # Dibujar timer en esquina superior derecha (no estorba)
                quiz_timer.draw(screen, timer_font, (SCREEN_WIDTH - 120, 20))
                
                # Dibujar botón de enviar
                submit_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - 80,
                    main_rect.bottom + 80,
                    160, 50
                )
                pygame.draw.rect(screen, GREEN, submit_rect, border_radius=10)
                pygame.draw.rect(screen, BLACK, submit_rect, 2, border_radius=10)
                submit_text = medium_font.render("ENVIAR", True, WHITE)
                submit_text_rect = submit_text.get_rect(center=submit_rect.center)
                screen.blit(submit_text, submit_text_rect)
            
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    # Verificar clic en botón de enviar (solo si la mecánica está visible)
                    if show_mechanic_after_delay and 'submit_rect' in locals() and submit_rect.collidepoint(mouse_pos) and not answer_given:
                        # Verificar si la relación es correcta
                        if current_pair is not None:
                            num_idx, img_idx = current_pair
                            selected_number = current_question["numbers"][num_idx]
                            selected_image_name = current_question["images"][img_idx]
                            correct_number = current_question["correct_answer"]
                            correct_image = current_question["correct_image"]
                            
                            if selected_number == correct_number and selected_image_name == correct_image:
                                score += 1
                                answer_results.append("correct")
                                flash_color(screen, GREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
                            else:
                                answer_results.append("incorrect")
                                flash_color(screen, RED, SCREEN_WIDTH, SCREEN_HEIGHT)
                            
                            answer_given = True
                            question_finished = True
                            question_index += 1
                        else:
                            # Si no hay relación formada, cuenta como incorrecta
                            answer_results.append("incorrect")
                            flash_color(screen, RED, SCREEN_WIDTH, SCREEN_HEIGHT)
                            answer_given = True
                            question_finished = True
                            question_index += 1
                    
                    # Verificar clic en botones de números (solo si la mecánica está visible)
                    if show_mechanic_after_delay:
                        for i, btn in enumerate(number_buttons):
                            if btn.contains_point(mouse_pos) and not answer_given:
                                if selected_number == i:
                                    selected_number = None  # Deseleccionar
                                    current_pair = None
                                else:
                                    selected_number = i
                                    # Si ya hay una imagen seleccionada, formar par inmediatamente
                                    if selected_image is not None:
                                        current_pair = (selected_number, selected_image)
                                        selected_number = None
                                        selected_image = None
                                break
                        
                        # Verificar clic en botones de imágenes (solo si la mecánica está visible)
                        for i, btn in enumerate(image_buttons):
                            if btn.contains_point(mouse_pos) and not answer_given:
                                if selected_image == i:
                                    selected_image = None  # Deseleccionar
                                    current_pair = None
                                else:
                                    selected_image = i
                                    # Si ya hay un número seleccionado, formar par inmediatamente
                                    if selected_number is not None:
                                        current_pair = (selected_number, selected_image)
                                        selected_number = None
                                        selected_image = None
                                break
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    # Determinar si ganó o perdió (4 de 6 aciertos para pasar)
    passed = score >= 4
    show_final_screen(screen, background, score, total_questions, passed, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    return passed

def flash_color(screen, color, screen_width, screen_height):
    flash = pygame.Surface((screen_width, screen_height))
    flash.fill(color)
    flash.set_alpha(150)
    screen.blit(flash, (0, 0))
    pygame.display.flip()
    pygame.time.wait(500)

def show_final_screen(screen, background, score, total, passed, screen_width, screen_height):
    screen.blit(background, (0, 0))
    
    # Crear fuentes para resultados
    large_font = pygame.font.Font(None, screen_height // 10)
    medium_font = pygame.font.Font(None, screen_height // 15)
    small_font = pygame.font.Font(None, screen_height // 25)
    
    # Área de resultados (fondo blanco con marco café)
    result_rect = pygame.Rect(
        screen_width // 10,
        screen_height // 4,
        screen_width * 0.8,
        screen_height // 2
    )
    
    # Dibujar área de resultados
    pygame.draw.rect(screen, WHITE, result_rect, border_radius=15)
    pygame.draw.rect(screen, BROWN, result_rect, 4, border_radius=15)
    
    if passed:
        # Pantalla de victoria
        win_text = large_font.render("¡GANASTE!!", True, GREEN)
        win_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(win_text, win_rect)
        
        score_text = medium_font.render(f"Puntaje: {score}/{total}", True, BLACK)
        score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
        screen.blit(score_text, score_rect)
        
        message_text = medium_font.render("Has superado el nivel 3", True, BLUE)
        message_rect = message_text.get_rect(center=(screen_width // 2, screen_height // 2 + 70))
        screen.blit(message_text, message_rect)
    else:
        # Pantalla de derrota
        lose_text = large_font.render("¡PERDISTE!!", True, RED)
        lose_rect = lose_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(lose_text, lose_rect)
        
        score_text = medium_font.render(f"Puntaje: {score}/{total}", True, BLACK)
        score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
        screen.blit(score_text, score_rect)
        
        message_text = medium_font.render("Necesitas al menos 4 aciertos para pasar", True, BLUE)
        message_rect = message_text.get_rect(center=(screen_width // 2, screen_height // 2 + 70))
        screen.blit(message_text, message_rect)
    
    # Botón para continuar (fondo blanco, letras negras) - Texto adaptado al botón
    continue_rect = pygame.Rect(
        screen_width // 2 - 150,
        screen_height - 120,
        300, 60
    )
    pygame.draw.rect(screen, WHITE, continue_rect, border_radius=15)
    pygame.draw.rect(screen, BLACK, continue_rect, 3, border_radius=15)
    
    # Texto que se adapta al tamaño del botón
    continue_text = small_font.render("Presiona cualquier tecla", True, BLACK)
    continue_text_rect = continue_text.get_rect(center=(continue_rect.centerx, continue_rect.centery - 10))
    screen.blit(continue_text, continue_text_rect)
    
    continue_text2 = small_font.render("para continuar", True, BLACK)
    continue_text_rect2 = continue_text2.get_rect(center=(continue_rect.centerx, continue_rect.centery + 10))
    screen.blit(continue_text2, continue_text_rect2)
    
    pygame.display.flip()
    
    # Esperar a que el usuario presione una tecla
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

if __name__ == "__main__":
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Relaciona Números con Cantidades - Nivel 3")
    run_quiz_with_timer(screen, "Materials/Pictures/Assets/fondon3-Isis_Segura.png")