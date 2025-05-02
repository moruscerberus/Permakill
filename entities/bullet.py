# entities/bullet.py

import pygame
from settings import *

class Bullet:
    def __init__(self, pos, direction, speed=500):
        self.pos = pygame.Vector2(pos)
        self.velocity = direction.normalize() * speed
        self.radius = 4
        self.lifetime = 1.5

    def update(self, dt):
        self.pos += self.velocity * dt
        self.lifetime -= dt

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius)

    def is_dead(self):
        return self.lifetime <= 0
