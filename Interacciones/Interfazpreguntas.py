import pygame

class InventoryWindow:
    def __init__(self, screen_size):
        self.width = 600
        self.height = 400
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.rect = pygame.Rect(
            (self.screen_width - self.width) / 2,
            (self.screen_height - self.height) / 2,
            self.width,
            self.height
        )
        self.color = (30, 30, 30)
        self.border_color = (150, 150, 150)
        self.font = pygame.font.SysFont(None, 40)
        self.text_surface = self.font.render("preguntas", True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 5)
        surface.blit(self.text_surface, self.text_rect)