import pygame

class Characterb:
    def __init__(self, x, y, speed=2):
        # ⬅ Define la velocidad de movimiento del personaje.
        self.speed = speed
        
        # Diccionario para guardar todas las animaciones (imágenes)
        self.animations = {
            "down": [
                pygame.image.load("Materials/Pictures/Characters/boy/chico_down1.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_down2.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_down3.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_down4.png").convert_alpha()
            ],
            "up": [
                pygame.image.load("Materials/Pictures/Characters/boy/chico_up1.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_up2.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_up3.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_up4.png").convert_alpha()
            ],
            "left": [
                pygame.image.load("Materials/Pictures/Characters/boy/chico_left1.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_left2.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_left3.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_left4.png").convert_alpha()
            ],
            "right": [
                pygame.image.load("Materials/Pictures/Characters/boy/chico_right1.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_right2.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_right3.png").convert_alpha(),
                pygame.image.load("Materials/Pictures/Characters/boy/chico_right4.png").convert_alpha()
            ]
        }
        
        # Inicialización de estado
        self.direction = "down"
        self.frame_index = 0
        self.image = self.animations[self.direction][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_float = float(x)
        self.y_float = float(y)
        
        # Parámetros de animación
        self.frame_timer = 0
        self.frame_speed = 0.1  # Controla qué tan rápido cambian los frames
        
        # Offset de la valla (límites inferiores)
        self.fence_offset = 80 # Valor predeterminado

    def update_animation(self):
        self.frame_timer += self.frame_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
            self.image = self.animations[self.direction][self.frame_index]

    def move_animation_only(self):
        # Mantiene el personaje estático, solo muestra el primer frame
        self.image = self.animations[self.direction][0]


    # --- FUNCIÓN MOVE CON MÁRGENES POR NIVEL ---
    def move(self, keys, screen_width, screen_height, npc_rect=None, level_id=2, can_move=True):
        
        MARGINS = {
            # ⬅️ Colisiones Nivel 1: (Ejemplo, ajusta los valores si el Nivel 1 tenía otros límites)
            1: [100, 50, 0], 
            
            # ⬅️ Colisiones Nivel 2: (Usando tus valores anteriores: 340 superior, 100 lateral, 80 inferior)
            2: [340, 215, 80], 
            
            # ⬅️ Colisiones Nivel 3: (Ejemplo de nuevos límites, AJUSTAR NECESARIAMENTE)
            3: [200, 150, 100] 
        }

        # Aplicar el margen del nivel. Usa Nivel 2 por defecto si el ID no existe o no se pasa.
        current_margins = MARGINS.get(level_id, MARGINS[2])
        margin_top, margin_side, fence_offset = current_margins
        
        # ----------------------------------------------------
        
        if not can_move:
            self.image = self.animations[self.direction][0]
            return 
        
        moving = False
        
        previous_x = self.x_float
        previous_y = self.y_float
        
        # Lógica de movimiento
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y_float -= self.speed
            self.direction = "up"
            moving = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y_float += self.speed
            self.direction = "down"
            moving = True

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x_float -= self.speed
            self.direction = "left"
            moving = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x_float += self.speed
            self.direction = "right"
            moving = True


        self.rect.x = int(self.x_float)
        self.rect.y = int(self.y_float)
        
        # Lógica de Colisión con NPC
        if npc_rect is not None:
            if self.rect.colliderect(npc_rect):
                self.x_float = previous_x
                self.y_float = previous_y 
                self.rect.x = int(self.x_float)
                self.rect.y = int(self.y_float)

        # 🟢 Lógica de límites de pantalla APLICADA POR NIVEL
        bottom_fence_limit = screen_height - fence_offset 

        if self.rect.left < margin_side:
            self.rect.left = margin_side
            self.x_float = float(self.rect.x)
        if self.rect.right > screen_width - margin_side:
            self.rect.right = screen_width - margin_side
            self.x_float = float(self.rect.x)
        if self.rect.top < margin_top:
            self.rect.top = margin_top
            self.y_float = float(self.rect.y)
            
        if self.rect.bottom > bottom_fence_limit:
            self.rect.bottom = bottom_fence_limit
            self.y_float = float(self.rect.y)

        # Lógica de animación
        if moving:
            self.update_animation()
        else:
            self.image = self.animations[self.direction][0]

    def draw(self, surface):
        surface.blit(self.image, self.rect)