import pygame
import random
import numpy as np
from .shapes import Circle
from .physics import Solid


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60


def random_circle():
    r = random.randint(10, 20)
    x = random.randint(r, WINDOW_WIDTH - r)
    y = random.randint(r, WINDOW_HEIGHT - r)

    return Solid(Circle(np.array([x, y]), r))


if __name__ == '__main__':
    pygame.init()

    BLACK = (0,   0,   0)
    WHITE = (255, 255, 255)

    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

    circles = [random_circle() for _ in range(10)]

    done = False
    clock = pygame.time.Clock()
    while not done:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.lock()
        screen.fill(BLACK)

        for c in circles:
            c.display(screen)

        screen.unlock()
        pygame.display.flip()

    pygame.quit()
