import pygame
import random
import math

# CLASE PARA GESTIONAR LAS NUBES EN MOVIMIENTO
class Cloud:
    """Representa una nube que se mueve horizontalmente y se reinicia al salir de la pantalla."""
    def __init__(self, image, screen_width, screen_height):
        # Escalar la nube a un tamaño aleatorio
        scale = random.uniform(0.9, 1.0) 
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        
        # Posición inicial aleatoria (fuera de la pantalla por la derecha)
        self.rect.x = random.randint(-screen_width * 2, screen_width + 500)
        self.rect.y = random.randint(50, screen_height // 5)
        self.speed = random.uniform(0.3, 1.5) # Velocidad de movimiento
        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def move(self):
        self.rect.x -= self.speed
        # Si la nube sale por la izquierda, reiniciarla por la derecha
        if self.rect.right < 0:
            self.rect.x = self.screen_width + random.randint(50, 500)
            self.rect.y = random.randint(50, self.screen_height // 5)
            self.speed = random.uniform(0.5, 2.0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# CLASE PARA GESTIONAR EL GLOBO AERÓSTATICO
class HotAirBalloon:
    """Representa un globo que se mueve horizontalmente y oscila verticalmente."""
    def __init__(self, image, screen_width, screen_height):
        self.image = pygame.transform.scale(image, (150, 200)) # Tamaño fijo
        self.rect = self.image.get_rect()
        self.rect.x = screen_width + 50 # Inicia fuera de la pantalla, a la derecha
        
        # Parámetros de oscilación
        self.base_y = screen_height // 8 
        self.rect.y = self.base_y
        self.speed_x = 1.5
        self.amplitude = 15 # Cuánto sube y baja
        self.frequency = 0.01 # Velocidad de oscilación
        self.time = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self):
        self.time += self.frequency
        
        # Movimiento horizontal constante
        self.rect.x -= self.speed_x
        
        # Movimiento vertical oscilante (usando la función seno)
        self.rect.y = self.base_y + self.amplitude * math.sin(self.time)
        
        # Si el globo sale por la izquierda, reiniciarlo por la derecha
        if self.rect.right < 0:
            self.rect.x = self.screen_width + random.randint(100, 500)
          
    def draw(self, screen):
        screen.blit(self.image, self.rect)