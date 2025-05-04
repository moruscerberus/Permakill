import pygame
from core.utils.ship_generator import ShipGenerator


class Assets:
    _loaded = False
    images = {}
    sound_enabled = True
    music_enabled = True

    @classmethod
    def load(cls):
        if cls._loaded:
            return
        cls._loaded = True

        cls.images['cursor'] = pygame.transform.scale(
            pygame.image.load('assets/sprites/cursor.png').convert_alpha(), (24, 24)
        )

        # === SHIP SPRITES ===
        cls.images['enemy'] = pygame.transform.scale(pygame.image.load('assets/sprites/enemy.png').convert_alpha(), (32, 32))
        cls.images['sniper'] = pygame.transform.scale(pygame.image.load('assets/sprites/sniper.png').convert_alpha(), (32, 32))
        cls.images['bomber'] = pygame.transform.scale(pygame.image.load('assets/sprites/bomber.png').convert_alpha(), (32, 32))
        cls.images['player'] = pygame.transform.scale(pygame.image.load('assets/sprites/player.png').convert_alpha(), (48, 48))


        # === UI ICONS ===
        cls.images['audio_on'] = pygame.transform.scale(pygame.image.load('assets/sprites/audio_on.png').convert_alpha(), (32, 32))
        cls.images['audio_off'] = pygame.transform.scale(pygame.image.load('assets/sprites/audio_off.png').convert_alpha(), (32, 32))

        cls.images['music_on'] = pygame.transform.scale(pygame.image.load('assets/sprites/music_on.png').convert_alpha(), (32, 32))
        cls.images['music_off'] = pygame.transform.scale(pygame.image.load('assets/sprites/music_off.png').convert_alpha(), (32, 32))

        cls.images['warning'] = pygame.transform.scale(pygame.image.load('assets/sprites/warning_triangle.png').convert_alpha(), (32, 32))

        cls.fonts = {}
        cls.fonts['main'] = pygame.font.Font('assets/fonts/runescape_uf.ttf', 32)
        cls.fonts['small'] = pygame.font.Font('assets/fonts/runescape_uf.ttf', 20)

        cls.fonts['splash_main'] = pygame.font.Font('assets/fonts/runescape_uf.ttf', 64)
        cls.fonts['splash_small'] = pygame.font.Font('assets/fonts/runescape_uf.ttf', 32)


        # === SOUNDS ===
        cls.sounds = {
            'click': pygame.mixer.Sound('assets/sounds/click.wav'),
            'hover': pygame.mixer.Sound('assets/sounds/hover.wav'),
            'shoot': pygame.mixer.Sound('assets/sounds/shoot.wav'),
            'hit': pygame.mixer.Sound('assets/sounds/hitHurt.wav'),
            'explode': pygame.mixer.Sound('assets/sounds/explosion.wav'),
            'powerup': pygame.mixer.Sound('assets/sounds/powerUp.wav'),
        }

        # === MUSIC ===
        # pygame.mixer.music.load('assets/sounds/music.mp3')
        # pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play(-1)  # loop forever

    @classmethod
    def toggle_music(cls):
        cls.music_enabled = not cls.music_enabled
        if cls.music_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    @classmethod
    def get(cls, name):
        return cls.images.get(name)
