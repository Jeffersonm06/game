import pygame
from utils.settings import WHITE
from objects.Player import Player
from objects.Obstacle import Obstacle
from utils.Screen import Screen
from characters.Defalt import DefaltCharacter

class ArenaBase(Screen):
    def __init__(self, screen, width, height):
        super().__init__(screen, width, height, 2000, 1000)
        self.clock = pygame.time.Clock()
        self.player = DefaltCharacter(screen, 130, 130, self.world_width, self.world_height, self.all_sprites)
        self.create_obstacles()
        #self.create_moving_obstacles()
        self.all_sprites.add(self.player)

    def create_obstacles(self):
        self.create_obstacles_course([
            Obstacle(0, self.world_height - 900, 70, 900, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(self.world_width - 70, self.world_height - 900, 70, 900, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(0, self.world_height - 200, 500, 50, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(self.world_width - 500, self.world_height - 200, 500, 50, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(self.world_width // 2 - 320, self.world_height - 350, 500, 50, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(self.world_width // 2 - 95, self.world_height - 600, 50, 300, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(self.world_width // 2 - 320, self.world_height - 610, 500, 50, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(0, self.world_height - 500, 500, 50, self.world_width, self.world_height, image_path="assets/images/parede.png"),
            Obstacle(self.world_width - 500, self.world_height - 500, 500, 50, self.world_width, self.world_height, image_path="assets/images/parede.png"),
        ])

    """ def create_moving_obstacles(self):
        self.create_moving_obstacles_course([
            Obstacle(400, 500, 70, 70, self.world_width, self.world_height, image_path="assets/images/parede.png", moving=True, direction='vertical'),
            Obstacle(800, self.world_height - 600, 70, 70, self.world_width, self.world_height, image_path="assets/images/parede.png", moving=True, direction='horizontal'),
            Obstacle(800, self.world_height - 100, 70, 70, self.world_width, self.world_height, image_path="assets/images/parede.png", moving=True, direction='horizontal'),
            Obstacle(self.world_width - 470, 500, 70, 70, self.world_width, self.world_height, image_path="assets/images/parede.png", moving=True, direction='vertical'),
        ]) """

    def run(self):
        dt = self.clock.tick(60) / 1000  # Tempo desde o último frame em segundos
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False

        # Atualização dos elementos
        self.update(dt, self.player)

        # Desenho da cena
        self.base_surface.fill(WHITE)
        self.draw()

        # Centralizar a superfície na tela
        self.screen.blit(self.base_surface, (0, 0))

        pygame.display.flip()
        return True

