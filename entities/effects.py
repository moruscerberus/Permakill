import pygame

class HitEffect:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.radius = 6
        self.lifetime = 0.15

    def update(self, dt):
        self.lifetime -= dt

    def draw(self, screen, camera):
        if self.lifetime > 0:
            pygame.draw.circle(screen, (255, 255, 0), camera.apply(self.pos), int(self.radius))

    def is_dead(self):
        return self.lifetime <= 0
