# core/states/menu.py

import pygame
from settings import *
from core.assets import Assets

class MenuState:
    def __init__(self, manager, screen):
        self.manager = manager
        self.screen = screen
        self.font = Assets.fonts['main']

    def enter(self):
        pass

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((10, 10, 10))
        title = self.font.render("PERMAKILL", True, WHITE)
        start = self.font.render("Press [ENTER] to Play", True, WHITE)
        settings = self.font.render("Press [S] for Settings", True, WHITE)
        quit_game = self.font.render("Press [ESC] to Quit", True, WHITE)

        self.screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
        self.screen.blit(start, start.get_rect(center=(WIDTH//2, HEIGHT//2)))
        self.screen.blit(settings, settings.get_rect(center=(WIDTH//2, HEIGHT//2 + 40)))
        self.screen.blit(quit_game, quit_game.get_rect(center=(WIDTH//2, HEIGHT//2 + 80)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.manager.set_state("gameplay")
            elif event.key == pygame.K_s:
                self.manager.set_state("settings")
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
