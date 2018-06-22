from .physics import Collision

EPSILON = 0.0001


class Manifold:
    def __init__(self, body_a, body_b):
        self.body_a = body_a
        self.body_b = body_b
        self.contacts = [None, None]
        self.contact_count = None
        self.penetration = None
        self.normal = None
        self.e = None

    def initialize(self, dtime, gravity):
        self.e = min(self.body_a.restituition, self.body_b.restituition)

        for i in range(self.contact_count):
            rv = self.body_b.vel - self.body_a.vel

            if (rv.length_squared() < (dtime * gravity).length_squared() +
                    EPSILON):
                self.e = 0.0

    def solve(self):
        shape_a = type(self.body_a.shape).__name__
        shape_b = type(self.body_b.shape).__name__

        if shape_a == 'Circle':
            if shape_b == 'Circle':
                Collision.circle_to_circle(self, self.body_a, self.body_b)
        else:
            raise NotImplementedError

    def apply_impulse(self):
        for i in range(self.contact_count):
            rv = self.body_b.vel - self.body_a.vel

            contact_vel = rv.dot(self.normal)

            if contact_vel > 0:
                return

            j = -(1.0 + self.e) * contact_vel
            inv_mass_sum = self.body_a.inv_mass + self.body_b.inv_mass
            j /= inv_mass_sum
            j /= self.contact_count

            impulse = self.normal * j
            self.body_a.apply_impulse(-impulse)
            self.body_b.apply_impulse(impulse)

    def correct_position(self):
        k_slop = 0.05
        percent = 0.4
        correction = max(self.penetration - k_slop, 0) / \
            (self.body_a.inv_mass + self.body_b.inv_mass) \
            * self.normal * percent

        self.body_a.position -= correction * self.body_a.inv_mass
        self.body_b.position += correction * self.body_b.inv_mass
