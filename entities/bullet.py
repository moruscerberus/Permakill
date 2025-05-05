# entities/bullet.py

import pygame
from settings import *

class Bullet:
    def __init__(self, pos, direction, speed=500):
        self.pos = pygame.Vector2(pos)
        self.velocity = direction.normalize() * speed
        self.radius = 8
        self.lifetime = 1.5

    def update(self, dt):
        self.pos += self.velocity * dt
        self.lifetime -= dt

    def is_dead(self):
        return self.lifetime <= 0
    
    def draw(self, screen, camera):
        # Base position
        screen_pos = camera.apply(self.pos)

        # Calculate tip offset
        tip_offset = self.velocity.normalize() * self.radius
        tip_pos = screen_pos + tip_offset

        # Draw yellow tip (smaller)
        pygame.draw.circle(screen, (255, 255, 0), tip_pos, int(self.radius * 0.6))

        # Draw core body
        pygame.draw.circle(screen, WHITE, screen_pos, self.radius)
