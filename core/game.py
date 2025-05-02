# core/game.py

from settings import *
from entities.player import Player
from entities.enemy import Enemy
from systems.arena import draw_arena
import pygame

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 1.5
        self.score = 0
        self.font = pygame.font.SysFont("consolas", 32, bold=True)

    def update(self, dt):
        self.player.update(dt)

        # Spawn enemies over time
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.enemies.append(Enemy(self.player.pos))
            self.spawn_timer = 0

        # Update enemies
        for enemy in self.enemies:
            enemy.update(dt, self.player.pos)

        # Bullet collisions with enemies
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies:
                if enemy.collides_with(bullet):
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                        self.score += 50
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    break

        # Enemy contact with player
        for enemy in self.enemies:
                for bullet in enemy.bullets[:]:
                    if bullet.pos.distance_to(self.player.pos) < bullet.radius + self.player.radius:
                        self.player.take_damage(10)
                        enemy.bullets.remove(bullet)

        # Check for game over
        if self.player.health <= 0:
            print("GAME OVER")
            # Here you could pause the game, trigger a restart, etc.

    def draw(self):
        self.screen.fill(BLACK)
        draw_arena(self.screen)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw score
        score_text = self.font.render(f"{self.score}pts!", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, ARENA_CENTER[1] + ARENA_RADIUS + 30))
        self.screen.blit(score_text, score_rect)

        # Draw health bar
        bar_width = 200
        bar_height = 20
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = ARENA_CENTER[1] + ARENA_RADIUS + 60

        pygame.draw.rect(self.screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))  # background
        health_ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.screen, (200, 50, 50), (bar_x, bar_y, bar_width * health_ratio, bar_height))  # health
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)  # border
