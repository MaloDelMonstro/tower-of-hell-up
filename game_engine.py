import arcade
from arcade import camera
from constants import *
from player import Player
from platform_manager import PlatformManager
from utils import load_record, save_record
from pause import Pause
from vector import Vector2


class Game(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self._camera = camera.Camera2D()
        self._gui_camera = camera.Camera2D()
        self._difficulty = DEFAULT_DIFFICULTY
        self._current_gravity = DIFFICULTY_SETTINGS[DEFAULT_DIFFICULTY][0]
        self._current_jump = DIFFICULTY_SETTINGS[DEFAULT_DIFFICULTY][1]
        self._current_max_jump_height = DIFFICULTY_SETTINGS[DEFAULT_DIFFICULTY][2]

    def set_difficulty(self, difficulty: str) -> None:
        self._difficulty = difficulty
        self._current_gravity, self._current_jump, self._current_max_jump_height = DIFFICULTY_SETTINGS[difficulty]
        self._platform_manager = PlatformManager()
        self._platform_manager.generate_initial_platforms()

    def setup(self) -> None:
        self._game_over = False
        self._max_height = 0.0
        self._scan_line_y = 0.0
        self._player = Player()
        self._platform_manager = PlatformManager()
        self._platform_manager.generate_initial_platforms()
        self._camera.position = (400.0, 200.0)
        self._gui_camera.position = (400.0, 300.0)
        self._record = load_record()

    def on_update(self, delta_time: float) -> None:
        if self._game_over:
            return

        self._player.update(
            platforms=self._platform_manager._platforms,
            gravity=self._current_gravity,
            jump_power=self._current_jump
        )

        if self._player._center_y > self._max_height:
            self._max_height = self._player._center_y
            current_m = int(self._max_height / METER_SCALE)
            if current_m > self._record:
                self._record = current_m
                save_record(self._record)

        self._platform_manager.update(
            self._max_height,
            SCREEN_HEIGHT,
            self._current_max_jump_height
        )

        curr_x, curr_y = self._camera.position
        target_x = self._player._center_x
        target_y = self._player._center_y
        smoothed_x = curr_x + (target_x - curr_x) * 0.1
        smoothed_y = curr_y + (target_y - curr_y) * 0.1
        self._camera.position = (smoothed_x, smoothed_y)

        if self._player._center_y < self._max_height - 900:
            self._game_over = True

        self._scan_line_y = (self._scan_line_y + 150 * delta_time) % (SCREEN_HEIGHT * 2)

    def on_draw(self) -> None:
        self.clear()

        self._camera.use()
        self._platform_manager._platforms.draw()

        p = self._player
        body_l = p._center_x - p._width / 2
        body_r = p._center_x + p._width / 2
        body_b = p._center_y - p._height / 2
        body_t = p._center_y + p._height / 2
        arcade.draw_lrbt_rectangle_filled(body_l, body_r, body_b, body_t, (255, 0, 0, 255))

        head_size = 12
        head_b = body_t
        head_t = head_b + head_size
        head_l = p._center_x - head_size / 2
        head_r = p._center_x + head_size / 2
        arcade.draw_lrbt_rectangle_filled(head_l, head_r, head_b, head_t, (255, 50, 50, 255))

        self._gui_camera.use()

        scan_y = self._scan_line_y - SCREEN_HEIGHT
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, scan_y - 1, scan_y + 1, (0, 100, 0, 80))

        height_m = int(self._max_height / METER_SCALE)
        arcade.draw_text(f"{height_m:05d} М", 20, SCREEN_HEIGHT - 40,
                         UI_COLOR, 24, font_name="Courier New", bold=True)
        arcade.draw_text(f"РЕКОРД: {self._record:05d} М", 20, SCREEN_HEIGHT - 70,
                         (0, 200, 50), 16, font_name="Courier New")

        if self._game_over:
            arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, (0, 0, 0, 200))
            arcade.draw_text("СИСТЕМА ОСТАНОВЛЕНА", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30,
                             UI_COLOR, 28, anchor_x="center", font_name="Courier New", bold=True)
            arcade.draw_text("R — ПЕРЕЗАПУСК", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20,
                             (0, 200, 50), 18, anchor_x="center", font_name="Courier New")

    def on_key_press(self, key: int, modifiers: int) -> None:
        if self._game_over:
            if key == arcade.key.R:
                self.setup()
            return

        if key == arcade.key.LEFT or key == arcade.key.A:
            self._player._move_left = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self._player._move_right = True
        elif (key == arcade.key.SPACE and self._player.can_jump()) or (key == arcade.key.W and self._player.can_jump()):
            self._player._velocity = Vector2(self._player._velocity.x, self._current_jump)
            self._player._jumps_used += 1
        elif key == arcade.key.R:
            self.setup()
        elif key == arcade.key.ESCAPE:
            pause = Pause(self)
            self.window.show_view(pause)

    def on_key_release(self, key: int, modifiers: int) -> None:
        if key == arcade.key.LEFT or key == arcade.key.A:
            self._player._move_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self._player._move_right = False