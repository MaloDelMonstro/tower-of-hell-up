import arcade
from arcade import camera
from constants import *
from player import Player
from platform_manager import PlatformManager
from utils import load_record, save_record
from vector import Vector2


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.camera = camera.Camera2D()
        self.gui_camera = camera.Camera2D()

    def setup(self):
        self.game_over = False
        self.max_height = 0.0
        self.scan_line_y = 0.0

        self.player = Player()

        self.platform_manager = PlatformManager()
        self.platform_manager.generate_initial_platforms()

        self.camera.position = (400.0, 200.0)
        self.gui_camera.position = (400.0, 300.0)

        self.record = load_record()

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

        self.platform_manager.update(self.max_height, SCREEN_HEIGHT)

        curr_x, curr_y = self.camera.position
        target_x = self.player.center_x
        target_y = self.player.center_y
        smoothed_x = curr_x + (target_x - curr_x) * 0.1
        smoothed_y = curr_y + (target_y - curr_y) * 0.1
        self.camera.position = (smoothed_x, smoothed_y)

        if self.player.center_y < self.max_height - 900:
            self.game_over = True

        self.scan_line_y = (self.scan_line_y + 150 * delta_time) % (SCREEN_HEIGHT * 2)

    def on_draw(self):
        self.clear()

        self.camera.use()
        self.platform_manager.platforms.draw()

        p = self.player

        body_l = p.center_x - p.width / 2
        body_r = p.center_x + p.width / 2
        body_b = p.center_y - p.height / 2
        body_t = p.center_y + p.height / 2
        arcade.draw_lrbt_rectangle_filled(body_l, body_r, body_b, body_t, (255, 0, 0, 255))

        head_size = 12
        head_b = body_t
        head_t = head_b + head_size
        head_l = p.center_x - head_size / 2
        head_r = p.center_x + head_size / 2
        arcade.draw_lrbt_rectangle_filled(head_l, head_r, head_b, head_t, (255, 50, 50, 255))

        self.gui_camera.use()

        scan_y = self.scan_line_y - SCREEN_HEIGHT
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH,
            scan_y - 1, scan_y + 1,
            (0, 100, 0, 80)
        )

        height_m = int(self.max_height / METER_SCALE)
        arcade.draw_text(f"{height_m:05d} М", 20, SCREEN_HEIGHT - 40,
                         UI_COLOR, 24, font_name="Courier New", bold=True)
        arcade.draw_text(f"РЕКОРД: {self.record:05d} М", 20, SCREEN_HEIGHT - 70,
                         (0, 200, 50), 16, font_name="Courier New")

        if self.game_over:
            arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, (0, 0, 0, 200))
            arcade.draw_text("СИСТЕМА ОСТАНОВЛЕНА", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30,
                             UI_COLOR, 28, anchor_x="center", font_name="Courier New", bold=True)
            arcade.draw_text("R — ПЕРЕЗАПУСК", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20,
                             (0, 200, 50), 18, anchor_x="center", font_name="Courier New")

    def on_key_press(self, key, modifiers):
        if self.game_over:
            if key == arcade.key.R:
                self.setup()
            return

        if key == arcade.key.LEFT:
            self.player.velocity = Vector2(self.player.velocity.x - PLAYER_SPEED, self.player.velocity.y)
        elif key == arcade.key.RIGHT:
            self.player.velocity = Vector2(self.player.velocity.x + PLAYER_SPEED, self.player.velocity.y)
        elif key == arcade.key.SPACE and self.player.can_jump():
            self.player.velocity = Vector2(self.player.velocity.x, PLAYER_JUMP)
            self.player.jumps_used += 1
        elif key == arcade.key.R:
            self.setup()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.velocity = Vector2(0, self.player.velocity.y)