# entities/enemy_bullet.py

import pygame
from settings import *

class EnemyBullet:
    def __init__(self, pos, direction):
        self.pos = pygame.Vector2(pos)
        self.velocity = direction.normalize() * 300
        self.radius = 4
        self.lifetime = 3.0  # seconds

    def update(self, dt):
        self.pos += self.velocity * dt
        self.lifetime -= dt

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), self.radius)

    def is_dead(self):
        return self.lifetime <= 0
