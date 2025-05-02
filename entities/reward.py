import pygame
import math
from settings import *

class Reward:
    def __init__(self, reward_data, position, on_claim):
        self.name = reward_data["name"]
        self.description = reward_data["description"]
        self.data = reward_data
        self.pos = pygame.Vector2(position)
        self.radius = 18
        self.max_health = 5
        self.health = self.max_health
        self.on_claim = on_claim
        self.font = pygame.font.SysFont("consolas", 14)
        self.claimed = False

        self.flash_timer = 0
        self.bounce_timer = 0

    def update(self, dt):
        if self.flash_timer > 0:
            self.flash_timer -= dt
        self.bounce_timer += dt

    def take_hit(self):
        if self.claimed:
            return
        self.health -= 1
        self.flash_timer = 0.1
        if self.health <= 0:
            self.claim()


    def claim(self):
        self.claimed = True
        self.on_claim(self)

    def draw(self, screen, camera):
        # Bounce effect
        bounce_offset = math.sin(self.bounce_timer * 8) * 3
        draw_pos = pygame.Vector2(self.pos.x, self.pos.y + bounce_offset)

        # Flash effect
        color = (255, 255, 255) if self.flash_timer > 0 else (100, 200, 255)
        pygame.draw.circle(screen, color, camera.apply(draw_pos), self.radius)

        # Name / Description
        name_surf = self.font.render(self.name, True, WHITE)
        desc_surf = self.font.render(self.description, True, (180, 180, 180))
        screen.blit(desc_surf, desc_surf.get_rect(center=camera.apply((self.pos.x, self.pos.y - 40))))
        screen.blit(name_surf, name_surf.get_rect(center=camera.apply((self.pos.x, self.pos.y - 24))))

