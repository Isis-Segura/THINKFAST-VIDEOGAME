import pygame

class Characterb:
    def __init__(self, x, y, speed=2):
        self.speed = speed
         #Velocidad y posición

        #Animaciones por frames
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

        #Escalas de los frames al mismo tamaño
        for direction, frames in self.animations.items():
            self.animations[direction] = [
                pygame.transform.scale(img, (70, 100)) for img in frames
            ]
        #Imagen inicial y rectángulo
        self.direction = "down"
        self.frame_index = 0
        self.image = self.animations[self.direction][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        self.x_float = float(x)
        self.y_float = float(y)

        #Velocidad de animación
        self.frame_timer = 0
        self.frame_speed = 0.018

    #Movimiento y cambio de direccción
    def move(self, keys, screen_width, screen_height):
        moving = False
        
        #Lógica de movimiento
        if keys[pygame.K_w]:
            self.y_float -= self.speed
            self.direction = "up"
            moving = True
        elif keys[pygame.K_s]:
            self.y_float += self.speed
            self.direction = "down"
            moving = True

        if keys[pygame.K_a]:
            self.x_float -= self.speed
            self.direction = "left"
            moving = True
        elif keys[pygame.K_d]:
            self.x_float += self.speed
            self.direction = "right"
            moving = True

        #Actualiza el rectángulo con la posición flotante
        self.rect.x = int(self.x_float)
        self.rect.y = int(self.y_float)

        if moving:
            self.update_animation()
        else:
            self.image = self.animations[self.direction][0]

        # Lógica de los márgenes
        margin = 200
        margin2 = 75

        if self.rect.left < margin2:
            self.rect.left = margin2
            self.x_float = float(self.rect.x)
        if self.rect.right > screen_width - margin2:
            self.rect.right = screen_width - margin2
            self.x_float = float(self.rect.x)
        if self.rect.top < margin:
            self.rect.top = margin
            self.y_float = float(self.rect.y)
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.y_float = float(self.rect.y)

    def update_animation(self):
        self.frame_timer += self.frame_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
            self.image = self.animations[self.direction][self.frame_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect)