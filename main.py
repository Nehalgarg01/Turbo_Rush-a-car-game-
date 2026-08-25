import pygame
import random

from player import Player
from enemy import Enemy
from coin import Coin


pygame.init()


# ==========================================
# WINDOW

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Turbo Rush"
)

clock = pygame.time.Clock()


# ==========================================
# COLORS

GRASS = (40, 150, 40)
NIGHT_GRASS = (12, 55, 25)

ROAD = (55, 55, 55)
NIGHT_ROAD = (30, 30, 40)

WHITE = (255, 255, 255)
BLACK = (15, 15, 15)

YELLOW = (255, 210, 30)
ORANGE = (255, 130, 20)

RED = (220, 30, 30)


# ==========================================
# FONTS

font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 70)
small_font = pygame.font.Font(None, 24)


# ==========================================
# PLAYER

player = Player(375, 470)


# ==========================================
# GAME VARIABLES

score = 0
coins_collected = 0

lives = 3

level = 1

nitro = 100

enemies = []
coins = []


spawn_timer = 0
coin_timer = 0

road_offset = 0

near_miss_message = 0

hit_cooldown = 0


game_started = False
game_over = False


# ==========================================
# RESET GAME

def reset_game():

    global score
    global coins_collected
    global lives
    global level
    global nitro
    global enemies
    global coins
    global spawn_timer
    global coin_timer
    global road_offset
    global game_started
    global game_over
    global hit_cooldown

    player.x = 375

    score = 0
    coins_collected = 0

    lives = 3

    level = 1

    nitro = 100

    enemies = []
    coins = []

    spawn_timer = 0
    coin_timer = 0

    road_offset = 0

    hit_cooldown = 0

    game_started = True
    game_over = False


# ==========================================
# MAIN LOOP
# ==========================================

running = True

while running:

    dt = clock.get_time()


    # ======================================
    # EVENTS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:

                if not game_started:
                    reset_game()

            if event.key == pygame.K_r:

                if game_over:
                    reset_game()


    # ======================================
    # START SCREEN

    if not game_started:

        screen.fill(
            (15, 40, 20)
        )

        title = big_font.render(
            "TURBO RUSH",
            True,
            YELLOW
        )

        subtitle = font.render(
            "Ultimate Car Racing Challenge",
            True,
            WHITE
        )

        start = font.render(
            "Press ENTER to Start",
            True,
            WHITE
        )

        controls = small_font.render(
            "LEFT / RIGHT = Drive     SPACE = Nitro",
            True,
            WHITE
        )

        screen.blit(
            title,
            (250, 180)
        )

        screen.blit(
            subtitle,
            (245, 260)
        )

        screen.blit(
            start,
            (285, 340)
        )

        screen.blit(
            controls,
            (260, 390)
        )

        pygame.display.update()

        clock.tick(60)

        continue


    # ======================================
    # GAME LOGIC


    if not game_over:

        # ----------------------------------
        # LEVEL
    

        level = min(
            10,
            1 + score // 100
        )


        # ----------------------------------
        # SPEED

        enemy_speed = 5 + level * 0.7

        road_speed = 7 + level * 0.5


        # ----------------------------------
        # PLAYER

        player.move()


        # ----------------------------------
        # NITRO

        keys = pygame.key.get_pressed()

        using_nitro = False

        if keys[pygame.K_SPACE] and nitro > 0:

            using_nitro = True

            nitro -= 0.8

            road_speed += 6
            enemy_speed += 6

        else:

            if nitro < 100:

                nitro += 0.12


        # ----------------------------------
        # ROAD MOVEMENT

        road_offset += road_speed

        if road_offset >= 80:

            road_offset = 0


        # ----------------------------------
        # ENEMY SPAWNING

        spawn_timer += dt

        spawn_delay = max(
            400,
            900 - level * 45
        )

        if spawn_timer >= spawn_delay:

            enemies.append(
                Enemy(enemy_speed)
            )

            spawn_timer = 0


        # ----------------------------------
        # MOVE ENEMIES

        for enemy in enemies:

            enemy.speed = enemy_speed

            if using_nitro:
                enemy.speed = enemy_speed

            enemy.move()


        # ----------------------------------
        # REMOVE ENEMIES

        for enemy in enemies[:]:

            if enemy.y > HEIGHT:

                enemies.remove(enemy)

                score += 10


        # ----------------------------------
        # COIN SPAWNING

        coin_timer += dt

        if coin_timer >= 1200:

            coins.append(
                Coin(road_speed)
            )

            coin_timer = 0


        # ----------------------------------
        # MOVE COINS

        for coin in coins:

            coin.speed = road_speed

            coin.move()


        # ----------------------------------
        # REMOVE COINS
    

        for coin in coins[:]:

            if coin.y > HEIGHT:

                coins.remove(coin)


        # ----------------------------------
        # PLAYER RECT
    

        player_rect = player.get_rect()


        # ----------------------------------
        # COIN COLLECTION
    

        for coin in coins[:]:

            if player_rect.colliderect(
                coin.get_rect()
            ):

                coins.remove(coin)

                coins_collected += 1

                score += 25

                nitro += 20

                if nitro > 100:

                    nitro = 100


        # ----------------------------------
        # COLLISION

        if hit_cooldown <= 0:

            for enemy in enemies:

                if player_rect.colliderect(
                    enemy.get_rect()
                ):

                    lives -= 1

                    player.x = 375

                    hit_cooldown = 1200

                    enemy.y = HEIGHT + 200

                    if lives <= 0:

                        game_over = True

                    break


        else:

            hit_cooldown -= dt


        # ----------------------------------
        # NEAR MISS
        # ----------------------------------

        for enemy in enemies:

            if (
                enemy.y > player.y + player.height
                and not enemy.passed
            ):

                enemy.passed = True

                distance = abs(
                    enemy.x - player.x
                )

                if distance < 75:

                    score += 50

                    near_miss_message = 1000


        if near_miss_message > 0:

            near_miss_message -= dt


    # ======================================
    # DRAW BACKGROUND

    if level >= 5:

        grass_color = NIGHT_GRASS
        road_color = NIGHT_ROAD

    else:

        grass_color = GRASS
        road_color = ROAD


    screen.fill(
        grass_color
    )


    # ======================================
    # ROAD

    pygame.draw.rect(
        screen,
        road_color,
        (200, 0, 400, HEIGHT)
    )


    # Road borders

    pygame.draw.rect(
        screen,
        WHITE,
        (200, 0, 5, HEIGHT)
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (595, 0, 5, HEIGHT)
    )


    # ======================================
    # MOVING CENTER LINE

    for y in range(
        -80,
        HEIGHT,
        80
    ):

        pygame.draw.rect(
            screen,
            WHITE,
            (
                395,
                y + road_offset,
                10,
                40
            )
        )


    # ======================================
    # COINS

    for coin in coins:

        coin.draw(screen)


    # ======================================
    # ENEMY CARS

    for enemy in enemies:

        enemy.draw(screen)


    # ======================================
    # PLAYER CAR

    # Blink after collision

    if hit_cooldown <= 0 or (
        int(hit_cooldown / 100) % 2 == 0
    ):

        player.draw(
            screen,
            using_nitro
        )


    # ======================================
    # HUD

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    coin_text = font.render(
        f"Coins: {coins_collected}",
        True,
        YELLOW
    )

    level_text = font.render(
        f"LEVEL {level}",
        True,
        WHITE
    )

    lives_text = font.render(
        "Lives: " + "♥ " * lives,
        True,
        RED
    )


    screen.blit(
        score_text,
        (20, 20)
    )

    screen.blit(
        coin_text,
        (20, 55)
    )

    screen.blit(
        lives_text,
        (20, 90)
    )

    screen.blit(
        level_text,
        (680, 20)
    )


    # ======================================
    # NITRO BAR

    pygame.draw.rect(
        screen,
        BLACK,
        (530, 550, 240, 25)
    )

    pygame.draw.rect(
        screen,
        ORANGE,
        (
            535,
            555,
            int(nitro * 2.3),
            15
        )
    )

    nitro_text = small_font.render(
        "NITRO - SPACE",
        True,
        WHITE
    )

    screen.blit(
        nitro_text,
        (580, 525)
    )


    # ======================================
    # NEAR MISS

    if near_miss_message > 0:

        near_text = font.render(
            "NEAR MISS! +50",
            True,
            YELLOW
        )

        screen.blit(
            near_text,
            (290, 150)
        )


    # ======================================
    # LEVEL MESSAGE

    if level >= 5:

        night_text = small_font.render(
            "NIGHT MODE",
            True,
            (180, 200, 255)
        )

        screen.blit(
            night_text,
            (20, 125)
        )


    # ======================================
    # GAME OVER

    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(190)

        overlay.fill(BLACK)

        screen.blit(
            overlay,
            (0, 0)
        )


        game_over_text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        final_score = font.render(
            f"Final Score: {score}",
            True,
            WHITE
        )

        restart = font.render(
            "Press R to Restart",
            True,
            YELLOW
        )


        screen.blit(
            game_over_text,
            (265, 220)
        )

        screen.blit(
            final_score,
            (310, 300)
        )

        screen.blit(
            restart,
            (280, 350)
        )


    # ======================================
    # UPDATE

    pygame.display.update()

    clock.tick(60)

pygame.quit()