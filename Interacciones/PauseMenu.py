import pygame
from Interacciones.Settings import SettingsPanel # Reutilizamos la clase de Configuración

# Dimensiones del panel de pausa
PAUSE_PANEL_WIDTH = 600
PAUSE_PANEL_HEIGHT = 500
SLIDE_SPEED = 30 

# Colores (Asegúrate que coincidan con los de Menu.py)
white = (255, 255, 255)
brown = (87, 27, 15)

class PauseMenu:
    def __init__(self, screen, size, font_small, language):
        self.screen = screen
        self.size = size
        self.font_small = font_small
        self.language = language
        
        # Estado de la animación
        self.target_x = (size[0] - PAUSE_PANEL_WIDTH) // 2 
        self.panel_x = -PAUSE_PANEL_WIDTH # Inicialmente fuera de pantalla
        self.is_closing = False
        self.is_open = False # True cuando está completamente abierto
        self.game_paused = False # Bandera principal para el nivel

        # Sub-estado del menú de pausa (para manejar el panel de configuración)
        self.in_config = False
        self.settings_panel = SettingsPanel(screen, size)
        
        # --- IMÁGENES y RECTÁNGULOS del PANEL DE PAUSA ---
        
        # Fondo del panel (reutilizamos la imagen de configuración o creamos una nueva)
        try:
            self.panel_bg_img = pygame.image.load("Materials/Pictures/Assets/fondo_conf.png").convert_alpha()
            self.panel_bg_img = pygame.transform.scale(self.panel_bg_img, (PAUSE_PANEL_WIDTH, PAUSE_PANEL_HEIGHT))
        except pygame.error:
            # Fondo de respaldo
            self.panel_bg_img = pygame.Surface((PAUSE_PANEL_WIDTH, PAUSE_PANEL_HEIGHT), pygame.SRCALPHA)
            self.panel_bg_img.fill((0, 0, 0, 180)) # Negro semi-transparente
            
        # Marco del Título
        self.text_bg = pygame.transform.scale(
            pygame.image.load("Materials/Pictures/Assets/marco_titles.png").convert_alpha(), 
            (PAUSE_PANEL_WIDTH - 100, 80)
        )
        
        # Carga de Botones (debes asegurarte de que estas imágenes existen)
        self.btn_play_1 = pygame.image.load("Materials/Pictures/Assets/btn_play1.png").convert_alpha()
        self.btn_play_3 = pygame.image.load("Materials/Pictures/Assets/btn_play3.png").convert_alpha()
        self.btn_play_2 = pygame.image.load("Materials/Pictures/Assets/btn_play2.png").convert_alpha()
        
        self.btn_reset_1 = pygame.image.load("Materials/Pictures/Assets/btn_reset1.png").convert_alpha()
        self.btn_reset_3 = pygame.image.load("Materials/Pictures/Assets/btn_reset3.png").convert_alpha()
        self.btn_reset_2 = pygame.image.load("Materials/Pictures/Assets/btn_reset2.png").convert_alpha()
        
        self.btn_menu_1 = pygame.image.load("Materials/Pictures/Assets/btn_menu1.png").convert_alpha()
        self.btn_menu_3 = pygame.image.load("Materials/Pictures/Assets/btn_menu3.png").convert_alpha()
        self.btn_menu_2 = pygame.image.load("Materials/Pictures/Assets/btn_menu2.png").convert_alpha()
        
        self.btn_conf_1 = pygame.image.load("Materials/Pictures/Assets/btn_confi1.png").convert_alpha()
        self.btn_conf_3 = pygame.image.load("Materials/Pictures/Assets/btn_confi3.png").convert_alpha()
        self.btn_conf_2 = pygame.image.load("Materials/Pictures/Assets/btn_confi2.png").convert_alpha()
        
        # Rectángulos de botones
        btn_w, btn_h = 190, 80
        center_x = self.size[0] // 2 
        center_y = self.size[1] // 2 
        
        self.play_rect = pygame.Rect(0, 0, btn_w, btn_h); self.play_rect.center = (center_x - 120, center_y - 80)
        self.reset_rect = pygame.Rect(0, 0, btn_w, btn_h); self.reset_rect.center = (center_x + 120, center_y - 80)
        self.menu_rect = pygame.Rect(0, 0, btn_w, btn_h); self.menu_rect.center = (center_x - 120, center_y + 80)
        self.conf_rect = pygame.Rect(0, 0, btn_w, btn_h); self.conf_rect.center = (center_x + 120, center_y + 80)

        self.button_pressed = None

        # Textos
        self.texts = {
            "es": {"title": "JUEGO PAUSADO", "play": "Continuar", "reset": "Reiniciar", "menu": "Menú", "config": "Config"},
            "en": {"title": "GAME PAUSED", "play": "Resume", "reset": "Restart", "menu": "Menu", "config": "Settings"}
        }

    # Función auxiliar para dibujar texto con contorno (copiada de Menu.py)
    def _draw_text_with_outline(self, text, font, text_color, outline_color, offset=3):
        outline_surface = font.render(text, True, outline_color)
        text_surface = font.render(text, True, text_color)
        width = text_surface.get_width() + 2 * offset
        height = text_surface.get_height() + 2 * offset
        final_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        for dx in [-offset, 0, offset]:
            for dy in [-offset, 0, offset]:
                if dx != 0 or dy != 0:
                    final_surface.blit(outline_surface, (dx + offset, dy + offset))
        final_surface.blit(text_surface, (offset, offset))
        return final_surface

    def _draw_button_with_text_3_state(self, rect, text_key, font, mouse_pos, button_id, img_1, img_3, img_2, text_color=white, outline_color=brown, text_adjust_x=-40, text_adjust_y=-5):
        # Lógica para determinar la imagen (1, 2 o 3)
        current_pressed_state = self.button_pressed
        
        if current_pressed_state == button_id:
            image = img_2 
            text_offset_y = 5 
        elif rect.collidepoint(mouse_pos):
            image = img_3 
            text_offset_y = 0 
        else:
            image = img_1 
            text_offset_y = 0 
            
        scaled_img = pygame.transform.scale(image, (rect.width, rect.height))
        self.screen.blit(scaled_img, rect)
        
        text_content = self.texts[self.language].get(text_key, text_key)
        if text_content:
            text_surface = self._draw_text_with_outline(text_content, font, text_color, outline_color)
            
            text_rect = text_surface.get_rect(
                center=(
                    rect.center[0] + text_adjust_x,             
                    rect.center[1] + text_adjust_y + text_offset_y
                )
            )
            self.screen.blit(text_surface, text_rect)

    def handle_events(self, event):
        """Procesa los eventos dentro del menú de pausa. Retorna una acción."""
        if not self.game_paused and self.panel_x == -PAUSE_PANEL_WIDTH:
            return "none" # No procesar si no está en pausa

        if self.in_config:
            # Si estamos en el submenú de configuración, delegamos el evento
            language, volume_level, action = self.settings_panel.update_logic(event, self.language, self.settings_panel.volume_level, self.settings_panel.panel_x)
            
            # Actualizamos el idioma y volumen para Level1F si es necesario
            self.language = language
            self.settings_panel.language = language
            pygame.mixer.music.set_volume(volume_level)

            if action == "CLOSE":
                self.settings_panel.config_closing = True # Inicia animación de cierre de config
            return "none"
        
        # Lógica del menú principal de pausa
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.play_rect.collidepoint(mouse_pos): self.button_pressed = "play"
            elif self.reset_rect.collidepoint(mouse_pos): self.button_pressed = "reset"
            elif self.menu_rect.collidepoint(mouse_pos): self.button_pressed = "menu"
            elif self.conf_rect.collidepoint(mouse_pos): self.button_pressed = "config"

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.button_pressed:
            mouse_pos = event.pos
            action = "none"
            
            if self.button_pressed == "play" and self.play_rect.collidepoint(mouse_pos):
                action = "resume"
            elif self.button_pressed == "reset" and self.reset_rect.collidepoint(mouse_pos):
                action = "reset"
            elif self.button_pressed == "menu" and self.menu_rect.collidepoint(mouse_pos):
                action = "menu"
            elif self.button_pressed == "config" and self.conf_rect.collidepoint(mouse_pos):
                self.in_config = True
                self.settings_panel.panel_x = -PAUSE_PANEL_WIDTH
                self.settings_panel.config_closing = False
                action = "none"

            self.button_pressed = None
            return action
        
        return "none"

    def update(self):
        """Actualiza la animación del panel y el submenú de configuración."""
        
        if self.in_config:
            # Lógica de animación del panel de configuración dentro de la pausa
            if self.settings_panel.config_closing:
                self.settings_panel.panel_x = max(-PAUSE_PANEL_WIDTH, self.settings_panel.panel_x - SLIDE_SPEED)
                if self.settings_panel.panel_x <= -PAUSE_PANEL_WIDTH:
                    self.settings_panel.panel_x = -PAUSE_PANEL_WIDTH
                    self.settings_panel.config_closing = False
                    self.in_config = False # Vuelve al menú de pausa principal
            else:
                self.settings_panel.panel_x = min(self.target_x, self.settings_panel.panel_x + SLIDE_SPEED)

        elif self.game_paused:
            # Animación de entrada: deslizar hacia la derecha hasta el centro
            if not self.is_open:
                self.panel_x = min(self.target_x, self.panel_x + SLIDE_SPEED)
                if self.panel_x == self.target_x:
                    self.is_open = True
        
        elif self.is_closing:
            # Animación de salida: deslizar hacia la izquierda
            self.panel_x = max(-PAUSE_PANEL_WIDTH, self.panel_x - SLIDE_SPEED)
            if self.panel_x <= -PAUSE_PANEL_WIDTH:
                self.panel_x = -PAUSE_PANEL_WIDTH
                self.is_closing = False
                self.is_open = False
                
        return self.game_paused

    def draw(self, mouse_pos):
        """Dibuja el panel de pausa y sus elementos."""
        
        if not self.game_paused and not self.is_closing:
            return

        # 1. Dibuja el fondo del panel
        panel_rect = self.panel_bg_img.get_rect(topleft=(self.panel_x, self.size[1] // 2 - PAUSE_PANEL_HEIGHT // 2))
        self.screen.blit(self.panel_bg_img, panel_rect)

        # Si el panel de configuración está abierto, no dibujar los botones principales
        if self.in_config or self.settings_panel.config_closing:
            self.settings_panel.draw(self.language, self.settings_panel.volume_level, mouse_pos, self.settings_panel.panel_x)
            return
            
        # 2. Dibuja el Título
        title_surface = self._draw_text_with_outline(self.texts[self.language]["title"], self.font_small, white, brown)
        title_bg_rect = self.text_bg.get_rect(center=(panel_rect.centerx, panel_rect.y + 45))
        self.screen.blit(self.text_bg, title_bg_rect)
        self.screen.blit(title_surface, title_surface.get_rect(center=title_bg_rect.center))

        # 3. Dibuja los 4 botones
        self._draw_button_with_text_3_state(self.play_rect, "play", self.font_small, mouse_pos, "play", self.btn_play_1, self.btn_play_3, self.btn_play_2, text_adjust_x=-41)
        self._draw_button_with_text_3_state(self.reset_rect, "reset", self.font_small, mouse_pos, "reset", self.btn_reset_1, self.btn_reset_3, self.btn_reset_2, text_adjust_x=-41)
        self._draw_button_with_text_3_state(self.menu_rect, "menu", self.font_small, mouse_pos, "menu", self.btn_menu_1, self.btn_menu_3, self.btn_menu_2, text_adjust_x=-41)
        self._draw_button_with_text_3_state(self.conf_rect, "config", self.font_small, mouse_pos, "config", self.btn_conf_1, self.btn_conf_3, self.btn_conf_2, text_adjust_x=-41)

    # --- Métodos de control externo ---
    def toggle_pause(self):
        """Activa o desactiva la pausa e inicia las animaciones."""
        if not self.game_paused:
            # Pausar: Inicia la animación de entrada
            self.game_paused = True
            self.is_closing = False
            self.is_open = False
            self.panel_x = -PAUSE_PANEL_WIDTH
            pygame.mixer.music.pause()
        elif self.game_paused and not self.in_config:
            # Reanudar: Inicia la animación de salida
            self.is_closing = True
            self.game_paused = False
            pygame.mixer.music.unpause()