# core/states/gameplay.py
from settings import *
from entities.player import Player
from entities.enemy import BaseEnemy, SniperEnemy, BomberEnemy
from entities.reward import Reward
from entities.effects import HitEffect, RewardBurstEffect
from systems.arena import draw_arena
from core.rewards import load_rewards, apply_reward
from core.assets import Assets
from core.camera import Camera
import pygame
import random
import math

class GamePlayState:
    def __init__(self, manager, screen):
        self.manager = manager
        self.screen = screen

        self.font = Assets.fonts['main']


        self.rewards_data = load_rewards()
        self.rewards = []
        self.in_reward_phase = False
        self.reward_claimed = False
        self.reward_resume_timer = 0
        self.last_reward_score = -1
        self.dead = False
        self.camera = Camera()
        self.effects = []

        self.ring_pulse = 0
        self.show_health_timer = 0

        self.wave_number = 1
        self.enemies_to_spawn = 0
        self.enemies_spawned = 0
        self.wave_duration = 0
        self.wave_timer = 0
        self.spawn_interval = 1.0
        self.spawn_timer = 0
        self.next_wave_pending = False
        self.pending_reward_trigger = False

    def enter(self):
        self.player = Player()
        self.enemies = []
        self.spawn_timer = 0
        self.score = 0
        self.rewards.clear()
        self.in_reward_phase = False
        self.reward_claimed = False
        self.reward_resume_timer = 0
        self.last_reward_score = -1
        self.dead = False
        self.camera = Camera()
        self.effects.clear()
        self.wave_number = 1
        self.start_wave()

    def start_wave(self):
        self.wave_timer = 0
        self.enemies_spawned = 0
        self.enemies_to_spawn = 5 + self.wave_number * 3
        self.wave_duration = 10 + self.wave_number * 2
        self.spawn_interval = max(0.3, 1.2 - self.wave_number * 0.05)
        print(f"--- Wave {self.wave_number} started ---")

    def spawn_enemy(self):
        if self.wave_number >= 5 and random.random() < 0.2:
            return BomberEnemy(self.player.pos)
        elif self.wave_number >= 2 and random.random() < 0.3:
            return SniperEnemy(self.player.pos)
        else:
            return BaseEnemy(self.player.pos)

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
            reward.on_shake = lambda intensity, cam=self.camera: cam.shake(intensity=intensity, duration=0.1)
            self.rewards.append(reward)

    def claim_reward(self, reward):
        if self.reward_claimed:
            return

        apply_reward(self.player, reward.data)
        self.effects.append(RewardBurstEffect(reward.pos))
        self.camera.shake(intensity=10, duration=0.3)
        self.reward_claimed = True
        self.in_reward_phase = False
        self.rewards.clear()
        self.reward_resume_timer = 1.0
        self.next_wave_pending = True

    def update(self, dt):
        if self.player_is_dead() and not self.dead:
            self.dead = True
            self.manager.set_state("game_over")

        if self.dead:
            return

        self.camera.update(dt)
        self.player.update(dt)

        if self.player.try_shoot():
            self.camera.shake(intensity=2, duration=0.05)
            self.ring_pulse = 12

        for fx in self.effects[:]:
            fx.update(dt)
            if fx.is_dead():
                self.effects.remove(fx)

        if self.ring_pulse > 0:
            self.ring_pulse -= 60 * dt

        if self.show_health_timer > 0:
            self.show_health_timer -= dt

        if not self.in_reward_phase and not self.reward_claimed:
            self.wave_timer += dt

            if self.enemies_spawned < self.enemies_to_spawn:
                self.spawn_timer += dt
                if self.spawn_timer >= self.spawn_interval:
                    self.enemies.append(self.spawn_enemy())
                    self.spawn_timer = 0
                    self.enemies_spawned += 1

            if self.wave_timer >= self.wave_duration:
                self.pending_reward_trigger = True

            if self.pending_reward_trigger and len(self.enemies) == 0:
                self.wave_number += 1
                self.pending_reward_trigger = False
                self.enter_reward_phase()

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
                if self.next_wave_pending:
                    self.next_wave_pending = False
                    self.start_wave()

        for enemy in self.enemies:
            enemy.update(dt, self.player.pos)

        for bullet in self.player.bullets[:]:
            for enemy in self.enemies:
                if enemy.collides_with(bullet):
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                        self.score += 50
                        self.camera.shake(intensity=6, duration=0.2)
                        self.effects.append(HitEffect(enemy.pos))
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    break

        for enemy in self.enemies[:]:
            if isinstance(enemy, BomberEnemy) and not enemy.exploded:
                if enemy.pos.distance_to(self.player.pos) < enemy.explode_radius:
                    enemy.explode()
                    self.player.take_damage(30)
                    self.camera.shake(intensity=10, duration=0.3)
                    self.ring_pulse = 25
                    self.show_health_timer = 2.0

        self.enemies = [e for e in self.enemies if not (isinstance(e, BomberEnemy) and e.exploded)]

        for enemy in self.enemies:
            if enemy.pos.distance_to(self.player.pos) < enemy.radius + self.player.radius:
                if self.player.time_since_hit >= self.player.damage_cooldown:
                    self.player.take_damage(10)
                    self.player.time_since_hit = 0
                    self.ring_pulse = 20
                    self.show_health_timer = 2.0

        for enemy in self.enemies:
            for bullet in getattr(enemy, 'bullets', [])[:]:
                if bullet.pos.distance_to(self.player.pos) < bullet.radius + self.player.radius:
                    self.player.take_damage(10)
                    enemy.bullets.remove(bullet)
                    self.ring_pulse = 20
                    self.show_health_timer = 2.0

    def draw(self):
        self.screen.fill(BLACK)
        draw_arena(
            self.screen,
            pulse=self.ring_pulse,
            show_health=self.show_health_timer > 0,
            health_ratio=self.player.health / self.player.max_health
        )

        self.player.draw(self.screen, self.camera)
        for fx in self.effects:
            fx.draw(self.screen, self.camera)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera, self.player.pos)
        for reward in self.rewards:
            reward.draw(self.screen, self.camera)

        score_text = self.font.render(f"{self.score}pts!", True, WHITE)
        self.screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, ARENA_CENTER[1] + ARENA_RADIUS + 30)))

        wave_text = self.font.render(f"WAVE {self.wave_number}", True, (180, 180, 255))
        self.screen.blit(wave_text, (20, 20))

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
