import pygame
from scenes.game import Game
from scenes.arena_base import ArenaBase
from scenes.Testes import Testes

def main():
    pygame.init()

    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    pygame.display.set_caption("Meu Jogo")
    clock = pygame.time.Clock()

    game = ArenaBase(screen, screen_width, screen_height)

    fullscreen = True

    running = True
    paused = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Tecla 'P' para pausar/despausar
                    paused = not paused
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen_width, screen_height))

        if not paused:
            # Atualizar e desenhar o jogo apenas se não estiver pausado
            running = game.run()

        clock.tick(60)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
