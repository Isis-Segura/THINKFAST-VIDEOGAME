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
        self.color = (250, 250, 250)
        self.border_color = (250, 250, 250)
        self.font = pygame.font.SysFont(None, 20)
        self.text_surface = self.font.render("preguntas", True, (30, 30, 30))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        # Lógica del quiz
        self.questions = questions
        self.current_question = 0
        self.correct_answers = 0
        self.answer_color = None
        self.finished = False  # bandera para indicar que acabó el quiz

        # Crear botones para las respuestas
        self.button_height = 50
        self.buttons = self.create_buttons()

    def create_buttons(self):
        buttons = []
        button_width = self.width - 40
        button_y_start = self.rect.top + 300

        for i in range(4):
            button_rect = pygame.Rect(
                (self.screen_width - button_width) / 2,
                button_y_start + i * (self.button_height + 10),
                button_width,
                self.button_height
            )
            buttons.append({"rect": button_rect, "text": self.questions[self.current_question]["choices"][i]})
        return buttons

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 5)
        surface.blit(self.text_surface, self.text_rect)
        

        # mostrar la pregunta actual
        image = pygame.image.load(self.questions[self.current_question]["image"])
        image = pygame.transform.scale(image, (self.width - 40, 100))
        surface.blit(image, (self.rect.x + 20, self.rect.y + 50))

        for button in self.buttons:
            # si ya respondió, color cambia
            button_color = (255, 165, 0)  # naranja por defecto
            if self.answer_color:
                button_color = self.answer_color
            pygame.draw.rect(surface, button_color, button["rect"])
            text_surface = self.font.render(button["text"], True, (30, 30, 30))
            text_rect = text_surface.get_rect(center=button["rect"].center)
            surface.blit(text_surface, text_rect)

        correct_text = f"ACIERTOS: {self.correct_answers}"
        correct_surface = self.font.render(correct_text, True, (30, 30, 30))
        surface.blit(correct_surface, (self.rect.x + 20, self.rect.y + self.height - 40))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, button in enumerate(self.buttons):
                if button["rect"].collidepoint(mouse_pos):
                    self.check_answer(i)

    def check_answer(self, index):
        correct_index = self.questions[self.current_question]["correct_answer"]
        if index == correct_index:
            self.answer_color = (0, 255, 0)
            self.correct_answers += 1
        else:
            self.answer_color = (255, 0, 0)
        pygame.time.delay(1000)
        self.next_question()

    def next_question(self):
        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.finished = True
            self.show_results()
        else:
            self.buttons = self.create_buttons()
            self.answer_color = None

    def show_results(self):
        self.answer_color = None
        print(f"Has respondido correctamente {self.correct_answers} de {len(self.questions)} preguntas.")
        pygame.time.delay(2000)
