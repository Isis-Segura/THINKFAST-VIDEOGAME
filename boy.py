import pygame

class Characterb():
    def __init__(self, x, y, image_path, speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        margin = 175
        margin2 = 75

        if self.rect.left < margin2:
            self.rect.left = margin2
        if self.rect.right > screen_width - margin2:
            self.rect.right = screen_width - margin2
        if self.rect.top < margin:
            self.rect.top = margin
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)