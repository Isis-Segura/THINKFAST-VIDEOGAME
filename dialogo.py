import pygame

class DialogBox:
    def __init__(self, width=800, height=100, font=None):
        self.width = width
        self.height = height
        self.font = font if font else pygame.font.SysFont(None, 32)
        self.active = False
        self.text = ""
        self.typewriter = None
        self.speed = 25  # letras por segundo

    def start_dialogo(self, text):
        self.text = text
        self.typewriter = typewritertext (text, self.font, speed=self.speed)
        self.active = True

    def update(self):
        if self.typewriter:
            self.typewriter.update()

    def draw(self, surface, x=50, y=550):
        if not self.active or not self.typewriter:
            return
        rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(surface, (0,0,0), rect)
        pygame.draw.rect(surface, (255,255,255), rect, 3)
        self.typewriter.draw(surface, (rect.x + 20, rect.y + 30))

    def finished(self):
        if self.typewriter:
            return self.typewriter.finished()
        return True

    def end_dialogo(self):
        self.active = False
        self.typewriter = None
