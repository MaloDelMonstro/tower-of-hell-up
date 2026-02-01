import arcade
from arcade.color import ARCADE_GREEN

from constants import GRAVITY, PLAYER_SPEED, PLAYER_JUMP
from vector import Vector2


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_circle_texture(50, (255, 255, 255, 255))
        self.center_x, self.center_y = 400.0, 200.0
        self.velocity = Vector2.zero()
        self.jumps_used = 0
        self.max_jumps = 2
        self.on_ground = True

    def reset_jump(self):
        self.jumps_used = 0
        self.on_ground = True

    def can_jump(self) -> bool:
        return self.jumps_used < self.max_jumps

    def update(self, platforms):
        self.center_x += self.velocity.x
        if self.left < 0:
            self.left = 0
        elif self.right > 800:
            self.right = 800

        self.velocity = Vector2(self.velocity.x, self.velocity.y - GRAVITY)
        self.center_y += self.velocity.y

        hit_list = arcade.check_for_collision_with_list(self, platforms)
        landed = False

        if hit_list:
            if self.velocity.y < 0:
                highest = max(hit_list, key=lambda p: p.top)
                if self.bottom < highest.top + 1:
                    self.bottom = highest.top
                    self.velocity = Vector2(self.velocity.x, 0.0)
                    self.reset_jump()
                    landed = True
            elif self.velocity.y > 0:
                lowest = min(hit_list, key=lambda p: p.bottom)
                self.top = lowest.bottom
                self.velocity = Vector2(self.velocity.x, 0.0)

        if not landed:
            self.on_ground = False

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        if self.texture is None:
            (arcade.draw_lbwh_rectangle_filled(
                self.center_x,
                self.center_y,
                30, 30,
                (255, 0, 0, 255)
            ))
