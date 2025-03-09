import pygame
from utils.Camera import Camera
from utils.hud import Hud

class Screen:
    def __init__(self, screen, width, height, world_width, world_height):
        self.screen = screen
        self.width = width
        self.height = height
        self.base_surface = pygame.Surface((self.width, self.height))
        self.world_width = world_width
        self.world_height = world_height
        self.camera = Camera(world_width, world_height)
        self.camera.camera_rect = pygame.Rect(0, 0, self.width, self.height)
        self.clock = pygame.time.Clock()
        self.player = None
        self.obstacles = []
        self.moving_obstacles = []
        self.enemies = []
        self.projectiles = []

        # Inicializa o grupo de todos os sprites
        self.all_sprites = pygame.sprite.Group()
        self.hud = None

    def update(self, dt, player=None, enemies=[]):
        self.player = player

        # Evitar adicionar inimigos repetidamente
        self.enemies = enemies

        if self.player and not self.hud:
            # Inicializa o HUD apenas uma vez quando o player está disponível
            self.hud = Hud(
                self.player.image,
                self.world_width,
                self.world_height,
                self.player.health,
                self.player.max_health,
                self.player.magic,
                self.player.max_magic
            )

        # Definindo os obstáculos e inimigos no player
        self.player.obstacles = self.obstacles + self.moving_obstacles
        self.player.enemies = self.enemies

        self.player.update(dt)
        self.camera.center_on(self.player.rect)
        self.update_moving_obstacles()

        try:
            for projectile in self.player.projectiles[:]:
                self.draw_projectile(projectile)
                projectile.update(dt, self.obstacles + self.moving_obstacles, self.enemies)
                if projectile.should_be_removed:
                    self.player.projectiles.remove(projectile)
                    self.all_sprites.remove(projectile)  # Remove do grupo de sprites também
        except Exception as e:
            print(f"Erro ao atualizar projéteis: {e}")

        # Atualiza todos os sprites no grupo
        self.all_sprites.update(dt)


    def update_moving_obstacles(self):
        for obstacle in self.moving_obstacles:
            obstacle.update()


    def update_moving_obstacles(self):
        for obstacle in self.moving_obstacles:
            obstacle.update()

    def create_obstacles_course(self, obstacles):
        for obstacle in obstacles:
            self.obstacles.append(obstacle)
            self.all_sprites.add(obstacle)  # Adiciona ao grupo de sprites

    def create_moving_obstacles_course(self, obstacles):
        for obstacle in obstacles:
            self.moving_obstacles.append(obstacle)
            self.all_sprites.add(obstacle)  # Adiciona ao grupo de sprites

    def draw_objects(self, objects):
        """Desenhar objetos na tela"""
        for obj in objects:
            adjusted_position = self.camera.apply(obj)
            self.base_surface.blit(obj.image, adjusted_position)

    def draw_player(self, player):
        """Desenhar o jogador ajustado pela câmera"""
        self.player = player
        adjusted_position = self.camera.apply(player)
        self.base_surface.blit(player.image, adjusted_position)

    def draw_projectile(self, projectile):
        """Desenhar projéteis"""
        self.base_surface.blit(projectile.image, self.camera.apply(projectile))

    def draw_enemy(self):
        """Desenhar inimigos"""
        for enemy in self.player.enemies:
            adjusted_position = self.camera.apply(enemy)
            self.base_surface.blit(enemy.image, adjusted_position)

    def draw_hud(self):
        """Desenhar HUD"""
        if self.hud:
            self.hud.update(self.player.health, self.player.magic)
            self.base_surface.blit(self.hud.image, self.hud.rect)


    def draw(self):
        for sprite in self.all_sprites:
            adjusted_position = self.camera.apply(sprite)
            self.base_surface.blit(sprite.image, adjusted_position)
