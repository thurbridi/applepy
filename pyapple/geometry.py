import pygame
from pygame.math import Vector2

BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 69, 0)


class Point:
    def __init__(self, point):
        self.point = point

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y

    def draw(self, screen, color=ORANGE, size=3):
        pygame.draw.circle(
            screen, color, (int(self.x), int(self.y)), size, 0)


class Segment:
    def __init__(self, point, vector):
        self.point = point
        self.vector = vector

    def length(self):
        return self.vector.length()

    def project(self, other):
        if isinstance(other, Segment):
            v1 = self.vector
            v2 = other.vector
            d = v2.dot(v2)
            if 0 < d:
                dp = v1.dot(v2)
                multiplier = dp / d
                rx = v2.x * multiplier
                ry = v2.y * multiplier
                return Segment(self.point, Vector2(rx, ry))
            return Segment(Vector2(0, 0), Vector2(0, 0))
        else:
            raise NotImplementedError

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y

    def draw(self, screen, color=BLUE, width=2):
        pygame.draw.line(screen, color, self.point, self.point + self.vector)


class Circle:
    def __init__(self, point, r):
        self.point = point
        self.r = r
        self.radius_line = Segment(point, Vector2(r, 0))

    def point_collision(self, point):
        if isinstance(point, Point):
            seg = Segment(self.point, Vector2(
                point.x - self.x, point.y - self.y))
            if seg.length() <= self.r:
                return True
            else:
                return False
        else:
            raise NotImplementedError

    def segment_collision(self, segment):
        if isinstance(segment, Segment):
            segC = Segment(segment.point, self.point - segment.point)
            segB = segC.project(segment)
            segA = Segment(self.point, segB.point + segB.vector - self.point)
            if segA.length() <= self.r:
                return True
            else:
                return False
        else:
            raise NotImplementedError

    def circle_collision(self, other):
        if isinstance(other, Circle):
            seg = Segment(self.point, Vector2(
                other.x - self.x, other.y - self.y))
            if seg.length() <= self.r + other.r:
                return True
            else:
                return False
        else:
            raise NotImplementedError

    def draw(self, screen, color=WHITE, width=0):
        pygame.draw.circle(
            screen, color, (int(self.x), int(self.y)), self.r, width)
        self.radius_line.draw(screen)

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y
