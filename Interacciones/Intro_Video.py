import pygame, sys
from Interacciones.Controldeobjetos.pyvidplayer import Video 

def run_intro_video(screen, size, skip_img1, skip_img3, skip_img2):
    """
    Inicializa y reproduce el video de introducción, incluyendo un botón de saltar 
    con retraso y animación de entrada.
    """
    
    # ------------------ CONFIGURACIÓN DEL BOTÓN DE SALTAR ------------------
    SKIP_BUTTON_SIZE = (120, 80) 
    SKIP_PADDING = 15
    
    # Posición FINAL del botón (Esquina Inferior Derecha)
    FINAL_X = size[0] - SKIP_BUTTON_SIZE[0] - SKIP_PADDING
    FINAL_Y = size[1] - SKIP_BUTTON_SIZE[1] - SKIP_PADDING
    
    # Posición inicial para la animación (fuera de la pantalla, a la derecha)
    INITIAL_X = size[0] 
    
    # Variables de Control de Animación y Tiempo
    DELAY_MS = 3000          # 3 segundos de retraso antes de que empiece a aparecer
    ANIMATION_SPEED = 4     # Velocidad de deslizamiento (píxeles por frame)
    
    # Estado del Botón
    button_pressed = None 
    is_button_ready = False  # Bandera para saber si el tiempo de retraso terminó
    BUTTON_CURRENT_X = INITIAL_X # Posición X actual para la animación
    
    # El rectángulo final, usado para la detección de colisión/clic.
    skip_button_rect = pygame.Rect(FINAL_X, FINAL_Y, SKIP_BUTTON_SIZE[0], SKIP_BUTTON_SIZE[1])
    
    # Asegurar que las imágenes tengan el tamaño correcto
    skip_img1 = pygame.transform.scale(skip_img1, SKIP_BUTTON_SIZE)
    skip_img3 = pygame.transform.scale(skip_img3, SKIP_BUTTON_SIZE)
    skip_img2 = pygame.transform.scale(skip_img2, SKIP_BUTTON_SIZE)
    
    # ------------------ REPRODUCCIÓN DEL VIDEO ------------------
    video_clock = pygame.time.Clock()
    FPS = 60 
    START_TIME = pygame.time.get_ticks() # Registra el tiempo de inicio
    
    try:
        intro_path = "Materials/videos/intro.mp4" 
        vid = Video(intro_path)
        vid.set_size(size) 
        
        intro_running = True
        while intro_running and vid.active:
            
            mouse_pos = pygame.mouse.get_pos()
            current_time = pygame.time.get_ticks()
            
            # 1. Lógica de Activación del Botón (Retraso)
            if not is_button_ready and current_time - START_TIME >= DELAY_MS:
                is_button_ready = True
            
            # 2. Lógica de Animación (Deslizamiento)
            if is_button_ready and BUTTON_CURRENT_X > FINAL_X:
                BUTTON_CURRENT_X = max(FINAL_X, BUTTON_CURRENT_X - ANIMATION_SPEED)
            
            # 3. Actualizar la posición del rectángulo de clic para el frame actual
            skip_button_rect.x = BUTTON_CURRENT_X

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    vid.close()
                    pygame.quit()
                    sys.exit()
                
                # --- LÓGICA DEL BOTÓN DE SALTAR (Solo si la animación terminó o está visible) ---
                if is_button_ready:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # Usamos skip_button_rect para la colisión
                        if skip_button_rect.collidepoint(event.pos):
                            button_pressed = "skip"
                            
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if button_pressed == "skip" and skip_button_rect.collidepoint(event.pos):
                            vid.close()
                            intro_running = False
                            return 
                        button_pressed = None
                
                # --- LÓGICA de Tecla de Salto (ESC) ---
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    vid.close()
                    intro_running = False
                    return 
        
            if intro_running and vid.active:
                # 1. Dibuja el frame del video
                vid.draw(screen, (0, 0)) 
                
                # 2. Dibuja el botón de saltar SÓLO si está listo o animándose
                if is_button_ready:
                    
                    if button_pressed == "skip" and skip_button_rect.collidepoint(mouse_pos):
                        current_skip_img = skip_img2 # Clicked
                    elif skip_button_rect.collidepoint(mouse_pos) and BUTTON_CURRENT_X == FINAL_X:
                        # Sólo hover si la animación ya terminó
                        current_skip_img = skip_img3 
                    else:
                        current_skip_img = skip_img1 # Normal
                        
                    # Dibuja el botón en su posición actual (BUTTON_CURRENT_X, FINAL_Y)
                    screen.blit(current_skip_img, (BUTTON_CURRENT_X, FINAL_Y))
                
                pygame.display.flip()
                video_clock.tick(FPS)
                
        vid.close() 

    except Exception as e:
        print(f"ERROR FATAL al reproducir el video con pyvidplayer: {e}. Iniciando en el menú.")
        return