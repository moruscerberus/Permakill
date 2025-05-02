# core/camera.py

import pygame
import random

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)
        self.shake_timer = 0
        self.intensity = 0

    def update(self, dt):
        if self.shake_timer > 0:
            self.shake_timer -= dt
            self.offset.x = random.uniform(-self.intensity, self.intensity)
            self.offset.y = random.uniform(-self.intensity, self.intensity)
        else:
            self.offset.update(0, 0)

    def shake(self, intensity=5, duration=0.2):
        self.intensity = intensity
        self.shake_timer = duration

    def apply(self, pos):
        return pos + self.offset
