from attrs import frozen


@frozen
class Vector2Int:
    x: int
    y: int

    @classmethod
    def zero(cls) -> "Vector2Int":
        return cls(0, 0)

    @classmethod
    def right(cls) -> "Vector2Int":
        return cls(1, 0)

    @classmethod
    def up(cls) -> "Vector2Int":
        return cls(0, 1)

    @classmethod
    def ones(cls) -> "Vector2Int":
        return cls(1, 1)

    @property
    def as_vector2(self) -> "Vector2":
        return Vector2(float(self.x), float(self.y))

    @property
    def inverse(self) -> "Vector2Int":
        return self * -1

    @property
    def length(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @property
    def tuple(self) -> tuple[int, int]:
        return self.x, self.y

    def scale_rounded(self, ratio: float) -> "Vector2Int":
        return Vector2Int.from_vector2(self.as_vector2 * ratio, strict=False)

    @classmethod
    def from_vector2(cls, v: "Vector2", strict: bool = True) -> "Vector2Int":
        if strict and (v.x != int(v.x) or v.y != int(v.y)):
            raise ValueError("Non-integer vector in strict mode")
        return cls(int(round(v.x)), int(round(v.y)))

    def with_x(self, x: int) -> "Vector2Int":
        return type(self)(x, self.y)

    def with_y(self, y: int) -> "Vector2Int":
        return type(self)(self.x, y)

    def __add__(self, other: "Vector2Int") -> "Vector2Int":
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2Int") -> "Vector2Int":
        return self + -other

    def __mul__(self, number: int) -> "Vector2Int":
        return type(self)(self.x * number, self.y * number)

    def __neg__(self) -> "Vector2Int":
        return self.inverse

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Vector2Int index out of range")


@frozen
class Vector2:
    x: float
    y: float

    @classmethod
    def zero(cls) -> "Vector2":
        return cls(0.0, 0.0)

    @classmethod
    def right(cls) -> "Vector2":
        return cls(1.0, 0.0)

    @classmethod
    def up(cls) -> "Vector2":
        return cls(0.0, 1.0)

    @classmethod
    def ones(cls) -> "Vector2":
        return cls(1.0, 1.0)

    @property
    def inverse(self) -> "Vector2":
        return self * -1.0

    @property
    def normalize(self) -> "Vector2":
        length = self.length
        if length == 0:
            return Vector2.zero()
        return self * (1.0 / length)

    @property
    def length(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @property
    def tuple(self) -> tuple[float, float]:
        return self.x, self.y

    @property
    def as_90(self) -> "Vector2":
        return type(self)(self.y, -self.x)

    def with_x(self, x: float) -> "Vector2":
        return type(self)(x, self.y)

    def with_y(self, y: float) -> "Vector2":
        return type(self)(self.x, y)

    def __add__(self, other: "Vector2") -> "Vector2":
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2") -> "Vector2":
        return self + -other

    def __mul__(self, number: float) -> "Vector2":
        return type(self)(self.x * number, self.y * number)

    def __neg__(self) -> "Vector2":
        return self.inverse

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Vector2 index out of range")