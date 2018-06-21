class Environment:
    def __init__(self, gravity, boundries):
        self._gravity = gravity
        self.boundries = boundries


class Solid:
    def __init__(self, shape, velocity=0, acceleration=0, mass=0):
        self._shape = shape
        self._velocity = velocity
        self._acceleration = acceleration
        self._mass = mass

    def move(self, dtime):
        ...

    @property
    def x(self):
        return self._shape.x

    @x.setter
    def x(self, value):
        self._shape.x(value)

    @property
    def y(self):
        return self._shape.y

    @y.setter
    def y(self, value):
        self._shape.y(value)

    @property
    def shape(self):
        return self._shape

    @property
    def mass(self):
        return self.mass

    @property
    def velocity(self):
        return self.velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    @property
    def acceleration(self):
        return self.acceleration

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = value

    def display(self, screen):
        self._shape.display(screen)
