import pygame

class Characternpc:
    def __init__(self, x, y, image_path):
        # Cargar y escalar la imagen del guardia
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (79, 110))

        # Rectángulo principal del guardia
        self.rect = self.image.get_rect(center=(x, y))

    def player_facing_guard(self, player_rect):
        """
        Devuelve True si el jugador está justo frente al guardia,
        pegado a cualquiera de sus cuatro lados (arriba, abajo, izquierda o derecha).
        """
        offset = 10  # margen para permitir un pequeño desajuste

        # Jugador abajo del guardia (mirando hacia arriba)
        cond1 = (
            abs(player_rect.top - self.rect.bottom) <= offset and
            player_rect.centerx in range(self.rect.left - offset, self.rect.right + offset)
        )

        # Jugador arriba del guardia (mirando hacia abajo)
        cond2 = (
            abs(player_rect.bottom - self.rect.top) <= offset and
            player_rect.centerx in range(self.rect.left - offset, self.rect.right + offset)
        )

        # Jugador a la derecha del guardia (mirando a la izquierda)
        cond3 = (
            abs(player_rect.left - self.rect.right) <= offset and
            player_rect.centery in range(self.rect.top - offset, self.rect.bottom + offset)
        )

        # Jugador a la izquierda del guardia (mirando a la derecha)
        cond4 = (
            abs(player_rect.right - self.rect.left) <= offset and
            player_rect.centery in range(self.rect.top - offset, self.rect.bottom + offset)
        )

        return cond1 or cond2 or cond3 or cond4

    def draw(self, surface):
        """
        Dibuja al guardia en la pantalla.
        """
        surface.blit(self.image, self.rect)
