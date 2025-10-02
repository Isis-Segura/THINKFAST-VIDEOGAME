import pygame

class Characternpc:
    def __init__(self, x, y, image_path):
        # Cargar y escalar la imagen del guardia
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 150)) # Asumiendo 100x150 como tamaño final

        # Rectángulo principal del guardia (usado solo para dibujar, la colisión es 'guardia_collision_rect' en Level1)
        # Nota: 'center=(x, y)' posicionará el centro del sprite en 470, 330.
        self.rect = self.image.get_rect(center=(x, y))

    def player_facing_guard(self, player_rect):
        # ... (La lógica de esta función no se usa en la colisión de movimiento,
        # pero es funcional para la interacción con la tecla ESPACIO) ...
        # ... (código mantenido) ...
        offset = 10  

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
        """Dibuja al guardia en la pantalla."""
        surface.blit(self.image, self.rect)