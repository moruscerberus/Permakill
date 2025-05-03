import pygame

class ShipGenerator:
    @staticmethod
    def generate_triangle(size=24, top_color=(255, 80, 80), side_color=(180, 50, 50)):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        height = size

        # Triangle points
        top = (center, 0)
        left = (0, height)
        right = (size, height)

        # Shade left side
        pygame.draw.polygon(surf, side_color, [top, (center, height), left])

        # Shade right side
        pygame.draw.polygon(surf, side_color, [top, right, (center, height)])

        # Main triangle on top
        pygame.draw.polygon(surf, top_color, [top, left, right])

        return surf

    @staticmethod
    def generate_square(size=24, fill_color=(255, 80, 80), outline_color=(255, 30, 30)):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(surf, fill_color, (4, 4, size - 8, size - 8))
        pygame.draw.rect(surf, outline_color, (4, 4, size - 8, size - 8), 2)
        return surf

    @staticmethod
    def generate_diamond(size=24, fill_color=(255, 255, 255), shadow_color=(180, 180, 180)):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        points = [
            (center, 0),
            (size, center),
            (center, size),
            (0, center)
        ]
        pygame.draw.polygon(surf, shadow_color, points)
        pygame.draw.polygon(surf, fill_color, points, 1)
        return surf


    @staticmethod
    def generate_player_ship(size=48, top_color=(255, 255, 255), side_color=(180, 180, 180)):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2

        top = (center, 0)
        left = (0, size)
        right = (size, size)
        mid_bottom = (center, size)

        # Fake shading on sides
        pygame.draw.polygon(surf, side_color, [top, mid_bottom, left])
        pygame.draw.polygon(surf, side_color, [top, right, mid_bottom])

        # Main white triangle
        pygame.draw.polygon(surf, top_color, [top, left, right])

        return surf
