import pygame

class Characternpc:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 150))

        # Rectángulo principal para dibujar al guardia
        self.rect = self.image.get_rect(center=(x, y))

        # Rectángulo de colisión en la parte superior (cabeza)
        self.collision_rect = pygame.Rect(
            self.rect.x, self.rect.y,        # mismo X, empieza arriba
            self.rect.width, 50              # ancho igual, alto de 50 px (solo la cabeza)
        )

    def player_facing_guard(self, player_rect):
        offset = 10  

        cond1 = (
            abs(player_rect.top - self.collision_rect.bottom) <= offset and
            player_rect.centerx in range(self.collision_rect.left - offset, self.collision_rect.right + offset)
        )

        cond2 = (
            abs(player_rect.bottom - self.collision_rect.top) <= offset and
            player_rect.centerx in range(self.collision_rect.left - offset, self.collision_rect.right + offset)
        )

        cond3 = (
            abs(player_rect.left - self.collision_rect.right) <= offset and
            player_rect.centery in range(self.collision_rect.top - offset, self.collision_rect.bottom + offset)
        )

        cond4 = (
            abs(player_rect.right - self.collision_rect.left) <= offset and
            player_rect.centery in range(self.collision_rect.top - offset, self.collision_rect.bottom + offset)
        )

        return cond1 or cond2 or cond3 or cond4

    def draw(self, surface):
        surface.blit(self.image, self.rect)