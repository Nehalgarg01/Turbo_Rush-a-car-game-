import pygame


class Player:
    def __init__(self, x, y, min_x=0, max_x=800):
        self.x = x
        self.y = y
        self.min_x = min_x 
        self.max_x = max_x

        self.width = 50
        self.height = 90

        self.speed = 7
        self.color = (220, 30, 30)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Keep car on road
        if self.x < self.min_x:
            self.x = self.min_x

        if self.x > self.max_x:
            self.x = self.max_x

    def draw(self, screen, nitro=False):

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

        # Car body
        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y, self.width, self.height)
        )

        # Front windshield
        pygame.draw.rect(
            screen,
            (20, 30, 40),
            (self.x + 8, self.y + 10, 34, 25)
        )

        # Front bumper
        pygame.draw.rect(
            screen,
            (255, 240, 240),
            (self.x + 8, self.y + 78, 34, 6)
        )

        # Nitro flame
        if nitro:
            pygame.draw.polygon(
                screen,
                (255, 150, 0),
                [
                    (self.x + 12, self.y + 90),
                    (self.x + 25, self.y + 115),
                    (self.x + 38, self.y + 90)
                ]
            )

            pygame.draw.polygon(
                screen,
                (255, 230, 50),
                [
                    (self.x + 18, self.y + 90),
                    (self.x + 25, self.y + 108),
                    (self.x + 32, self.y + 90)
                ]
            )

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )