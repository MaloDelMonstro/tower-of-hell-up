import arcade
import random
from constants import (
    SCREEN_WIDTH,
    PLATFORM_WIDTH_MIN,
    PLATFORM_WIDTH_MAX,
    PLATFORM_SPACING_MIN,
    PLATFORM_SPACING_MAX,
    MAX_JUMP_HORIZONTAL,
    PLATFORM_COLOR
)

class PlatformManager:
    def __init__(self):
        self.platforms = arcade.SpriteList()

    def generate_initial_platforms(self):
        platform = arcade.SpriteSolidColor(SCREEN_WIDTH, 12, PLATFORM_COLOR)
        platform.center_x = SCREEN_WIDTH // 2
        platform.center_y = 150
        self.platforms.append(platform)

        self.add_next_platform(150, 200)

    def add_next_platform(self, reference_y, max_jump_height):
        vertical_gap = random.randint(
            PLATFORM_SPACING_MIN,
            min(PLATFORM_SPACING_MAX, max_jump_height)
        )
        new_y = reference_y + vertical_gap

        last_platform = self.platforms[-1]
        max_offset = min(MAX_JUMP_HORIZONTAL, SCREEN_WIDTH // 2 - PLATFORM_WIDTH_MIN // 2)
        horizontal_offset = random.randint(-max_offset, max_offset)
        new_x = last_platform.center_x + horizontal_offset

        min_x = PLATFORM_WIDTH_MIN // 2
        max_x = SCREEN_WIDTH - PLATFORM_WIDTH_MIN // 2
        new_x = max(min_x, min(max_x, new_x))

        width = random.randint(PLATFORM_WIDTH_MIN, PLATFORM_WIDTH_MAX)
        platform = arcade.SpriteSolidColor(width, 12, PLATFORM_COLOR)
        platform.center_x, platform.center_y = new_x, new_y
        self.platforms.append(platform)

    def update(self, player_max_y, screen_height, max_jump_height):
        while self.platforms[-1].center_y < player_max_y + screen_height + 300:
            self.add_next_platform(self.platforms[-1].center_y, max_jump_height)

        cutoff = player_max_y - 800
        while self.platforms and self.platforms[0].center_y < cutoff:
            self.platforms.pop(0)