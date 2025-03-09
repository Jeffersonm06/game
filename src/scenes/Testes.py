import pygame
from utils.settings import WHITE
from characters.Defalt import DefaltCharacter
from enemies.defaultEnimy import DefaultEnemy
from utils.Screen import Screen

class Testes(Screen):
    def __init__(self, screen, width, height):
        super().__init__(screen, width, height, width, height)
        self.clock = pygame.time.Clock()
        
        # Cria o jogador e adiciona ao grupo de sprites
        self.player = DefaltCharacter(screen, 130, 130, self.world_width, self.world_height, self.all_sprites)
        self.enemies = [
            DefaultEnemy(screen, 130, 130, self.world_width, self.world_height, self.all_sprites, self.player)
        ]
        self.all_sprites.add(self.player)
        self.all_sprites.add(*self.enemies)

    def run(self):
        dt = self.clock.tick(60) / 1000  # Tempo desde o último frame em segundos
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False

        # Atualiza todos os sprites
        self.update(dt, self.player, self.enemies)
        
        # Desenho da cena
        self.base_surface.fill((111, 111, 111))
        self.draw()
        self.draw_hud()
        
        # Centralizar a superfície na tela
        self.screen.blit(self.base_surface, (0, 0))

        pygame.display.flip()
        return True