import pygame
import time
import random

FONT_NAME = None  # Usa la fuente por defecto si no se proporciona
FONT_SIZE = 20
BOARD_PADDING = 20
BOARD_WIDTH = 760
BOARD_HEIGHT = 460

# Colores para emparejamientos (se rotan por cada relación formada)
PAIR_COLORS = [
    (255, 99, 71),      # tomato
    (60, 179, 113),     # medium sea green
    (30, 144, 255),     # dodger blue
    (218, 112, 214),    # orchid
    (255, 215, 0),      # gold
    (244, 164, 96),     # sandy brown
]


def draw_text(surface, text, pos, font, color=(0, 0, 0)):
    surf = font.render(text, True, color)
    surface.blit(surf, pos)
    return surf.get_rect(topleft=pos)


def _compute_layout(board_rect, question_data, font):
    """
    Devuelve estructuras de layout para dibujar y detectar clicks:
    - left_rects: list of pygame.Rect (coordenadas ABSOLUTAS)
    - right_rects: list of pygame.Rect (ABSOLUTAS)
    - question_rect: área donde se dibuja la pregunta
    - top_y, per_h, left_x, right_x: valores para dibujado
    """
    left_items = question_data.get("left", [])
    right_items = question_data.get("right", [])

    # Área de la pregunta
    q_x = board_rect.left + BOARD_PADDING
    q_y = board_rect.top + BOARD_PADDING

    title_font = pygame.font.Font(FONT_NAME, FONT_SIZE + 2)
    q_height = title_font.size(question_data.get("question", ""))[1] + 8

    top_y = board_rect.top + BOARD_PADDING + q_height + 6
    max_items = max(len(left_items), len(right_items), 1)
    per_h = (BOARD_HEIGHT - (top_y - board_rect.top) - BOARD_PADDING - 40) // max_items

    left_x = board_rect.left + BOARD_PADDING
    right_x = board_rect.left + BOARD_WIDTH // 2 + BOARD_PADDING

    left_rects = []
    right_rects = []

    for i in range(len(left_items)):
        r = pygame.Rect(left_x, top_y + i * per_h, BOARD_WIDTH // 2 - BOARD_PADDING * 2, per_h - 6)
        left_rects.append(r)

    for j in range(len(right_items)):
        r = pygame.Rect(right_x, top_y + j * per_h, BOARD_WIDTH // 2 - BOARD_PADDING * 2, per_h - 6)
        right_rects.append(r)

    question_rect = pygame.Rect(q_x, q_y, BOARD_WIDTH - BOARD_PADDING * 2, q_height)
    return left_rects, right_rects, question_rect, top_y, per_h, left_x, right_x


def show_question_board(screen, question_data, font=None, time_limit=None):
    """
    Muestra una pizarra blanca simple encima del fondo del nivel.
    Interacción:
        - Clic en un ítem izquierdo → selección
        - Clic en un ítem derecho → formar relación
        - ENTER/ESPACIO → enviar y salir
        - ESC → cancelar
        - Si expira el tiempo → devuelve timeout
    Retorna:
        {"pairs": {left_index: right_index, ...}, "cancelled": bool, "timeout": bool}
    """
    clock = pygame.time.Clock()
    if font is None:
        font = pygame.font.Font(FONT_NAME, FONT_SIZE)

    sw, sh = screen.get_size()

    # Tablero centrado
    board_rect = pygame.Rect((sw - BOARD_WIDTH) // 2, (sh - BOARD_HEIGHT) // 2, BOARD_WIDTH, BOARD_HEIGHT)
    left_items = question_data.get("left", [])
    right_items = question_data.get("right", [])

    if len(left_items) == 0 or len(right_items) == 0:
        return {"cancelled": True}

    pairs = {}          # left_index -> right_index
    pair_colors = {}    # left_index -> color
    left_selected = None
    running = True
    start_ticks = pygame.time.get_ticks()
    remaining = time_limit if time_limit is not None else None

    # Bucle principal
    while running:
        dt = clock.tick(30)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return {"cancelled": True}

            elif ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    running = False
                    break
                if ev.key == pygame.K_ESCAPE:
                    return {"cancelled": True}

            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                left_rects, right_rects, _, _, _, _, _ = _compute_layout(board_rect, question_data, font)

                # Click en izquierda
                for i, r in enumerate(left_rects):
                    if r.collidepoint(mx, my):
                        left_selected = None if left_selected == i else i
                        break

                # Click en derecha
                if left_selected is not None:
                    for j, r in enumerate(right_rects):
                        if r.collidepoint(mx, my):
                            pairs[left_selected] = j
                            if left_selected not in pair_colors:
                                pair_colors[left_selected] = random.choice(PAIR_COLORS)
                            left_selected = None
                            break

        # Actualizar temporizador
        if remaining is not None:
            elapsed = (pygame.time.get_ticks() - start_ticks) / 1000.0
            remaining = max(0.0, time_limit - elapsed)
            if remaining <= 0.0:
                return {"timeout": True, "pairs": pairs}

        # --- DIBUJADO ---
        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        # Tablero blanco
        pygame.draw.rect(screen, (255, 255, 255), board_rect)
        pygame.draw.rect(screen, (0, 0, 0), board_rect, 3)

        left_rects, right_rects, question_rect, _, _, _, _ = _compute_layout(board_rect, question_data, font)

        # Pregunta
        title_font = pygame.font.Font(FONT_NAME, FONT_SIZE + 2)
        q_lines = str(question_data.get("question", "")).split("\n")
        qy = question_rect.top
        for line in q_lines:
            qsurf = title_font.render(line, True, (10, 10, 10))
            screen.blit(qsurf, (question_rect.left, qy))
            qy += qsurf.get_height() + 2

        # Timer
        if remaining is not None:
            timer_text = f"Tiempo: {int(remaining)}s"
            t_surf = font.render(timer_text, True, (20, 20, 20))
            t_rect = t_surf.get_rect(topright=(board_rect.right - BOARD_PADDING, board_rect.top + 2))
            screen.blit(t_surf, t_rect)

        # Columna izquierda
        for i, item in enumerate(left_items):
            r = left_rects[i]
            if i == left_selected:
                bg = (200, 230, 255)
            elif i in pairs:
                bg = (230, 255, 230)
            else:
                bg = (245, 245, 245)
            pygame.draw.rect(screen, bg, r, border_radius=6)
            pygame.draw.rect(screen, (0, 0, 0), r, 1, border_radius=6)
            txt = font.render(f"{i + 1}. {item}", True, (10, 10, 10))
            screen.blit(txt, (r.left + 8, r.top + (r.height - txt.get_height()) // 2))

        # Columna derecha
        for j, item in enumerate(right_items):
            r = right_rects[j]
            matched_left = None
            for li, ri in pairs.items():
                if ri == j:
                    matched_left = li
                    break
            if matched_left is not None:
                color = pair_colors.get(matched_left, (200, 200, 200))
                bg = tuple(min(255, c + 30) for c in color)
            else:
                bg = (245, 245, 245)
            pygame.draw.rect(screen, bg, r, border_radius=6)
            pygame.draw.rect(screen, (0, 0, 0), r, 1, border_radius=6)
            txt = font.render(f"{chr(65 + j)}. {item}", True, (10, 10, 10))
            screen.blit(txt, (r.left + 8, r.top + (r.height - txt.get_height()) // 2))

        # Líneas que conectan pares
        for li, ri in pairs.items():
            if li < len(left_rects) and ri < len(right_rects):
                lrect = left_rects[li]
                rrect = right_rects[ri]
                start_pos = (lrect.right - 4, lrect.centery)
                end_pos = (rrect.left + 4, rrect.centery)
                color = pair_colors.get(li, random.choice(PAIR_COLORS))
                pygame.draw.line(screen, color, start_pos, end_pos, 6)
                inner = tuple(max(0, c - 60) for c in color)
                pygame.draw.line(screen, inner, start_pos, end_pos, 2)

        # Instrucciones
        instr = "Selecciona una opción izquierda y luego su pareja derecha. ENTER/ESPACIO enviar - ESC cancelar"
        instr_surf = font.render(instr, True, (30, 30, 30))
        instr_pos = instr_surf.get_rect(midbottom=(board_rect.centerx, board_rect.bottom - BOARD_PADDING))
        screen.blit(instr_surf, instr_pos)

        pygame.display.flip()

    return {"pairs": pairs, "cancelled": False, "timeout": False}