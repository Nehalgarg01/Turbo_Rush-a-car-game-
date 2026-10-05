import pygame
import random

class SceneryManager:
    def __init__(self, width, height, road_x, road_right):
        self.width = width
        self.height = height
        self.road_x = road_x
        self.road_right = road_right
        
        self.items = []
        self.spawn_timer = 0

    def spawn_item(self, road_speed):
        side = random.choice(["left", "right"])
        # Added benches and pedestrians alongside trees, buildings, and lamps
        item_type = random.choices(
            ["tree", "building", "lamp", "bench", "person_walking", "person_standing"],
            weights=[30, 20, 15, 12, 13, 10],
            k=1
        )[0]

        # Define roadside boundary for objects
        if side == "left":
            x_min = 30
            x_max = max(40, self.road_x - 70)
            sidewalk_x = self.road_x - 30
        else:
            x_min = self.road_right + 30
            x_max = max(self.road_right + 40, self.width - 70)
            sidewalk_x = self.road_right + 15

        x = random.randint(x_min, x_max)
        y = -140

        if item_type == "tree":
            self.items.append({
                "type": "tree",
                "x": x,
                "y": y,
                "speed": road_speed,
                "radius": random.randint(20, 28)
            })

        elif item_type == "building":
            w = random.randint(65, 105)
            h = random.randint(100, 150)
            color = random.choice([
                (70, 75, 85), (55, 60, 70), (80, 85, 95), (60, 65, 80), (75, 65, 60)
            ])
            self.items.append({
                "type": "building",
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "color": color,
                "speed": road_speed
            })

        elif item_type == "lamp":
            lamp_x = self.road_x - 18 if side == "left" else self.road_right + 12
            self.items.append({
                "type": "lamp",
                "x": lamp_x,
                "y": y,
                "side": side,
                "speed": road_speed
            })

        elif item_type == "bench":
            # Bench placed along the roadside edge, sometimes with a person sitting
            has_person = random.choice([True, False])
            shirt_color = random.choice([(220, 60, 60), (50, 120, 220), (230, 180, 40), (220, 220, 220)])
            self.items.append({
                "type": "bench",
                "x": sidewalk_x,
                "y": y,
                "has_person": has_person,
                "shirt_color": shirt_color,
                "speed": road_speed
            })

        elif item_type == "person_walking":
            shirt_color = random.choice([(230, 70, 70), (40, 150, 230), (240, 200, 50), (160, 60, 200)])
            self.items.append({
                "type": "person",
                "sub": "walking",
                "x": sidewalk_x + random.randint(-5, 5),
                "y": y,
                "shirt": shirt_color,
                "speed": road_speed
            })

        elif item_type == "person_standing":
            shirt_color = random.choice([(46, 204, 113), (231, 76, 60), (241, 196, 15), (155, 89, 182)])
            self.items.append({
                "type": "person",
                "sub": "standing",
                "x": sidewalk_x + random.randint(-5, 5),
                "y": y,
                "shirt": shirt_color,
                "speed": road_speed
            })

    def update(self, dt, road_speed):
        self.spawn_timer += dt
        # Decreased spawn delay from 220 to 80 so objects are frequent and tightly packed
        if self.spawn_timer >= 80:
            self.spawn_item(road_speed)
            self.spawn_timer = 0

        # Scroll downward with road movement
        for item in self.items:
            item["y"] += road_speed

        # Remove objects once off the bottom
        self.items = [item for item in self.items if item["y"] < self.height + 160]

    def draw(self, surface, mode="day"):
        # Draw concrete sidewalks along both sides of the asphalt
        curb_color = (130, 130, 135) if mode == "day" else (50, 50, 55)
        walk_color = (165, 165, 170) if mode == "day" else (65, 65, 70)

        # Left sidewalk
        pygame.draw.rect(surface, walk_color, (self.road_x - 36, 0, 36, self.height))
        pygame.draw.rect(surface, curb_color, (self.road_x - 5, 0, 5, self.height))

        # Right sidewalk
        pygame.draw.rect(surface, walk_color, (self.road_right, 0, 36, self.height))
        pygame.draw.rect(surface, curb_color, (self.road_right, 0, 5, self.height))

        for item in self.items:
            # 1. BUILDINGS
            if item["type"] == "building":
                b_color = item["color"] if mode == "day" else (item["color"][0] // 2, item["color"][1] // 2, item["color"][2] // 2)
                pygame.draw.rect(surface, b_color, (item["x"], item["y"], item["w"], item["h"]), border_radius=3)
                pygame.draw.rect(surface, (20, 20, 25), (item["x"], item["y"], item["w"], item["h"]), 2, border_radius=3)

                win_color = (255, 235, 130) if mode == "night" else (220, 235, 250)
                for r in range(item["x"] + 10, item["x"] + item["w"] - 12, 16):
                    for c in range(int(item["y"]) + 12, int(item["y"]) + item["h"] - 14, 20):
                        pygame.draw.rect(surface, win_color, (r, c, 8, 10))

            # 2. TREES
            elif item["type"] == "tree":
                trunk_color = (90, 50, 20) if mode == "day" else (40, 25, 12)
                leaf_color = (34, 139, 34) if mode == "day" else (14, 65, 20)
                leaf_dark = (25, 110, 25) if mode == "day" else (10, 45, 15)

                pygame.draw.rect(surface, trunk_color, (item["x"] - 5, item["y"], 10, 35))
                pygame.draw.circle(surface, leaf_dark, (item["x"], int(item["y"]) - 8), item["radius"] + 2)
                pygame.draw.circle(surface, leaf_color, (item["x"] - 3, int(item["y"]) - 10), item["radius"])

            # 3. BENCHES (With optional seated person)
            elif item["type"] == "bench":
                wood_color = (139, 69, 19) if mode == "day" else (70, 35, 10)
                metal_color = (50, 50, 50)
                
                # Bench slats and frame
                pygame.draw.rect(surface, wood_color, (item["x"], item["y"], 24, 12), border_radius=2)
                pygame.draw.rect(surface, metal_color, (item["x"], item["y"], 24, 12), 1, border_radius=2)
                pygame.draw.line(surface, wood_color, (item["x"] + 2, item["y"] + 6), (item["x"] + 22, item["y"] + 6), 1)

                # Seated person on bench
                if item["has_person"]:
                    skin = (245, 200, 160) if mode == "day" else (150, 120, 95)
                    pygame.draw.circle(surface, skin, (item["x"] + 12, int(item["y"]) - 2), 4)  # head
                    pygame.draw.rect(surface, item["shirt_color"], (item["x"] + 8, item["y"] + 2, 8, 8), border_radius=2)  # body

            # 4. PEDESTRIANS (Walking or standing)
            elif item["type"] == "person":
                skin = (245, 200, 160) if mode == "day" else (150, 120, 95)
                pants = (40, 50, 70) if mode == "day" else (20, 25, 35)

                px, py = int(item["x"]), int(item["y"])

                # Head
                pygame.draw.circle(surface, skin, (px, py), 4)
                # Torso / Shirt
                pygame.draw.rect(surface, item["shirt"], (px - 4, py + 4, 8, 10), border_radius=2)
                # Legs
                if item["sub"] == "walking":
                    # Walking stride posture
                    pygame.draw.line(surface, pants, (px - 2, py + 14), (px - 4, py + 22), 2)
                    pygame.draw.line(surface, pants, (px + 2, py + 14), (px + 4, py + 20), 2)
                else:
                    # Standing straight
                    pygame.draw.line(surface, pants, (px - 2, py + 14), (px - 2, py + 22), 2)
                    pygame.draw.line(surface, pants, (px + 2, py + 14), (px + 2, py + 22), 2)

            # 5. STREET LAMPS
            elif item["type"] == "lamp":
                pole_color = (180, 180, 190) if mode == "day" else (70, 75, 80)
                pygame.draw.rect(surface, pole_color, (item["x"], item["y"], 5, 45))

                head_x = item["x"] + (7 if item["side"] == "left" else -7)
                pygame.draw.line(surface, pole_color, (item["x"] + 2, item["y"]), (head_x, item["y"]), 4)
                pygame.draw.circle(surface, (255, 230, 100), (head_x, item["y"] + 2), 4)

                if mode == "night":
                    glow = pygame.Surface((80, 80), pygame.SRCALPHA)
                    pygame.draw.circle(glow, (255, 235, 140, 45), (40, 40), 40)
                    surface.blit(glow, (head_x - 40, item["y"] - 15))