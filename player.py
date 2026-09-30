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

        self.has_shield = False
        self.boost_timer = 0
        self.magnet_timer = 0 
        self.multiplier_timer = 0

    def move(self):
        keys = pygame.key.get_pressed()
        curr_speed = self.speed * 1.5 if self.boost_timer > 0 else self.speed

        if keys[pygame.K_LEFT]:
            self.x -= curr_speed

        if keys[pygame.K_RIGHT]:
            self.x += curr_speed

        # Keep car on road
        if self.x < self.min_x:
            self.x = self.min_x

        if self.x > self.max_x:
            self.x = self.max_x

        # count down timers 
        if self.boost_timer > 0:
            self.boost_timer -= 1
        if self.magnet_timer > 0:
            self.magnet_timer -= 1
        if self.multiplier_timer > 0:
            self.multiplier_timer -= 1

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
        # Jetpack Thruster Trails
        if self.boost_timer > 0:
            pygame.draw.polygon(screen, (0, 220, 255), [(self.x + 5, self.y + 90), (self.x + 15, self.y + 125), (self.x + 22, self.y + 90)])
            pygame.draw.polygon(screen, (0, 220, 255), [(self.x + 28, self.y + 90), (self.x + 35, self.y + 125), (self.x + 45, self.y + 90)])

        # Magnet Attraction Ring
        if self.magnet_timer > 0:
            pygame.draw.circle(screen, (255, 60, 60), (self.x + self.width // 2, self.y + self.height // 2), 65, 2)

        # 2X Multiplier Purple Border
        if self.multiplier_timer > 0:
            pygame.draw.rect(screen, (190, 60, 255), (self.x - 3, self.y - 3, self.width + 6, self.height + 6), 2, border_radius=4)

        # Shield Bubble
        if self.has_shield:
            bubble = pygame.Surface((self.width + 24, self.height + 24), pygame.SRCALPHA)
            pygame.draw.ellipse(bubble, (0, 210, 255, 75), (0, 0, self.width + 24, self.height + 24))
            pygame.draw.ellipse(bubble, (200, 245, 255, 220), (0, 0, self.width + 24, self.height + 24), 3)
            screen.blit(bubble, (self.x - 12, self.y - 12))
            

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )