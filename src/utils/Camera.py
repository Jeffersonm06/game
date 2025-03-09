import pygame

class Camera:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.camera_rect = pygame.Rect(0, 0, 0, 0)

    def apply(self, entity):
        """Ajusta a posição de um objeto baseado na posição atual da câmera."""
        return entity.rect.move(-self.camera_rect.left, -self.camera_rect.top)

    def center_on(self, target_rect):
        """Centraliza a câmera em relação ao alvo (jogador)."""
        self.camera_rect = pygame.Rect(
            target_rect.centerx - self.camera_rect.width // 2,
            target_rect.centery - self.camera_rect.height // 2,
            self.camera_rect.width,
            self.camera_rect.height
        )

        # Garantir que a câmera não ultrapasse os limites do mundo
        self.camera_rect.clamp_ip(pygame.Rect(0, 0, self.world_width, self.world_height))
