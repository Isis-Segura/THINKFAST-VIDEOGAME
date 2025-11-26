import pygame
import sys

# Definimos el ancho y alto del panel (para centrar y animar)
PANEL_WIDTH = 700
PANEL_HEIGHT = 650

class SettingsPanel: 
    """
    Panel de Configuración que maneja el dibujo de todos los elementos 
    y la lógica de eventos de volumen/idioma.
    """
    def __init__(self, screen, size):
        self.screen = screen
        self.size = size
        self.width = size[0]
        self.height = size[1]
        
        # --- COLORES ---
        self.white = (255, 255, 255)
        self.brown = (87, 27, 15)
        self.pink = (255, 182, 193)
        self.black = (0, 0, 0)

        # --- FUENTES ---
        try:
            self.font_medium = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 28)
            self.font_small = pygame.font.Font("Materials/Fonts/PressStart2P-Regular.ttf", 18)
        except:
            self.font_medium = pygame.font.Font(None, 40)
            self.font_small = pygame.font.Font(None, 30)

        # --- TEXTOS ---
        self.texts = {
            "es": {
                "title_config": "Menú de Configuración", "language": "Idioma", 
                "volume": "Volumen"
            },
            "en": {
                "title_config": "Settings Menu", "language": "Language", 
                "volume": "Volume"
            }
        }

        # --- CARGA de IMÁGENES ---
        try:
            # Fondo del Panel de Configuración (fondo_conf)
            self.panel_bg_img = pygame.image.load("Materials/Pictures/Assets/fondo_conf.png").convert_alpha()
            self.panel_bg_img = pygame.transform.scale(self.panel_bg_img, (PANEL_WIDTH, PANEL_HEIGHT))
        except pygame.error:
            print("ADVERTENCIA: No se encontró 'fondo_conf.png'. Usando color sólido.")
            self.panel_bg_img = pygame.Surface((PANEL_WIDTH, PANEL_HEIGHT), pygame.SRCALPHA)
            self.panel_bg_img.fill((100, 100, 200, 230)) # Color de respaldo semi-transparente

        self.text_bg = pygame.transform.scale(pygame.image.load("Materials/Pictures/Assets/marco_titles.png").convert_alpha(), (PANEL_WIDTH - 50, 80))

        # Botones Idioma
        self.btn_sp_1 = pygame.image.load("Materials/Pictures/Assets/btn_spanish1.png").convert_alpha()
        self.btn_sp_2 = pygame.image.load("Materials/Pictures/Assets/btn_spanish2.png").convert_alpha()
        self.btn_sp_3 = pygame.image.load("Materials/Pictures/Assets/btn_spanish3.png").convert_alpha()
        
        self.btn_en_1 = pygame.image.load("Materials/Pictures/Assets/btn_english1.png").convert_alpha()
        self.btn_en_2 = pygame.image.load("Materials/Pictures/Assets/btn_english2.png").convert_alpha()
        self.btn_en_3 = pygame.image.load("Materials/Pictures/Assets/btn_english3.png").convert_alpha()

        # Botones Volumen y Slider
        self.btn_plus_1 = pygame.image.load("Materials/Pictures/Assets/btn_mas1.png").convert_alpha()
        self.btn_plus_2 = pygame.image.load("Materials/Pictures/Assets/btn_mas2.png").convert_alpha()
        self.btn_plus_3 = pygame.image.load("Materials/Pictures/Assets/btn_mas3.png").convert_alpha()
        self.btn_minus_1 = pygame.image.load("Materials/Pictures/Assets/btn_menos1.png").convert_alpha()
        self.btn_minus_2 = pygame.image.load("Materials/Pictures/Assets/btn_menos2.png").convert_alpha()
        self.btn_minus_3 = pygame.image.load("Materials/Pictures/Assets/btn_menos3.png").convert_alpha()
        self.thumb_1 = pygame.image.load("Materials/Pictures/Assets/btn_subir_bajar1.png").convert_alpha()
        self.thumb_2 = pygame.image.load("Materials/Pictures/Assets/btn_subir_bajar2.png").convert_alpha()
        self.thumb_3 = pygame.image.load("Materials/Pictures/Assets/btn_subir_bajar3.png").convert_alpha()

        # Botón Back
        self.btn_back_1 = pygame.image.load("Materials/Pictures/Assets/btn_back1.png").convert_alpha()
        self.btn_back_2 = pygame.image.load("Materials/Pictures/Assets/btn_back2.png").convert_alpha()
        self.btn_back_3 = pygame.image.load("Materials/Pictures/Assets/btn_back3.png").convert_alpha()

        # --- POSICIONES RELATIVAS DENTRO DEL PANEL ---
        self.panel_y = (self.height - PANEL_HEIGHT) // 2
        internal_cx = PANEL_WIDTH // 2
        
        # Puntos de referencia internos
        self.title_y = 50
        self.lang_y = 150
        self.vol_y = 300
        
        # Idiomas
        self.sp_rect_local = pygame.Rect(0, 0, 140, 70); self.sp_rect_local.center = (internal_cx - 80, self.lang_y + 60)
        self.en_rect_local = pygame.Rect(0, 0, 140, 70); self.en_rect_local.center = (internal_cx + 80, self.lang_y + 60)

        # Volumen
        self.slider_rect_area_local = pygame.Rect(internal_cx - 200, self.vol_y + 40, 400, 20)
        self.minus_rect_local = pygame.Rect(0, 0, 85, 55); self.minus_rect_local.center = (internal_cx - 150, self.vol_y + 100)
        self.plus_rect_local = pygame.Rect(0, 0, 85, 55); self.plus_rect_local.center = (internal_cx + 150, self.vol_y + 100)

        # Botón Back
        self.back_rect_local = pygame.Rect(0, 0, 160, 80); self.back_rect_local.center = (internal_cx, PANEL_HEIGHT - 70)
        
        # Control de estado interno
        self.dragging_volume = False
        self.button_pressed = None

    # --- HELPERS INTERNOS ---
    def render_text_outline(self, text, font, color, outline_color, pos, offset_x):
        # ... (Lógica para dibujar texto con contorno, sin cambios)
        outline = font.render(text, True, outline_color)
        txt = font.render(text, True, color)
        off = 3
        surf = pygame.Surface((txt.get_width() + off*2, txt.get_height() + off*2), pygame.SRCALPHA)
        for dx in [-off, 0, off]:
            for dy in [-off, 0, off]:
                if dx or dy: surf.blit(outline, (dx+off, dy+off))
        surf.blit(txt, (off, off))
        rect = surf.get_rect(center=(pos[0] + offset_x, pos[1] + self.panel_y))
        self.screen.blit(surf, rect)

    def draw_3_state(self, rect, img1, img3, img2, mouse_pos, my_id, offset_x):
        # Lógica para dibujar el botón con los 3 estados
        local_mouse_pos = (mouse_pos[0] - offset_x, mouse_pos[1] - self.panel_y)
        collision_rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height)

        if self.button_pressed == my_id: img = img2
        elif collision_rect.collidepoint(local_mouse_pos): img = img3
        else: img = img1
            
        scaled = pygame.transform.scale(img, (rect.width, rect.height))
        self.screen.blit(scaled, (rect.x + offset_x, rect.y + self.panel_y))
        return pygame.Rect(rect.x + offset_x, rect.y + self.panel_y, rect.width, rect.height)


    # --- LÓGICA DE EVENTOS (UPDATE) ---
    def update_logic(self, event, current_language, current_volume, offset_x):
        
        lang = current_language
        vol = current_volume
        action = None # Acción a devolver (ej: "CLOSE")
        
        # Rectángulos globales para colisión (necesitan la posición actual del panel)
        panel_rect = pygame.Rect(offset_x, self.panel_y, PANEL_WIDTH, PANEL_HEIGHT)
        sp_rect_global = pygame.Rect(self.sp_rect_local.x + offset_x, self.sp_rect_local.y + self.panel_y, self.sp_rect_local.width, self.sp_rect_local.height)
        en_rect_global = pygame.Rect(self.en_rect_local.x + offset_x, self.en_rect_local.y + self.panel_y, self.en_rect_local.width, self.en_rect_local.height)
        minus_rect_global = pygame.Rect(self.minus_rect_local.x + offset_x, self.minus_rect_local.y + self.panel_y, self.minus_rect_local.width, self.minus_rect_local.height)
        plus_rect_global = pygame.Rect(self.plus_rect_local.x + offset_x, self.plus_rect_local.y + self.panel_y, self.plus_rect_local.width, self.plus_rect_local.height)
        back_rect_global = pygame.Rect(self.back_rect_local.x + offset_x, self.back_rect_local.y + self.panel_y, self.back_rect_local.width, self.back_rect_local.height)
        slider_rect_global = pygame.Rect(self.slider_rect_area_local.x + offset_x, self.slider_rect_area_local.y + self.panel_y, self.slider_rect_area_local.width, self.slider_rect_area_local.height)
        
        if event.type == pygame.MOUSEBUTTONDOWN and panel_rect.collidepoint(event.pos):
            if back_rect_global.collidepoint(event.pos): self.button_pressed = "back"
            elif sp_rect_global.collidepoint(event.pos): self.button_pressed = "es"
            elif en_rect_global.collidepoint(event.pos): self.button_pressed = "en"
            elif minus_rect_global.collidepoint(event.pos): self.button_pressed = "minus"
            elif plus_rect_global.collidepoint(event.pos): self.button_pressed = "plus"
            elif slider_rect_global.collidepoint(event.pos): self.dragging_volume = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.button_pressed == "back" and back_rect_global.collidepoint(event.pos):
                action = "CLOSE" # Indica que debe comenzar la animación de cierre
            elif self.button_pressed == "es": lang = "es"
            elif self.button_pressed == "en": lang = "en"
            elif self.button_pressed == "minus": 
                vol = max(0.0, vol - 0.1)
            elif self.button_pressed == "plus": 
                vol = min(1.0, vol + 0.1)
            
            self.button_pressed = None
            self.dragging_volume = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging_volume:
            rel_x = event.pos[0] - slider_rect_global.left
            vol = max(0.0, min(1.0, rel_x / slider_rect_global.width))

        # Aplica volumen inmediatamente para feedback
        if vol != current_volume:
            pygame.mixer.music.set_volume(vol)
            
        return lang, vol, action


    # --- DIBUJO (DRAW) ---
    def draw(self, lang, vol, mouse_pos, offset_x):
        internal_cx = PANEL_WIDTH // 2
        
        # 1. Fondo del Panel (dibuja el fondo deslizante)
        panel_draw_pos = (offset_x, self.panel_y)
        self.screen.blit(self.panel_bg_img, panel_draw_pos)
        
        # 2. Título
        title_pos = (internal_cx, self.title_y)
        bg_rect = self.text_bg.get_rect(center=(title_pos[0] + offset_x, title_pos[1] + self.panel_y))
        self.screen.blit(self.text_bg, bg_rect.topleft)
        self.render_text_outline(self.texts[lang]["title_config"], self.font_medium, self.white, self.brown, title_pos, offset_x)

        # 3. Idioma
        self.render_text_outline(f"{self.texts[lang]['language']}:", self.font_medium, self.white, self.brown, (internal_cx, self.lang_y), offset_x)
        
        # Botones Idioma
        if lang == "es": sp_img = self.btn_sp_2
        elif self.button_pressed == "es": sp_img = self.btn_sp_2
        elif self.sp_rect_local.collidepoint(mouse_pos[0] - offset_x, mouse_pos[1] - self.panel_y): sp_img = self.btn_sp_3
        else: sp_img = self.btn_sp_1
        scaled = pygame.transform.scale(sp_img, (self.sp_rect_local.width, self.sp_rect_local.height))
        self.screen.blit(scaled, (self.sp_rect_local.x + offset_x, self.sp_rect_local.y + self.panel_y))

        if lang == "en": en_img = self.btn_en_2
        elif self.button_pressed == "en": en_img = self.btn_en_2
        elif self.en_rect_local.collidepoint(mouse_pos[0] - offset_x, mouse_pos[1] - self.panel_y): en_img = self.btn_en_3
        else: en_img = self.btn_en_1
        scaled = pygame.transform.scale(en_img, (self.en_rect_local.width, self.en_rect_local.height))
        self.screen.blit(scaled, (self.en_rect_local.x + offset_x, self.en_rect_local.y + self.panel_y))

        # 4. Volumen
        vol_pct = int(vol * 100)
        self.render_text_outline(f"{self.texts[lang]['volume']}: {vol_pct}%", self.font_medium, self.white, self.brown, (internal_cx, self.vol_y), offset_x)

        # Slider Bar
        slider_rect_global = pygame.Rect(self.slider_rect_area_local.x + offset_x, self.slider_rect_area_local.y + self.panel_y, self.slider_rect_area_local.width, self.slider_rect_area_local.height)
        pygame.draw.rect(self.screen, (200,200,200), slider_rect_global, border_radius=10)
        fill_w = int(self.slider_rect_area_local.width * vol)
        pygame.draw.rect(self.screen, self.pink, (slider_rect_global.x, slider_rect_global.y, fill_w, 20), border_radius=10)
        pygame.draw.rect(self.screen, self.black, slider_rect_global, 2, border_radius=10)

        # Slider Thumb
        thumb_x = self.slider_rect_area_local.x + fill_w + offset_x
        thumb_rect = pygame.Rect(0, 0, 50, 35)
        thumb_rect.center = (thumb_x, slider_rect_global.centery)
        
        if self.dragging_volume: th_img = self.thumb_2
        elif thumb_rect.collidepoint(mouse_pos): th_img = self.thumb_3
        else: th_img = self.thumb_1
        self.screen.blit(pygame.transform.scale(th_img, (thumb_rect.width, thumb_rect.height)), thumb_rect)

        # Botones +/-
        self.draw_3_state(self.minus_rect_local, self.btn_minus_1, self.btn_minus_3, self.btn_minus_2, mouse_pos, "minus", offset_x)
        self.draw_3_state(self.plus_rect_local, self.btn_plus_1, self.btn_plus_3, self.btn_plus_2, mouse_pos, "plus", offset_x)

        # 5. Botón Regresar
        self.draw_3_state(self.back_rect_local, self.btn_back_1, self.btn_back_3, self.btn_back_2, mouse_pos, "back", offset_x)