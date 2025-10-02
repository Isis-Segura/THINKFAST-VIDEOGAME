import pygame 
import math
import sys 

class Timer:
    def __init__(self, total_seconds):
        self.total_seconds = total_seconds
        self.start_ticks = None
        self.finished = False
        
        # --- COLORES DEL DISEÑO (Cian Brillante) ---
        self.primary_orange = (0, 255, 255)       
        self.white = (255, 255, 255)       
        self.dark_gray = (50, 50, 50)      
        self.gradient_end = (0, 200, 200)  
        
        # COLORES DE ADVERTENCIA PERSONALIZADOS PARA EL QUIZ
        self.quiz_color_low_warning = (255, 140, 0)   # Naranja Oscuro (5 y 4 seg)
        # El Rojo Brillante se usará para 3, 2 y 1 seg.
        self.quiz_color_danger = (255, 0, 0)   

    def start(self):
        self.start_ticks = pygame.time.get_ticks()
        self.finished = False

    def update(self):
        if self.start_ticks is None:
            return self.total_seconds

        elapsed_ticks = pygame.time.get_ticks() - self.start_ticks
        elapsed_seconds = elapsed_ticks // 1000
        remaining = self.total_seconds - elapsed_seconds
        
        if remaining <= 0:
            self.finished = True
            return 0
        return remaining

    def draw(self, screen, font, is_quiz_timer=False, position=(560, 10)): 
        remaining = self.update()
        
        # --- Calcular la posición principal del cronómetro ---
        timer_radius = 40 
        timer_center_x = position[0] + timer_radius 
        timer_center_y = position[1] + timer_radius + 10

        # --- DIBUJAR LA SOMBRA GENERAL ---
        shadow_offset = 5
        pygame.draw.circle(screen, self.dark_gray, (timer_center_x + shadow_offset, timer_center_y + shadow_offset), timer_radius + 2)

        # --- DIBUJAR EL CRONÓMETRO ---
        pygame.draw.circle(screen, self.primary_orange, (timer_center_x, timer_center_y), timer_radius)
        
        # Botones superiores
        button_radius = 10
        pygame.draw.circle(screen, self.primary_orange, (timer_center_x - timer_radius * 0.5, timer_center_y - timer_radius - button_radius + 5), button_radius)
        pygame.draw.circle(screen, self.primary_orange, (timer_center_x + timer_radius * 0.5, timer_center_y - timer_radius - button_radius + 5), button_radius)

        # Cara del reloj (blanco)
        face_radius = timer_radius - 8 
        pygame.draw.circle(screen, self.white, (timer_center_x, timer_center_y), face_radius)

        # --- DIBUJAR SECTOR DE TIEMPO (RELLENO Y VACÍO) ---
        total_seconds_display = self.total_seconds if self.total_seconds > 0 else 1 
        percentage_remaining = remaining / total_seconds_display
        
        angle_start = 90
        angle_end = 90 - (360 * percentage_remaining) 
        
        fill_color = self.gradient_end 
        if remaining > 0 and percentage_remaining < 1.0: 
              pygame.draw.arc(screen, fill_color, 
                              (timer_center_x - face_radius, timer_center_y - face_radius, face_radius * 2, face_radius * 2), 
                              math.radians(angle_end), math.radians(angle_start), face_radius)
              
              pygame.draw.polygon(screen, fill_color, 
                              [ (timer_center_x, timer_center_y),
                                (timer_center_x + face_radius * math.cos(math.radians(angle_start)), timer_center_y - face_radius * math.sin(math.radians(angle_start))),
                                (timer_center_x + face_radius * math.cos(math.radians(angle_end)), timer_center_y - face_radius * math.sin(math.radians(angle_end))) ] )
        
        if percentage_remaining < 1.0:
            elapsed_angle_start = 90 - (360 * percentage_remaining)
            elapsed_angle_end = 90 - 360 
            
            if elapsed_angle_end < elapsed_angle_start: 
                pygame.draw.arc(screen, (200, 200, 200), 
                                (timer_center_x - face_radius, timer_center_y - face_radius, face_radius * 2, face_radius * 2), 
                                math.radians(elapsed_angle_end), math.radians(elapsed_angle_start), face_radius)

        # Centro del cronómetro 
        pygame.draw.circle(screen, self.primary_orange, (timer_center_x, timer_center_y), 3)

        # --- DIBUJAR LA ETIQUETA DE TIEMPO Y MANEJAR COLOR DE TEXTO ---
        
        if is_quiz_timer and self.total_seconds <= 60:
            time_str = f"{remaining}"
            unit_str = "Segundos" if remaining != 1 else "Segundo"
        else:
            minutes = remaining // 60
            seconds = remaining % 60
            time_str = f"{minutes:02}:{seconds:02}"
            unit_str = "" 
        
        # Texto por defecto (NEGRO)
        tag_text_color = (0, 0, 0)
        
        if is_quiz_timer:
            # 🛑 3, 2 y 1 segundos: ROJO (Lógica simplificada a "menor o igual a 3")
            if remaining <= 3:
                tag_text_color = self.quiz_color_danger 
            elif remaining <= 5:
                # 5 y 4 segundos: NARANJA OSCURO
                tag_text_color = self.quiz_color_low_warning
            # De 10 a 6 segundos usa el color negro por defecto.
 
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
        shadow_rect_tag = pygame.Rect(tag_rect.x + shadow_offset, tag_rect.y + shadow_offset, tag_rect.width, tag_rect.height)
        pygame.draw.rect(screen, self.dark_gray, shadow_rect_tag, border_radius=int(tag_height / 2))
        pygame.draw.rect(screen, self.primary_orange, tag_rect, border_radius=int(tag_height / 2))

        number_rect = number_surface.get_rect(center=(tag_rect.centerx, tag_rect.centery - (unit_surface.get_height() // 2 if unit_str else 0)))
        screen.blit(number_surface, number_rect)
        
        if unit_str:
            unit_rect = unit_surface.get_rect(center=(tag_rect.centerx, tag_rect.centery + number_surface.get_height() // 2 - 5))
            screen.blit(unit_surface, unit_rect)

    def reset(self):
        self.start_ticks = None
        self.finished = False