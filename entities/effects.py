import pygame
import random
import math

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




class RewardBurstEffect:
    def __init__(self, pos):
        self.particles = []
        self.lifetime = 0.5
        for _ in range(16):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 160)
            velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
            color = random.choice([(255, 255, 0), (100, 255, 100), (0, 200, 255)])
            self.particles.append({
                "pos": pygame.Vector2(pos),
                "vel": velocity,
                "radius": 4,
                "color": color
            })

    def update(self, dt):
        self.lifetime -= dt
        for p in self.particles:
            p["pos"] += p["vel"] * dt
            p["radius"] = max(0, p["radius"] - 20 * dt)

    def draw(self, screen, camera):
        for p in self.particles:
            if p["radius"] > 0:
                pygame.draw.circle(screen, p["color"], camera.apply(p["pos"]), int(p["radius"]))

    def is_dead(self):
        return self.lifetime <= 0
