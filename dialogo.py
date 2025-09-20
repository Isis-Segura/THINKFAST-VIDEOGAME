import pygame

class DialogBox:
    def __init__(self, text, width=400, height=100):
        self.text = text
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 24)
        #Fuente del texto

        self.active = False
        #Si es False no se dibuja nada

    def draw(self, surface):
        if not self.active:
            return

        #Rectángulo negro del cuadro
        rect = pygame.Rect(50, surface.get_height() - self.height - 50,
                           self.width, self.height)
        pygame.draw.rect(surface, (0, 0, 0), rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 3)
        #Borde blanco

        #Dibuja el texto en el cuadro
        rendered = self.font.render(self.text, True, (255, 255, 255))
        surface.blit(rendered, (rect.x + 10, rect.y + 10))
