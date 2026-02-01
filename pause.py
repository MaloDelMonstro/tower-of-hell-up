import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, UI_COLOR
from game_engine import Game


class Pause(arcade.View):
    def __init__(self, game: 'Game') -> None:
        super().__init__()
        self._game = game
        self._selected = self._game._difficulty
        self._options = ["easy", "medium", "hard"]
        self._names = {"easy": "ЛЕГКО", "medium": "СРЕДНЕ", "hard": "СЛОЖНО"}

    def on_draw(self) -> None:
        self.clear((0, 0, 0, 200))
        arcade.draw_text("ПАУЗА", SCREEN_WIDTH//2, SCREEN_HEIGHT-100,
                         UI_COLOR, 36, anchor_x="center", font_name="Courier New")

        y = SCREEN_HEIGHT - 200
        for opt in self._options:
            color = UI_COLOR if opt == self._selected else (100, 200, 100)
            mark = "X" if opt == self._selected else " "
            arcade.draw_text(f"[{mark}] {self._names[opt]}", SCREEN_WIDTH // 2, y,
                             color, 24, anchor_x="center", font_name="Courier New")
            y -= 50

        arcade.draw_text("ENTER — ПРИМЕНИТЬ", SCREEN_WIDTH//2, 150,
                         (0, 200, 50), 20, anchor_x="center", font_name="Courier New")
        arcade.draw_text("ESC — ВЕРНУТЬСЯ", SCREEN_WIDTH//2, 100,
                         (0, 200, 50), 20, anchor_x="center", font_name="Courier New")

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.UP:
            idx = self._options.index(self._selected)
            self._selected = self._options[(idx - 1) % len(self._options)]
        elif key == arcade.key.DOWN:
            idx = self._options.index(self._selected)
            self._selected = self._options[(idx + 1) % len(self._options)]
        elif key == arcade.key.ENTER:
            self._game.set_difficulty(self._selected)
            self.window.show_view(self._game)
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self._game)