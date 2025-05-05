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


class SpawnBurstEffect:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.timer = 0.25
        self.elapsed = 0

    def update(self, dt):
        self.elapsed += dt

    def is_dead(self):
        return self.elapsed >= self.timer

    def draw(self, screen, camera):
        t = self.elapsed / self.timer
        alpha = max(0, int(255 * (1 - t)))
        base_size = 64  # more room for thick lines
        scale_factor = 2  # final size: 128×128
        line_width = 5    # super chunky ✧

        color = (255, 255, 255, alpha)

        # Draw on pixel canvas
        low_res = pygame.Surface((base_size, base_size), pygame.SRCALPHA)
        center = base_size // 2

        pygame.draw.line(low_res, color, (0, center), (base_size, center), line_width)         # horizontal
        pygame.draw.line(low_res, color, (center, 0), (center, base_size), line_width)         # vertical
        pygame.draw.line(low_res, color, (0, 0), (base_size, base_size), line_width)           # diagonal ↘
        pygame.draw.line(low_res, color, (0, base_size), (base_size, 0), line_width)           # diagonal ↗

        # Pixel-perfect scale-up
        burst = pygame.transform.scale(low_res, (base_size * scale_factor, base_size * scale_factor))
        draw_pos = camera.apply(self.pos - pygame.Vector2(burst.get_width() // 2, burst.get_height() // 2))
        screen.blit(burst, draw_pos)

