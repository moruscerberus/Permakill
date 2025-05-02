# entities/player.py
import pygame
from settings import *
from entities.bullet import Bullet

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(ARENA_CENTER)
        self.radius = 10
        self.health = 60
        self.max_health = 60
        self.regen = 0  # health per second
        self.bullet_speed = 500
        self.move_speed = PLAYER_SPEED
        self.shoot_cooldown = 0.25
        self.time_since_last_shot = 0

        self.damage_cooldown = 0.3
        self.time_since_hit = 0

        self.bullets = []

    def update(self, dt):
        keys = pygame.key.get_pressed()
        movement = pygame.Vector2(0, 0)

        if keys[pygame.K_w]: movement.y -= 1
        if keys[pygame.K_s]: movement.y += 1
        if keys[pygame.K_a]: movement.x -= 1
        if keys[pygame.K_d]: movement.x += 1

        if movement.length_squared() > 0:
            movement = movement.normalize() * self.move_speed
            new_pos = self.pos + movement

            to_center = new_pos - pygame.Vector2(ARENA_CENTER)
            if to_center.length() < ARENA_RADIUS - self.radius:
                self.pos = new_pos

        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.is_dead():
                self.bullets.remove(bullet)

        self.time_since_last_shot += dt
        self.time_since_hit += dt

        if self.regen > 0:
            self.health += self.regen * dt
            if self.health > self.max_health:
                self.health = self.max_health

    def try_shoot(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.time_since_last_shot > self.shoot_cooldown:
            self.shoot()
            self.time_since_last_shot = 0
            return True
        return False

    def shoot(self):
        mouse_pos = pygame.mouse.get_pos()
        dir_vec = pygame.Vector2(mouse_pos) - self.pos
        if dir_vec.length_squared() == 0:
            dir_vec = pygame.Vector2(1, 0)
        self.bullets.append(Bullet(self.pos, dir_vec, self.bullet_speed))

    def take_damage(self, amount):
        if self.health <= 0:
            return
        self.health = max(0, self.health - amount)
        self.time_since_hit = 0
        print(f"[DAMAGE] Took {amount}, health: {self.health}")

    def draw(self, screen, camera):
        color = WHITE if self.time_since_hit > 0.1 else (255, 50, 50)
        pygame.draw.circle(screen, color, camera.apply(self.pos), self.radius)
        for bullet in self.bullets:
            bullet.draw(screen, camera)
