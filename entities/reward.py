# entities/reward.py

import pygame
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

    def update(self, dt):
        pass

    def take_hit(self):
        self.health -= 1
        if self.health <= 0:
            self.claim()

    def claim(self):
        self.on_claim(self)

    def draw(self, screen):
        pygame.draw.circle(screen, (100, 200, 255), (int(self.pos.x), int(self.pos.y)), self.radius)

        # Improved spacing between name and description
        name_surf = self.font.render(self.name, True, WHITE)
        desc_surf = self.font.render(self.description, True, (180, 180, 180))

        screen.blit(desc_surf, desc_surf.get_rect(center=(self.pos.x, self.pos.y - 40)))
        screen.blit(name_surf, name_surf.get_rect(center=(self.pos.x, self.pos.y - 24)))

        # Health bar
        bar_width = 40
        bar_height = 6
        fill_ratio = self.health / self.max_health
        bar_x = self.pos.x - bar_width // 2
        bar_y = self.pos.y + self.radius + 6

        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (100, 255, 100), (bar_x, bar_y, bar_width * fill_ratio, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
