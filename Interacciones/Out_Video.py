import pygame, sys
# Se asume que Interacciones.Controldeobjetos.pyvidplayer es la ruta correcta
from Interacciones.Controldeobjetos.pyvidplayer import Video 

def run_out_video(screen, size, language):
    """
    Inicializa y reproduce el video.
    NOTA: Se renombró de 'run_intro_video' a 'run_out_video' para resolver el ImportError.
    """
    
    video_clock = pygame.time.Clock()
    FPS = 60 
    
    try:
        if language == 'es':
            intro_path = "Materials/videos/credi.mp4" 
            vid = Video(intro_path)
        else:
            intro_path = "Materials/videos/crediI.mp4" 
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
                vid.draw(screen, (0, 0)) 
                
                pygame.display.flip()
                
                # Controla la velocidad del bucle
                video_clock.tick(FPS)
                
        vid.close() 

    except Exception as e:
        print(f"ERROR FATAL al reproducir el video: {e}. Iniciando en el menú.")