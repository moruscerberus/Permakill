# core/states/settings.py

import pygame
from settings import *

class SettingsState:
    def __init__(self, manager, screen):
        self.manager = manager
        self.screen = screen
        self.font = pygame.font.SysFont("consolas", 32)

    def enter(self):
        pass

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((20, 20, 30))
        text = self.font.render("Settings - Press [ESC] to go back", True, WHITE)
        self.screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_state("menu")
