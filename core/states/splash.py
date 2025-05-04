# core/states/splash.py

import pygame
from settings import *
from core.assets import Assets

class SplashState:
    def __init__(self, manager, screen):
        self.manager = manager
        self.screen = screen
        self.font_large = Assets.fonts['splash_main']
        self.font_small = Assets.fonts['splash_small']
        self.phase = 0  # 0 = intro, 1 = warning
        self.warning_icon = Assets.get('warning')

    def enter(self):
        self.timer = 0
        self.phase = 0
        self.has_started_transition = False

    def update(self, dt):
        self.timer += dt

        if self.phase == 0 and self.timer > 2.0:
            self.phase = 1
            self.timer = 0
        elif self.phase == 1 and self.timer > 5.0 and not self.has_started_transition:
            self.manager.set_state("menu")
            self.has_started_transition = True

    def draw(self):
        self.screen.fill((20, 20, 20))

        if self.phase == 0:
            title_arrival = 0.5
            creator_arrival = 1.0

            # === Game Title ===
            logo_surface = self.font_large.render("Permakill", True, WHITE)
            if self.timer <= title_arrival:
                progress = self.timer / title_arrival
                slide_offset = int((1 - progress) * WIDTH * 0.3)
                title_x = WIDTH // 2 - slide_offset
            else:
                title_x = WIDTH // 2

            logo_rect = logo_surface.get_rect(center=(title_x, HEIGHT // 2 - 30))
            self.screen.blit(logo_surface, logo_rect)

            # === Creator Name ===
            if self.timer > creator_arrival:
                creator_surface = self.font_small.render("by moruscerberus", True, WHITE)
                creator_progress = min((self.timer - creator_arrival), 1.0)
                slide_offset = int((1 - creator_progress) * WIDTH * 0.3)
                creator_x = WIDTH // 2 - slide_offset

                creator_rect = creator_surface.get_rect(center=(creator_x, HEIGHT // 2 + 30))
                self.screen.blit(creator_surface, creator_rect)

        elif self.phase == 1:
            # === Seizure Warning Phase ===
            fade_duration = 1.0
            alpha = min(255, int((self.timer / fade_duration) * 255))

            # Fade background
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))

            # Warning icon with alpha
            icon = self.warning_icon.copy()
            icon.set_alpha(alpha)
            icon_rect = icon.get_rect()
            icon_rect.center = (WIDTH // 2 - 100, HEIGHT // 2 - 30)
            self.screen.blit(icon, icon_rect)

            # Warning text next to icon
            warning_text = self.font_large.render("Seizure Warning", True, WHITE)
            warning_rect = warning_text.get_rect(midleft=(icon_rect.right + 10, icon_rect.centery))
            self.screen.blit(warning_text, warning_rect)

            # Detail text below
            detail_text = self.font_small.render(
                "This game contains flashing lights. Player discretion is advised.",
                True, WHITE
            )
            detail_rect = detail_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
            self.screen.blit(detail_text, detail_rect)

    def handle_event(self, event):
        pass
