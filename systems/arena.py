# systems/arena.py

import pygame
import math
from settings import *

def draw_arena(screen, pulse=0):
    points = []
    tick = pygame.time.get_ticks() / 100  # animate

    for angle in range(0, 360, 6):
        radians = math.radians(angle)
        offset = math.sin(math.radians(angle * 4 + tick * 10)) * 6
        radius = ARENA_RADIUS + offset + pulse
        x = ARENA_CENTER[0] + radius * math.cos(radians)
        y = ARENA_CENTER[1] + radius * math.sin(radians)
        points.append((x, y))

    pygame.draw.polygon(screen, WHITE, points, 2)


    
