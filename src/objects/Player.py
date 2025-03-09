import pygame
from objects.Enemy import Enemy
from objects.Obstacle import Obstacle
from objects.Projectile import Projectile 
import time
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, name, health, max_health, magic, max_magic, sprites_intervals, action_sprites, screen, width, height, world_width, world_height, all_sprites):
        super().__init__()
        self.name = name
        self.health = health
        self.max_health = max_health
        self.magic = magic
        self.max_magic = max_magic
        self.sprite_intervals = sprites_intervals
        self.action_sprites = action_sprites
        self.all_sprites = all_sprites
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.3
        self.collision_side = None
        self.direction = 'right'
        self.screen = screen
        self.world_width = world_width
        self.world_height = world_height
        self.is_on_ground = None
        self.is_on_obstacle = None

        self.dash_distance = 300
        self.dash_speed = 2000  # Pixels por segundo
        self.is_dashing = False
        self.dash_remaining = 0

        self.is_attacking = False
        self.attack_range = 50  # Distância do ataque (em pixels)
        self.attack_duration = 800  # Tempo de duração do ataque (em milissegundos)
        self.attack_timer = 0
        self.attack_cooldown = 400  # Tempo de cooldown entre ataques em milissegundos

        self.combo_count = 0  # Contador de combo
        self.combo_time_limit = 1000  # Limite de tempo para combo (em milissegundos)
        self.last_attack_time = 0  # Tempo do último ataque

        self.projectiles = []  # Lista de projéteis disparados

        self.default_sprite = pygame.image.load("assets/sprites/default_sprite.png").convert_alpha()
        self.sprites = self.load_sprites()
        self.atual = 0

        self.state = 'idle'
        self.current_sprite_index = 0
        self.sprite_timer = 0
        self.sprite_interval = 300  # Tempo em milissegundos entre cada sprite

        self.image = self.sprites['idle']['right'][0]

        # Define o rect com as dimensões específicas e centraliza no mundo
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (200, world_height - self.rect.height)

        self.last_shot_time = 0  # Tempo do último disparo
        self.shot_cooldown = 500

        self.obstacles = []
        self.enemies = []

        self.last_damage_time = 0  # Tempo do último dano recebido
        self.damage_cooldown = 1000  # Cooldown de 1 segundo (em milissegundos)

        self.knockback_speed = 15  # Velocidade inicial de empurrão
        self.knockback_angle = -45  # Ângulo do empurrão (em graus), -45 para cima e para trás
        self.knockback_decay = 0.9  # Fator de desaceleração do empurrão



    def update(self, dt=0):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = 'left'
            self.rect.x -= self.speed
            if not self.is_attacking:
                self.state = 'run'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = 'right'
            self.rect.x += self.speed
            if not self.is_attacking:
                self.state = 'run'
        elif not self.is_attacking and self.velocity_y > 0:
            self.state = 'idle'

        if keys[pygame.K_h]:
            self.start_dash()
            self.state = 'dash'

        self.dash(dt, self.obstacles)

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.velocity_y > 0 and not self.is_on_ground:
            if not self.is_attacking and not self.is_dashing and not self.is_on_obstacle:
             self.state = 'fall'

        self.is_on_ground = False
        for obstacle in self.obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.handle_collision_with_obstacle(obstacle)
                if self.rect.bottom == obstacle.rect.top:
                    self.is_on_ground = True

        if self.rect.bottom >= self.world_height:
            self.rect.bottom = self.world_height
            self.is_on_ground = True

        if self.is_on_ground:
            self.velocity_y = 0

        if keys[pygame.K_k]:
            self.start_attack('sword', dt)  # Inicia o ataque (físico)

        if keys[pygame.K_l]:
            self.start_attack('kick', dt)  # Inicia o ataque (físico)

        if keys[pygame.K_j]:
            self.shoot_projectile(dt)  # Dispara o projétil (separado do ataque físico)


        if keys[pygame.K_UP] or keys[pygame.K_w] and (self.rect.bottom == self.world_height or self.is_on_ground):
            self.jump()

        # Atualiza o ataque
        if self.is_attacking:
            self.attack_timer += dt * 1000  # Convertendo para milissegundos
            if self.attack_timer >= self.attack_duration:
                self.end_attack()

        # Verificar colisão com inimigos durante o ataque
        if self.is_attacking:
            self.check_attack_collision()
        
        # Gerenciar o combo
        if self.combo_count > 0:
            time_since_last_attack = pygame.time.get_ticks() - self.last_attack_time
            if time_since_last_attack > self.combo_time_limit:
                self.combo_count = 0  # Resetar o combo após o tempo limite

        self.check_bounds()

        # Gerenciar o combo
        if self.combo_count > 0:
            time_since_last_attack = pygame.time.get_ticks() - self.last_attack_time
            if time_since_last_attack > self.combo_time_limit:
                self.combo_count = 0  # Resetar o combo após o tempo limite

        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time < self.damage_cooldown:
            # Faz o jogador piscar (invisível a cada intervalo de 100ms)
            self.image.set_alpha(128 if (current_time // 100) % 2 == 0 else 255)
        else:
            self.image.set_alpha(255)  # Totalmente visível quando fora do cooldown

        self.apply_knockback()
        self.apply_sprites()


    def load_sprites(self):
        """Carrega os sprites de acordo com as ações e direções, usando um sprite padrão em caso de erro."""
        def load_image(path):
            try:
                return pygame.image.load(path).convert_alpha()
            except (pygame.error, FileNotFoundError):
                return self.default_sprite

        def load_action_sprites(base_path, num_sprites):
            """Carrega os sprites para uma ação."""
            sprites_right = [load_image(f"{base_path}_{i}.png") for i in range(1, num_sprites + 1)]
            sprites_left = [pygame.transform.flip(sprite, True, False) for sprite in sprites_right]
            return {'right': sprites_right, 'left': sprites_left}
    
        return {action: load_action_sprites(f"assets/sprites/{self.name}/{self.name}_{action}", num_sprites)
                for action, num_sprites in self.action_sprites.items()}

    def apply_sprites(self):
        """Aplica o sprite atual de forma linear com velocidades específicas por estado."""
        current_sprites = self.sprites[self.state][self.direction]
        self.atual += self.sprite_intervals.get(self.state)  # Padrão: 0.05

        if self.atual >= len(current_sprites):
            self.atual = 0

        self.image = current_sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def jump(self):
        if self.is_on_ground:
            self.state = 'jump'
            self.velocity_y = -15

    def start_dash(self):
        """Inicia o dash."""
        self.is_dashing = True
        self.dash_remaining = self.dash_distance

    def dash(self, dt, obstacles):
        """Executa o dash baseado no tempo delta."""
        if not self.is_dashing:
            return

        dash_step = self.dash_speed * dt
        if self.dash_remaining <= 0:
            self.is_dashing = False
            return
        
        initial_position = self.rect.copy()

        if self.direction == 'left':
            self.rect.centerx -= dash_step
        elif self.direction == 'right':
            self.rect.centerx += dash_step
        elif self.direction == 'up':
            self.rect.centery -= dash_step
        elif self.direction == 'down' and not self.is_on_ground:
            self.rect.centery += dash_step

        self.dash_remaining -= dash_step

        collided = False
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                collided = True
                break

        if collided:
            # Reverter para a posição inicial e parar o dash
            self.rect = initial_position
            self.is_dashing = False
            self.dash_remaining = 0

    def start_attack(self, type, dt):
        current_time = pygame.time.get_ticks()

        # Verifica se o cooldown foi concluído
        if current_time - self.last_attack_time < self.attack_cooldown:
           return  # Se o cooldown não foi completado, não faz nada
    
        """Inicia o ataque e o combo."""
        if self.combo_count == 3 and not self.is_attacking:
            self.combo_count = 0
        
        if not self.is_attacking:
            if type == 'sword':
                self.is_attacking = True
                self.combo_count += 1  # Aumenta o combo
                self.state = f'attack{self.combo_count}'  # Define o ataque atual, sendo attack1, attack2 ou attack3
                self.attack_timer = 0
                self.last_attack_time = current_time
            elif type == 'kick':
                self.is_attacking = True
                self.combo_count += 1  # Aumenta o combo
                self.state = type
                self.attack_timer = 0
                self.last_attack_time = current_time
            if self.direction == 'left':
                if self.is_on_ground:
                    self.rect.x -= 20
            elif self.direction == 'right':
                if self.is_on_ground:
                    self.rect.x += 20

    def end_attack(self):
        """Finaliza o ataque."""
        self.is_attacking = False
        self.state = 'idle'
        self.sprite_interval = 200

    def check_attack_collision(self):
        """Verifica se algum inimigo foi atingido pelo ataque."""
        attack_hitbox = pygame.Rect(self.rect.centerx - self.attack_range, self.rect.centery - 10, self.attack_range * 2, 20)
        for enemy in self.enemies:
            if attack_hitbox.colliderect(enemy.rect):
                self.attack_enemy(enemy)

    def attack_enemy(self, enemy):
        """Aplica dano ao inimigo."""
        enemy.take_damage(10, self.direction)  # Aplica 10 de dano, por exemplo

    def shoot_projectile(self, dt):
        """Dispara um projétil se o tempo de cooldown tiver passado."""
        if self.magic <= 0 :
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shot_cooldown:
            # Define a posição inicial do projétil com base na direção do jogador
            projectile_x = self.rect.centerx
            projectile_y = self.rect.centery

            # Ajusta a posição inicial com base na direção
            if self.direction == 'left':
                projectile_x -= self.rect.width // 2
            elif self.direction == 'right':
                projectile_x += self.rect.width // 2

            # Cria um novo projétil
            self.state = 'shoot'
            new_projectile = Projectile('player', self.screen, projectile_x, projectile_y, self.direction, speed=1000)
            self.projectiles.append(new_projectile)
            self.all_sprites.add(new_projectile)

            # Atualiza o tempo do último disparo
            self.last_shot_time = current_time
            self.magic -= 10



    def draw(self, screen):
        self.screen = screen
        screen.blit(self.image, self.rect)

        for projectile in self.projectiles:
            projectile.draw(screen)


    def check_bounds(self):
        """Limita a posição do jogador dentro dos limites do mundo."""
        # Limitar posição horizontal
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.world_width:
            self.rect.right = self.world_width

        # Limitar posição vertical
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.world_height:
            self.rect.bottom = self.world_height

    def handle_collision_with_obstacle(self, obstacle):
        """Determina o lado da colisão com o obstáculo e ajusta a posição do jogador."""
        delta_x = (self.rect.centerx - obstacle.rect.centerx) / (obstacle.rect.width / 2)
        delta_y = (self.rect.centery - obstacle.rect.centery) / (obstacle.rect.height / 2)

        if abs(delta_x) > abs(delta_y):
            if delta_x > 0:
                self.rect.left = obstacle.rect.right
                self.collision_side = 'left'
            else:
                self.rect.right = obstacle.rect.left
                self.collision_side = 'right'
        else:
            if delta_y > 0:
                self.rect.top = obstacle.rect.bottom
                self.velocity_y = 0
                self.is_on_obstacle = True
                self.collision_side = 'bottom'
            else:
                self.rect.bottom = obstacle.rect.top
                self.velocity_y = 0
                self.collision_side = 'top'

    def take_damage(self, damage, direction):
        if self.is_dashing :
            return
        
        """Reduz a vida do jogador com cooldown."""
        current_time = pygame.time.get_ticks()

        # Verifica se o cooldown de dano foi concluído
        if current_time - self.last_damage_time >= self.damage_cooldown:
            self.health -= damage
            self.knockback_speed = 15  # Velocidade inicial de empurrão
            if direction == 'left':
                self.knockback_angle = -45 
            elif direction == 'right':
                self.knockback_angle = 45 
            else:
                self.knockback_angle = 0
            self.knockback_decay = 0.9  # Fator de desaceleração do empurrão
            self.last_damage_time = current_time  # Atualiza o tempo do último dano

            if self.health < 0:
                self.health = 0
                self.is_alive = self.health > 0
                self.die()


    def die(self):
        """Lida com a morte do jogador."""
        print(f"{self.name} morreu!")


    def apply_knockback(self):
        """Aplica a física de empurrão ao jogador."""
        if hasattr(self, 'knockback_speed') and self.knockback_speed > 0:
            # Converter ângulo para radianos
            angle_rad = math.radians(self.knockback_angle)

            # Calcular componentes de movimento em x e y
            dx = math.cos(angle_rad) * self.knockback_speed
            dy = math.sin(angle_rad) * self.knockback_speed

            # Atualizar posição do jogador
            self.rect.x += dx
            self.rect.y += dy

           # Reduzir a velocidade do empurrão para desaceleração suave
            self.knockback_speed *= self.knockback_decay

            # Parar o empurrão se a velocidade for muito baixa
            if self.knockback_speed < 1:
                self.knockback_speed = 0