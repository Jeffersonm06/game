import pygame
import os
import sys
import time


def load_image(path):
    return pygame.image.load(path).convert_alpha()

def play_sound(path):
    sound = pygame.mixer.Sound(path)
    sound.play()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Clock:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.counter = 0
    

    def contador(self, max_count):
        """Função contador que incrementa até atingir max_count."""
        self.counter += 1
        
        if self.counter >= max_count:
            self.counter = 0  # Resetar para permitir novo uso
            return True
        return False
    

    def cronometro(self, duration):
        """Cronômetro que conta o tempo especificado em minutos e décimos de segundo."""
        if self.start_time is None:
            self.start_time = time.time()
        
        self.elapsed_time = time.time() - self.start_time
        total_duration = duration * 60  # Convertendo minutos reais para segundos

        if self.elapsed_time >= total_duration:
            self.start_time = None  # Resetar para permitir novo uso
            return True
        return False

    def timer(self, duration):
        """Timer que conta o tempo regressivamente, especificado em minutos e décimos de segundo."""
        if self.start_time is None:
            self.start_time = time.time()
        
        self.elapsed_time = time.time() - self.start_time
        total_duration = duration * 60  # Convertendo minutos reais para segundos

        if self.elapsed_time >= total_duration:
            self.start_time = None  # Resetar para permitir novo uso
            return True
        return False

    def reset(self):
        """Reseta o relógio."""
        self.start_time = None
        self.elapsed_time = 0
