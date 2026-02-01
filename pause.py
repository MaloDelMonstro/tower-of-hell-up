import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, UI_COLOR

class Pause(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.selected = self.game_view.difficulty
        self.options = ["easy", "medium", "hard"]
        self.names = {"easy": "ЛЕГКО", "medium": "СРЕДНЕ", "hard": "СЛОЖНО"}

    def on_draw(self):
        self.clear((0, 0, 0, 200))
        arcade.draw_text("ПАУЗА", SCREEN_WIDTH//2, SCREEN_HEIGHT-100,
                         UI_COLOR, 36, anchor_x="center", font_name="Courier New")

        y = SCREEN_HEIGHT - 200
        for opt in self.options:
            color = UI_COLOR if opt == self.selected else (100, 200, 100)
            mark = "X" if opt == self.selected else " "
            arcade.draw_text(f"[{mark}] {self.names[opt]}", SCREEN_WIDTH//2, y,
                             color, 24, anchor_x="center", font_name="Courier New")
            y -= 50

        arcade.draw_text("ENTER — ПРИМЕНИТЬ", SCREEN_WIDTH//2, 150,
                         (0, 200, 50), 20, anchor_x="center", font_name="Courier New")
        arcade.draw_text("ESC — ВЕРНУТЬСЯ", SCREEN_WIDTH//2, 100,
                         (0, 200, 50), 20, anchor_x="center", font_name="Courier New")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            idx = self.options.index(self.selected)
            self.selected = self.options[(idx - 1) % len(self.options)]
        elif key == arcade.key.DOWN:
            idx = self.options.index(self.selected)
            self.selected = self.options[(idx + 1) % len(self.options)]
        elif key == arcade.key.ENTER:
            self.game_view.set_difficulty(self.selected)
            self.window.show_view(self.game_view)
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)