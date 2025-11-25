import pygame
import random
import os
import time
from Personajes.boy import Characterb
from Personajes.girl import Characterg
from Personajes.Prefect import Characternpcp 
from Interacciones.Controldeobjetos.velotex import TypewriterText
from Interacciones.Controldeobjetos.timer2 import Timer

# --- COLORES Y CONFIGURACIÓN ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
BLUE = (0, 100, 255)
RED = (200, 0, 0)

MIXER_INITIALIZED = False
try:
    pygame.mixer.init()
    MIXER_INITIALIZED = True
except pygame.error:
    pass

# ============================================================
# CLASE RELATION BUTTON
# ============================================================
class RelationButton:
    def __init__(self, x, y, width, height, text, is_image=False, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_image = is_image
        self.image = None
        self.selected = False
        
        if is_image and image_path:
            try:
                full_path = os.path.join("Materials", "Pictures", "Assets", image_path)
                if os.path.exists(full_path):
                    self.image = pygame.image.load(full_path).convert_alpha()
                    img_ratio = self.image.get_width() / self.image.get_height()
                    if img_ratio > 1:
                        new_width = width - 10
                        new_height = new_width / img_ratio
                    else:
                        new_height = height - 10
                        new_width = new_height * img_ratio
                    self.image = pygame.transform.scale(self.image, (int(new_width), int(new_height)))
            except Exception:
                pass

    def draw(self, surface):
        color_border = (255, 255, 0) if self.selected else BROWN
        thickness = 5 if self.selected else 3
        
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=8)
        pygame.draw.rect(surface, color_border, self.rect, thickness, border_radius=8)
        
        if self.is_image and self.image:
            img_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, img_rect)
        else:
            font = pygame.font.Font(None, 40)
            text_surf = font.render(self.text, True, BLACK)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def contains_point(self, point):
        return self.rect.collidepoint(point)

# ============================================================
# CLASE CONFETTI
# ============================================================
class Confetti:
    def __init__(self, screen_width, screen_height):
        self.particles = []
        self.colors = [(255,0,0), (0,255,0), (0,150,255), (255,255,0), (255,0,255), (255,128,0)]
        self.w, self.h = screen_width, screen_height
        self.active = False
        self.spawn_rate = 5

    def start(self):
        self.active = True; self.particles = []
    def stop(self): self.active = False
    def reset(self): self.particles = []; self.active = False
    def update(self):
        if self.active:
            for _ in range(self.spawn_rate):
                x = random.randint(0, self.w); y = random.randint(-50, 0)
                dx = random.uniform(-2, 2); dy = random.uniform(2, 5)
                color = random.choice(self.colors); size = random.randint(4, 7)
                self.particles.append([x, y, dx, dy, color, size])
        for p in self.particles:
            p[0] += p[2]; p[1] += p[3]
        self.particles = [p for p in self.particles if p[1] < self.h]
    def draw(self, surf):
        for p in self.particles: pygame.draw.circle(surf, p[4], (int(p[0]), int(p[1])), p[5])

# ============================================================
# CLASE ARROWSPRITE
# ============================================================
class ArrowSprite:
    def __init__(self, x, y):
        self.images = []
        for i in range(1, 5): 
            try:
                img = pygame.image.load(f'Materials/Pictures/Assets/flecha{i}.png').convert_alpha()
                self.images.append(pygame.transform.scale(img, (80, 80)))
            except:
                s = pygame.Surface((40,40), pygame.SRCALPHA); s.fill((255,0,0)); self.images.append(s)
        self.idx = 0; self.img = self.images[0]; self.rect = self.img.get_rect(center=(x,y))
        self.last = 0; self.active = False
    def start(self): self.active = True
    def update(self):
        if not self.active: return
        now = pygame.time.get_ticks()
        if now - self.last > 150:
            self.last = now; self.idx = (self.idx + 1) % len(self.images)
            self.img = self.images[self.idx]
    def draw(self, surf):
        if self.active: surf.blit(self.img, self.rect)

# ============================================================
# CLASE LEVEL3
# ============================================================
class Level3:
    def __init__(self, screen, size, font, character_choice):
        self.screen = screen
        self.size = size
        self.font = font
        self.character_choice = character_choice

        # --- TUTORIALES ---
        self.tuto_image = None; self.tuto_image_2 = None; self.tuto_image_3 = None; self.tuto_image_4 = None
        self.tuto_4_active = False
        self.tuto_alpha = 0; self.tuto_max_alpha = 255
        self.tuto_fade_speed = 8; self.tuto_slide_speed = 10
        self.tuto_visible_timer = Timer(5)
        self.tuto_fade_in_started = False; self.tuto_fade_out_started = False
        self.tuto_finished = False; self.tuto_3_has_appeared = False
        self.current_tuto_index = 1
        self.tuto_target_x = 20; self.tuto_exit_x = -250; self.tuto_current_x = -250; self.tuto_y = 20

        try:
            self.tuto_image = pygame.transform.scale(pygame.image.load('Materials/Pictures/Assets/tuto1.jpg').convert_alpha(), (250, 180))
            self.tuto_image_2 = pygame.transform.scale(pygame.image.load('Materials/Pictures/Assets/tuto2.jpg').convert_alpha(), (250, 180))
            self.tuto_image_3 = pygame.transform.scale(pygame.image.load('Materials/Pictures/Assets/tuto3.jpg').convert_alpha(), (250, 180))
            self.tuto_image_4 = pygame.transform.scale(pygame.image.load('Materials/Pictures/Assets/tuto4.jpg').convert_alpha(), (250, 180))
            self.tuto_rect = self.tuto_image.get_rect(topleft=(-250, 20))
        except: self.current_tuto_index = 0

        # --- PANTALLA CONTROLES ---
        try:
            try: self.control_image = pygame.image.load('Materials/Pictures/Assets/Control3.jpg').convert()
            except: self.control_image = pygame.image.load('Materials/Pictures/Assets/Control.jpg').convert()
        except: self.control_image = None

        self.fade_alpha = 255 if self.control_image else 0
        self.is_fading = True
        self.target_state = None
        self.state = "controls_screen" if self.control_image else "game"
        self.fade_in_speed = 5; self.fade_out_speed = 10
        self.control_timer = Timer(5) 
        self.control_timer_started = False
        self.can_skip_controls = False

        # --- JUGADOR & NPC ---
        if character_choice == "boy": self.player = Characterb(440, 600, 2)
        else: self.player = Characterg(440, 600, 2)

        self.maestro = Characternpcp(500, 250, 'Materials/Pictures/Characters/MAESTRO_NIVEL_3.png')
        mw, mh = self.maestro.rect.width, self.maestro.rect.height
        new_w = int(mw*0.1); new_h = 4
        self.maestro_col = pygame.Rect(self.maestro.rect.x + int((mw-new_w)/2), self.maestro.rect.y + mh - new_h, new_w, new_h)

        # --- ENTORNO ---
        self.obstacles = [pygame.Rect(0,0,size[0],0), pygame.Rect(0,0,10,size[1]), pygame.Rect(size[0]-10,0,5,size[1]), pygame.Rect(0,size[1]-10,size[0],10)]
        try: self.bg = pygame.transform.scale(pygame.image.load('Materials/Pictures/Assets/fondo_nivel_3.png').convert(), size)
        except: self.bg = pygame.Surface(size); self.bg.fill((50,50,50))

        # --- DIÁLOGOS ---
        self.dialog_rect = pygame.Rect((size[0]-800)//2, size[1]-130, 800, 100)
        self.dialog_text = "Bienvenidos. Resuelve los problemas\nmatematicos para pasar."
        self.typewriter = None
        self.dialog_active = False

        # --- PREGUNTAS ---
        self.questions = [
            {
                "question": "Tengo 9 naranjas y las reparto entre 3 companeros\nCuantas naranjas recibe cada uno?",
                "numbers": ["2", "3", "4", "5"],
                "images": ["3naranjas.png", "6 naranjas.png", "2naranjas.png", "4naranjas.png"],
                "correct_number": "3",
                "correct_image": "3naranjas.png"
            },
            {
                "question": "Carlos tenia 3 canicas. Su amigo le regala 5 mas\nCuantas canicas tiene ahora?",
                "numbers": ["2", "8", "4", "7"],
                "images": ["4canicas.png", "8canicas.png", "2canicas.png", "7canicas.png"],
                "correct_number": "8",
                "correct_image": "8canicas.png"
            },
            {
                "question": "Tengo 14 caramelos y los reparto entre 10 amigos\ncuantos caramelos me quedan?",
                "numbers": ["3", "4", "5", "7"],
                "images": ["4caramelos.png", "3caramelos.png", "7caramelos.png", "5carmelos.png"],
                "correct_number": "4",
                "correct_image": "4caramelos.png"
            },
            {
                "question": "En una fiesta hay 8 ninos y cada uno recibe 1 globo\nCuantos globos dimos?",
                "numbers": ["8", "1", "7", "3"],
                "images": ["8GLOBOS.png", "7GLOBOS.png", "1GLOBO.png", "3GLOBOS.png"],
                "correct_number": "8",
                "correct_image": "8GLOBOS.png"
            }
        ]
        self.q_idx = 0
        self.guard_interacted = False
        self.confetti = Confetti(size[0], size[1])
        self.win_zone = pygame.Rect(420, 280, 65, 65)
        self.arrow = ArrowSprite(452, 312)

        # --- VARIABLES DEL MINIJUEGO ---
        self.minigame_active = False
        self.number_buttons = []
        self.image_buttons = []
        self.submit_btn = None
        
        self.selected_num_idx = None
        self.selected_img_idx = None
        self.current_pair = None 
        self.results = []

        # --- TIMERS Y FUENTES ---
        self.timer = Timer(150)
        
        fp = "Materials/Fonts/PressStart2P-Regular.ttf" if os.path.exists("Materials/Fonts/PressStart2P-Regular.ttf") else None
        self.f_base = pygame.font.Font(fp, 18)
        self.f_dial = pygame.font.Font(fp, 15)
        self.f_quest = pygame.font.Font(None, 36) 
        self.f_timer = pygame.font.Font(fp, 24)
        self.f_ctrl_t = pygame.font.Font(fp, 36)
        self.f_ctrl_s = pygame.font.Font(fp, 18)

        # --- SONIDOS ---
        self.controls_music = None
        self.level_music_loaded = False
        if MIXER_INITIALIZED:
            try:
                self.controls_music = pygame.mixer.Sound('Materials/Music/controls.wav')
                pygame.mixer.music.load('Materials/Music/Level3.wav')
                self.level_music_loaded = True
                self.s_win = pygame.mixer.Sound('Materials/Music/Ganar.wav')
                self.s_lose = pygame.mixer.Sound('Materials/Music/antesover.wav')
                self.s_ok = pygame.mixer.Sound('Materials/Music/PreguntaB.wav')
                self.s_bad = pygame.mixer.Sound('Materials/Music/PreguntaM.wav')
                self.game_over_music = pygame.mixer.Sound('Materials/Music/GameOver.wav')
            except: pass

        # Assets UI
        try:
            # Aseguramos .convert_alpha() para evitar el efecto oscuro
            self.img_ok = pygame.transform.scale(pygame.image.load("Materials/Pictures/Assets/palomita.png").convert_alpha(), (40,40))
            self.img_bad = pygame.transform.scale(pygame.image.load("Materials/Pictures/Assets/tache.png").convert_alpha(), (40,40))
            self.img_frm = pygame.transform.scale(pygame.image.load("Materials/Pictures/Assets/marco.png").convert_alpha(), (56,56))
        except: 
            self.img_ok = None
            self.img_bad = None
            self.img_frm = None
        
        self.win_music_played = False
        self.game_over_music_played = False
        try:
            self.game_over_image = pygame.transform.scale(pygame.image.load('Materials/Pictures/Assets/perdiste.png').convert(), size)
            self.win_image = pygame.transform.scale(pygame.image.load('Materials/Pictures/Assets/ganaste.png').convert(), size)
        except: self.game_over_image = None; self.win_image = None

    # ============================================================
    # LÓGICA MINIJUEGO
    # ============================================================
    def init_minigame(self):
        self.minigame_active = True
        self.selected_num_idx = None
        self.selected_img_idx = None
        self.current_pair = None
        
        # INICIAR EL TIMER AQUÍ SÓLO LA PRIMERA VEZ QUE APARECE EL QUIZ (q_idx == 0)
        if self.q_idx == 0 and not self.timer.is_running():
            self.timer.start()
        
        if self.q_idx >= len(self.questions):
            self.minigame_active = False
            self.check_final_score()
            return

        q = self.questions[self.q_idx]
        w, h = self.size
        
        # --- POSICIÓN AJUSTADA (MÁS ABAJO) ---
        base_y = h // 10 + 10  
        self.rect_q = pygame.Rect(w//10, base_y, w*0.8, h//6)
        self.rect_main = pygame.Rect(w//10, base_y + h//6 + 20, w*0.8, h*0.6)
        
        self.number_buttons = []
        btn_w = self.rect_main.width // 6
        btn_h = self.rect_main.height // 4
        
        total_w_nums = len(q["numbers"]) * btn_w + (len(q["numbers"])-1)*20
        start_x_nums = self.rect_main.left + (self.rect_main.width - total_w_nums)//2
        start_y_nums = self.rect_main.top + 40
        
        for i, txt in enumerate(q["numbers"]):
            x = start_x_nums + i*(btn_w+20)
            btn = RelationButton(x, start_y_nums, btn_w, btn_h, txt, False)
            self.number_buttons.append(btn)
            
        self.image_buttons = []
        total_w_imgs = len(q["images"]) * btn_w + (len(q["images"])-1)*20
        start_x_imgs = self.rect_main.left + (self.rect_main.width - total_w_imgs)//2
        start_y_imgs = start_y_nums + btn_h + 40
        
        for i, img_path in enumerate(q["images"]):
            x = start_x_imgs + i*(btn_w+20)
            btn = RelationButton(x, start_y_imgs, btn_w, btn_h, "", True, img_path)
            self.image_buttons.append(btn)
            
        bx = w//2 - 80
        by = self.rect_main.bottom - 70
        self.submit_btn = pygame.Rect(bx, by, 160, 50)

    def update_minigame(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for i, btn in enumerate(self.number_buttons):
                if btn.contains_point(pos):
                    self.selected_num_idx = i
                    for b in self.number_buttons: b.selected = False
                    btn.selected = True
                    if self.selected_img_idx is not None:
                        self.current_pair = (self.selected_num_idx, self.selected_img_idx)
                    return

            for i, btn in enumerate(self.image_buttons):
                if btn.contains_point(pos):
                    self.selected_img_idx = i
                    for b in self.image_buttons: b.selected = False
                    btn.selected = True
                    if self.selected_num_idx is not None:
                        self.current_pair = (self.selected_num_idx, self.selected_img_idx)
                    return

            if self.submit_btn.collidepoint(pos) and self.current_pair:
                self.check_single_answer()

    def check_single_answer(self):
        q = self.questions[self.q_idx]
        num_idx, img_idx = self.current_pair
        sel_num = q["numbers"][num_idx]
        sel_img = q["images"][img_idx]
        
        if sel_num == q["correct_number"] and sel_img == q["correct_image"]:
            self.results.append("correct")
            if hasattr(self, 's_ok'): self.s_ok.play()
        else:
            self.results.append("incorrect")
            if hasattr(self, 's_bad'): self.s_bad.play()
        
        self.q_idx += 1
        if self.q_idx < len(self.questions):
            self.init_minigame()
        else:
            self.minigame_active = False
            self.check_final_score()

    def check_final_score(self):
        correct_count = self.results.count("correct")
        if correct_count >= 3:
            self.maestro.rect.x -= 130
            self.maestro_col.x = self.maestro.rect.x + int(self.maestro.rect.width*0.1)
            self.player.rect.topleft = (450, 570)
            self.guard_interacted = True
            self.arrow.start()
            self.confetti.start()
            if self.tuto_image_4:
                self.tuto_4_active = True; self.tuto_fade_in_started = True
                self.tuto_visible_timer.reset()
        else:
            self.state = "game_over"
            pygame.mixer.music.stop()

    def draw_minigame(self):
        # Dibuja la capa semi-transparente para oscurecer el fondo
        s = pygame.Surface(self.size, pygame.SRCALPHA)
        s.fill((0,0,0,150))
        self.screen.blit(s, (0,0))
        
        if self.q_idx >= len(self.questions): return

        q = self.questions[self.q_idx]
        pygame.draw.rect(self.screen, WHITE, self.rect_q, border_radius=10)
        pygame.draw.rect(self.screen, BROWN, self.rect_q, 3, border_radius=10)
        
        lines = q["question"].split('\n')
        for i, line in enumerate(lines):
            t_surf = self.f_quest.render(line, True, BLACK)
            t_rect = t_surf.get_rect(center=(self.rect_q.centerx, self.rect_q.centery - 15 + i*30))
            self.screen.blit(t_surf, t_rect)
            
        pygame.draw.rect(self.screen, WHITE, self.rect_main, border_radius=15)
        pygame.draw.rect(self.screen, BROWN, self.rect_main, 4, border_radius=15)
        
        for btn in self.number_buttons: btn.draw(self.screen)
        for btn in self.image_buttons: btn.draw(self.screen)
        
        if self.current_pair:
            n_idx, i_idx = self.current_pair
            if n_idx < len(self.number_buttons) and i_idx < len(self.image_buttons):
                start = self.number_buttons[n_idx].rect.midbottom
                end = self.image_buttons[i_idx].rect.midtop
                pygame.draw.line(self.screen, GREEN, start, end, 6)
            
        pygame.draw.rect(self.screen, GREEN, self.submit_btn, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, self.submit_btn, 2, border_radius=10)
        t_sub = self.f_dial.render("ENVIAR", True, WHITE)
        self.screen.blit(t_sub, t_sub.get_rect(center=self.submit_btn.center))

    # ============================================================
    # UPDATE
    # ============================================================
    def handle_events(self, event):
        if self.state in ["game_over", "loss_sound_state", "win_state"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    pygame.mixer.stop(); self.__init__(self.screen, self.size, self.font, self.character_choice); return "restart"
                if event.key == pygame.K_ESCAPE: pygame.mixer.stop(); return "menu"
            return None

        if self.state == "controls_screen" and not self.is_fading:
            if self.can_skip_controls and event.type == pygame.KEYDOWN and (event.key in [pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN]):
                self.is_fading = True; self.target_state = "game"; self.fade_alpha = 0
                if self.controls_music: self.controls_music.stop()
            return None

        if self.state == "game" and self.minigame_active:
            self.update_minigame(event)
            return

        if self.state == "game" and event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                if self.dialog_active:
                    if not self.typewriter.finished(): self.typewriter.complete_text()
                    else: 
                        self.dialog_active = False; self.init_minigame()
                elif not self.guard_interacted and self.player.rect.colliderect(self.maestro_col.inflate(60,60)):
                    self.dialog_active = True
                    self.typewriter = TypewriterText(self.dialog_text, self.f_dial, (0,0,0), 30)
                    if self.tuto_image_3 and not self.tuto_3_has_appeared:
                        self.current_tuto_index = 3; self.tuto_fade_in_started = True; self.tuto_visible_timer.reset()

    def update(self):
        keys = pygame.key.get_pressed()

        if self.is_fading:
            if self.state == "controls_screen":
                if self.target_state is None:
                    self.fade_alpha = max(0, self.fade_alpha - self.fade_in_speed)
                    if self.fade_alpha == 0:
                        self.is_fading = False
                        if self.controls_music and not self.controls_music.get_num_channels(): self.controls_music.play(-1)
                elif self.target_state == "game":
                    self.fade_alpha = min(255, self.fade_alpha + self.fade_out_speed)
                    if self.fade_alpha == 255:
                        self.state = self.target_state; self.target_state = None; self.is_fading = True
            elif self.state == "game" and self.target_state is None:
                self.fade_alpha = max(0, self.fade_alpha - self.fade_in_speed)
                if self.fade_alpha == 0:
                    self.is_fading = False
                    if self.level_music_loaded and not pygame.mixer.music.get_busy(): pygame.mixer.music.play(-1)
                    if (self.tuto_image or self.tuto_image_2 or self.tuto_image_3) and self.current_tuto_index > 0 and not self.tuto_fade_in_started:
                        self.tuto_fade_in_started = True

        if self.state == "controls_screen" and not self.is_fading:
            if not self.control_timer_started: self.control_timer.start(); self.control_timer_started = True
            if self.control_timer.is_running(): self.control_timer.update()
            if self.control_timer.finished: self.can_skip_controls = True
            return self.state

        if self.state == "game":
            if self.minigame_active:
                pass 
            else:
                barrier = self.maestro_col if not self.guard_interacted else None
                self.player.move(keys, self.size[0], self.size[1], barrier, self.obstacles, 3)
                self.arrow.update()
                
                if self.guard_interacted and self.player.rect.colliderect(self.win_zone):
                    self.state = "win_state"; pygame.mixer.music.stop(); self.confetti.reset()
                    if self.tuto_4_active: self.tuto_fade_out_started = True
                    if hasattr(self, 's_win') and not self.win_music_played: 
                        self.s_win.play(); self.win_music_played = True
            
            # TIMER ACTUALIZADO SIEMPRE (Si ya se inició)
            if self.timer.is_running(): self.timer.update()
            
            if self.timer.finished and not self.guard_interacted: 
                self.state = "loss_sound_state"; pygame.mixer.music.stop(); 
                if hasattr(self, 's_lose'): self.s_lose.play()
                return self.state

        elif self.state == "loss_sound_state":
            if not pygame.mixer.get_busy():
                self.state = "game_over"
                if self.game_over_music and not self.game_over_music_played: 
                    self.game_over_music.play(-1); self.game_over_music_played = True

        if self.dialog_active and self.typewriter: self.typewriter.update()
        
        if (self.current_tuto_index > 0 and not self.tuto_4_active) or self.tuto_4_active:
            if self.tuto_fade_in_started and not self.tuto_fade_out_started:
                self.tuto_alpha = min(self.tuto_max_alpha, self.tuto_alpha + self.tuto_fade_speed)
                self.tuto_current_x = min(self.tuto_target_x, self.tuto_current_x + self.tuto_slide_speed)
                if self.tuto_current_x >= self.tuto_target_x and not self.tuto_visible_timer.is_running():
                     self.tuto_visible_timer.start()
            if self.tuto_visible_timer.is_running():
                self.tuto_visible_timer.update()
                if self.tuto_visible_timer.finished: self.tuto_fade_out_started = True
                is_near = self.player.rect.colliderect(self.maestro_col.inflate(100,100))
                if self.current_tuto_index == 1 and is_near: self.tuto_fade_out_started = True
            if self.tuto_fade_out_started:
                self.tuto_alpha = max(0, self.tuto_alpha - self.tuto_fade_speed)
                self.tuto_current_x = max(self.tuto_exit_x, self.tuto_current_x - self.tuto_slide_speed)
                if self.tuto_alpha == 0:
                    if self.current_tuto_index == 1 and is_near:
                        self.current_tuto_index = 2; self.tuto_fade_in_started = True; self.tuto_fade_out_started = False; self.tuto_visible_timer.reset(); self.tuto_current_x = -250
                    else:
                        if self.tuto_4_active: self.tuto_4_active = False
                        elif self.current_tuto_index != 0: self.current_tuto_index = 0
                        self.tuto_fade_in_started = False; self.tuto_fade_out_started = False
            self.tuto_rect.topleft = (self.tuto_current_x, self.tuto_y)

        self.confetti.update()
        return self.state

    def _draw_text_with_border(self, surface, text, font, text_color, border_color, center_pos, border_size=2):
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=center_pos)
        for dx in range(-border_size, border_size + 1):
            for dy in range(-border_size, border_size + 1):
                if dx != 0 or dy != 0:
                    border_rect = text_surface.get_rect(center=(center_pos[0] + dx, center_pos[1] + dy))
                    border_surface = font.render(text, True, border_color)
                    surface.blit(border_surface, border_rect)
        surface.blit(text_surface, text_rect)

    def draw(self):
        if self.state == "controls_screen":
            if self.control_image:
                self.screen.fill((255,255,255))
                iw, ih = self.control_image.get_size()
                scale = min(self.size[0]/iw, self.size[1]/ih)
                nw, nh = int(iw*scale), int(ih*scale)
                img = pygame.transform.scale(self.control_image, (nw, nh))
                self.screen.blit(img, img.get_rect(center=(self.size[0]//2, self.size[1]//2)))
                
                cx, cy = self.size[0]//2, 40
                self._draw_text_with_border(self.screen, "CONTROLES", self.f_ctrl_t, (0,0,0), (255,128,0), (cx, cy), 4)
                cy = self.size[1]-30
                if self.can_skip_controls: msg = "Presiona ESPACIO para comenzar"
                elif self.control_timer_started: msg = f"Esperando un momento..."
                else: msg = "Cargando..."
                self._draw_text_with_border(self.screen, msg, self.f_ctrl_s, (0,0,0), (255,128,0), (cx, cy), 3)
            if self.is_fading:
                s = pygame.Surface(self.size); s.fill((0,0,0)); s.set_alpha(self.fade_alpha)
                self.screen.blit(s, (0,0))
            return

        # 1. Dibujar fondo, sombras y personajes
        self.screen.blit(self.bg, (0,0))
        
        s = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.ellipse(s, (0,0,0,100), (self.player.rect.centerx-20, self.player.rect.bottom-5, 40, 10))
        pygame.draw.ellipse(s, (0,0,0,100), (self.maestro.rect.centerx-25, self.maestro.rect.bottom-8, 50, 10))
        self.screen.blit(s, (0,0))

        self.maestro.draw(self.screen)
        self.player.draw(self.screen)

        # 2. Dibujar diálogo (si está activo)
        if self.dialog_active:
            pygame.draw.rect(self.screen, (WHITE), self.dialog_rect, border_radius=10)
            pygame.draw.rect(self.screen, (BROWN), self.dialog_rect, 4, border_radius=10)
            self.typewriter.draw(self.screen, (self.dialog_rect.x+20, self.dialog_rect.y+20))

        # 3. Dibujar la interfaz de Minigame (Esto incluye la capa oscura que oculta el fondo)
        if self.minigame_active: self.draw_minigame()

        # 4. Dibujar elementos de UI Superiores (Se dibujan DESPUÉS de la capa oscura para que sean visibles)
        
        # Dibujar Marcos de Resultados
        if self.img_frm:
            for i in range(4):
                x = (self.size[0] - (4*74))//2 + i*74
                self.screen.blit(self.img_frm, (x, 10))
                if i < len(self.results):
                    ic = self.img_ok if self.results[i] == "correct" else self.img_bad
                    # El icono se centra en el marco
                    self.screen.blit(ic, (x+8, 18))

        # Dibujar Timer (A 720, 20 que es 20px a la derecha de 700)
        if self.minigame_active:
            self.timer.draw(self.screen, self.f_timer, (720, 20))

        # 5. Otros elementos de superposición (Flecha, Confetti, Tutoriales)
        self.arrow.draw(self.screen)
        self.confetti.draw(self.screen)
        
        if self.current_tuto_index > 0 and not self.tuto_4_active:
            img = [None, self.tuto_image, self.tuto_image_2, self.tuto_image_3][self.current_tuto_index]
            if img: img.set_alpha(self.tuto_alpha); self.screen.blit(img, self.tuto_rect)
        if self.tuto_4_active and self.tuto_image_4:
            self.tuto_image_4.set_alpha(self.tuto_alpha); self.screen.blit(self.tuto_image_4, self.tuto_rect)

        # 6. Pantallas de Fin de Juego
        if self.state in ["win_state", "game_over"]:
            self.screen.fill((0,0,0))
            img = self.game_over_image if self.state == "game_over" else self.win_image
            if img: self.screen.blit(img, (0,0))
            t = self.f_base.render("R: Reiniciar   ESC: Menu", True, (255,255,255))
            self.screen.blit(t, t.get_rect(center=(self.size[0]//2, self.size[1]-50)))
            if self.state == "win_state": self.confetti.draw(self.screen)

        # 7. Pantalla de Transición (Fade)
        if self.is_fading:
            s = pygame.Surface(self.size); s.fill((0,0,0)); s.set_alpha(self.fade_alpha)
            self.screen.blit(s, (0,0))