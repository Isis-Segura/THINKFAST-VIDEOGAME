import pygame

class Characterg:
    def __init__(self, x, y, speed=2):
        # ---- Velocidad y posición ----
        self.speed = speed

        # ---- Animaciones ----
        # Cada dirección tiene una lista de imágenes (frames)
        # Ajusta las rutas de las imágenes a las que tengas en tu carpeta
        self.animations = {
            "down": [
                pygame.image.load("Pictures/Characters/chica_down1.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_down2.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_down3.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_down4.png").convert_alpha()

            ],
            "up": [
                pygame.image.load("Pictures/Characters/chica_up1.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_up2.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_up3.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_up4.png").convert_alpha()
            ],
            "left": [
                pygame.image.load("Pictures/Characters/chica_left1.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_left2.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_left3.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_left4.png").convert_alpha()
            ],
            "right": [
                pygame.image.load("Pictures/Characters/chica_right1.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_right2.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_right3.png").convert_alpha(),
                pygame.image.load("Pictures/Characters/chica_right4.png").convert_alpha()
            ]
        }

        # Escala todos los frames al mismo tamaño
        for direction, frames in self.animations.items():
            self.animations[direction] = [
                pygame.transform.scale(img, (90, 100)) for img in frames
            ]

        # Imagen inicial y rectángulo
        self.direction = "down"
        self.frame_index = 0
        self.image = self.animations[self.direction][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        # Temporizador para controlar la velocidad de animación
        self.frame_timer = 0
        self.frame_speed = 0.018  # Ajusta este número: más alto = más lento

    def move(self, keys):
        moving = False

        # --- Movimiento y cambio de dirección ---
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = "up"
            moving = True
        elif keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = "down"
            moving = True

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = "left"
            moving = True
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = "right"
            moving = True

        # Si se mueve, actualizar animación
        if moving:
            self.update_animation()
        else:
            # Si no se mueve, mostrar el primer frame de la dirección actual
            self.image = self.animations[self.direction][0]

    def update_animation(self):
        """Avanza al siguiente frame de la animación de la dirección actual."""
        self.frame_timer += self.frame_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
            self.image = self.animations[self.direction][self.frame_index]

    def draw(self, surface):
        """Dibuja la imagen actual en pantalla."""
        surface.blit(self.image, self.rect)
