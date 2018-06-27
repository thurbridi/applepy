import random
import math

from pygame.math import Vector2

from .geometry import Circle
from .physics import Body
from .manifold import Manifold


class Simulation:
    '''
    F = m * A
    A = F * 1/m
    '''

    def __init__(self, scene, gravity=Vector2(0, 9.8)):
        self.scene = scene
        self.gravity = gravity
        self.bodies = []
        self.contacts = []

    def integrate_forces(self, body, dtime):
        if body.inv_mass == 0:
            return

        body.vel += (body.acc * body.inv_mass +
                     self.gravity) * (dtime / 2.0)

    def integrate_velocity(self, body, dtime):
        if body.inv_mass == 0:
            return

        body.position += body.vel * dtime
        self.integrate_forces(body, dtime)

    def sum_kinectic_energy(self):
        k_energies = ((body.mass * body.vel.length_squared())/2.0
                      for body in self.bodies)

        return sum(k_energies)

    def step(self, dtime):
        # Generate new collision info
        self.contacts.clear()

        for i, a in enumerate(self.bodies):
            for j in range(i + 1, len(self.bodies)):
                b = self.bodies[j]

                if a.inv_mass == 0 and b.inv_mass == 0:
                    continue
                m = Manifold(a, b)
                m.solve()
                if m.contact_count:
                    self.contacts.append(m)

        # Integrate forces
        for body in self.bodies:
            self.integrate_forces(body, dtime)

        # Initialize collision
        for collision in self.contacts:
            collision.initialize(dtime, self.gravity)

        # Solve collisions
        for collision in self.contacts:
            collision.apply_impulse()

        # Correct positions
        for collision in self.contacts:
            collision.correct_position()

        # Integrate velocities
        for body in self.bodies:
            self.integrate_velocity(body, dtime)

        # Clear all forces
        for body in self.bodies:
            body.acc = Vector2(0, 0)

    def __random_circle(self, max_speed):
        r = random.randint(10, 20)
        x = random.randint(r, self.scene.get_size()[0] - r)
        y = random.randint(r, self.scene.get_size()[1] - r)

        angle = random.uniform(0, math.pi*2)
        v_x = math.sin(angle)
        v_y = math.cos(angle)

        v = Vector2(v_x, v_y)
        v.normalize()
        v *= max_speed

        return Body(Circle(Vector2(x, y), r), velocity=v)

    def add_random_body(self, max_speed):
        self.bodies.append(self.__random_circle(max_speed))

    def add_body(self, body):
        self.bodies.append(body)
