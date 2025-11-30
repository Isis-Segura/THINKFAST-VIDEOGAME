import pygame

class AnswerPickup(pygame.sprite.Sprite):
    """Representa una opción de respuesta en el suelo que el jugador puede recoger."""
    def __init__(self, x, y, text, font, is_correct, question_index):
        super().__init__()
        self.text = text
        self.is_correct = is_correct
        self.question_index = question_index 
        self.font = font
        self.image = self._render_text()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.original_pos = (x, y)
        self.is_held = False # El jugador la está llevando
        self.visible = True

    def _render_text(self):
        # Renderiza el texto con un estilo de "objeto recogible"
        text_surface = self.font.render(self.text, True, (0, 0, 0)) # Texto en negro
        padding = 10
        width = text_surface.get_width() + 2 * padding
        height = text_surface.get_height() + 2 * padding
        
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Fondo y borde de color
        pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), border_radius=5)
        pygame.draw.rect(surface, (255, 128, 0), surface.get_rect(), 3, border_radius=5)
        surface.blit(text_surface, (padding, padding))
        return surface

    def update_position(self, player_rect):
        """Mantiene la respuesta encima del jugador si está siendo sostenida."""
        if self.is_held:
            self.rect.midbottom = player_rect.midtop
            
    def draw(self, screen):
        """Dibuja la respuesta si está visible."""
        if self.visible:
            screen.blit(self.image, self.rect)

# NOTA: La clase FloorQuiz (para el Nivel 1) NO debe ser modificada.