import builtins
from sys import exception
from typing import Any, Literal, Self, Type, overload
from math import sqrt, sin, cos, tan, asin, acos, atan2, radians, degrees

repeats = 1
def print(*a, **k):
    global repeats
    k['sep'] = k['sep'] if 'sep' in k else ' | '
    builtins.print(f'{repeats}.\t{a[0]}', *(a[1:]), **k)
    repeats += 1


class Vector:
    __slots__ = ('x', 'y', 'r', 'θ', 'type', 'k')

    def __init__(self, c=(0, 0), *, k=5):
        self.x = self.y = self.r = self.θ = None
        self.k = k
        if isinstance(c, tuple):
            self.x, self.y = c
        elif isinstance(c, list):
            self.r, self.θ = c
        elif isinstance(c, Vector) or issubclass(type(c), Vector):
            c._ensure_polar()
            self.r, self.θ = c.r, c.θ
        elif [a for a in c.__dir__() if 'vect' in a]:
            c = [c.__getattribute__(a) for a in c.__dir__() if 'vect' in a][0]
            c._ensure_polar()
            self.r, self.θ = c.r, c.θ
        else:
            raise TypeError(f'Coordinates of Vector must be tuple or list, not {type(c).__name__}.')


    def __repr__(self):
        parts = [f'{a} = {round(getattr(self, a), self.k)}'
                 for a in ('x', 'y', 'r', 'θ') if getattr(self, a) is not None]
        return f'Vector({"; ".join(parts)})'

    def _ensure_polar(self):
        if self.r is None:
            self.to_polar()

    def _ensure_coord(self):
        if self.x is None:
            self.to_coord()

    @staticmethod
    def _coerce(value):
        if isinstance(value, Vector):
            return value
        if isinstance(value, (int, float, complex)):
            z = complex(value)
            return Vector((z.real, z.imag))
        if isinstance(value, tuple):
            return Vector(value)
        return NotImplemented

    def to_polar(self):
        if self.r is not None:
            raise TypeError(f'This vector is already has polar coordinates.')
        if self.x == self.y == 0:
            self.r, self.θ = 0.0, 0.0
        else:
            self.r = sqrt(self.x ** 2 + self.y ** 2)
            self.θ = degrees(atan2(self.y, self.x))   # знак сохраняется
        self.x = self.y = None
        return self

    def to_coord(self):
        if self.x is not None:
            raise TypeError(f'This vector is already lies on the coordinate plane.')
        if self.r == 0:
            self.x = self.y = 0.0
        else:
            self.x = self.r * cos(radians(self.θ))
            self.y = self.r * sin(radians(self.θ))
        self.r = self.θ = None
        return self

    def to_im(self) -> complex:
        self._ensure_coord()
        return complex(round(self.x, self.k), round(self.y, self.k))

    def __float__(self) -> float:
        self._ensure_polar()
        return self.r

    def __int__(self) -> int:
        return round(float(self))

    def __mul__(self, other) -> 'Vector':
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        self._ensure_polar()
        other._ensure_polar()
        return Vector([self.r * other.r,
                  (self.θ + other.θ) % 360])

    __rmul__ = __mul__

    def __add__(self, other) -> 'Vector':
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        self._ensure_coord()
        other._ensure_coord()
        return Vector((self.x + other.x,
                  self.y + other.y))

    __radd__ = __add__

    def __pow__(self, n) -> 'Vector':
        result = self
        if not isinstance(n, (int, float)):
            raise TypeError(f'Argument can not be {type(n).__name__} type')
        if isinstance(n, float):
            z = int(n)
            a = n-z
            b = a*10-a
            c = round(9/b) # 1/c = a
            d = round(z*c+1) # d/c = n
            result = result ** d
            result._ensure_polar()
            result.θ /= c
            result.r **=a
            return result
        if n < 0:
            for _ in range(abs(n-1)):
                result = result * self
            return 1/result
        for _ in range(n-1):
            result = result * self
        return result

    def __truediv__(self, other) -> 'Vector':
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        self._ensure_polar()
        other._ensure_polar()
        return Vector([self.r / other.r,
                  (self.θ - other.θ) % 360])

    __rtruediv__ = __truediv__


if __name__ == '__main__':
    v = Vector((2, 3))
    print(v) # 1
    v.to_polar()
    print(v) # 2
    v = v*2
    print(v) # 3
    v = v+2
    print(v) # 4
    v = v.to_polar()
    print(v) # 5
    v = v**(1/7)#pow(v, 3)
    print(v) # 6
    h = v
    h = int(h)
    print(h) # 7
    h = v
    h = h.to_im()
    print(h) # 8
