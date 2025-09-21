import pygame

class Characternpc:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        
        self.image = pygame.transform.scale(self.image, (79, 160))
        
        self.rect = self.image.get_rect(center=(x, y))

    def is_interacting(self, player_rect, keys):
        interaction_distance = 50
        
        if self.rect.colliderect(player_rect):
            if keys[pygame.K_e]:
                return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)