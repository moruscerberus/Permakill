# entities/enemy.py

import pygame
import random
import math
from settings import *
from entities.enemy_bullet import EnemyBullet


class Enemy:
    def __init__(self, player_pos):
        # Spawn at a random angle around the arena
        angle = random.uniform(0, 2 * math.pi)
        radius = ARENA_RADIUS - 10
        self.pos = pygame.Vector2(
            ARENA_CENTER[0] + radius * math.cos(angle),
            ARENA_CENTER[1] + radius * math.sin(angle)
        )

        self.radius = 12
        self.speed = 100  # pixels per second
        self.color = (255, 50, 50)
        self.dead = False

        self.shoot_cooldown = 1.5
        self.shoot_timer = 0
        self.bullets = []

    def shoot(self, target_pos):
        direction = pygame.Vector2(target_pos) - self.pos
        if direction.length_squared() == 0:
            direction = pygame.Vector2(1, 0)
        self.bullets.append(EnemyBullet(self.pos, direction))


    def update(self, dt, player_pos):
        direction = (player_pos - self.pos).normalize()
        self.pos += direction * self.speed * dt

        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot(player_pos)
            self.shoot_timer = 0

        # Update bullets
        for b in self.bullets[:]:
            b.update(dt)
            if b.is_dead():
                self.bullets.remove(b)


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        for b in self.bullets:
            b.draw(screen)

    def collides_with(self, bullet):
        return self.pos.distance_to(bullet.pos) < self.radius + bullet.radius
