import pygame

class InventoryWindow:
    def __init__(self, screen_size, questions):
        self.width = 800
        self.height = 600
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.rect = pygame.Rect(
            (self.screen_width - self.width) / 2,
            (self.screen_height - self.height) / 2,
            self.width,
            self.height
        )

        self.bg_color = (240, 240, 240)
        self.font = pygame.font.SysFont(None, 28)

        # Quiz
        self.questions = questions
        self.current_question = 0
        self.correct_answers = 0
        self.answer_colors = [None] * 4
        self.finished = False

        # Botones
        self.button_width = (self.width // 2) - 60
        self.button_height = 60
        self.buttons = self.create_buttons()

    def create_buttons(self):
        buttons = []
        margin_x = 40
        margin_y = 300
        spacing_x = 40
        spacing_y = 20

        for i in range(4):
            col = i % 2
            row = i // 2
            button_rect = pygame.Rect(
                self.rect.x + margin_x + col * (self.button_width + spacing_x),
                self.rect.y + margin_y + row * (self.button_height + spacing_y),
                self.button_width,
                self.button_height
            )
            buttons.append({
                "rect": button_rect,
                "text": self.questions[self.current_question]["choices"][i]
            })
        return buttons

    def draw(self, surface):
        # Fondo
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 4)

        # Imagen de la pregunta
        image = pygame.image.load(self.questions[self.current_question]["image"])
        image = pygame.transform.scale(image, (250, 150))
        image_rect = image.get_rect(center=(self.rect.centerx, self.rect.y + 100))
        surface.blit(image, image_rect)

        # Pregunta
        question_text = self.questions[self.current_question]["question"]
        question_surface = self.font.render(question_text, True, (0, 0, 0))
        question_rect = question_surface.get_rect(center=(self.rect.centerx, self.rect.y + 220))
        surface.blit(question_surface, question_rect)

        # Botones
        for i, button in enumerate(self.buttons):
            color = (255, 140, 0)  # naranja por defecto
            if self.answer_colors[i]:
                color = self.answer_colors[i]
            pygame.draw.rect(surface, color, button["rect"])
            text_surface = self.font.render(button["text"], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=button["rect"].center)
            surface.blit(text_surface, text_rect)

        # Aciertos
        correct_text = f"Aciertos: {self.correct_answers}"
        correct_surface = self.font.render(correct_text, True, (0, 0, 0))
        surface.blit(correct_surface, (self.rect.x + 20, self.rect.y + self.height - 40))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.finished:
            mouse_pos = event.pos
            for i, button in enumerate(self.buttons):
                if button["rect"].collidepoint(mouse_pos):
                    self.check_answer(i)

    def check_answer(self, index):
        correct_index = self.questions[self.current_question]["correct_answer"]
        self.answer_colors = [None] * 4
        if index == correct_index:
            self.answer_colors[index] = (0, 255, 0)  # verde
            self.correct_answers += 1
        else:
            self.answer_colors[index] = (255, 0, 0)  # rojo
            self.answer_colors[correct_index] = (0, 255, 0)  # correcto verde
        pygame.time.delay(1000)
        self.next_question()

    def next_question(self):
        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.finished = True
            self.show_results()
        else:
            self.buttons = self.create_buttons()
            self.answer_colors = [None] * 4

    def show_results(self):
        print(f"Has respondido correctamente {self.correct_answers} de {len(self.questions)} preguntas.")
        pygame.time.delay(2000)


# ------------------ EJEMPLO DE USO ------------------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Quiz Normal")

    questions = [ 
        {
            "image": "Materials/Pictures/imagen1.jpg",
            "question": "¿Cómo se llama nuestro país?",
            "choices": ["España", "México", "Roma", "Berlín"],
            "correct_answer": 1
        },
        {
            "image": "Materials/Pictures/imagen2.jpg",
            "question": "Si tienes 5 manzanas y te comes 2, ¿cuántas manzanas te quedan?",
            "choices": ["5", "4", "3", "10"],
            "correct_answer": 1
        },
        {
            "image": "Materials/Pictures/imagen3.jpg",
            "question": "¿En qué estación del año las hojas de los árboles cambian de color y caen?",
            "choices": ["primavera", "verano", "otoño", "invierno"],
            "correct_answer": 2
        },
        {
            "image": "Materials/Pictures/imagen4.jpg",
            "question": "que se celebra el 1 de noviembre?",
            "choices": ["DIA DE MUERTOS", "NAVIDAD", "10 DE MAYO", "AÑO NUEVO"],
            "correct_answer": 0
        }
    ]

    quiz = InventoryWindow((800, 600), questions)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            quiz.handle_event(event)

        quiz.draw(screen)
        pygame.display.flip()