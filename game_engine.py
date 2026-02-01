import arcade
from arcade import camera
from constants import *
from player import Player
from platform_manager import PlatformManager
from utils import load_record, save_record


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.camera = camera.Camera2D()
        self.gui_camera = camera.Camera2D()
        self.record = load_record()
        self.scan_line_y = 0.0
        self.max_height = 0.0
        self.game_over = False

    def setup(self):
        self.game_over = False
        self.max_height = 0.0
        self.scan_line_y = 0.0

        self.player = Player()

        self.platform_manager = PlatformManager()
        self.platform_manager.generate_initial_platforms()

        self.camera.position = (400.0, 200.0)
        self.gui_camera.position = (400.0, 300.0)

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.player.update(self.platform_manager.platforms)

        if self.player.center_y > self.max_height:
            self.max_height = self.player.center_y
            current_m = int(self.max_height / METER_SCALE)
            if current_m > self.record:
                self.record = current_m
                save_record(self.record)

        cam_bottom = self.camera.bottom
        self.platform_manager.update(cam_bottom, SCREEN_HEIGHT)

        target = (self.player.center_x, self.player.center_y)
        curr = self.camera.position
        smoothed = (
            curr[0] + (target[0] - curr[0]) * 0.1,
            curr[1] + (target[1] - curr[1]) * 0.1
        )
        self.camera.position = smoothed

        if self.player.center_y < self.max_height - 900:
            self.game_over = True

        self.scan_line_y = (self.scan_line_y + 150 * delta_time) % (SCREEN_HEIGHT * 2)

    def on_draw(self):
        self.clear()

        self.camera.use()
        self.platform_manager.platforms.draw()
        self.player.draw()

        self.gui_camera.use()

        scan_y = self.scan_line_y - SCREEN_HEIGHT
        arcade.draw_lrbt_rectangle_filled(
            left=0,
            right=SCREEN_WIDTH,
            bottom=scan_y - 1,
            top=scan_y + 1,
            color=(0, 100, 0, 80)
        )

        height_m = int(self.max_height / METER_SCALE)
        arcade.draw_text(f"{height_m:05d} М", 20, SCREEN_HEIGHT - 40,
                         UI_COLOR, 24, font_name="Courier New", bold=True)
        arcade.draw_text(f"РЕКОРД: {self.record:05d} М", 20, SCREEN_HEIGHT - 70,
                         (0, 200, 50), 16, font_name="Courier New")

        if self.game_over:
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                (0, 0, 0, 200)
            )
            arcade.draw_text("СИСТЕМА ОСТАНОВЛЕНА", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30,
                             UI_COLOR, 28, anchor_x="center", font_name="Courier New", bold=True)
            arcade.draw_text("R — ПЕРЕЗАПУСК", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20,
                             (0, 200, 50), 18, anchor_x="center", font_name="Courier New")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.velocity = self.player.velocity.with_x(-PLAYER_SPEED)
        elif key == arcade.key.RIGHT:
            self.player.velocity = self.player.velocity.with_x(PLAYER_SPEED)
        elif key == arcade.key.SPACE and self.player.can_jump():
            self.player.velocity = self.player.velocity.with_y(PLAYER_JUMP)
            self.player.jumps_used += 1
        elif key == arcade.key.R:
            self.setup()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.velocity = self.player.velocity.with_x(0)