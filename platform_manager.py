import arcade
import random
from constants import (
    PLATFORM_WIDTH_MIN, PLATFORM_WIDTH_MAX,
    PLATFORM_SPACING_MIN, PLATFORM_SPACING_MAX,
    PLATFORM_COLOR, SCREEN_WIDTH
)

class PlatformManager:
    def __init__(self):
        self.platforms = arcade.SpriteList()

    def generate_initial_platforms(self):
        platform = arcade.SpriteSolidColor(SCREEN_WIDTH, 12, PLATFORM_COLOR)
        platform.center_x = SCREEN_WIDTH // 2
        platform.center_y = 150
        self.platforms.append(platform)

        y = 150 + random.randint(PLATFORM_SPACING_MIN, PLATFORM_SPACING_MAX)
        while y < 1100:
            self.add_random_platform(y)
            y += random.randint(PLATFORM_SPACING_MIN, PLATFORM_SPACING_MAX)

    def add_random_platform(self, y):
        width = random.randint(PLATFORM_WIDTH_MIN, PLATFORM_WIDTH_MAX)
        x = random.randint(width // 2, SCREEN_WIDTH - width // 2)
        platform = arcade.SpriteSolidColor(width, 12, PLATFORM_COLOR)
        platform.center_x, platform.center_y = x, y
        self.platforms.append(platform)

    def update(self, player_max_y, screen_height):
        last_platform = self.platforms[-1]
        while last_platform.center_y < player_max_y + screen_height + 300:
            spacing = random.randint(PLATFORM_SPACING_MIN, PLATFORM_SPACING_MAX)
            new_y = last_platform.center_y + spacing
            self.add_random_platform(new_y)
            last_platform = self.platforms[-1]

        cutoff = player_max_y - 800
        while self.platforms and self.platforms[0].center_y < cutoff:
            self.platforms.pop(0)