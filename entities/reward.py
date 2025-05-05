import pygame
import math
from settings import *
from core.assets import Assets

class Reward:
    def __init__(self, reward_data, position, on_claim):
        self.name = reward_data["name"]
        self.description = reward_data["description"]
        self.type = reward_data.get("type", "generic")
        self.data = reward_data
        self.pos = pygame.Vector2(position)
        self.radius = 18
        self.max_health = 5
        self.health = self.max_health
        self.on_claim = on_claim
        self.font = Assets.fonts['main']
        self.claimed = False

        self.flash_timer = 0
        self.bounce_timer = 0

        self.sprite = self.get_sprite_for_type(self.type)

    def get_sprite_for_type(self, reward_type):
        sprite_map = {
            "bullet": "reward_bullet",
            "health": "reward_health",
            "movement": "reward_movement"
        }
        return Assets.get(sprite_map.get(reward_type))

    def update(self, dt):
        if self.flash_timer > 0:
            self.flash_timer -= dt
        self.bounce_timer += dt

    def take_hit(self):
        if self.claimed:
            return

        self.health -= 1
        self.flash_timer = 0.1

        health_ratio = self.health / self.max_health
        intensity = 4 + (1 - health_ratio) * 6
        if hasattr(self, "on_shake"):
            self.on_shake(intensity)

        if self.health <= 0:
            self.claim()

    def claim(self):
        self.claimed = True
        self.on_claim(self)
        if Assets.sound_enabled:
            Assets.sounds['powerup'].play()

    def draw(self, screen, camera):
        # Bounce
        bounce_offset = math.sin(self.bounce_timer * 8) * 3
        draw_pos = pygame.Vector2(self.pos.x, self.pos.y + bounce_offset)
        screen_pos = camera.apply(draw_pos)

        if self.sprite:
            rect = self.sprite.get_rect(center=screen_pos)
            screen.blit(self.sprite, rect)

            # Real flash effect using white overlay with additive blend
            if self.flash_timer > 0:
                flash_image = self.sprite.copy()
                pixel_array = pygame.PixelArray(flash_image)
                width, height = flash_image.get_size()

                for x in range(width):
                    for y in range(height):
                        color = flash_image.unmap_rgb(pixel_array[x, y])
                        if color.a > 0:
                            r = min(color.r + 60, 255)
                            g = min(color.g + 60, 255)
                            b = min(color.b + 60, 255)
                            pixel_array[x, y] = (r, g, b, color.a)

                del pixel_array
                screen.blit(flash_image, rect)

        else:
            color = WHITE
            pygame.draw.circle(screen, color, screen_pos, self.radius)

        # Hover text
        mouse_pos_screen = pygame.mouse.get_pos()
        mouse_pos_world = camera.reverse_apply(mouse_pos_screen)

        if self.pos.distance_to(mouse_pos_world) <= self.radius + 10:
            name_surf = self.font.render(self.name, True, WHITE)
            desc_surf = self.font.render(self.description, True, (180, 180, 180))
            screen.blit(desc_surf, desc_surf.get_rect(center=camera.apply((self.pos.x, self.pos.y - 90))))
            screen.blit(name_surf, name_surf.get_rect(center=camera.apply((self.pos.x, self.pos.y - 64))))
