from pygame.math import Vector2
import math


class Body:
    def __init__(self,
                 shape,
                 velocity=Vector2(0, 0),
                 acceleration=Vector2(0, 0),
                 restituition=0.2,
                 density=5.0):
        self.shape = shape
        self.vel = velocity
        self.acc = acceleration
        self.restituition = restituition
        self.mass = shape.mass(density)
        self.inv_mass = 1.0 / self.mass

    def apply_force(self, force):
        self.acc += force

    def apply_impulse(self, impulse):
        self.vel += self.inv_mass * impulse

    @property
    def position(self):
        return self.shape.point

    @position.setter
    def position(self, value):
        self.shape.point = value

    @property
    def x(self):
        return self.shape.x

    @property
    def y(self):
        return self.shape.y


class Collision:
    @classmethod
    def circle_to_circle(cls, manifold, a, b):
        normal = b.position - a.position
        dist_sqr = normal.length_squared()
        radius = a.shape.radius + b.shape.radius

        # No collision
        if dist_sqr >= radius * radius:
            manifold.contact_count = 0
            return

        distance = math.sqrt(dist_sqr)
        manifold.contact_count = 1

        if distance == 0:
            manifold.penetration = a.shape.radius
            manifold.normal = Vector2(1, 0)
        else:
            manifold.penetration = radius - distance
            manifold.normal = normal / distance

    @classmethod
    def circle_to_polygon(cls, manifold, a, b):
        # a: circle
        # b: polygon
        ...

    @classmethod
    def polygon_to_circle(cls, manifold, a, b):
        # a: polygon
        # b: circle
        Collision.circle_to_polygon(manifold, b, a)

    @classmethod
    def polygon_to_polygon(cls, manifold, a, b):
        ...
