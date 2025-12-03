import pygame, sys
from Interacciones.Controldeobjetos.pyvidplayer import Video 

def run_out_video(screen, size, language, skip_img1, skip_img3, skip_img2):
    """
    Inicializa y reproduce el video de salida (créditos), incluyendo un botón de saltar 
    con retraso, animación de entrada y animación de clic (3 estados).
    """
    
    # ------------------ CONFIGURACIÓN DEL BOTÓN DE SALTAR (COPIADO DE Intro_Video.py) ------------------
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
    button_clicked_state = None  # Almacena el ID del botón presionado ("skip")
    is_button_ready = False      # Bandera para saber si el tiempo de retraso terminó
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
        # Lógica para seleccionar el video según el idioma
        if language == 'es':
            intro_path = "Materials/videos/credi.mp4" 
        else:
            intro_path = "Materials/videos/crediI.mp4" 
            
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
            skip_button_rect.x = BUTTON_CURRENT_X # Importante para la colisión

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    vid.close()
                    pygame.quit()
                    sys.exit()
                
                # --- LÓGICA DEL BOTÓN DE SALTAR (3 ESTADOS) ---
                # Solo interactuable cuando la animación terminó y está listo
                if is_button_ready and BUTTON_CURRENT_X == FINAL_X: 
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if skip_button_rect.collidepoint(event.pos):
                            # 🔥 CAMBIO DE IMAGEN A PRESIONADO (skip_img2) 🔥
                            button_clicked_state = "skip" 
                            
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        # Acción: Saltar (Sólo si soltamos el botón sobre el área de colisión)
                        if button_clicked_state == "skip" and skip_button_rect.collidepoint(event.pos):
                            vid.close()
                            intro_running = False
                            return 
                        # Reinicia el estado visual
                        button_clicked_state = None
                
                # --- LÓGICA de Tecla de Salto (ESC) ---
                # Se mantiene la opción de saltar con ESC
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    vid.close()
                    intro_running = False
                    return 
                
                # Se elimina la lógica de MOUSEBUTTONDOWN para saltar, ya que ahora usamos el botón.
                # if event.type == pygame.MOUSEBUTTONDOWN: # ELIMINADO

            if intro_running and vid.active:
                # 1. Dibuja el frame del video
                vid.draw(screen, (0, 0)) 
                
                # 2. Dibuja el botón de saltar
                if is_button_ready:
                    
                    # Lógica para seleccionar la imagen correcta (3 estados)
                    if button_clicked_state == "skip" and skip_button_rect.collidepoint(mouse_pos):
                        # 🔴 ESTADO PRESIONADO/CLIC: Usa skip_img2
                        current_skip_img = skip_img2 
                    elif skip_button_rect.collidepoint(mouse_pos) and BUTTON_CURRENT_X == FINAL_X:
                        # 🟡 ESTADO HOVER: Usa skip_img3 (el que se vuelve algo blanco)
                        current_skip_img = skip_img3 
                    else:
                        # 🟢 ESTADO NORMAL: Usa skip_img1
                        current_skip_img = skip_img1 
                        
                    # Dibuja el botón en su posición actual (X animada, Y final)
                    screen.blit(current_skip_img, (BUTTON_CURRENT_X, FINAL_Y))
                
                pygame.display.flip()
                video_clock.tick(FPS)
                
        vid.close() 

    except Exception as e:
        print(f"ERROR FATAL al reproducir el video: {e}. Iniciando en el menú.")
        return