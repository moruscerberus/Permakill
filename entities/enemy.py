import pygame
import math
import random
from settings import *
from entities.bullet import Bullet
from core.assets import Assets

class BaseEnemy:
    def __init__(self, player_pos):
        self.pos = self.get_spawn_position(player_pos)
        self.radius = 12
        self.speed = 100
        self.bullets = []

    def get_spawn_position(self, player_pos):
        angle = random.uniform(0, 2 * math.pi)
        dist = ARENA_RADIUS - 20
        x = ARENA_CENTER[0] + dist * math.cos(angle)
        y = ARENA_CENTER[1] + dist * math.sin(angle)
        return pygame.Vector2(x, y)

    def update(self, dt, player_pos):
        direction = player_pos - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        self.pos += direction * self.speed * dt

    def draw(self, screen, camera, player_pos):
        image = Assets.get('enemy')
        if image:
            rect = image.get_rect(center=camera.apply(self.pos))
            screen.blit(image, rect)

        for bullet in self.bullets:
            bullet.draw(screen, camera)

    def collides_with(self, bullet):
        return self.pos.distance_to(bullet.pos) < self.radius + bullet.radius

class SniperEnemy(BaseEnemy):
    def __init__(self, player_pos):
        super().__init__(player_pos)
        self.radius = 10
        self.speed = 60
        self.shoot_timer = 0
        self.shoot_cooldown = 2.5
        self.aim_duration = 1.0
        self.aim_time = 0
        self.is_aiming = False
        self.locked_direction = None

    def update(self, dt, player_pos):
        direction = player_pos - self.pos
        distance = direction.length()

        if not self.is_aiming:
            if distance < 140:
                self.pos -= direction.normalize() * self.speed * dt
            elif distance > 180:
                self.pos += direction.normalize() * self.speed * dt

        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_cooldown:
            if not self.is_aiming:
                self.is_aiming = True
                self.aim_time = 0
                aim_vec = player_pos - self.pos
                if aim_vec.length_squared() > 0:
                    self.locked_direction = aim_vec.normalize()

            self.aim_time += dt
            if self.aim_time >= self.aim_duration:
                self.fire()
                self.shoot_timer = 0
                self.is_aiming = False

        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.is_dead():
                self.bullets.remove(bullet)

    def fire(self):
        if self.locked_direction:
            self.bullets.append(Bullet(self.pos, self.locked_direction, speed=350))

    def draw(self, screen, camera, player_pos):
        if self.is_aiming and self.locked_direction:
            progress = min(self.aim_time / self.aim_duration, 1.0)
            alpha = int(100 + 155 * progress)
            aim_color = (255, 0, 0, alpha)
            start = camera.apply(self.pos)
            end_point = pygame.Vector2(start) + self.locked_direction * 100
            aim_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            pygame.draw.line(aim_surface, aim_color, start, end_point, 4)
            screen.blit(aim_surface, (0, 0))

        image = Assets.get('sniper')
        if image:
            rect = image.get_rect(center=camera.apply(self.pos))
            screen.blit(image, rect)
        for bullet in self.bullets:
            bullet.draw(screen, camera)

class BomberEnemy(BaseEnemy):
    def __init__(self, player_pos):
        super().__init__(player_pos)
        self.radius = 14
        self.speed = 150
        self.explode_radius = 30
        self.exploded = False

    def update(self, dt, player_pos):
        if self.exploded:
            return

        direction = player_pos - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        self.pos += direction * self.speed * dt

        if self.pos.distance_to(player_pos) < self.explode_radius:
            self.explode()

    def explode(self):
        self.exploded = True
        self.radius = 0
        self.damage = 30
        print("[BOMBER] Exploded!")

    def draw(self, screen, camera, player_pos):
        if not self.exploded:
            # Danger zone circle
            dist = self.pos.distance_to(player_pos)
            if dist < self.explode_radius * 2:
                alpha = max(0, 255 - int((dist / (self.explode_radius * 2)) * 255))
                danger_surface = pygame.Surface((self.explode_radius * 4, self.explode_radius * 4), pygame.SRCALPHA)
                pygame.draw.circle(
                    danger_surface,
                    (255, 0, 0, alpha),
                    (danger_surface.get_width() // 2, danger_surface.get_height() // 2),
                    self.explode_radius * 2
                )
                danger_rect = danger_surface.get_rect(center=camera.apply(self.pos))
                screen.blit(danger_surface, danger_rect)

            image = Assets.get('bomber')
            if image:
                rect = image.get_rect(center=camera.apply(self.pos))
                screen.blit(image, rect)
