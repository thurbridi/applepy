import pygame
from pygame.math import Vector2
import random
import math
from .geometry import Circle, Segment, Point


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
INITIAL_VELOCITY = 20.0


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

    return Circle(Vector2(x, y), r)


if __name__ == '__main__':
    pygame.init()

    BLACK = (0,   0,   0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    ORANGE = (255, 69, 0)
    GREEN = (0, 255, 0)

    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

    objects = []

    done = False
    clock = pygame.time.Clock()
    while not done:
        dtime_ms = clock.tick(FPS)
        dtime = dtime_ms / 1000.0

        m_pos = Vector2(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        seg1 = Segment(Vector2(100, 100), Vector2(180, 256))
        seg2 = Segment(m_pos, Vector2(300, 175) - m_pos)

        screen.lock()
        screen.fill(BLACK)

        seg1.draw(screen)
        seg2.draw(screen, color=RED)

        if seg1.intersection(seg2):
            seg1.intersection(seg2).draw(screen)

        screen.unlock()
        pygame.display.flip()

    pygame.quit()
