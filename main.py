import pygame
import random
import os

from player import Player
from enemy import Enemy
from coin import Coin, Booster
from sound import snd_coin, snd_crash, snd_start

pygame.init()


# ==========================================
# WINDOW

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

ROAD_WIDTH = 500
ROAD_X = (WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_X + ROAD_WIDTH
CENTER_X = WIDTH // 2

LANES = [
    ROAD_X + 45,
    ROAD_X + 160,
    ROAD_X + 285,
    ROAD_X + 405
]

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

def draw_heart(surface, x, y, size=18, color=RED):
    r = size // 4
    pygame.draw.circle(surface, color, (x + r, y + r), r)
    pygame.draw.circle(surface, color, (x + 3 * r, y + r), r)
    points = [
        (x, y + r),
        (x + 4 * r, y + r),
        (x + 2 * r, y + size)
    ]
    pygame.draw.polygon(surface, color, points)


# ==========================================
# PLAYER

player = Player(CENTER_X - 25, HEIGHT - 130, min_x=ROAD_X + 5, max_x=ROAD_RIGHT - 55)

# ==========================================
# HIGH SCORE SYSTEM
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, IOError):
            return 0
    return 0

def save_high_score(new_high):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(new_high))
    except IOError:
        pass

high_score = load_high_score()

# ==========================================
# GAME VARIABLES

selected_mode = "day"

score = 0
coins_collected = 0

lives = 3

level = 1

nitro = 100

enemies = []
coins = []
boosters = []

spawn_timer = 0
coin_timer = 0
booster_timer = 0

road_offset = 0
near_miss_message = 0
hit_cooldown = 0

game_started = False
game_over = False


# ==========================================
# RESET GAME

def reset_game():
    
    global high_score
    global score
    global coins_collected
    global lives
    global level
    global nitro
    global enemies
    global coins
    global boosters
    global spawn_timer
    global coin_timer
    global booster_timer
    global road_offset
    global game_started
    global game_over
    global hit_cooldown
    

    player.x = CENTER_X - 25
    player.y = HEIGHT - 130

    score = 0
    coins_collected = 0

    lives = 3

    level = 1

    nitro = 100

    enemies = []
    coins = []
    boosters = []
    booster_timer = 0
    player.has_shield = False
    player.boost_timer = 0
    player.magnet_timer = 0
    player.multiplier_timer = 0

    spawn_timer = 0
    coin_timer = 0

    road_offset = 0

    hit_cooldown = 0

    game_started = True
    game_over = False
    snd_start.play()


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

            if event.key == pygame.K_ESCAPE:
                running = False

            if not game_started:
                if event.key == pygame.K_d:
                    selected_mode = "day"
                elif event.key == pygame.K_n:
                    selected_mode = "night"

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

        mode_prompt = font.render(
            f"Mode: [D] Day  [N] Night (Current: {selected_mode.upper()})",
            True,
            YELLOW
        )

        controls = small_font.render(
            "LEFT / RIGHT = Drive     SPACE = Nitro   ESC = Quit",
            True,
            WHITE
        )

        screen.blit(
            title,
            title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        )

        screen.blit(
            subtitle,
            subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        )

        screen.blit(
            mode_prompt,
            mode_prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        )

        screen.blit(
            start,
            start.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90))
        )

        screen.blit(
            controls,
            controls.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))
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
                Enemy(enemy_speed, LANES)
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
                Coin(road_speed, LANES)
            )

            coin_timer = 0

        # ----------------------------------
        # MOVE COINS

        for coin in coins:
            coin.speed = road_speed
            coin.move()

            # magnet pulls coins from any lane toward player
            if player.magnet_timer > 0:
                if coin.x < player.x:
                    coin.x += 8
                elif coin.x > player.x:
                    coin.x -= 8
                if coin.y < player.y:
                    coin.y += 6

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
                snd_coin.play()
                coins.remove(coin)

                multiplier = 2 if player.multiplier_timer > 0 else 1
                coins_collected += 1 * multiplier
                score += 25 * multiplier

                nitro += 20

                if nitro > 100:

                    nitro = 100

        # BOOSTER SPAWNING & MOVEMENT
        booster_timer += dt
        if booster_timer >= 5000:  # Spawns every 5 seconds
            boosters.append(Booster(road_speed, LANES))
            booster_timer = 0

        for b in boosters[:]:
            b.speed = road_speed + (5 if player.boost_timer > 0 else 0)
            b.move()
            if b.y > HEIGHT:
                boosters.remove(b)

        # BOOSTER PICKUP
        for b in boosters[:]:
            if player_rect.colliderect(b.get_rect()):
                if b.kind == "shield":
                    player.has_shield = True
                elif b.kind == "jetpack":
                    player.boost_timer = 240       # 4 seconds
                elif b.kind == "magnet":
                    player.magnet_timer = 360      # 6 seconds
                elif b.kind == "star":
                    mult = 2 if player.multiplier_timer > 0 else 1
                    score += 150 * mult
                elif b.kind == "double":
                    player.multiplier_timer = 300  # 5 seconds
                boosters.remove(b)

        # ----------------------------------
        # COLLISION

        if hit_cooldown <= 0:

            for enemy in enemies:

                if player_rect.colliderect(
                    enemy.get_rect()
                ):
                    snd_crash.play()
                    if player.has_shield:
                        player.has_shield = False
                        hit_cooldown = 600
                        enemy.y = HEIGHT + 200
                        break
                    else:
                        lives -= 1
                        player.x = CENTER_X - 25
                        hit_cooldown = 1200
                        enemy.y = HEIGHT + 200
                        
                        if lives <= 0:
                           game_over = True
                           if score > high_score:
                             high_score = score
                             save_high_score(high_score)
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

    if selected_mode == "night":

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
        (ROAD_X, 0, ROAD_WIDTH, HEIGHT)
    )


    # Road borders

    pygame.draw.rect(
        screen,
        WHITE,
        (ROAD_X, 0, 5, HEIGHT)
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (ROAD_RIGHT - 5, 0, 5, HEIGHT)
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
                CENTER_X - 5,
                y + road_offset,
                10,
                40
            )
        )


    # ======================================
    # COINS

    for coin in coins:
        coin.draw(screen)
    for b in boosters : 
        b.draw(screen)

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

    lives_label = font.render(
        "Lives: ",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (25, 20)
    )

    screen.blit(
        coin_text,
        (25, 55)
    )

    screen.blit(
        lives_label,
        (25, 90)
    )

    for i in range(lives):
        draw_heart(screen, 25 + lives_label.get_width() + (i * 24), 93, size=18, color=RED)
        
    screen.blit(
        level_text,
        (WIDTH - level_text.get_width() - 25, 20)
    )
    # Active booster status indicators (Top Right)
    hud_y = 60
    if player.has_shield:
        screen.blit(small_font.render("SHIELD ACTIVE", True, (0, 220, 255)), (WIDTH - 180, hud_y))
        hud_y += 24
    if player.boost_timer > 0:
        screen.blit(small_font.render(f"JETPACK: {player.boost_timer // 60}s", True, (255, 160, 0)), (WIDTH - 180, hud_y))
        hud_y += 24
    if player.magnet_timer > 0:
        screen.blit(small_font.render(f"MAGNET: {player.magnet_timer // 60}s", True, (255, 80, 80)), (WIDTH - 180, hud_y))
        hud_y += 24
    if player.multiplier_timer > 0:
        screen.blit(small_font.render(f"2X MULTIPLIER: {player.multiplier_timer // 60}s", True, (210, 80, 255)), (WIDTH - 180, hud_y))



    # ======================================
    # NITRO BAR

    nitro_bar_x = WIDTH - 265
    nitro_bar_y = HEIGHT - 45

    pygame.draw.rect(
        screen,
        BLACK,
        (nitro_bar_x, nitro_bar_y, 240, 25)
    )

    pygame.draw.rect(
        screen,
        ORANGE,
        (
            nitro_bar_x + 5, 
            nitro_bar_y + 5, 
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
        (nitro_bar_x +50, nitro_bar_y - 25)
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
            near_text.get_rect(center=(WIDTH // 2, 140))
        )


    # ======================================
    # LEVEL MESSAGE

    if selected_mode == "night":

        night_text = small_font.render(
            "NIGHT MODE",
            True,
            (180, 200, 255)
        )

        screen.blit(
            night_text,
            (25, 140)
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
            game_over_text.get_rect(center=(WIDTH //2, HEIGHT //2 - 50))
        )

        screen.blit(
            final_score,
            final_score.get_rect(center=(WIDTH //2, HEIGHT //2 + 10))
        )

        screen.blit(
            restart,
            restart.get_rect(center=(WIDTH //2, HEIGHT //2 + 60))
        )


    # ======================================
    # UPDATE

    pygame.display.update()

    clock.tick(60)

pygame.quit() 