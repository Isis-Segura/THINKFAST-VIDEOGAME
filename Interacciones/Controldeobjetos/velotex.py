import pygame

class TypewriterText:
    def __init__(self, text, font, color, speed=25):
        self.full_text = text
        self.font = font
        self.color = color
        self.speed = speed # Caracteres por segundo (simulación de velocidad)
        
        # 1. Separar el texto en líneas usando \n
        self.lines = self.full_text.split('\n')
        self.current_line_index = 0
        
        self.display_text = ""
        self.char_index = 0
        self.time_elapsed = 0
        self.finished_typing = False

    def update(self):
        if self.finished_typing:
            return
        
        # Se calcula cuántos caracteres deberían haberse escrito
        target_chars = int(self.time_elapsed * self.speed)
        
        # Si aún hay líneas y no hemos terminado de teclear en la línea actual
        if self.current_line_index < len(self.lines):
            line = self.lines[self.current_line_index]
            
            # Si target_chars excede el tamaño de la línea actual
            if target_chars >= len(line):
                # Completa la línea actual
                self.display_text = line
                
                # Mueve el índice a la siguiente línea y reinicia el conteo de tiempo/caracteres para la siguiente línea
                self.current_line_index += 1
                self.time_elapsed = 0 
                self.char_index = 0 
                
                # Si la siguiente línea existe, empieza a teclearla en el siguiente update.
                if self.current_line_index < len(self.lines):
                    # Reinicia el display_text para la nueva línea
                    self.display_text = ""
                else:
                    # Todas las líneas terminadas
                    self.finished_typing = True
            
            else:
                # Escribe carácter por carácter en la línea actual
                self.char_index = target_chars
                self.display_text = line[:self.char_index]

            self.time_elapsed += 0.016 # Asumiendo un framerate de ~60 fps (1/60 ~ 0.016)
        else:
            self.finished_typing = True

    def complete_text(self):
        self.display_text = self.full_text # Ya no es suficiente
        self.finished_typing = True
        self.current_line_index = len(self.lines)

    def finished(self):
        return self.finished_typing

    def draw(self, surface, position):
        # Esta es la parte CLAVE, renderizar línea por línea
        x, y = position
        line_height = self.font.get_height()
        
        current_y = y
        
        # 1. Dibuja las líneas COMPLETAS (ya tipeadas)
        for i in range(self.current_line_index):
            line_surface = self.font.render(self.lines[i], True, self.color)
            surface.blit(line_surface, (x, current_y))
            current_y += line_height
            
        # 2. Dibuja la línea ACTUAL (la que se está tipeando)
        if self.current_line_index < len(self.lines):
            # Si el texto está siendo tipeado (no completado instantáneamente)
            if not self.finished_typing:
                line_surface = self.font.render(self.display_text, True, self.color)
                surface.blit(line_surface, (x, current_y))
            # Si el usuario presiona para completar, la última línea es la que queda completa
            else:
                last_line_index = len(self.lines) - 1
                line_surface = self.font.render(self.lines[last_line_index], True, self.color)
                surface.blit(line_surface, (x, current_y))