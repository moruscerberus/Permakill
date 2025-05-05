import os
import struct
import json
import pygame
from io import BytesIO
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from core.utils.ship_generator import ShipGenerator

class Assets:
    _loaded = False
    images = {}
    sounds = {}
    fonts = {}
    jsons = {}
    sound_enabled = True
    music_enabled = True

    ASSET_FILE = "game.assets"
    _AES_KEY = b'\x9e\xfaA\xf3\xcfY\xb4\xa7\xe0\xd3t\xe3R\xc1\xe1\x87\xdc\x13\x90\xd5\x1a\xc7V\x05\x83^\xa4\xc3L\xc0\xa2K'

    @classmethod
    def load(cls):
        if cls._loaded:
            return
        cls._loaded = True

        assets = cls._load_encrypted_asset_file(cls.ASSET_FILE)

        # === IMAGES ===
        def load_img(key, scale=None):
            if key not in assets:
                return None
            img = pygame.image.load(BytesIO(assets[key])).convert_alpha()
            return pygame.transform.scale(img, scale) if scale else img

        cls.images['cursor'] = load_img("assets/sprites/cursor.png", (24, 24))
        cls.images['enemy'] = load_img("assets/sprites/enemy.png", (32, 32))
        cls.images['sniper'] = load_img("assets/sprites/sniper.png", (32, 32))
        cls.images['bomber'] = load_img("assets/sprites/bomber.png", (32, 32))
        cls.images['player'] = load_img("assets/sprites/player.png", (48, 48))

        cls.images['audio_on'] = load_img("assets/sprites/audio_on.png", (32, 32))
        cls.images['audio_off'] = load_img("assets/sprites/audio_off.png", (32, 32))
        cls.images['music_on'] = load_img("assets/sprites/music_on.png", (32, 32))
        cls.images['music_off'] = load_img("assets/sprites/music_off.png", (32, 32))
        cls.images['warning'] = load_img("assets/sprites/warning_triangle.png", (32, 32))

        cls.images['reward_bullet'] = load_img("assets/sprites/reward_bullet.png", (64, 64))
        cls.images['reward_health'] = load_img("assets/sprites/reward_health.png", (64, 64))
        cls.images['reward_movement'] = load_img("assets/sprites/reward_movement.png", (64, 64))

        # === SOUNDS ===
        def load_sound(key):
            return pygame.mixer.Sound(BytesIO(assets[key])) if key in assets else None

        cls.sounds = {
            'click': load_sound("assets/sounds/click.wav"),
            'hover': load_sound("assets/sounds/hover.wav"),
            'shoot': load_sound("assets/sounds/shoot.wav"),
            'hit': load_sound("assets/sounds/hitHurt.wav"),
            'explode': load_sound("assets/sounds/explosion.wav"),
            'powerup': load_sound("assets/sounds/powerUp.wav"),
        }

        # === FONTS ===
        def load_font(key, size):
            return pygame.font.Font(BytesIO(assets[key]), size) if key in assets else None

        cls.fonts['main'] = load_font("assets/fonts/runescape_uf.ttf", 32)
        cls.fonts['small'] = load_font("assets/fonts/runescape_uf.ttf", 20)
        cls.fonts['splash_main'] = load_font("assets/fonts/runescape_uf.ttf", 64)
        cls.fonts['splash_small'] = load_font("assets/fonts/runescape_uf.ttf", 32)

        # === JSON DATA ===
        for key in assets:
            if key.endswith("rewards.json"):
                cls.jsons["rewards"] = json.loads(assets[key].decode("utf-8"))
                break


    @classmethod
    def _load_encrypted_asset_file(cls, path):
        assets = {}
        with open(path, "rb") as f:
            file_count = struct.unpack("<I", f.read(4))[0]
            for _ in range(file_count):
                path_len = struct.unpack("<H", f.read(2))[0]
                asset_path = f.read(path_len).decode("utf-8")
                data_len = struct.unpack("<I", f.read(4))[0]
                enc_data = f.read(data_len)

                iv = enc_data[:16]
                cipher = AES.new(cls._AES_KEY, AES.MODE_CBC, iv)
                decrypted = unpad(cipher.decrypt(enc_data[16:]), AES.block_size)

                assets[asset_path] = decrypted
        return assets

    @classmethod
    def get(cls, name):
        return cls.images.get(name)

    @classmethod
    def toggle_music(cls):
        cls.music_enabled = not cls.music_enabled
        if cls.music_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
