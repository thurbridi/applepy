import pygame
from pygame.math import Vector2
import random
import math
from .geometry import Circle
from .physics import Body
from .manifold import Manifold


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MAX_FPS = 144
INITIAL_VELOCITY = 70.0

BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 69, 0)
GREEN = (0, 255, 0)


def random_circle():
    r = random.randint(10, 20)
    x = random.randint(r, WINDOW_WIDTH - r)
    y = random.randint(r, WINDOW_HEIGHT - r)

    angle = random.uniform(0, math.pi*2)
    v_x = math.sin(angle)
    v_y = math.cos(angle)

    v = Vector2(v_x, v_y)
    v.normalize()
    v *= INITIAL_VELOCITY

    return Body(Circle(Vector2(x, y), r), velocity=v)


class Simulation:
    '''
    F = m * A
    A = F * 1/m
    '''

    def __init__(self, gravity=Vector2(0, 9.8)):
        self.gravity = gravity
        self.bodies = []
        self.contacts = []

    def resolve_forces(self, body, dtime):
        if body.inv_mass == 0:
            return

        body.vel += (body.acc * body.inv_mass +
                     self.gravity) * (dtime / 2.0)

    def resolve_velocity(self, body, dtime):
        if body.inv_mass == 0:
            return

        body.position += body.vel * dtime
        self.resolve_forces(body, dtime)

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
            self.resolve_forces(body, dtime)

        # Initialize collision
        for collision in self.contacts:
            collision.initialize(dtime, self.gravity)

        # Solve collisions
        for collision in self.contacts:
            collision.apply_impulse()

        # Integrate velocities
        for body in self.bodies:
            self.resolve_velocity(body, dtime)

        # Correct positions
        for collision in self.contacts:
            collision.correct_position()

        # Clear all forces
        for body in self.bodies:
            body.acc = Vector2(0, 0)

    def add_random_body(self):
        self.bodies.append(random_circle())

    def add_body(self, body):
        self.bodies.append(body)


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

    objects = [random_circle() for _ in range(10)]

    sim = Simulation(gravity=Vector2(0, 0))
    # for _ in range(20):
    #     sim.add_random_body()
    sim.add_body(Body(Circle(Vector2(WINDOW_WIDTH/2, 100), 10),
                      velocity=Vector2(0, 100)))

    sim.add_body(
        Body(Circle(Vector2(WINDOW_WIDTH/2, 400), 10), velocity=Vector2(0, 0)))
    sim.add_body(
        Body(Circle(Vector2(WINDOW_WIDTH/2, 405), 10), velocity=Vector2(0, 0)))
    sim.add_body(
        Body(Circle(Vector2(WINDOW_WIDTH/2, 405), 10), velocity=Vector2(0, 0)))
    sim.add_body(
        Body(Circle(Vector2(WINDOW_WIDTH/2, 410), 10), velocity=Vector2(0, 0)))
    sim.add_body(
        Body(Circle(Vector2(WINDOW_WIDTH/2, 410), 10), velocity=Vector2(0, 0)))
    sim.add_body(
        Body(Circle(Vector2(WINDOW_WIDTH/2, 410), 10), velocity=Vector2(0, 0)))
    sim.add_body(
        Body(Circle(Vector2(WINDOW_WIDTH/2, 415), 10), velocity=Vector2(0, 0)))
    sim.add_body(
        Body(Circle(Vector2(WINDOW_WIDTH/2, 415), 10), velocity=Vector2(0, 0)))
    sim.add_body(
        Body(Circle(Vector2(WINDOW_WIDTH/2, 415), 10), velocity=Vector2(0, 0)))
    sim.add_body(
        Body(Circle(Vector2(WINDOW_WIDTH/2, 415), 10), velocity=Vector2(0, 0)))

    done = False
    clock = pygame.time.Clock()
    current_time = 0
    while not done:
        m_pos = Vector2(pygame.mouse.get_pos())

        dtime_ms = clock.tick(MAX_FPS)
        dtime = dtime_ms / 1000
        current_time += dtime

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        sim.step(dtime)

        screen.lock()
        screen.fill(BLACK)

        for body in sim.bodies:
            body.shape.draw(screen)

        screen.unlock()
        pygame.display.flip()

    pygame.quit()
