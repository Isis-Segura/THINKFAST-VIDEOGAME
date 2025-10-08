import pygame

class TypewriterText:
    """
    Simula el efecto de escritura de máquina de escribir para texto,
    incluyendo soporte para múltiples líneas usando el carácter '\\n'.
    """
    def __init__(self, text, font, color, speed=25):
        # Almacena todas las líneas que deben mostrarse, divididas por '\n'
        self.full_lines = text.split('\n') 
        
        self.font = font
        self.color = color
        
        # Velocidad de escritura: caracteres por segundo (valor por defecto 25)
        self.speed = speed 
        self.time_per_char = 1000 / self.speed # Milisegundos por caracter
        
        # Estados para el proceso de escritura
        self.current_line_index = 0
        self.current_char_index = 0
        self.last_update_time = pygame.time.get_ticks()
        
        # Almacena el alto de la línea para el dibujo
        self.line_height = self.font.get_linesize()

    def update(self):
        """Avanza la animación de escritura caracter por caracter o línea por línea."""
        if self.finished():
            return
            
        current_time = pygame.time.get_ticks()
        
        # Comprueba si ha pasado suficiente tiempo para mostrar el siguiente carácter
        if current_time - self.last_update_time > self.time_per_char:
            self.last_update_time = current_time
            
            current_line_text = self.full_lines[self.current_line_index]
            
            if self.current_char_index < len(current_line_text):
                # Escribir el siguiente carácter
                self.current_char_index += 1
            else:
                # La línea actual terminó, pasar a la siguiente línea si existe
                if self.current_line_index + 1 < len(self.full_lines):
                    self.current_line_index += 1
                    self.current_char_index = 0
                        
    def complete_text(self):
        """Muestra el texto completo inmediatamente (salta la animación)."""
        if not self.finished() and self.full_lines:
            # Pone el índice en la última línea y en el último carácter
            self.current_line_index = len(self.full_lines) - 1
            self.current_char_index = len(self.full_lines[-1])

    def finished(self):
        """Retorna True si todo el texto ha terminado de escribirse."""
        if not self.full_lines:
             return True
        return (self.current_line_index == len(self.full_lines) - 1 and 
                self.current_char_index >= len(self.full_lines[-1]))

    def draw(self, screen, position):
        """Dibuja el texto actual en la pantalla."""
        y_offset = 0

        for i, line in enumerate(self.full_lines):
            text_to_render = ""
            
            # 1. Si la línea ya fue escrita
            if i < self.current_line_index:
                text_to_render = line
            # 2. Si la línea se está escribiendo actualmente
            elif i == self.current_line_index:
                text_to_render = line[:self.current_char_index]
            # 3. Si la línea aún no ha comenzado (no se dibuja)
            # (text_to_render queda como "")

            if text_to_render:
                try:
                    text_surface = self.font.render(text_to_render, True, self.color)
                    # La posición Y se ajusta con el offset
                    screen.blit(text_surface, (position[0], position[1] + y_offset))
                except pygame.error as e:
                    # Captura si la fuente no puede renderizar caracteres vacíos o raros
                    print(f"Error al renderizar texto en TypewriterText: {e}")
            
            # Incrementa el offset para la siguiente línea, incluso si no se dibuja aún
            y_offset += self.line_height