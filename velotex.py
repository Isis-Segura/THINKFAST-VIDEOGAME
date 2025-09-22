import pygame

class TypewriterText:
    def __init__(self, text, font, color=(255,255,255), speed=30):
        """
        text: texto completo
        font: fuente de pygame
        color: color del texto
        speed: caracteres por segundo
        """
        self.full_text = text
        self.font = font
        self.color = color
        self.speed = speed
        self.current = ""
        self.start_time = pygame.time.get_ticks()

    def update(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000.0
        chars = int(elapsed * self.speed)
        self.current = self.full_text[:chars]

    def draw(self, surface, pos):
        surface.blit(self.font.render(self.current, True, self.color), pos)

    def finished(self):
        return self.current == self.full_text