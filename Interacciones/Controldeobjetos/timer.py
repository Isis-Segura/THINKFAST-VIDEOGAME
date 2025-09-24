import pygame

class Timer:
    def __init__(self, total_seconds):
        self.total_seconds = total_seconds
        self.start_ticks = None
        self.finished = False

    def start(self):
        """Inicia el temporizador."""
        self.start_ticks = pygame.time.get_ticks()
        self.finished = False

    def update(self):
        """Actualiza y retorna los segundos restantes.
        
        No hace nada si el temporizador no ha sido iniciado.
        """
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
        """Dibuja el temporizador en la pantalla."""
        remaining = self.update()
        minutes = remaining // 60
        seconds = remaining % 60
        time_text = f"{minutes:02}:{seconds:02}"
        
        text_surface = font.render(time_text, True, (255, 0, 0))
        screen.blit(text_surface, position)
        
    def reset(self):
        """Reinicia el temporizador a su valor inicial."""
        self.start_ticks = None
        self.finished = False
        # Para que el temporizador regrese a 120 segundos
        # Se necesita guardar el valor inicial para resetearlo.
        # En tu caso, lo tienes en el constructor.
        # Si quieres un valor diferente, puedes pasarlo como argumento a reset().
        # Por ahora, con None es suficiente para que no inicie automáticamente.