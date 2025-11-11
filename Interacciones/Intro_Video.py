import pygame, sys
# Se asume que Interacciones.Controldeobjetos.pyvidplayer es la ruta correcta
from Interacciones.Controldeobjetos.pyvidplayer import Video 

def run_intro_video(screen, size):
    """
    Inicializa y reproduce el video de introducción.
    Solución: Se utiliza vid.set_size() y vid.draw() para que la librería
    maneje la reproducción, el avance y el escalado automáticamente.
    """
    
    video_clock = pygame.time.Clock()
    FPS = 60 
    
    try:
        intro_path = "Materials/videos/intro.mp4" 
        vid = Video(intro_path)
        
        # PASO CRÍTICO: Usar el método de la librería para escalar la salida
        vid.set_size(size) 
        
        intro_running = True
        while intro_running and vid.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    vid.close()
                    pygame.quit()
                    sys.exit()
                
                # Permite saltar el video con teclado o ratón
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    vid.close()
                    intro_running = False
                    return 
    
            if intro_running and vid.active:
                # Usa el método draw() de la clase Video, que internamente:
                # 1. Llama a _update() (avanza el frame y obtiene la superficie)
                # 2. Escala la superficie si se llamó a set_size()
                # 3. Dibuja la superficie en la pantalla (screen)
                vid.draw(screen, (0, 0)) 
                
                pygame.display.flip()
                
                # Controla la velocidad del bucle
                video_clock.tick(FPS)
                
        vid.close() 

    except Exception as e:
        print(f"ERROR FATAL al reproducir el video: {e}. Iniciando en el menú.")