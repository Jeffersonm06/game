import pygame

class Hud(pygame.sprite.Sprite):
    def __init__(self, player_image, world_width, world_height, health, max_health, magic, max_magic):
        super().__init__()
        self.image = pygame.Surface((world_width, world_height // 4), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))

        # Carrega a imagem do personagem
        self.player_image = pygame.transform.scale(player_image, (100, 100))
        
        # Atributos do jogador
        self.health = health
        self.max_health = max_health
        self.magic = magic
        self.max_magic = max_magic

    def update(self, health=None, magic=None):
        if health is not None:
            self.health = health
        if magic is not None:
            self.magic = magic
        self.redraw()


    def redraw(self):
        # Limpa a superfície
        self.image.fill((0, 0, 0, 0))  # Preenche com transparente
        
        # Desenha a imagem do jogador
        self.image.blit(self.player_image, (10, 10))
        
        # Desenha os círculos vermelhos para a vida
        for i in range(self.max_health):
            color = (255, 0, 0) if i < self.health else (128, 0, 0)
            pygame.draw.circle(self.image, color, (150 + i * 30, 50), 15)

        # Desenha a barra de magia
        magic_bar_width = 200
        magic_bar_height = 20
        filled_width = int((self.magic / self.max_magic) * magic_bar_width)
        pygame.draw.rect(self.image, (0, 0, 255), (10, 120, filled_width, magic_bar_height))
        pygame.draw.rect(self.image, (255, 255, 255), (10, 120, magic_bar_width, magic_bar_height), 2)
