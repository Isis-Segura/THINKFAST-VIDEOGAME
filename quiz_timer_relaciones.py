import pygame
import sys
import os

pygame.init()

# --- CONFIGURACIONES ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 180, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Fuentes
FONT_LARGE = pygame.font.Font(None, 48)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 28)

# --- DATOS DE LAS PREGUNTAS ---
questions_data = [
    {
        "question": "Relaciona cada número con la cantidad correcta de naranjas",
        "numbers": ["3", "4", "5", "6"],
        "images": ["naranjas_3.png", "naranjas_4.png", "naranjas_5.png", "naranjas_6.png"],
        "correct_pairs": {"3": "naranjas_3.png", "4": "naranjas_4.png", "5": "naranjas_5.png", "6": "naranjas_6.png"}
    },
    {
        "question": "Relaciona cada número con la cantidad correcta de manzanas",
        "numbers": ["2", "5", "7", "8"],
        "images": ["manzanas_2.png", "manzanas_5.png", "manzanas_7.png", "manzanas_8.png"],
        "correct_pairs": {"2": "manzanas_2.png", "5": "manzanas_5.png", "7": "manzanas_7.png", "8": "manzanas_8.png"}
    },
    {
        "question": "Relaciona cada número con la cantidad correcta de estrellas",
        "numbers": ["4", "6", "9", "10"],
        "images": ["estrellas_4.png", "estrellas_6.png", "estrellas_9.png", "estrellas_10.png"],
        "correct_pairs": {"4": "estrellas_4.png", "6": "estrellas_6.png", "9": "estrellas_9.png", "10": "estrellas_10.png"}
    },
    {
        "question": "Relaciona cada número con la cantidad correcta de globos",
        "numbers": ["1", "3", "7", "9"],
        "images": ["globos_1.png", "globos_3.png", "globos_7.png", "globos_9.png"],
        "correct_pairs": {"1": "globos_1.png", "3": "globos_3.png", "7": "globos_7.png", "9": "globos_9.png"}
    }
]

class RelationButton:
    def __init__(self, x, y, width, height, text, is_image=False, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_image = is_image
        self.image_path = image_path
        self.image = None
        self.selected = False
        self.matched = False
        self.match_color = None
        
        if is_image and image_path:
            try:
                full_path = os.path.join("Materials", "Pictures", "Assets", image_path)
                if os.path.exists(full_path):
                    self.image = pygame.image.load(full_path).convert_alpha()
                    # Escalar imagen para que quepa en el botón
                    img_width = width - 20
                    img_height = height - 20
                    self.image = pygame.transform.scale(self.image, (img_width, img_height))
                else:
                    print(f"Image not found: {full_path}")
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

    def draw(self, surface):
        # Dibujar botón
        if self.matched:
            color = self.match_color
        elif self.selected:
            color = LIGHT_BLUE
        else:
            color = BLUE
            
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=12)
        
        if self.is_image and self.image:
            # Centrar imagen en el botón
            img_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, img_rect)
        else:
            # Dibujar texto centrado
            text_surf = FONT_MEDIUM.render(self.text, True, WHITE)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def contains_point(self, point):
        return self.rect.collidepoint(point)

def load_default_images():
    """Crear imágenes por defecto si no existen los archivos"""
    default_images = {}
    sizes = {
        "naranjas": [3, 4, 5, 6],
        "manzanas": [2, 5, 7, 8],
        "estrellas": [4, 6, 9, 10],
        "globos": [1, 3, 7, 9]
    }
    
    for item, counts in sizes.items():
        for count in counts:
            key = f"{item}_{count}.png"
            # Crear una superficie para la imagen por defecto
            surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            # Dibujar un círculo de color según el item
            if item == "naranjas":
                color = (255, 165, 0)  # Naranja
            elif item == "manzanas":
                color = (255, 0, 0)    # Rojo
            elif item == "estrellas":
                color = (255, 255, 0)  # Amarillo
            else:  # globos
                color = (0, 255, 255)  # Cyan
            
            # Dibujar los objetos según la cantidad
            radius = 15
            spacing = 25
            start_x = 50 - ((count - 1) * spacing) / 2
            
            for i in range(count):
                x = start_x + i * spacing
                y = 50
                pygame.draw.circle(surf, color, (int(x), y), radius)
                pygame.draw.circle(surf, BLACK, (int(x), y), radius, 2)
            
            # Dibujar el número en la parte inferior
            text = FONT_SMALL.render(str(count), True, BLACK)
            text_rect = text.get_rect(center=(50, 85))
            surf.blit(text, text_rect)
            
            default_images[key] = surf
    
    return default_images

def run_quiz_with_timer(screen, fondo_path):
    # Cargar y ajustar el fondo
    try:
        background = pygame.image.load(fondo_path).convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill((50, 100, 200))
    
    # Cargar imágenes por defecto
    default_images = load_default_images()
    
    score = 0
    question_index = 0
    total_questions = len(questions_data)
    running = True
    
    # Colores para las líneas de relación
    pair_colors = [
        (255, 100, 100),   # Rojo
        (100, 255, 100),   # Verde
        (100, 100, 255),   # Azul
        (255, 255, 100),   # Amarillo
    ]
    
    while running and question_index < total_questions:
        current_question = questions_data[question_index]
        
        # Crear botones para números (lado izquierdo)
        number_buttons = []
        button_width = 120
        button_height = 80
        spacing = 20
        start_y = 300
        
        for i, number in enumerate(current_question["numbers"]):
            x = 200
            y = start_y + i * (button_height + spacing)
            btn = RelationButton(x, y, button_width, button_height, number, False)
            number_buttons.append(btn)
        
        # Crear botones para imágenes (lado derecho)
        image_buttons = []
        for i, image_name in enumerate(current_question["images"]):
            x = SCREEN_WIDTH - 200 - button_width
            y = start_y + i * (button_height + spacing)
            
            # Usar imagen por defecto si no existe el archivo
            if image_name in default_images:
                btn = RelationButton(x, y, button_width, button_height, "", True)
                btn.image = default_images[image_name]
            else:
                btn = RelationButton(x, y, button_width, button_height, f"Img {i+1}", True)
            image_buttons.append(btn)
        
        # Variables para el emparejamiento
        selected_number = None
        selected_image = None
        pairs = {}  # {índice_número: índice_imagen}
        pair_colors_dict = {}  # {índice_número: color}
        
        question_finished = False
        
        # Bucle principal de la pregunta actual
        while not question_finished and running:
            screen.blit(background, (0, 0))
            
            # Dibujar título de la pregunta
            title_text = FONT_LARGE.render(current_question["question"], True, BLACK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(title_text, title_rect)
            
            # Dibujar instrucciones
            instr_text = FONT_SMALL.render("Haz clic en un número y luego en la imagen que corresponde", True, DARK_GRAY)
            instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            screen.blit(instr_text, instr_rect)
            
            # Dibujar etiquetas de columnas
            left_label = FONT_MEDIUM.render("NÚMEROS", True, BLACK)
            right_label = FONT_MEDIUM.render("CANTIDADES", True, BLACK)
            screen.blit(left_label, (200, 250))
            screen.blit(right_label, (SCREEN_WIDTH - 200 - button_width, 250))
            
            # Dibujar todos los botones
            for btn in number_buttons + image_buttons:
                btn.draw(screen)
            
            # Dibujar líneas de conexión para pares ya formados
            for num_idx, img_idx in pairs.items():
                if num_idx < len(number_buttons) and img_idx < len(image_buttons):
                    start_pos = number_buttons[num_idx].rect.midright
                    end_pos = image_buttons[img_idx].rect.midleft
                    color = pair_colors_dict.get(num_idx, BLUE)
                    pygame.draw.line(screen, color, start_pos, end_pos, 4)
            
            # Dibujar línea temporal si hay una selección activa
            if selected_number is not None and selected_image is None:
                mouse_pos = pygame.mouse.get_pos()
                start_pos = number_buttons[selected_number].rect.midright
                pygame.draw.line(screen, LIGHT_BLUE, start_pos, mouse_pos, 3)
            
            # Dibujar botón de enviar
            submit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 100, 160, 50)
            pygame.draw.rect(screen, GREEN, submit_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, submit_rect, 2, border_radius=10)
            submit_text = FONT_MEDIUM.render("ENVIAR", True, WHITE)
            submit_text_rect = submit_text.get_rect(center=submit_rect.center)
            screen.blit(submit_text, submit_text_rect)
            
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    # Verificar clic en botón de enviar
                    if submit_rect.collidepoint(mouse_pos):
                        # Verificar si todas las relaciones son correctas
                        all_correct = True
                        for num_idx, img_idx in pairs.items():
                            number = current_question["numbers"][num_idx]
                            correct_image = current_question["correct_pairs"][number]
                            actual_image = current_question["images"][img_idx]
                            if correct_image != actual_image:
                                all_correct = False
                                break
                        
                        if all_correct and len(pairs) == len(current_question["numbers"]):
                            score += 1
                            flash_color(screen, GREEN)
                        else:
                            flash_color(screen, RED)
                        
                        question_finished = True
                        question_index += 1
                    
                    # Verificar clic en botones de números
                    for i, btn in enumerate(number_buttons):
                        if btn.contains_point(mouse_pos) and i not in pairs:
                            if selected_number == i:
                                selected_number = None  # Deseleccionar
                            else:
                                selected_number = i
                                selected_image = None
                            break
                    
                    # Verificar clic en botones de imágenes
                    for i, btn in enumerate(image_buttons):
                        if btn.contains_point(mouse_pos) and i not in pairs.values():
                            if selected_image == i:
                                selected_image = None  # Deseleccionar
                            else:
                                selected_image = i
                            
                            # Si tenemos ambos seleccionados, formar par
                            if selected_number is not None and selected_image is not None:
                                pairs[selected_number] = selected_image
                                # Asignar color al par
                                if selected_number not in pair_colors_dict:
                                    pair_colors_dict[selected_number] = pair_colors[len(pair_colors_dict) % len(pair_colors)]
                                selected_number = None
                                selected_image = None
                            break
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    
    # Mostrar resultados finales
    show_results(screen, background, score, total_questions)
    pygame.time.wait(3000)
    
    return score

def flash_color(screen, color):
    flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    flash.fill(color)
    flash.set_alpha(150)
    screen.blit(flash, (0, 0))
    pygame.display.flip()
    pygame.time.wait(500)

def show_results(screen, background, score, total):
    screen.blit(background, (0, 0))
    
    result_text = f"Has acertado {score} de {total} preguntas."
    text_surface = FONT_LARGE.render(result_text, True, BLACK)
    rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, rect)
    
    if score == total:
        congrats = FONT_MEDIUM.render("¡Perfecto! 🎉", True, GREEN)
    elif score >= total * 0.75:
        congrats = FONT_MEDIUM.render("¡Muy bien! 👍", True, GREEN)
    elif score >= total * 0.5:
        congrats = FONT_MEDIUM.render("¡Buen trabajo! 😊", True, BLUE)
    else:
        congrats = FONT_MEDIUM.render("¡Sigue practicando! 💪", True, RED)
    
    congrats_rect = congrats.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(congrats, congrats_rect)
    
    continue_text = FONT_SMALL.render("La pantalla se cerrará en 3 segundos...", True, DARK_GRAY)
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
    screen.blit(continue_text, continue_rect)
    
    pygame.display.flip()

if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Relaciona Números con Cantidades - Nivel 3")
    run_quiz_with_timer(screen, "Materials/Pictures/Assets/fondon3-Isis_Segura.png")