import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, world_width, world_height, image_path=None, color=None, moving=False, direction="vertical"):
        super().__init__()
        if image_path:
            original_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (width, height))
        elif color:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        else:
            # Default to a gray color if no image or color is provided
            self.image = pygame.Surface((width, height))
            self.image.fill((128, 128, 128))

        if y <= 0:
            self.rect = pygame.Rect(x, world_height - height, width, height)
        else:
            self.rect = pygame.Rect(x, y, width, height)

        self.speed = 3 if moving else 0
        self.world_width = world_width
        self.world_height = world_height
        self.moving = moving
        self.direction = direction  # Direção do movimento: "vertical" ou "horizontal"

    def update(self, *args):
        """Atualiza a posição do obstáculo se estiver em movimento."""
        if self.moving:
            if self.direction == "vertical":
                # Movimento vertical
                self.rect.y += self.speed
                if self.rect.top <= 0 or self.rect.bottom >= self.world_height:
                    self.speed = -self.speed
            elif self.direction == "horizontal":
                # Movimento horizontal
                self.rect.x += self.speed
                if self.rect.left <= 0 or self.rect.right >= self.world_width:
                    self.speed = -self.speed
