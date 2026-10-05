import pygame
import os

# Initialize mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.set_num_channels(16)

# Locate the assets directory relative to this script
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def load_sound(file_name, volume=1.0):
    # Checks assets folder first, then falls back to current directory
    path = os.path.join(ASSETS_DIR, file_name)
    if not os.path.exists(path):
        path = os.path.join(BASE_DIR, file_name)

    if os.path.exists(path):
        snd = pygame.mixer.Sound(path)
        snd.set_volume(volume)
        return snd
    else:
        # Fallback dummy so the game never crashes
        class DummySound:
            def play(self, *args, **kwargs):
                pass
            def stop(self):
                pass
        return DummySound()

# One-time starting roar
snd_engine_start = load_sound("car-engine-roaring.mp3", volume=1.0)

# Gameplay sounds
snd_coin      = load_sound("coin-pickup.mp3", volume=0.85)
snd_booster   = load_sound("retro_gaming.mp3", volume=0.95)
snd_nitro     = load_sound("winds-swoosh.mp3", volume=0.85)
snd_crash     = load_sound("car-crash.mp3", volume=0.90)
snd_near_miss = load_sound("fast-swoosh.mp3", volume=0.85)
snd_game_over = load_sound("game-over.mp3", volume=1.0)