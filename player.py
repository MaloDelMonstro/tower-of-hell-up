from constants import GRAVITY
from vector import Vector2

class Player:
    def __init__(self):
        self.center_x = 400.0
        self.center_y = 200.0
        self.width = 20
        self.height = 30
        self.velocity = Vector2.zero()
        self.jumps_used = 0
        self.max_jumps = 2
        self.on_ground = False

    @property
    def left(self): return self.center_x - self.width / 2
    @property
    def right(self): return self.center_x + self.width / 2
    @property
    def bottom(self): return self.center_y - self.height / 2
    @property
    def top(self): return self.center_y + self.height / 2

    def reset_jump(self):
        self.jumps_used = 0
        self.on_ground = True

    def can_jump(self):
        return self.jumps_used < self.max_jumps

    def update(self, platforms):
        self.center_x += self.velocity.x
        if self.left < 0:
            self.center_x = self.width / 2
        elif self.right > 800:
            self.center_x = 800 - self.width / 2

        self.velocity = Vector2(self.velocity.x, self.velocity.y - GRAVITY)
        self.center_y += self.velocity.y

        landed = False
        for platform in platforms:
            if (self.velocity.y < 0 and
                self.right > platform.left and
                self.left < platform.right and
                    self.bottom <= platform.top <= self.bottom - self.velocity.y):

                self.center_y = platform.top + self.height / 2
                self.velocity = Vector2(self.velocity.x, 0.0)
                self.reset_jump()
                landed = True
                break

        if not landed:
            self.on_ground = False