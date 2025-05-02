# core/transition.py
import pygame
from settings import *

class TransitionManager:
    def __init__(self, screen):
        self.screen = screen
        self.overlay = pygame.Surface((WIDTH, HEIGHT))
        self.overlay.fill(BLACK)
        self.alpha = 0
        self.speed = 300  # alpha per second
        self.state = None  # 'in', 'out', or None
        self.on_complete = None

    def start_fade_in(self, on_complete=None):
        self.alpha = 255
        self.state = 'in'
        self.on_complete = on_complete

    def start_fade_out(self, on_complete=None):
        self.alpha = 0
        self.state = 'out'
        self.on_complete = on_complete

    def update(self, dt):
        if self.state == 'in':
            self.alpha -= self.speed * dt
            if self.alpha <= 0:
                self.alpha = 0
                self.state = None
                if self.on_complete:
                    self.on_complete()
                    self.on_complete = None
        elif self.state == 'out':
            self.alpha += self.speed * dt
            if self.alpha >= 255:
                self.alpha = 255
                self.state = None
                if self.on_complete:
                    self.on_complete()
                    self.on_complete = None

    def draw(self):
        if self.alpha > 0:
            self.overlay.set_alpha(int(self.alpha))
            self.screen.blit(self.overlay, (0, 0))

    def is_transitioning(self):
        return self.state is not None
