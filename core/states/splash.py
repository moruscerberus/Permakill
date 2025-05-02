# core/states/splash.py

import pygame
from settings import *

class SplashState:
    def __init__(self, manager, screen):
        self.manager = manager
        self.screen = screen
        self.font_large = pygame.font.SysFont("consolas", 64)
        self.font_small = pygame.font.SysFont("consolas", 32)

    def enter(self):
        self.timer = 2.0
        self.has_started_transition = False

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0 and not self.has_started_transition:
            self.manager.set_state("menu")
            self.has_started_transition = True  # prevent re-calling set_state


    def draw(self):
        self.screen.fill((20, 20, 20))
        logo = self.font_large.render("Permakill", True, WHITE)
        logo_rect = logo.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(logo, logo_rect)

        creator = self.font_small.render("by moruscerberus", True, WHITE)
        creator_rect = creator.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        self.screen.blit(creator, creator_rect)

    def handle_event(self, event):
        pass
