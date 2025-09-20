import pygame

class Characterb():
    def __init__(self, x, y, image_path, speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 150))
        self.rect = self.image.get_rect()
        
        self.x_float = float(x)
        self.y_float = float(y)
        self.rect.center = (int(self.x_float), int(self.y_float))
        
        self.speed = speed

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_a]:
            self.x_float -= self.speed
        if keys[pygame.K_d]:
            self.x_float += self.speed
        if keys[pygame.K_w]:
            self.y_float -= self.speed
        if keys[pygame.K_s]:
            self.y_float += self.speed

        self.rect.x = int(self.x_float)
        self.rect.y = int(self.y_float)

        margin = 175
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
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)