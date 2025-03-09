import pygame
from utils.settings import WHITE
from objects import Player
from objects import Obstacle

class Game:
    def __init__(self, screen_width, screen_height):
        self.base_width = screen_width  # Ajuste a largura base para a largura da tela
        self.base_height = screen_height  # Ajuste a altura base para a altura da tela
        self.base_surface = pygame.Surface((self.base_width, self.base_height))
        self.world_width = 3000  # Largura do mundo
        self.world_height = 1500  # Altura do mundo
        self.player = Player(100, 100, self.world_width, self.world_height)
        self.camera = pygame.Rect(0, 0, self.base_width, self.base_height)
        self.clock = pygame.time.Clock()
        self.obstacles = self.create_obstacle_course()

    def create_obstacle_course(self):
        """Cria uma série de obstáculos para a corrida."""
        obstacles = [
            # x, y, width, height, world_width, world_height, image_path, color, moving
            Obstacle(0, self.world_height - 900, 70, 900, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(self.world_width - 70, self.world_height - 900, 70, 900, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(500, self.world_height - 200, 500, 50, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(self.world_width - 1070, self.world_height - 200, 500, 50, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(self.world_width // 2 - 320, self.world_height - 350, 500, 50, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(self.world_width // 2 - 95, self.world_height - 600, 50, 300, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(500, self.world_height - 500, 500, 50, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(self.world_width - 1070, self.world_height - 500, 500, 50, self.world_width, self.world_height, image_path="assets/images/parede.png"),
        ]

        # Obstáculos móveis
        self.moving_obstacles = [
            # x, y, width, height, world_width, world_height, image_path, color, moving, direction
            Obstacle(400, 1100, 70, 70, self.world_width, self.world_height, color=(255, 127, 80), moving=True, direction='horizontal'),  # Coral
            Obstacle(800, 1400, 100, 100, self.world_width, self.world_height, image_path="assets/images/parede.png", moving=True, direction='horizontal'),
        ]

        return obstacles + self.moving_obstacles


    def run(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False

        # Atualização dos elementos
        self.player.update(self.obstacles)
        self.update_camera()
        self.update_moving_obstacles()

        # Desenhar as fireballs diretamente na tela ajustando pela câmera
        for fireball in self.player.fireballs:
            fireball_position = (fireball.rect.x - self.camera.x, fireball.rect.y - self.camera.y)
            screen.blit(fireball.image, fireball_position)
            fireball.update(self.obstacles, self.world_width, self.world_height)

        # Desenho dos elementos na superfície base
        self.base_surface.fill((WHITE))
        self.draw_world()

        # Centralizar a superfície na tela
        screen.blit(self.base_surface, (0, 0))

        pygame.display.flip()
        return True

    def update_camera(self):
        # Centrando a câmera no jogador
        self.camera.center = self.player.rect.center

        # Garantir que a câmera não saia dos limites do mundo
        self.camera.clamp_ip(pygame.Rect(0, 0, self.world_width, self.world_height))

    def update_moving_obstacles(self):
        for obstacle in self.moving_obstacles:
            obstacle.update()

    def draw_world(self):
        # Desenhar o jogador ajustando pela câmera
        player_position = (self.player.rect.topleft[0] - self.camera.topleft[0], 
                           self.player.rect.topleft[1] - self.camera.topleft[1])
        self.base_surface.blit(self.player.image, player_position)

        # Desenhar os obstáculos ajustando pela câmera
        for obstacle in self.obstacles:
            obstacle_position = (obstacle.rect.topleft[0] - self.camera.topleft[0], 
                                 obstacle.rect.topleft[1] - self.camera.topleft[1])
            self.base_surface.blit(obstacle.image, obstacle_position)
