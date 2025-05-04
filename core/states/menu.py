# core/states/menu.py

import pygame
import math
from settings import *
from core.assets import Assets
from systems.arena import draw_arena

class MenuState:
    def __init__(self, manager, screen):
        self.manager = manager
        self.screen = screen
        self.font = Assets.fonts['main']
        self.buttons = self.create_buttons()
        self.feedback_message = ""
        self.feedback_timer = 0

    def create_buttons(self):
        center_x, center_y = ARENA_CENTER
        return [
            {'label': 'START', 'pos': (center_x, center_y - 40), 'action': lambda: self.manager.set_state('gameplay')},
            {'label': 'CREDITS', 'pos': (center_x, center_y + 40), 'action': lambda: self.manager.set_state('settings')},
            {'label': '♫', 'pos': (center_x - 100, center_y), 'action': self.toggle_music},
            {'label': '🔊', 'pos': (center_x + 100, center_y), 'action': self.toggle_sound},
        ]

    def toggle_sound(self):
        Assets.sound_enabled = not getattr(Assets, 'sound_enabled', True)
        status = "ON" if Assets.sound_enabled else "OFF"
        self.feedback_message = f"SOUND: {status}"
        self.feedback_timer = 1.5
        if Assets.sound_enabled:
            Assets.sounds['click'].play()
        print(f"Sound {status.lower()}")

    def toggle_music(self):
        Assets.toggle_music()
        status = "ON" if Assets.music_enabled else "OFF"
        self.feedback_message = f"MUSIC: {status}"
        self.feedback_timer = 1.5
        print(f"Music {status.lower()}")

    def enter(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if self.is_hovering(btn):
                    if getattr(Assets, 'sound_enabled', True):
                        Assets.sounds['click'].play()
                    btn['action']()

    def is_hovering(self, button):
        mx, my = pygame.mouse.get_pos()
        bx, by = button['pos']
        return abs(mx - bx) < 50 and abs(my - by) < 20

    def update(self, dt):
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
            if self.feedback_timer <= 0:
                self.feedback_message = ""

    def draw_button(self, screen, label, pos, hovered):
        x, y = pos
        tick = pygame.time.get_ticks() / 100

        # Create low-res button outline surface
        w, h = 48, 32
        outline_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        cx, cy = w // 2, h // 2

        points = []
        for angle in range(0, 360, 20):
            radians = math.radians(angle)
            offset = math.sin(math.radians(angle * 4 + tick * 10)) * 2
            rx = (w // 2 - 4) + offset
            ry = (h // 2 - 4) + offset
            px = cx + rx * math.cos(radians)
            py = cy + ry * math.sin(radians)
            points.append((px, py))

        # Red outline if sound/music is off and this is the toggle
        if label == '♫' and not Assets.music_enabled:
            color = (255, 80, 80)
        elif label == '🔊' and not Assets.sound_enabled:
            color = (255, 80, 80)
        else:
            color = WHITE if not hovered else (200, 200, 255)

        pygame.draw.polygon(outline_surface, color, points, 1)

        # Scale up the outline
        scale = 3
        scaled_outline = pygame.transform.scale(outline_surface, (w * scale, h * scale))
        rect = scaled_outline.get_rect(center=(x, y))
        screen.blit(scaled_outline, rect)

        # Draw icon or text
        if label == '🔊':
            icon_key = 'audio_on' if getattr(Assets, 'sound_enabled', True) else 'audio_off'
            icon = Assets.images.get(icon_key)
            if icon:
                screen.blit(icon, icon.get_rect(center=(x, y)))
        elif label == '♫':
            icon_key = 'music_on' if getattr(Assets, 'music_enabled', True) else 'music_off'
            icon = Assets.images.get(icon_key)
            if icon:
                screen.blit(icon, icon.get_rect(center=(x, y)))
        else:
            text_surf = self.font.render(label, True, WHITE)
            text_rect = text_surf.get_rect(center=(x, y))
            screen.blit(text_surf, text_rect)

    def draw(self):
        self.screen.fill(BLACK)
        draw_arena(self.screen)

        # Central idle square
        time = pygame.time.get_ticks() / 500
        scale = 10 + math.sin(time) * 2
        pygame.draw.rect(
            self.screen,
            WHITE,
            pygame.Rect(ARENA_CENTER[0] - scale, ARENA_CENTER[1] - 100 - scale, scale * 2, scale * 2)
        )

        for btn in self.buttons:
            hovered = self.is_hovering(btn)
            self.draw_button(self.screen, btn['label'], btn['pos'], hovered)

        if self.feedback_message:
            feedback_surf = self.font.render(self.feedback_message, True, (255, 255, 100))
            rect = feedback_surf.get_rect(center=(WIDTH // 2, HEIGHT - 60))
            self.screen.blit(feedback_surf, rect)
