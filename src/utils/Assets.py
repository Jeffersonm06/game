class Player(pygame.sprite.Sprite):
    def __init__(self, screen, width, height, world_width, world_height):
        super().__init__()
        # Inicializa outras variáveis aqui
        self.default_sprite = pygame.image.load("assets/sprites/default_sprite.png").convert_alpha()
        self.sprites = self.load_sprites()

        self.attack_duration = 400  # Tempo de duração do ataque (em milissegundos)
        self.attack_cooldown = 400  # Tempo de cooldown entre ataques em milissegundos

        self.sprite_intervals = {
            'idle': 200,
            'run': 100,
            'jump': 200,
            'fall': 200,
            'dash': 150,
            'punch': 100,
            'attack1': self.attack_duration // 5,  # Ex: 400ms / 5 sprites = 80ms por sprite
            'attack2': self.attack_duration // 6,  # Ex: 400ms / 6 sprites = 67ms por sprite
            'attack3': self.attack_duration // 6,  # Ex: 400ms / 6 sprites = 67ms por sprite
            'kick': 100,
            'shoot': 100
        }

        self.state = 'idle'
        self.current_sprite_index = 0
        self.sprite_timer = 0

        self.image = self.sprites['idle']['right'][0]

        # Define o rect com as dimensões específicas e centraliza no mundo
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (world_width // 2, world_height // 2)

        self.last_shot_time = 0  # Tempo do último disparo
        self.shot_cooldown = 500

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

        # Configurar o número de sprites para cada ação
        action_sprites = {
            'idle': 4,
            'run': 5,
            'jump': 2,
            'fall': 2,
            'dash': 4,
            'punch': 4,
            'attack1': 5,
            'attack2': 6,
            'attack3': 6,
            'kick': 4,
            'shoot': 4,
        }
        
        return {action: load_action_sprites(f"assets/sprites/player/player_{action}", num_sprites)
                for action, num_sprites in action_sprites.items()}

    def update_sprite(self, dt):
        """Atualiza o sprite atual baseado na ação e direção."""
        self.sprite_timer += dt * 1000  # Convertendo dt para milissegundos

        # Pega o intervalo de sprite baseado no estado atual
        self.sprite_interval = self.sprite_intervals.get(self.state, 200)

        if self.sprite_timer >= self.sprite_interval:
            self.sprite_timer = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites[self.state]['right'])

            # Seleciona a sprite atual com base na ação e direção
            current_sprite = self.sprites[self.state][self.direction][self.current_sprite_index]

            # Ajusta o tamanho da imagem para caber no rect
            self.image = pygame.transform.scale(current_sprite, (self.rect.width, self.rect.height))
