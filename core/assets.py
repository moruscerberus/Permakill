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
        cls.images['enemy'] =  pygame.transform.scale(pygame.image.load('assets/sprites/enemy.png').convert_alpha(), (32, 32))
        cls.images['sniper'] = pygame.transform.scale(pygame.image.load('assets/sprites/sniper.png').convert_alpha(), (32, 32))
        cls.images['bomber'] = pygame.transform.scale(pygame.image.load('assets/sprites/bomber.png').convert_alpha(), (32, 32))
        cls.images['player'] = pygame.transform.scale(pygame.image.load('assets/sprites/player.png').convert_alpha(), (48, 48))

        cls.fonts = {}
        cls.fonts['main'] = pygame.font.Font('assets/fonts/runescape_uf.ttf', 32)
        cls.fonts['small'] = pygame.font.Font('assets/fonts/runescape_uf.ttf', 20)

        # === SOUNDS ===
        cls.sounds = {
            'click': pygame.mixer.Sound('assets/sounds/click.wav'),
            'hover': pygame.mixer.Sound('assets/sounds/hover.wav'),
            'shoot': pygame.mixer.Sound('assets/sounds/shoot.wav'),
            'hit': pygame.mixer.Sound('assets/sounds/hitHurt.wav'),
            'explode': pygame.mixer.Sound('assets/sounds/explosion.wav'),
            'powerup': pygame.mixer.Sound('assets/sounds/powerUp.wav'),
        }

    @classmethod
    def get(cls, name):
        return cls.images.get(name)
