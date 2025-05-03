# systems/arena.py

import pygame
import math
from settings import *

def draw_arena(screen, pulse=0, show_health=False, health_ratio=1.0):
    points = []
    tick = pygame.time.get_ticks() / 100

    for angle in range(0, 360, 6):
        radians = math.radians(angle)
        offset = math.sin(math.radians(angle * 4 + tick * 10)) * 6
        radius = ARENA_RADIUS + offset + pulse
        x = ARENA_CENTER[0] + radius * math.cos(radians)
        y = ARENA_CENTER[1] + radius * math.sin(radians)
        points.append((x, y))

    pygame.draw.polygon(screen, WHITE, points, 2)

    if show_health:
        bar_count = 4
        active_bars = int(bar_count * health_ratio)
        for i in range(bar_count):
            angle = -60 + i * 40  # centered at top
            radians = math.radians(angle)
            inner_r = ARENA_RADIUS - 8
            outer_r = ARENA_RADIUS + 8

            x1 = ARENA_CENTER[0] + inner_r * math.cos(radians)
            y1 = ARENA_CENTER[1] + inner_r * math.sin(radians)
            x2 = ARENA_CENTER[0] + outer_r * math.cos(radians)
            y2 = ARENA_CENTER[1] + outer_r * math.sin(radians)

            color = (255, 80, 80) if i < active_bars else (80, 80, 80)
            pygame.draw.line(screen, color, (x1, y1), (x2, y2), 4)
