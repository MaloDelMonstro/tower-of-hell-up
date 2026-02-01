import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, BG_COLOR
from game_engine import Game

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    arcade.set_background_color(BG_COLOR)
    game_view = Game()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()