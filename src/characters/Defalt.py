from objects.Player import Player

class DefaltCharacter(Player):
    def __init__(self,screen, width, height, world_width, world_height, all_sprites):
        self.attack_duration = 800

        self.sprite_intervals = {
            'idle': 0.05,
            'run': 0.05,
            'jump': 0.05,
            'fall': 0.05,
            'dash': 0.03,
            'punch': 0.03,
            'attack1': 0.06,  # Ex: 400ms / 5 sprites = 80ms por sprite
            'attack2': 0.08,  # Ex: 400ms / 6 sprites = 67ms por sprite
            'attack3': 0.08,  # Ex: 400ms / 6 sprites = 67ms por sprite
            'kick': 0.08,
            'shoot': 0.09
        }

        # Configurar o número de sprites para cada ação
        self.action_sprites = {
            'idle': 4,
            'run': 5,
            'jump': 2,
            'fall': 2,
            'dash': 4,
            'punch': 4,
            'attack1': 5,
            'attack2': 6,
            'attack3': 6,
            'kick': 8,
            'shoot': 9,
        }

        super().__init__('Default', 10, 10, 100, 100, self.sprite_intervals, self.action_sprites, screen, width, height, world_width, world_height, all_sprites)
