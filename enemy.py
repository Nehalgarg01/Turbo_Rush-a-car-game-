import pygame
import random


class Enemy:
    def __init__(self, speed):
        self.width = 50
        self.height = 90

        # Four road lanes
        lanes = [220, 315, 410, 505]

        self.x = random.choice(lanes)
        self.y = -110

        self.speed = speed

        self.color = random.choice([
            (30, 100, 220),
            (150, 40, 180),
            (255, 140, 20),
            (240, 210, 30),
            (20, 180, 150)
        ])

        self.passed = False

    def move(self):
        self.y += self.speed

    def draw(self, screen):

        # Wheels
        pygame.draw.rect(
            screen,
            (10, 10, 10),
            (self.x - 5, self.y + 12, 8, 25)
        )

        pygame.draw.rect(
            screen,
            (10, 10, 10),
            (self.x + 47, self.y + 12, 8, 25)
        )

        pygame.draw.rect(
            screen,
            (10, 10, 10),
            (self.x - 5, self.y + 53, 8, 25)
        )

        pygame.draw.rect(
            screen,
            (10, 10, 10),
            (self.x + 47, self.y + 53, 8, 25)
        )

        # Body
        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y, self.width, self.height)
        )

        # Window
        pygame.draw.rect(
            screen,
            (20, 30, 40),
            (self.x + 8, self.y + 10, 34, 25)
        )

        # Lights
        pygame.draw.rect(
            screen,
            (255, 80, 80),
            (self.x + 7, self.y + 78, 10, 6)
        )

        pygame.draw.rect(
            screen,
            (255, 80, 80),
            (self.x + 33, self.y + 78, 10, 6)
        )

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )