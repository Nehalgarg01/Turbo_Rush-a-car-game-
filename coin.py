import pygame
import random


class Coin:
    def __init__(self, speed, lanes=None):
        if lanes is None:
            lanes = [220, 315, 410, 505]

        self.x = random.choice(lanes) + 13
        self.y = -30

        self.size = 24
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            (255, 210, 20),
            (self.x + 12, self.y + 12),
            12
        )

        pygame.draw.circle(
            screen,
            (255, 150, 0),
            (self.x + 12, self.y + 12),
            7
        )

        pygame.draw.circle(
            screen,
            (255, 230, 70),
            (self.x + 12, self.y + 12),
            3
        )

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

class Booster:
    def __init__(self, speed, lanes=None):
        if lanes is None:
            lanes = [220, 315, 410, 505]

        # 5 Subway Surfers style power-ups
        self.kind = random.choice(["magnet", "shield", "jetpack", "star", "double"])
        self.x = random.choice(lanes) + 10
        self.y = -45
        self.size = 30
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        cx = self.x + self.size // 2
        cy = int(self.y + self.size // 2)

        if self.kind == "magnet":
            # Red Horseshoe Magnet
            pygame.draw.circle(screen, (220, 30, 30), (cx, cy), 15)
            pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 7)
            pygame.draw.rect(screen, (55, 55, 55), (cx - 15, cy, 30, 15))
            pygame.draw.rect(screen, (200, 200, 200), (cx - 15, cy - 2, 8, 7))
            pygame.draw.rect(screen, (200, 200, 200), (cx + 7, cy - 2, 8, 7))

        elif self.kind == "shield":
            # Cyan Shield Orb
            pygame.draw.circle(screen, (0, 210, 255), (cx, cy), 15)
            pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 15, 2)
            pygame.draw.rect(screen, (255, 255, 255), (cx - 3, cy - 9, 6, 18))
            pygame.draw.rect(screen, (255, 255, 255), (cx - 9, cy - 3, 18, 6))

        elif self.kind == "jetpack":
            # Orange Jetpack with Lightning Bolt
            pygame.draw.circle(screen, (255, 140, 0), (cx, cy), 15)
            pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 15, 2)
            pts = [(cx + 2, cy - 9), (cx - 5, cy), (cx + 1, cy), (cx - 2, cy + 9), (cx + 6, cy - 1), (cx - 1, cy - 1)]
            pygame.draw.polygon(screen, (255, 255, 255), pts)

        elif self.kind == "star":
            # Gold Star Instant Score Orb
            pygame.draw.circle(screen, (255, 215, 0), (cx, cy), 15)
            pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 15, 2)
            star_pts = [
                (cx, cy - 8), (cx + 3, cy - 2), (cx + 9, cy - 2),
                (cx + 4, cy + 2), (cx + 6, cy + 8), (cx, cy + 4),
                (cx - 6, cy + 8), (cx - 4, cy + 2), (cx - 9, cy - 2), (cx - 3, cy - 2)
            ]
            pygame.draw.polygon(screen, (255, 255, 255), star_pts)

        elif self.kind == "double":
            # Purple 2X Multiplier Orb
            pygame.draw.circle(screen, (170, 40, 230), (cx, cy), 15)
            pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 15, 2)
            font_s = pygame.font.Font(None, 22)
            txt = font_s.render("2X", True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=(cx, cy)))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)