import pygame
from pygame.math import Vector2

from pyapple import Simulation

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MAX_FPS = 60
MAX_SPEED = 50

BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 69, 0)
GREEN = (0, 255, 0)


if __name__ == '__main__':
    pygame.init()

    scene = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

    sim = Simulation(scene, gravity=Vector2(0, 10))
    for _ in range(20):
        sim.add_random_body(MAX_SPEED)

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

        scene.lock()
        scene.fill(BLACK)

        for body in sim.bodies:
            body.shape.draw(scene)

        scene.unlock()
        pygame.display.flip()

    pygame.quit()
