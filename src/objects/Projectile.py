import pygame
from objects.Obstacle import Obstacle

class Projectile(pygame.sprite.Sprite):
    def __init__(self, user, screen, x, y, direction, speed=1000):
        super().__init__()
        self.user = user
        self.screen = screen
        self.direction = direction
        self.speed = speed
        self.radius = 10  # Raio da esfera de projétil
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), self.radius)  # Esfera vermelha
        self.rect = self.image.get_rect(center=(x, y))
        self.damage = 10  # Dano causado pelo projétil
        self.collide = False
        self.should_be_removed = False  # Atributo para marcar projéteis que devem ser removidos

    def update(self, dt, obstacles=[], enemies=[]):
        """Atualiza a posição do projétil e verifica colisão com obstáculos e inimigos."""
        if self.direction == 'left':
            self.rect.centerx -= self.speed * dt
        elif self.direction == 'right':
            self.rect.centerx += self.speed * dt
        elif self.direction == 'up':
            self.rect.centery -= self.speed * dt
        elif self.direction == 'down':
            self.rect.centery += self.speed * dt

        # Verifica colisão com obstáculos
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.handle_collision(obstacle)
                self.should_be_removed = True  # Marca para remoção após a colisão
                return

        # Verifica colisão com inimigos
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.handle_collision(enemy)
                self.should_be_removed = True  # Marca para remoção após a colisão
                return

    def handle_collision(self, target):
        """Lógica de colisão. Pode ser obstáculo ou inimigo."""
        if isinstance(target, Obstacle):
            self.collide = True
            print("Colidiu com um obstáculo!")
        else :
            self.collide = True
            print("Colidiu com um inimigo!")
            target.take_damage(2, self.direction)  # Supondo que os inimigos têm um método 'take_damage'
        