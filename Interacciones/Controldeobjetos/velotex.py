import pygame

class TypewriterText:
    def __init__(self, text, font, color=(255, 255, 255), speed=25):
        self.text = text
        self.font = font
        self.color = color
        self.speed = speed
        self.current_char_index = 0
        self.last_update = pygame.time.get_ticks()
        # Esta línea es clave para manejar los saltos de línea
        self.lines = text.split('\n')

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.speed:
            if self.current_char_index < len(self.text):
                self.current_char_index += 1
                self.last_update = current_time

    def draw(self, surface, position):
        x, y = position
        rendered_text = self.text[:self.current_char_index]
        
        # Divide el texto que se ha renderizado hasta ahora para dibujar cada línea
        lines_to_draw = rendered_text.split('\n')
        
        line_spacing = self.font.get_height() + 5
        
        for line in lines_to_draw:
            text_surface = self.font.render(line, True, self.color)
            surface.blit(text_surface, (x, y))
            # Mueve el cursor 'y' hacia abajo para la siguiente línea
            y += line_spacing
        
    def finished(self):
        return self.current_char_index >= len(self.text)