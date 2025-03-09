import pygame

class Fireball:
    def __init__(self, x, y, direction, width, height):
        # Cria uma superfície transparente
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Desenha um círculo vermelho na superfície
        pygame.draw.circle(self.image, (255, 0, 0), (width // 2, height // 2), min(width, height) // 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 5
        self.active = True

    def update(self, obstacles, world_width, world_height):
        # Movimentação da fireball na direção especificada
        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        # Verificar colisão com limites do mundo
        if self.rect.left < 0 or self.rect.right > world_width:
            self.active = False

        # Verificar colisão com obstáculos
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.active = False
                break

    def draw(self, screen):
        screen.blit(self.image, self.rect)