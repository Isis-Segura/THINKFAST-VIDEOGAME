import pygame

class Timer:
    def __init__(self, total_seconds):
        self.total_seconds = total_seconds
        self.start_ticks = None  # No empieza hasta que se llama a start()
        self.finished = False

    def start(self):
        self.start_ticks = pygame.time.get_ticks()
        self.finished = False

    def update(self):
        if self.start_ticks is None:
            return self.total_seconds

        elapsed_ticks = pygame.time.get_ticks() - self.start_ticks
        elapsed_seconds = elapsed_ticks // 1000
        remaining = self.total_seconds - elapsed_seconds
        if remaining <= 0:
            self.finished = True
            return 0
        return remaining

    def draw(self, screen, font, position=(750, 10)):
        remaining = self.update()
        minutes = remaining // 60
        seconds = remaining % 60
        time_text = f"{minutes:02}:{seconds:02}"
        text_surface = font.render(time_text, True, (255, 0, 0))
        screen.blit(text_surface, position)
