import pygame

class LifeManager:
    def __init__(self, max_lives, heart_image_path):
        self.max_lives = max_lives
        self.current_lives = max_lives
        self.heart_image = pygame.image.load('Materials/Pictures/Assets/corazones.png')
        self.heart_image = pygame.transform.scale(self.heart_image, (128, 128))  # Tamaño ajustable

    def lose_life(self):
        if self.current_lives > 0:
            self.current_lives -= 1

    def gain_life(self):
        if self.current_lives < self.max_lives:
            self.current_lives += 1

    def is_dead(self):
        return self.current_lives == 0

    def draw(self, screen, position=(10, 10)):
        for i in range(self.current_lives):
            x = position[0] + i * 70  # Separación entre corazones
            screen.blit(self.heart_image, (x, position[1]))
