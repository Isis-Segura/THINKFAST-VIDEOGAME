import pygame

class Characterc():
    def __init__(self, x, y, image_path, speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1

    def move(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

    def draw(self, interfaz):
        interfaz.blit(self.image, self.rect)