from vector import Vector2
import arcade

class Player:
    def __init__(self) -> None:
        self._center_x = 400.0
        self._center_y = 200.0
        self._width = 20
        self._height = 30
        self._velocity = Vector2.zero()
        self._jumps_used = 0
        self._max_jumps = 2
        self._on_ground = False
        self._move_left = False
        self._move_right = False

    @property
    def left(self) -> float:
        return self._center_x - self._width / 2
    @property
    def right(self) -> float:
        return self._center_x + self._width / 2
    @property
    def bottom(self) -> float:
        return self._center_y - self._height / 2
    @property
    def top(self) -> float:
        return self._center_y + self._height / 2

    def reset_jump(self) -> None:
        self._jumps_used = 0
        self._on_ground = True

    def can_jump(self) -> int:
        return self._jumps_used < self._max_jumps

    def update(self, platforms: arcade.SpriteList, gravity: float, jump_power: int) -> None:
        move_x = 0
        if self._move_left:
            move_x -= 5
        if self._move_right:
            move_x += 5
        self._center_x += move_x

        if self.left < 0:
            self._center_x = self._width / 2
        elif self.right > 800:
            self._center_x = 800 - self._width / 2

        self._velocity = Vector2(self._velocity.x, self._velocity.y - gravity)
        self._center_y += self._velocity.y

        landed = False
        for platform in platforms:
            if (self._velocity.y < 0 and
                self.right > platform.left and
                self.left < platform.right and
                    self.bottom <= platform.top <= self.bottom - self._velocity.y):

                self._center_y = platform.top + self._height / 2
                self._velocity = Vector2(self._velocity.x, 0.0)
                self.reset_jump()
                landed = True
                break

        if not landed:
            self._on_ground = False