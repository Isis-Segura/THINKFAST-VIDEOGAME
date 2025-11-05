import pygame, sys
from Interacciones.Controldeobjetos.pyvidplayer import Video

def run_intro_video(screen, size):
    """
    Inicializa y reproduce el video de introducción.
    Permite saltar el video con cualquier tecla o clic del ratón.
    """
    try:
        intro_path = "Materials/videos/ramiro.mp4" 
        vid = Video(intro_path)
        
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
                    return # Salir de la función
    
            if intro_running and vid.active:
                vid.draw(screen, (0, 0)) 
                pygame.display.flip()
                # Esperar el tiempo adecuado para la reproducción del frame
                pygame.time.wait(int(vid.frame_delay * 1000))
                
        # Asegurarse de cerrar el video si termina por sí mismo
        vid.close() 

    except Exception as e:
        print(f"Advertencia/Error al reproducir el video: {e}. Iniciando en el menú.")
    
# NOTA: La función no toma 'size' pero se mantiene el argumento por consistencia si fuera necesario escalar el video.