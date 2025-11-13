import pygame 
import math 
import sys 

class Timer: 
    def __init__(self, total_seconds): 
        self.total_seconds = total_seconds 
        self.start_ticks = None 
        self.finished = False 
        
        # --- LÓGICA DE PAUSA ---
        self.paused = False 
        self.pause_ticks = 0 
        # ---------------------------------
        
        # --- COLORES --- 
        self.primary_orange = (0, 255, 255) 
        self.white = (255, 255, 255) 
        self.dark_gray = (50, 50, 50) 
        self.gradient_end = (0, 200, 200) 
        self.black = (0, 0, 0) 
        
        # COLORES DE ADVERTENCIA PARA EL QUIZ 
        self.quiz_color_low_warning = (255, 140, 0) 
        self.quiz_color_danger = (255, 0, 0) 

    # ----------------------------------------------------------------------
    # MÉTODOS DE CONTROL DE ESTADO
    # ----------------------------------------------------------------------
    def pause(self): 
        """Detiene el cronómetro y guarda el tiempo transcurrido.""" 
        if not self.paused and self.start_ticks is not None: 
            elapsed_ticks = pygame.time.get_ticks() - self.start_ticks 
            self.pause_ticks = elapsed_ticks 
            self.paused = True 

    def unpause(self): 
        """Reanuda el cronómetro.""" 
        if self.paused: 
            self.start_ticks = pygame.time.get_ticks() - self.pause_ticks 
            self.paused = False 
            self.pause_ticks = 0 

    def start(self): 
        self.start_ticks = pygame.time.get_ticks() 
        self.finished = False 
        self.paused = False 
        self.pause_ticks = 0

    def is_running(self):
        """Retorna True si el temporizador está activo (iniciado, no pausado y no terminado)."""
        return self.start_ticks is not None and not self.paused and not self.finished

    def update(self): 
        if self.start_ticks is None or self.paused: 
            if self.start_ticks is None: 
                return self.total_seconds 
            
            elapsed_seconds = self.pause_ticks // 1000 
            remaining = self.total_seconds - elapsed_seconds 
            return max(0, remaining) 

        elapsed_ticks = pygame.time.get_ticks() - self.start_ticks 
        elapsed_seconds = elapsed_ticks // 1000 
        remaining = self.total_seconds - elapsed_seconds 
        
        if remaining <= 0: 
            self.finished = True 
            return 0 
        return remaining

    def reset(self):
        """Reinicia el temporizador sin iniciarlo."""
        self.start_ticks = None
        self.finished = False
        self.paused = False
        self.pause_ticks = 0

    # ----------------------------------------------------------------------
    # MÉTODO DRAW (Dibuja el temporizador)
    # ----------------------------------------------------------------------
    # 🚨 CORRECCIÓN DEFINITIVA: SE AGREGA 'color=None' A LA FIRMA 🚨
    def draw(self, screen, font, is_quiz_timer=False, position=(560, 10), color=None): 
        remaining = self.update() if not self.paused else self.total_seconds - (self.pause_ticks // 1000)

        # ------------------------------------------------------------------
        # LÓGICA DE DIBUJO SIMPLE PARA PANTALLA DE CONTROLES
        # (Esto se activa si color se pasa, como en Level1F.py)
        # ------------------------------------------------------------------
        if not is_quiz_timer and color is not None:
            # Formato M:SS
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            formatted_time = f"{minutes:01d}:{seconds:02d}"

            text_color = color
            
            # Renderizado
            text_surface = font.render(formatted_time, True, text_color)
            text_rect = text_surface.get_rect(center=position)
            
            # Dibuja una sombra simple para mejorar la visibilidad
            shadow_color = (0, 0, 0)
            shadow_surface = font.render(formatted_time, True, shadow_color)
            screen.blit(shadow_surface, text_rect.move(2, 2)) 
            
            screen.blit(text_surface, text_rect)
            return
        
        # ------------------------------------------------------------------
        # LÓGICA DE DIBUJO COMPLEJA PARA EL QUIZ (CÓDIGO ORIGINAL DEL USUARIO)
        # ------------------------------------------------------------------

        # --- Calcular parámetros de dibujo ---
        timer_radius = 40 
        timer_center_x = position[0] + timer_radius 
        timer_center_y = position[1] + timer_radius + 10
        face_radius = timer_radius - 8 

        # --- DIBUJAR MARCO Y FONDO ---
        shadow_offset = 5
        pygame.draw.circle(screen, self.dark_gray, (timer_center_x + shadow_offset, timer_center_y + shadow_offset), timer_radius + 2)
        pygame.draw.circle(screen, self.primary_orange, (timer_center_x, timer_center_y), timer_radius)
        
        # Botones superiores
        button_radius = 10
        pygame.draw.circle(screen, self.primary_orange, (timer_center_x - timer_radius * 0.5, timer_center_y - timer_radius - button_radius + 5), button_radius)
        pygame.draw.circle(screen, self.primary_orange, (timer_center_x + timer_radius * 0.5, timer_center_y - timer_radius - button_radius + 5), button_radius)

        # Cara del reloj (fondo del tiempo consumido - Blanco o Advertencia)
        elapsed_color = self.white 
        if is_quiz_timer and remaining <= 5:
            elapsed_color = self.quiz_color_danger if remaining <= 3 else self.quiz_color_low_warning
            
        pygame.draw.circle(screen, elapsed_color, (timer_center_x, timer_center_y), face_radius)

        # --- DIBUJAR SECTOR DE TIEMPO RESTANTE (RELLENO CIAN) ---
        total_seconds_display = self.total_seconds if self.total_seconds > 0 else 1 
        percentage_remaining = remaining / total_seconds_display
        
        angle_start = 90  
        angle_end = 90 - (360 * percentage_remaining) 
        fill_color = self.gradient_end 
        
        if remaining > 0 and percentage_remaining < 1.0: 
            
            # 1. Lógica para crear los puntos del polígono de relleno
            points = [
                (timer_center_x, timer_center_y), 
            ]
            
            # Iterar y agregar puntos para dibujar el arco (relleno suave)
            start_range = int(angle_end)
            end_range = int(angle_start) + 1 
            
            for angle in range(start_range, end_range):
                rad = math.radians(angle)
                x = timer_center_x + face_radius * math.cos(rad)
                y = timer_center_y - face_radius * math.sin(rad)
                points.append((int(x), int(y)))

            # 2. Dibujar el polígono de relleno
            if len(points) > 2:
                pygame.draw.polygon(screen, fill_color, points)

            # --- DIBUJAR AGUJA SEPARADORA ---
            needle_angle = angle_end
            end_x = timer_center_x + face_radius * math.cos(math.radians(needle_angle))
            end_y = timer_center_y - face_radius * math.sin(math.radians(needle_angle))
            pygame.draw.line(screen, (30, 30, 30), (timer_center_x, timer_center_y), (int(end_x), int(end_y)), 3)

        # Centro del cronómetro 
        pygame.draw.circle(screen, self.primary_orange, (timer_center_x, timer_center_y), 3)

        # --- DIBUJAR LA ETIQUETA DE TIEMPO Y MANEJAR COLOR DE TEXTO ---
        
        if is_quiz_timer and self.total_seconds <= 60:
            time_str = f"{int(remaining)}" 
            unit_str = "Segundos" if remaining != 1 else "Segundo"
        else:
            minutes = int(remaining) // 60
            seconds = int(remaining) % 60
            time_str = f"{minutes:02}:{seconds:02}"
            unit_str = "" 
        
        # Color del texto por defecto NEGRO
        tag_text_color = self.black 

        # Si el control es el del quiz, aplica los colores de advertencia
        if is_quiz_timer:
            # Sobrescribe el color si es tiempo de advertencia (5, 4, 3, 2, 1)
            if remaining <= 3:
                tag_text_color = self.quiz_color_danger 
            elif remaining <= 5:
                tag_text_color = self.quiz_color_low_warning
    
        font_large = pygame.font.Font(None, font.get_height() + 10) 
        font_small = pygame.font.Font(None, font.get_height() - 5) 

        number_surface = font_large.render(time_str, True, tag_text_color)
        unit_surface = font_small.render(unit_str, True, tag_text_color)

        tag_padding_x = 25
        tag_padding_y = 15
        
        total_text_width = max(number_surface.get_width(), unit_surface.get_width() if unit_str else 0)
        min_tag_width = 120
        min_tag_height = 80
        
        tag_width = max(min_tag_width, total_text_width + tag_padding_x * 2)
        tag_height = max(min_tag_height, number_surface.get_height() + unit_surface.get_height() + tag_padding_y * 2 - 10)

        tag_x = timer_center_x + timer_radius + 5 
        tag_y = timer_center_y - tag_height // 2 

        tag_rect = pygame.Rect(tag_x, tag_y, tag_width, tag_height)
        
        shadow_offset = 5 
        shadow_rect_tag = pygame.Rect(tag_rect.x + shadow_offset, tag_rect.y + shadow_offset, tag_rect.width, tag_height)
        pygame.draw.rect(screen, self.dark_gray, shadow_rect_tag, border_radius=int(tag_height / 2))
        pygame.draw.rect(screen, self.primary_orange, tag_rect, border_radius=int(tag_height / 2))

        number_rect = number_surface.get_rect(center=(tag_rect.centerx, tag_rect.centery - (unit_surface.get_height() // 2 if unit_str else 0)))
        screen.blit(number_surface, number_rect)
        
        if unit_str:
            unit_rect = unit_surface.get_rect(center=(tag_rect.centerx, tag_rect.centery + number_surface.get_height() // 2 - 5))
            screen.blit(unit_surface, unit_rect)