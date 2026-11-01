import math
from math import sqrt, sin, cos, atan2, radians, degrees, pi

from my_lib.Python.new import *
from my_lib.Python.new.Vectors import *
import matplotlib.pyplot as plt

materials = {
    'aqua': {'ρ': 1000, 'C': 4200},
    'steel': {'ρ': 7850, 'C': 500},
}
fuel = {
    'gas': 2.7e7,
}

def _copy_vector(v: Vector) -> Vector:
    if v.x is not None:
        return Vector((v.x, v.y))
    if v.r is not None:
        return Vector([v.r, v.θ if v.θ is not None else 0.0])
    return Vector((0.0, 0.0))


# ─────────────────────────────── скалярные величины ───────────────────────────────

class Base:
    _value: float
    dimension: dict
    format = 'number'

    def __init__(self, value, model: 'Model' = None):
        self._value, self.Model = value, model if model is not None else Model()
        self.__name__ = type(self).__name__

    def __add__(self, value):
        if isinstance(value, (int, float)):
            return type(self)(self._value + value)
        if isinstance(value, type(self)):
            return type(self)(self._value + value._value)
        return NotImplemented
    __radd__ = __add__

    def __sub__(self, value):
        if isinstance(value, (int, float)):
            return type(self)(self._value - value)
        if isinstance(value, type(self)):
            return type(self)(self._value - value._value)
        return NotImplemented

    def __rsub__(self, value):
        if isinstance(value, (int, float)):
            return type(self)(value - self._value)
        return NotImplemented

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return type(self)(self._value * value)
        if isinstance(value, type(self)):
            return type(self)(self._value * value._value)
        return NotImplemented
    __rmul__ = __mul__

    def __truediv__(self, value):
        if isinstance(value, (int, float)):
            return type(self)(self._value / value)
        if isinstance(value, type(self)):
            return type(self)(self._value / value._value)
        return NotImplemented

    def __pow__(self, n):
        result = self.copy()
        if not isinstance(n, (int, float)):
            raise TypeError(f'Argument can not be {type(n).__name__} type')
        result._value = result._value ** n 
        return result

    def __repr__(self) -> str:
        return f'{round(self._value, self.Model.k) if self._value else None} {self.dimension[self.Model.lang]}'

    def copy(self):
        return type(self)(self._value)

    def __round__(self, k: int | float = None):
        k = k if k else self.Model.k
        return round(self._value, k) if self._value is not None else 'None'
    
    def __bool__(self) -> bool:
        return not 'None' in self.__repr__()


class Lenght(Base):
    dimension = {'ru': 'м', 'en': 'm'}


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


class Mass(Base):
    dimension = {'ru': 'кг', 'en': 'kg'}

    def __mul__(self, value):
        if isinstance(value, Acceleration):
            return Force((self._value * value.x, self._value * value.y))
        return super().__mul__(value)
    __rmul__ = __mul__

    def __truediv__(self, value):
        if isinstance(value, Density):
            return Volume(self._value / value._value)
        if isinstance(value, Volume):
            return Density(self._value / value._value)
        return super().__truediv__(value)


class Volume(Base):
    dimension = {'ru': 'м³', 'en': 'm³'}

    def __truediv__(self, value):
        if isinstance(value, Density):
            return Mass(self._value / value._value)
        if isinstance(value, Mass):
            return Density(self._value / value._value)
        return super().__truediv__(value)

    def __pow__(self, n):
        if abs(n - 1 / 3) < 1e-4:
            return Lenght(self._value ** (1 / 3))
        return super().__pow__(n)


class Density(Base):
    dimension = {'ru': 'кг/м³', 'en': 'kg/m³'}


class Specific_Heat(Base):
    dimension = {'ru': 'Дж/(кг*°С)', 'en': 'J/(kg*°C)'}


class Time(Base):
    dimension = {'ru': 'с', 'en': 's'}


# ─────────────────────────────── векторные величины ───────────────────────────────

class VectPhysical(Base):
    """Обёртка над Vector: сложение/вычитание через компоненты, без мутации операндов."""
    format = 'vector'

    def __init__(self, value=(0, 0), model: 'Model' = None):
        self.Model = model if model is not None else Model()

        self.__name__ = type(self).__name__
        if isinstance(value, type(self)):
            self._vector = _copy_vector(value._vector)
        elif isinstance(value, Vector):
            self._vector = _copy_vector(value)
        elif isinstance(value, (tuple, list)) and len(value) == 2:
            self._vector = Vector(value)
        else:
            raise TypeError(f'Value must be tuple, list, Vector or {type(self).__name__}, '
                            f'not {type(value).__name__}.')

    @property
    def x(self):
        self._vector._ensure_coord()
        return self._vector.x

    @property
    def y(self):
        self._vector._ensure_coord()
        return self._vector.y

    @property
    def θ(self):
        self._vector._ensure_polar()
        return self._vector.θ

    @property
    def _value(self):
        self._vector._ensure_polar()
        return self._vector.r if self._vector.r else None

    def __add__(self, value):
        if isinstance(value, type(self)):
            other = value._vector
        elif isinstance(value, Vector):
            other = value
        else:
            return NotImplemented
        self._vector._ensure_coord()
        other._ensure_coord()
        return type(self)((self._vector.x + other.x, self._vector.y + other.y))
    __radd__ = __add__

    def __sub__(self, value):
        if isinstance(value, type(self)):
            other = value._vector
        elif isinstance(value, Vector):
            other = value
        else:
            return NotImplemented
        self._vector._ensure_coord()
        other._ensure_coord()
        return type(self)((self._vector.x - other.x, self._vector.y - other.y))

    def __neg__(self):
        return type(self)((-self.x, -self.y))

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            k = value
        elif isinstance(value, Base) and isinstance(value._value, (int, float)):
            k = value._value
        elif isinstance(value, (type(self), VectPhysical)):
            return type(self)([self.r*value.r, self.θ+value.θ])
        else:
            return NotImplemented
        return type(self)((self.x * k, self.y * k))
    __rmul__ = __mul__

    def __truediv__(self, value):
        if isinstance(value, (int, float)):
            k = value
        elif isinstance(value, Base) and isinstance(value._value, (int, float)):
            k = value._value
        elif isinstance(value, (type(self), VectPhysical)):
            return type(self)([self.r*value.r, self.θ+value.θ])
        else:
            return NotImplemented
        return type(self)((self.x / k, self.y / k))

    def __repr__(self) -> str:
        return (f'{round(self._value, self.Model.k) if self._value else None} '
                f'{self.dimension[self.Model.lang]}')

    def copy(self):
        return type(self)(_copy_vector(self._vector))


class Velocity(VectPhysical):
    dimension = {'ru': 'м/с', 'en': 'm/s'}

    def __mul__(self, value):
        if isinstance(value, Time):
            return Velocity((self.x * value._value, self.y * value._value))
        return super().__mul__(value)


class Acceleration(VectPhysical):
    dimension = {'ru': 'м/с²', 'en': 'm/s²'}

    def __mul__(self, value) -> Type['Acceleration'] | Type['Position']:
        if isinstance(value, Time):
            return Position((self.x * value._value, self.y * value._value))
        return super().__mul__(value)


class Force(VectPhysical):
    dimension = {'ru': 'Н', 'en': 'N'}

    def __truediv__(self, value) -> Type['Force'] | Type['Acceleration']:
        if isinstance(value, Mass):
            return Acceleration([self._vector.r / value._value, self.θ])
        return super().__truediv__(value)


class Impulse(VectPhysical):
    dimension = {'ru': 'кг·м/с', 'en': 'kg·m/s'}

    def __truediv__(self, value) -> Type['Impulse'] | Type['Velocity']:
        if isinstance(value, Mass):
            return Velocity([self._vector.r / value._value, self.θ])
        return super().__truediv__(value)


class Position(VectPhysical):
    dimension = {'ru': 'м', 'en': 'm'}

    def __repr__(self) -> str:
        return (f'({round(self.x, self.Model.k)} {self.dimension[self.Model.lang]}, '
                f'{round(self.y, self.Model.k)} {self.dimension[self.Model.lang]})')


# ─────────────────────────────────── модель мира ──────────────────────────────────

def singleton(cls):
    instance = None

    def get(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        elif kwargs:
            for key, val in kwargs.items():
                if key == 'g':
                    instance.g = Acceleration(tuple(val), instance)
                elif key == 'ρ':
                    instance.ρ = Density(val, instance)
                else:
                    setattr(instance, key, val)
        return instance
    return get


@singleton
class Model:
    __el__ = ('k', 'lang', 'g', 'ρ', 't')
    π = 3.1415926535897
    G = 6.67430e-11 # 6,67430(15) · 10⁻¹¹
    R = 6371e3
    M = 5.9722e24

    def __init__(self, k=5, lang: Literal['ru', 'en' ] = 'ru', g: Literal['[9.81, 270]']=None, ρ=1.204, b: 'Body' = None):
        self.k = k
        self.b = b
        self.lang = lang
        self.g = Acceleration(g, self) if g else self.calc_g
        self.ρ = Density(ρ, self)
        self.t = Time(0, self)

    @property
    def calc_g(self):
        Δr = self.b.coordinates.y if self.b else 0
        g = self.G*self.M/(self.R+Δr)**2
        return Acceleration([g, 270], self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({'; '.join([f'{el} = {getattr(self, el)}' for el in self.__el__ if getattr(self, el)])})"


# ─────────────────────────────────── процессы ─────────────────────────────────────

Burning = lambda q=2.7e7, m=10e-3, η=1: Warmth(q*m*η)


# ───────────────────────────────────── тело ───────────────────────────────────────

class Body:
    __el__ = ('m', 'ρ', 'V', 'temp', 'C', 'Vel', 'coordinates', 'a', 'p')

    def __init__(self, m=1, ρ=None, V=None, temp=20, C=4200,
                 Vel=None, coordinates=None, a=None, p=None, model: 'Model' = None):
        self.Model = model if model is not None else Model(b=self)
        self.m = m if isinstance(m, Mass) else Mass(m)
        self.ρ = ρ if isinstance(ρ, Density) else Density(ρ if ρ is not None else 1000)
        self.V = V if isinstance(V, Volume) else Volume(self.m._value / self.ρ._value)
        self.temp = temp if isinstance(temp, Temperature) else Temperature(temp)
        self.C = C if isinstance(C, Specific_Heat) else Specific_Heat(C)
        self.Vel = Vel if isinstance(Vel, Velocity) else Velocity(Vel if Vel else (0, 0))
        self.coordinates = (coordinates if isinstance(coordinates, Position)
                            else Position(coordinates if coordinates else (0, 0)))
        self.a = a if isinstance(a, Acceleration) else Acceleration((0, 0))
        self.p = p if isinstance(p, Impulse) else Impulse((0, 0))

    def repair(self):
        for el in self.__el__:
            attr = getattr(self, el, None)
            if attr is None or getattr(attr, 'format', '') == 'vector':
                continue
            value = getattr(attr, '_value', None)
            if isinstance(value, Base):
                while isinstance(value, Base):
                    value = value._value
                setattr(self, el, type(attr)(value))

    def drag_acceleration(self, C=0.47, S=None, vel=None):
        """Ускорение сопротивления воздуха: F = ½·C·ρ·S·v²"""
        if vel is None:
            self.Vel._vector._ensure_polar()
            speed, θ = self.Vel._vector.r, self.Vel._vector.θ
        else:
            vx, vy = vel
            speed = sqrt(vx ** 2 + vy ** 2)
            θ = degrees(atan2(vy, vx)) if speed else 0.0

        if not speed:
            return Acceleration((0, 0))
        if S is None:
            r = (3 * self.m._value / (4 * self.Model.π * self.ρ._value)) ** (1 / 3)
            S = self.Model.π * r ** 2
        a = 0.5 * C * self.Model.ρ._value * S * speed ** 2 / self.m._value
        θ_drag = (θ + 180) % 360
        return Acceleration((a * cos(radians(θ_drag)), a * sin(radians(θ_drag))))

    def Σ_a(self, vel=None) -> Acceleration:
        return self.a + self.Model.g + self.drag_acceleration(vel=vel)


    def time(self, Δt=Time(1.0)):
        self.repair()
        self.fly(Δt)
        self.Model.t += Δt

    def calc_rk2(self, dt=Time(1.0)):
        self.repair()
        t = dt._value if isinstance(dt, Time) else Time(dt)._value
        a1 = self.Σ_a()
        vx, vy = self.Vel.x, self.Vel.y
        vxh, vyh = vx + a1.x * t / 2, vy + a1.y * t / 2
        acc = self.Σ_a(vel=(vxh, vyh))
        self.Vel = self.Vel + Velocity((acc.x * t, acc.y * t))
        self.coordinates = self.coordinates + Position((vxh * t, vyh * t))
        self.p = self.Vel * self.m

    def fly(self, duration=Time(-1), Δt=0.05, stop=None):
        t_total = duration._value if isinstance(duration, Time) else duration
        n = int(t_total / Δt)
        history = [(self.Model.t, self.coordinates.x, self.coordinates.y, self.Model.g)]
        if duration._value == -1:
            while self.coordinates.y > 0:
                self.calc_rk2(Time(Δt))
                history.append((self.Model.t, self.coordinates.x, self.coordinates.y, self.Model.g))
                self.Model.t += Δt
            history[-1] = self._interpolate_stop(history, Δt)
            return history
        for _ in range(n):
            self.calc_rk2(Time(Δt))
            history.append((self.Model.t, self.coordinates.x, self.coordinates.y, self.Model.g))
            if stop and stop(self):
                history[-1] = self._interpolate_stop(history, Δt)
                break
            self.Model.t += Δt
        return history

    def _interpolate_stop(self, history, dt):
        x0, y0 = history[-2][1], history[-2][2]
        x1, y1 = history[-1][1], history[-1][2]
        frac = y0 / (y0 - y1)
        x_land = x0 + frac * (x1 - x0)
        return (history[-1][0] + frac * dt, x_land, 0.0, self.Model.g)

    def move(self, dx=0, dy=0):
        self.coordinates = self.coordinates + Position((dx, dy))

    def copy(self):
        kw = {}
        for el in self.__el__:
            v = getattr(self, el)
            if getattr(v, 'format', '') == 'vector':
                kw[el] = v
            else:
                kw[el] = v._value
        result = type(self)(**kw, model=self.Model)
        result.repair()
        return result

    def __add__(self, other):
        if isinstance(other, Force):
            self.a = self.a + Acceleration((other.x / self.m._value, other.y / self.m._value))
            return self
        if isinstance(other, Warmth):
            ΔT = other._value / (self.m._value * self.C._value)
            self.temp = Temperature(self.temp._value + ΔT)
            return self
        if isinstance(other, Mass):
            self.m = Mass(self.m._value + other._value)
            self.V = Volume(self.m._value / self.ρ._value)
            return self
        return NotImplemented

    def __repr__(self) -> str:
        return f"{type(self).__name__}({'; '.join([f'{el} = {getattr(self, el)}' for el in self.__el__ if getattr(self, el)])})"

    @property
    def E_п(self):
        return Energy(self.m._value * (-self.Model.g.y) * self.coordinates.y)

    @property
    def E_к(self):
        return Energy(self.m._value * self.Vel._value**2 / 2)
    
    @property
    def E_м(self):
        return Energy(self.E_к._value + self.E_п._value)

    @property
    def U(self):
        return Energy(self.m._value * self.C._value * abs(self.temp))


# ─────────────────────────────────── демонстрация ─────────────────────────────────

if __name__ == '__main__':
    Model(k=4, lang='ru', ρ=0)
    print(Model())						# 1
    print(Body())						# 2
    sphere = Body(ρ=7850, C=500)
    print(sphere)						# 3
    m = Mass(5)
    print(m)							# 4
    sphere + m
    print(sphere)						# 5
    print(sphere.U)						# 6
    Q = Burning(2.7e7, η=0.3)
    print(Q)							# 7
    sphere + Q
    print(sphere)						# 8
    print(sphere.U)						# 9
    print(sphere.E_п)					# 10
    sphere.move(5, 5)
    print(sphere)						# 11
    print(sphere.E_п)					# 12

    c = 5         # количество траекторий
    ms = 0.5     # постоянный шаг интегрирования, с
    v0 = 30000 / 3.6

    s = sphere.copy()

    T = Model().t
    
    plt.figure(figsize=(10, 6))
    for i in [90 / c * n for n in range(c + 1)]:
        sphere.Vel = Velocity([v0, i])
        b = sphere.copy()
        
        history = b.fly(Δt=ms, stop=lambda body: body.coordinates.y <= 0)

        Model(t=T)
        
        ts = [t._value for t, _, _, _ in history]
        xs = [x for _, x, _, _ in history]
        ys = [y for _, _, y, _ in history]
        gs = [g._value for _, _, _, g in history]
        plt.plot(ts, gs, label=f'{round(i, 1)}°')

    plt.xlabel('t, c')
    plt.ylabel('g, м/c²')
    # plt.xlabel('t, c')
    # plt.ylabel('•, м')
    plt.title('Траектории с учётом сопротивления воздуха (RK2, шаг 0,05 с)')
    plt.legend(title='угол запуска')
    plt.grid(True)
    plt.show()

    print(Model())						# 13
