# entities/player.py
import pygame
from settings import *
from entities.bullet import Bullet
from core.assets import Assets
import math

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
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        direction = (mouse_pos - self.pos).normalize()

        # Perpendicular for gun spacing
        perp = pygame.Vector2(-direction.y, direction.x)

        # Gun positions
        left_gun = self.pos + direction * 20 + perp * 10
        right_gun = self.pos + direction * 20 - perp * 10

        # Aim each gun *toward the cursor*
        left_dir = (mouse_pos - left_gun).normalize()
        right_dir = (mouse_pos - right_gun).normalize()

        self.bullets.append(Bullet(left_gun, left_dir, self.bullet_speed))
        self.bullets.append(Bullet(right_gun, right_dir, self.bullet_speed))

        Assets.sounds['shoot'].play()

    def take_damage(self, amount):
        if self.health <= 0:
            return
        self.health = max(0, self.health - amount)
        self.time_since_hit = 0
        print(f"[DAMAGE] Took {amount}, health: {self.health}")
        Assets.sounds['hit'].play()

    def draw(self, screen, camera):
        image = Assets.get('player')
        if image:
            mouse_pos = pygame.mouse.get_pos()
            direction = pygame.Vector2(mouse_pos) - camera.apply(self.pos)
            angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
            rotated = pygame.transform.rotate(image, angle)
            rect = rotated.get_rect(center=camera.apply(self.pos))
            screen.blit(rotated, rect)

        for bullet in self.bullets:
            bullet.draw(screen, camera)
