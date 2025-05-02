# core/states/gameplay.py

from settings import *
from entities.player import Player
from entities.enemy import Enemy
from entities.reward import Reward
from systems.arena import draw_arena
from core.rewards import load_rewards, apply_reward
import pygame
import random

class GamePlayState:
    def __init__(self, manager, screen):
        self.manager = manager
        self.screen = screen
        self.font = pygame.font.SysFont("consolas", 32)

        self.rewards_data = load_rewards()
        self.rewards = []
        self.in_reward_phase = False
        self.reward_claimed = False
        self.reward_resume_timer = 0
        self.last_reward_score = -1
        self.dead = False  # track death state

    def enter(self):
        self.player = Player()
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 1.5
        self.score = 0
        self.rewards.clear()
        self.in_reward_phase = False
        self.reward_claimed = False
        self.reward_resume_timer = 0
        self.last_reward_score = -1
        self.dead = False

    def player_is_dead(self):
        return self.player.health <= 0

    def enter_reward_phase(self):
        self.in_reward_phase = True
        self.reward_claimed = False

        chosen = random.sample(self.rewards_data, 3)
        positions = [
            (WIDTH // 2 - 120, HEIGHT // 2),
            (WIDTH // 2, HEIGHT // 2),
            (WIDTH // 2 + 120, HEIGHT // 2)
        ]

        for reward_data, pos in zip(chosen, positions):
            reward = Reward(reward_data, pos, self.claim_reward)
            self.rewards.append(reward)

    def claim_reward(self, reward):
        if self.reward_claimed:
            return

        apply_reward(self.player, reward.data)
        self.reward_claimed = True
        self.in_reward_phase = False
        self.rewards.clear()
        self.reward_resume_timer = 1.0

    def update(self, dt):
        # Handle death check once
        if self.player_is_dead() and not self.dead:
            print("[DEBUG] Player is dead")
            self.dead = True
            self.manager.set_state("game_over")

        if self.dead:
            return  # Stop all game updates if dead

        self.player.update(dt)

        if not self.in_reward_phase and not self.reward_claimed:
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_interval:
                self.enemies.append(Enemy(self.player.pos))
                self.spawn_timer = 0

            for enemy in self.enemies:
                enemy.update(dt, self.player.pos)

            for bullet in self.player.bullets[:]:
                for enemy in self.enemies:
                    if enemy.collides_with(bullet):
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                            self.score += 50
                        if bullet in self.player.bullets:
                            self.player.bullets.remove(bullet)
                        break

            for enemy in self.enemies:
                if enemy.pos.distance_to(self.player.pos) < enemy.radius + self.player.radius:
                    if self.player.time_since_hit >= self.player.damage_cooldown:
                        self.player.take_damage(10)
                        self.player.time_since_hit = 0

            for enemy in self.enemies:
                for bullet in enemy.bullets[:]:
                    if bullet.pos.distance_to(self.player.pos) < bullet.radius + self.player.radius:
                        self.player.take_damage(10)
                        enemy.bullets.remove(bullet)

            # Trigger reward phase on score milestone
            if self.score % 500 == 0 and self.score > 0 and not self.in_reward_phase:
                if self.score != self.last_reward_score:
                    self.enter_reward_phase()
                    self.last_reward_score = self.score

        elif not self.reward_claimed:
            for bullet in self.player.bullets[:]:
                for reward in self.rewards:
                    if reward.pos.distance_to(bullet.pos) < reward.radius + bullet.radius:
                        reward.take_hit()
                        if bullet in self.player.bullets:
                            self.player.bullets.remove(bullet)
                        break
        else:
            self.reward_resume_timer -= dt
            if self.reward_resume_timer <= 0:
                self.reward_claimed = False
                self.in_reward_phase = False

    def draw(self):
        self.screen.fill(BLACK)
        draw_arena(self.screen)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for reward in self.rewards:
            reward.draw(self.screen)

        # Score display
        score_text = self.font.render(f"{self.score}pts!", True, WHITE)
        self.screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, ARENA_CENTER[1] + ARENA_RADIUS + 30)))

        # Health bar
        bar_width = 200
        bar_height = 20
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = ARENA_CENTER[1] + ARENA_RADIUS + 60

        pygame.draw.rect(self.screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
        health_ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.screen, (200, 50, 50), (bar_x, bar_y, bar_width * health_ratio, bar_height))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

    def handle_event(self, event):
        pass
