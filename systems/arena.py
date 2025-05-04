import pygame
import math
from settings import *

def draw_arena(screen, radius=ARENA_RADIUS, center=ARENA_CENTER, health_ratio=1.0, pulse=0, show_health=False):
    tick = pygame.time.get_ticks() / 100

    # Increase canvas size to avoid clipping on pulse
    base_size = 96
    padding = 16
    small_size = base_size + padding * 2
    arena_surface = pygame.Surface((small_size, small_size), pygame.SRCALPHA)
    center_px = base_size // 2 + padding

    points = []
    for angle in range(0, 360, 8):
        radians = math.radians(angle)
        wobble = math.sin(math.radians(angle * 3 + tick * 4)) * 4
        inner_wave = math.sin(radians * 5 + tick) * 2
        offset = wobble + inner_wave
        adjusted_radius = (base_size // 2 - 5 + pulse) + offset
        x = center_px + adjusted_radius * math.cos(radians)
        y = center_px + adjusted_radius * math.sin(radians)
        points.append((x, y))

    pygame.draw.polygon(arena_surface, WHITE, points, 1)

    # More accurate scale
    scale = round((radius * 2 * 1.25) / base_size)
    scaled = pygame.transform.scale(arena_surface, (small_size * scale, small_size * scale))
    rect = scaled.get_rect(center=center)
    screen.blit(scaled, rect)
