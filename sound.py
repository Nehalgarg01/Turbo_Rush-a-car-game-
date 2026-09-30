import pygame
import math
import random
import array

# Initialize audio mixer
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

def generate_tone(freq, duration_sec, wave_type="sine", vol=0.25):
    sample_rate = 22050
    n_samples = int(sample_rate * duration_sec)
    buf = array.array('h')
    
    for i in range(n_samples):
        t = float(i) / sample_rate
        if wave_type == "sine":
            val = math.sin(2.0 * math.pi * freq * t)
        elif wave_type == "noise":
            val = random.uniform(-0.8, 0.8)
        else:
            val = 0
            
        envelope = max(0.0, 1.0 - (float(i) / n_samples))
        sample = int(val * envelope * vol * 32767)
        buf.append(sample)
        buf.append(sample)
        
    return pygame.mixer.Sound(buf)

try:
    snd_coin = generate_tone(880, 0.12, "sine", 0.3)
    snd_crash = generate_tone(110, 0.35, "noise", 0.4)
    snd_start = generate_tone(520, 0.25, "sine", 0.3)
except Exception:
    class DummySound:
        def play(self):
            pass
    snd_coin = snd_crash = snd_start = DummySound()