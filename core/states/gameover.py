# core/states/gameover.py

import pygame
from settings import *
from core.highscore import load_high_score, save_high_score

class GameOverState:
    def __init__(self, manager, screen):
        self.manager = manager
        self.screen = screen
        self.font = pygame.font.SysFont("consolas", 36)

    def enter(self):
        print("[STATE] Game Over entered")

        self.last_score = self.manager.states["gameplay"].score
        self.high_score = load_high_score()

        if self.last_score > self.high_score:
            save_high_score(self.last_score)
            self.high_score = self.last_score
            self.new_high = True
        else:
            self.new_high = False


    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        game_over = self.font.render("GAME OVER", True, (255, 60, 60))
        score = self.font.render(f"Score: {self.last_score}", True, WHITE)
        high = self.font.render(f"High Score: {self.high_score}", True, (255, 215, 0))

        restart = self.font.render("Press [R] to Restart", True, WHITE)
        quit_game = self.font.render("Press [ESC] to Quit", True, WHITE)

        self.screen.blit(game_over, game_over.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
        self.screen.blit(score, score.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))
        self.screen.blit(high, high.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))

        if self.new_high:
            congrats = self.font.render("NEW HIGH SCORE!", True, (255, 255, 100))
            self.screen.blit(congrats, congrats.get_rect(center=(WIDTH//2, HEIGHT//2 + 60)))

        self.screen.blit(restart, restart.get_rect(center=(WIDTH//2, HEIGHT//2 + 110)))
        self.screen.blit(quit_game, quit_game.get_rect(center=(WIDTH//2, HEIGHT//2 + 150)))


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.manager.set_state("gameplay")
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
