import math
from typing import Self
import operator
from my_lib.Python.new import *
from my_lib.Python.new.Vectors import *
import matplotlib.pyplot as plt


class Base:
    _value: float
    dimension: dict

    def __init__(self, value, model: 'Model' = None):
        self._value, self.Model = value, model if model is not None else Model()
        self.__name__ = type(self).__name__

    def __add__(self, value):
        if isinstance(value, (int, float)):
            return type(self)(self._value + value)
        if not isinstance(value, type(self)):
            return NotImplemented
        return type(self)(self._value + value._value)
    __radd__ = __add__

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return type(self)(self._value * value)
        if not isinstance(value, type(self)):
            return NotImplemented
        return type(self)(self._value * value._value)
    __rmul__ = __mul__

    def __repr__(self) -> str:
        if self._value is None:
            return f'None {self.dimension[self.Model.lang]}'
        return f'{round(self._value, self.Model.k)} {self.dimension[self.Model.lang]}'

    def copy(self):
        return type(self)(self._value)


class Energy(Base):
    dimension = {'ru': 'Дж', 'en': 'J'}


class Warmth(Energy):
    ...


class Temperature(Base):
    dimension = {'ru': '°С', 'en': '°F'}

    def __abs__(self) -> float:
        value = self._value
        if self.Model.lang == 'en':
            value = (value - 32) / 1.8
        return value + 273.15

    def __repr__(self) -> str:
        return f'{round(self._value, self.Model.k)} {self.dimension[self.Model.lang]}'


class Mass(Base):
    dimension = {'ru': 'кг', 'en': 'kg'}


class Volume(Base):
    dimension = {'ru': 'м³', 'en': 'm³'}


class Density(Base):
    dimension = {'ru': 'кг/м³', 'en': 'kg/m³'}


class Specific_Heat(Base):
    dimension = {'ru': 'Дж/(кг*°С)', 'en': 'J/(kg*°F)'}


class Time(Base):
    dimension = {'ru': 'с', 'en': 's'}


class Velocity:
    dimension = {'ru': 'м/с', 'en': 'm/s'}

    def __init__(self, value=[0, 0], model: 'Model' = None):
        self.Model = model if model is not None else Model()
        self._vector = Vector(value)
        self.__name__ = type(self).__name__

    @property
    def x(self): return self._vector.x
    @property
    def y(self): return self._vector.y

    @property
    def _value(self):
        self._vector._ensure_polar()
        return self._vector.r if self._vector.r else None

    def __add__(self, value):
        if isinstance(value, Velocity):
            self._vector += value._vector
            return self
        if isinstance(value, Vector):
            self._vector += value
            return self
        return NotImplemented
    __radd__ = __add__

    def __mul__(self, value):
        if isinstance(value, Velocity):
            self._vector *= value._vector
            return self
        if isinstance(value, Vector):
            self._vector *= value
            return self
        if isinstance(value, Time):
            return float(self._vector * value._value)
        return NotImplemented
    __rmul__ = __mul__

    def __repr__(self) -> str:
        self._vector._ensure_polar()
        return f'{round(self._value, self.Model.k) if self._value else self._value} {self.dimension[self.Model.lang]}'

    def copy(self):
        self._vector._ensure_polar()
        return Velocity([self._vector.r, self._vector.θ])


class Acceleration(Velocity):
    dimension = {'ru': 'м/с²', 'en': 'm/s²'}

    def __mul__(self, other) -> Self:
        if isinstance(other, Time):
            c = self._vector
            c._ensure_polar()
            return Velocity([c.r*other._value, c.θ])
        elif isinstance(other, (int, float)):
            self._vector *= other
            return self

class Force(Velocity):
    dimension = {'ru': 'Н', 'en': 'N'}

    def __truediv__(self, _value):
        if isinstance(_value, Mass):
            self._vector._ensure_polar()
            return Acceleration([self._vector.r / _value._value, self._vector.θ])
        elif isinstance(_value, (int, float)) or isinstance(_value, Vector) or issubclass(type(_value), Vector):
            _value = Vector()._coerce(_value)
            self._vector._ensure_polar()
            self._vector.r /= _value
            return self

class Импульс(Velocity):
    dimension = {'ru': 'Н', 'en': 'N'}

    def __truediv__(self, _value):
        if isinstance(_value, Mass):
            self._vector._ensure_polar()
            return Velocity([self._vector.r / _value._value, self._vector.θ])
        elif isinstance(_value, (int, float)) or isinstance(_value, Vector) or issubclass(type(_value), Vector):
            _value = Vector()._coerce(_value)
            self._vector._ensure_polar()
            self._vector.r /= _value
            return self


@singleton
class Model:
    k, lang, g, ground, play, speed, ρ = 5, 'ru', Acceleration(
        [9.81, -90], Self), 0, False, 1, Density(1.204, Self)
    a = ('k', 'lang', 'g', 'ground', 'play', 'speed', 'ρ')

    def __init__(self, **kwargs):
        self.k = kwargs.get('k', 5)
        self.g = Acceleration([kwargs.get('g', 9.81), -90], self)
        self.speed = kwargs.get('speed', 1)
        self.lang = kwargs.get('lang', 'ru')
        self.ground = kwargs.get('ground', 0)
        self.play = kwargs.get('play', False)
        self.ρ = Density(kwargs.get('ρ', 1.204), self)

    def __repr__(self) -> str:
        parts = []
        for a in self.a:
            value = getattr(self, a)
            if value is None or 'None' in str(value):
                continue
            parts.append(f'{a} = {value}')
        return f'{type(self).__name__}({"; ".join(parts)})'


class Body:
    m: Mass
    ρ: Density
    V: Volume
    Vel: Velocity
    temp: Temperature
    C: Specific_Heat
    coordinates: Vector
    a: Acceleration
    p: Импульс
    __el__ = ('m', 'ρ', 'V', 'temp', 'C', 'Vel', 'coordinates', 'a', 'p')

    def __init__(self, model: Model = None, *args, **kwargs):
        self.Model = model if model is not None else Model()
        self.m: Mass = Mass(kwargs.get('m', 1))
        self.ρ: Density = Density(kwargs.get('ρ'))
        self.V: Volume = Volume(kwargs.get('V'))
        self.Vel: Velocity = Velocity(kwargs.get('Vel', [0, 0]))
        self.temp: Temperature = Temperature(kwargs.get('temp', 20))
        self.C: Specific_Heat = Specific_Heat(kwargs.get('C'))
        self.coordinates = Vector(kwargs.get('coordinates', (0, 0)))
        self.a: Acceleration = Acceleration(kwargs.get('a', [0, 0]))
        self.p: Импульс = Импульс(kwargs.get('p', [0, 0]))
        self.__name__ = type(self).__name__

    def move(self, to=None, around=None):
        if isinstance(to, tuple):
            self.coordinates = Vector(to)
        if isinstance(around, (tuple, Vector)):
            self.coordinates += around
        return

    def __repr__(self) -> str:
        parts = []
        for a in self.__el__:
            value = getattr(self, a)
            if not value or 'None' in str(value):
                continue
            parts.append(f'{a} = {value}')
        return f'{self.__name__}({"; ".join(parts)})'

    @property
    def E_п(self) -> Energy:
        c = self.coordinates
        c._ensure_coord()
        return Energy(self.Model.g._value * abs(c.y - self.Model.ground) * self.m._value)

    def __add__(self, _value):
        if isinstance(_value, Warmth):
            if self.C._value is None or not self.m._value:
                raise ValueError(
                    'Необходимы масса и теплоёмкость, чтобы добавить тепло')
            self.temp = self.temp + Temperature(
                _value._value / (self.m._value * self.C._value))
        elif isinstance(_value, Mass):
            self.m = self.m + _value
        elif isinstance(_value, Force):
            self.a = self.a + (_value/self.m)
        else:
            return NotImplemented
        return self
    __radd__ = __add__

    @property
    def U(self) -> Energy:
        t = self.temp._value
        if self.Model.lang == 'en':
            t = (t - 32) / 1.8
        return Energy(self.m._value * self.C._value * t)

    def time(self, time=Time(1.0)):
        value = time if isinstance(time, Time) else Time(value)
        self.Vel._vector._ensure_coord()
        self.coordinates._ensure_coord()
        self.coordinates.x = self.coordinates.x + \
            (self.Vel._vector.x*value)._value
        self.coordinates.y = self.coordinates.y + \
            (self.Vel._vector.y*value)._value - ((self.a+self.Model.g)*value*value)/2
        self.Vel += self.Model.g*value
        if self.Model.play:
            sleep(time._value/self.Model.speed)

    def copy(self):
        kw = {}
        for e in self.__el__:
            kw[e] = getattr(self, e)
        return type(self)(**kw, model=self.Model)


def inter(x, y, z, w, step=1, start=-10, stop=10, finish: int = None):
    '''x.w при x.y(z(n)) где start < n < stop, но x.w > finish'''
    ns = [stop]
    while start < stop:
        ns.insert(1, start)
        start += step
    ns.sort()
    rs = []

    for n in ns:
        original = x.copy()
        getattr(original, y)(z(n))
        attrs = w.split('.')
        value = original
        for attr in attrs:
            value = getattr(value, attr)

        rs.append(value)

        if finish is not None and value <= finish:
            ns = ns[:len(rs)]
            break
    if finish is not None:
        return (ns, rs), n
    return (ns, rs)


def saw(x, y: str, z, w: str | tuple[str], step=1, start=-10, stop=10):
    if isinstance(w, str):
        w = (w, )
    for kw in w:
        data = inter(x, y, z, kw, step, start, stop)
        plt.plot(*data)
        # print(data[0])


m = Model(lang='ru')
sphere = Body(ρ=7850, C=500)

print(sphere)					# 1
sphere.move(around=(5, 5))
print(sphere)					# 2
print(sphere.E_п)				# 3
sphere = sphere + Mass(5)
print(sphere)					# 4
Q = Warmth(10e-3 * 2.7e7)
print(Q)						# 5
sphere += Q
print(sphere)					# 6
print(sphere.U)					# 7
launch = Velocity([2500/3.6, 30])
print(launch)					# 8
sphere.Vel = launch
print(sphere)					# 9
F = Force([50, 90])
print(F)						# 10
sphere += F
print(sphere)					# 11

msp = 1000
mst = 0
ms = 0.05
c = 6

for i in [90/c*n for n in range(c+1)]:
    sphere.Vel = Velocity([2500/3.6, i])
    y = inter(sphere, 'time', Time, 'coordinates.y', start=mst, stop=msp, step=ms, finish=0)
    x = inter(sphere, 'time', Time, 'coordinates.x', start=mst, stop=y[1], step=ms)
    plt.plot(x[1], y[0][1])
plt.show()


time = Time(1)
print(time)						# 12
sphere.time(time)
print(sphere)					# 13
