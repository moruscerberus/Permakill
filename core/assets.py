import pygame
from core.utils.ship_generator import ShipGenerator


class Assets:
    _loaded = False
    images = {}

    @classmethod
    def load(cls):
        if cls._loaded:
            return
        cls._loaded = True

        cls.images['cursor'] = pygame.transform.scale(
    pygame.image.load('assets/sprites/cursor.png').convert_alpha(), (24, 24)
    )   

        # === SHIP SPRITES ===
        cls.images['enemy'] = ShipGenerator.generate_square(size=38)
        cls.images['sniper'] = ShipGenerator.generate_triangle()
        cls.images['bomber'] = ShipGenerator.generate_diamond()
        cls.images['player'] = pygame.transform.scale(pygame.image.load('assets/sprites/player.png').convert_alpha(), (48, 48))



        # You can preload more here:
        # cls.images['enemy'] = ...
        # cls.images['bg'] = ...

    @classmethod
    def get(cls, name):
        return cls.images.get(name)
