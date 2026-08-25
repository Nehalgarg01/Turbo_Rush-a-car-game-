import pygame
import random


class Coin:
    def __init__(self, speed):
        lanes = [220, 315, 410, 505]

        self.x = random.choice(lanes)
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