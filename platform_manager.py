import random
import arcade
from constants import (
    PLATFORM_WIDTH_MIN, PLATFORM_WIDTH_MAX,
    PLATFORM_SPACING_MIN, PLATFORM_SPACING_MAX,
    PLATFORM_COLOR, SCREEN_WIDTH
)
from vector import Vector2Int


class PlatformManager:
    def __init__(self):
        self.platforms = arcade.SpriteList()
        self.positions: list[Vector2Int] = []

    def generate_initial_platforms(self):
        self.add_full_width_platform(150)

        y = 150 + random.randint(PLATFORM_SPACING_MIN, PLATFORM_SPACING_MAX)
        while y < 1100:
            self.add_random_platform(y)
            y += random.randint(PLATFORM_SPACING_MIN, PLATFORM_SPACING_MAX)

    def add_full_width_platform(self, y: int):
        width = SCREEN_WIDTH
        x = SCREEN_WIDTH // 2
        pos = Vector2Int(x, y)
        self.positions.append(pos)

        platform = arcade.SpriteSolidColor(width, 12, PLATFORM_COLOR)
        platform.center_x, platform.center_y = float(pos.x), float(pos.y)
        self.platforms.append(platform)

    def add_random_platform(self, y: int):
        width = random.randint(PLATFORM_WIDTH_MIN, PLATFORM_WIDTH_MAX)
        x = random.randint(width // 2, SCREEN_WIDTH - width // 2)
        pos = Vector2Int(x, y)
        self.positions.append(pos)

        platform = arcade.SpriteSolidColor(width, 12, PLATFORM_COLOR)
        platform.center_x, platform.center_y = float(pos.x), float(pos.y)
        self.platforms.append(platform)

    def update(self, camera_bottom: float, screen_height: int):
        last_y = self.positions[-1].y
        while last_y < camera_bottom + screen_height + 300:
            spacing = random.randint(PLATFORM_SPACING_MIN, PLATFORM_SPACING_MAX)
            new_y = last_y + spacing
            self.add_random_platform(new_y)
            last_y = new_y

        while self.positions and self.positions[0].y < camera_bottom - 200:
            self.positions.pop(0)
            self.platforms.pop(0)