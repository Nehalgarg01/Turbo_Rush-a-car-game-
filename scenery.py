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
        
        # Pre-seed persistent terrain patches (flowers, grass tufts)
        self.tufts = []
        for _ in range(50):
            side = random.choice(["left", "right"])
            if side == "left":
                tx = random.randint(10, max(20, self.road_x - 50))
            else:
                tx = random.randint(self.road_right + 50, self.width - 20)
            ty = random.randint(0, self.height)
            kind = random.choice(["flower_yellow", "flower_white", "grass_patch"])
            self.tufts.append({"x": tx, "y": ty, "kind": kind})

    def spawn_item(self, road_speed):
        side = random.choice(["left", "right"])
        item_type = random.choices(
            ["tree", "building", "bench", "person_walking", "person_standing", "lamp", "flower_bed"],
            weights=[32, 18, 12, 14, 10, 10, 14],
            k=1
        )[0]

        if side == "left":
            x_min = 25
            x_max = max(35, self.road_x - 75)
            sidewalk_x = self.road_x - 38
        else:
            x_min = self.road_right + 35
            x_max = max(self.road_right + 45, self.width - 85)
            sidewalk_x = self.road_right + 12

        x = random.randint(x_min, x_max)
        y = -140

        if item_type == "tree":
            self.items.append({
                "type": "tree",
                "x": x,
                "y": y,
                "speed": road_speed,
                "radius": random.randint(22, 32),
                "variant": random.choice(["oak", "pine"])
            })

        elif item_type == "building":
            w = random.randint(70, 110)
            h = random.randint(110, 160)
            color = random.choice([
                (75, 80, 92), (62, 68, 78), (88, 92, 102), (72, 70, 84), (80, 68, 65)
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

        elif item_type == "bench":
            has_person = random.choice([True, False])
            shirt_color = random.choice([(210, 70, 60), (45, 120, 210), (225, 175, 45), (200, 200, 200)])
            self.items.append({
                "type": "bench",
                "x": sidewalk_x,
                "y": y,
                "has_person": has_person,
                "shirt_color": shirt_color,
                "speed": road_speed
            })

        elif item_type == "person_walking" or item_type == "person_standing":
            shirt_color = random.choice([(225, 75, 75), (50, 150, 220), (235, 195, 55), (145, 80, 190), (45, 180, 120)])
            self.items.append({
                "type": "person",
                "sub": "walking" if item_type == "person_walking" else "standing",
                "x": sidewalk_x + random.randint(-4, 4),
                "y": y,
                "shirt": shirt_color,
                "speed": road_speed
            })

        elif item_type == "flower_bed":
            self.items.append({
                "type": "flower_bed",
                "x": x,
                "y": y,
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

    def update(self, dt, road_speed):
        self.spawn_timer += dt
        if self.spawn_timer >= 75:
            self.spawn_item(road_speed)
            self.spawn_timer = 0

        # Scroll persistent ground tufts
        for t in self.tufts:
            t["y"] += road_speed
            if t["y"] > self.height:
                t["y"] = -10

        # Scroll active scenery
        for item in self.items:
            item["y"] += road_speed

        self.items = [item for item in self.items if item["y"] < self.height + 170]

    def draw(self, surface, mode="day"):
        # 1. Road curb / Red & White Rumble Strips (Racetrack Highway Border)
        curb_h = 30
        for y_pos in range(-curb_h, self.height + curb_h, curb_h):
            idx = (y_pos // curb_h) % 2
            strip_color = (210, 45, 45) if idx == 0 else (235, 235, 240)
            if mode == "night":
                strip_color = (120, 25, 25) if idx == 0 else (110, 110, 120)
            
            # Left & Right rumble strips right against the asphalt
            pygame.draw.rect(surface, strip_color, (self.road_x - 10, y_pos, 10, curb_h))
            pygame.draw.rect(surface, strip_color, (self.road_right, y_pos, 10, curb_h))

        # 2. Paved Sidewalk Walkway (runs parallel to curbs)
        walk_c = (150, 152, 158) if mode == "day" else (50, 52, 58)
        walk_border = (120, 122, 128) if mode == "day" else (40, 42, 46)
        
        # Left Walkway
        pygame.draw.rect(surface, walk_c, (self.road_x - 42, 0, 32, self.height))
        pygame.draw.line(surface, walk_border, (self.road_x - 42, 0), (self.road_x - 42, self.height), 2)
        
        # Right Walkway
        pygame.draw.rect(surface, walk_c, (self.road_right + 10, 0, 32, self.height))
        pygame.draw.line(surface, walk_border, (self.road_right + 42, 0), (self.road_right + 42, self.height), 2)

        # 3. Draw wild meadow flowers & grass patches
        for t in self.tufts:
            if t["kind"] == "flower_yellow":
                col = (245, 215, 65) if mode == "day" else (120, 105, 30)
                pygame.draw.circle(surface, col, (t["x"], int(t["y"])), 3)
            elif t["kind"] == "flower_white":
                col = (240, 240, 245) if mode == "day" else (90, 90, 100)
                pygame.draw.circle(surface, col, (t["x"], int(t["y"])), 2)
            else:
                g_col = (60, 155, 75) if mode == "day" else (22, 52, 35)
                pygame.draw.line(surface, g_col, (t["x"], int(t["y"])), (t["x"] - 2, int(t["y"]) - 5), 2)
                pygame.draw.line(surface, g_col, (t["x"] + 2, int(t["y"])), (t["x"] + 3, int(t["y"]) - 6), 2)

        # 4. Scenery Objects
        for item in self.items:
            # BUILDINGS
            if item["type"] == "building":
                b_color = item["color"] if mode == "day" else (item["color"][0] // 2, item["color"][1] // 2, item["color"][2] // 2)
                pygame.draw.rect(surface, (20, 22, 25), (item["x"] + 4, item["y"] + 4, item["w"], item["h"]), border_radius=4)
                pygame.draw.rect(surface, b_color, (item["x"], item["y"], item["w"], item["h"]), border_radius=4)
                pygame.draw.rect(surface, (30, 32, 38), (item["x"], item["y"], item["w"], item["h"]), 2, border_radius=4)

                win_color = (255, 235, 130) if mode == "night" else (210, 230, 245)
                for r in range(item["x"] + 12, item["x"] + item["w"] - 14, 18):
                    for c in range(int(item["y"]) + 14, int(item["y"]) + item["h"] - 16, 22):
                        pygame.draw.rect(surface, win_color, (r, c, 9, 12), border_radius=1)

            # FLOWER BEDS
            elif item["type"] == "flower_bed":
                bed_dirt = (95, 60, 35) if mode == "day" else (45, 30, 20)
                pygame.draw.ellipse(surface, bed_dirt, (item["x"], item["y"], 34, 18))
                colors = [(240, 90, 90), (245, 215, 65), (255, 140, 200)] if mode == "day" else [(110, 40, 40), (105, 90, 30), (115, 60, 90)]
                for idx, c in enumerate(colors):
                    pygame.draw.circle(surface, c, (item["x"] + 8 + idx * 9, int(item["y"]) + 9), 3)

            # TREES
            elif item["type"] == "tree":
                trunk = (90, 52, 24) if mode == "day" else (40, 25, 14)
                c_light = (42, 155, 52) if mode == "day" else (16, 68, 24)
                c_dark = (30, 115, 38) if mode == "day" else (10, 46, 16)

                pygame.draw.ellipse(surface, (25, 30, 25), (item["x"] - item["radius"] + 2, item["y"] + 26, item["radius"] * 2, 10))
                pygame.draw.rect(surface, trunk, (item["x"] - 5, item["y"], 10, 32), border_radius=2)
                pygame.draw.circle(surface, c_dark, (item["x"], int(item["y"]) - 8), item["radius"] + 2)
                pygame.draw.circle(surface, c_light, (item["x"] - 4, int(item["y"]) - 12), item["radius"] - 1)

            # BENCHES
            elif item["type"] == "bench":
                wood = (140, 72, 24) if mode == "day" else (70, 36, 14)
                pygame.draw.rect(surface, wood, (item["x"], item["y"], 24, 12), border_radius=2)
                pygame.draw.rect(surface, (45, 45, 45), (item["x"], item["y"], 24, 12), 1, border_radius=2)
                if item["has_person"]:
                    skin = (245, 200, 160) if mode == "day" else (145, 115, 90)
                    pygame.draw.circle(surface, skin, (item["x"] + 12, int(item["y"]) - 2), 4)
                    pygame.draw.rect(surface, item["shirt_color"], (item["x"] + 8, item["y"] + 2, 8, 8), border_radius=2)

            # PEDESTRIANS
            elif item["type"] == "person":
                skin = (245, 200, 160) if mode == "day" else (145, 115, 90)
                pants = (45, 55, 75) if mode == "day" else (22, 26, 36)
                px, py = int(item["x"]), int(item["y"])

                pygame.draw.circle(surface, skin, (px, py), 4)
                pygame.draw.rect(surface, item["shirt"], (px - 4, py + 4, 8, 10), border_radius=2)
                if item["sub"] == "walking":
                    pygame.draw.line(surface, pants, (px - 2, py + 14), (px - 4, py + 22), 2)
                    pygame.draw.line(surface, pants, (px + 2, py + 14), (px + 4, py + 20), 2)
                else:
                    pygame.draw.line(surface, pants, (px - 2, py + 14), (px - 2, py + 22), 2)
                    pygame.draw.line(surface, pants, (px + 2, py + 14), (px + 2, py + 22), 2)

            # LAMPS
            elif item["type"] == "lamp":
                pole = (175, 180, 190) if mode == "day" else (65, 70, 75)
                pygame.draw.rect(surface, pole, (item["x"], item["y"], 4, 46))
                head_x = item["x"] + (7 if item["side"] == "left" else -7)
                pygame.draw.line(surface, pole, (item["x"] + 2, item["y"]), (head_x, item["y"]), 4)
                pygame.draw.circle(surface, (255, 230, 100), (head_x, item["y"] + 2), 4)

                if mode == "night":
                    glow = pygame.Surface((80, 80), pygame.SRCALPHA)
                    pygame.draw.circle(glow, (255, 235, 140, 45), (40, 40), 40)
                    surface.blit(glow, (head_x - 40, item["y"] - 15))