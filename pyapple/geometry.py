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

    def normal(self):
        x1 = self.y
        y1 = self.x + self.vector.x
        y2 = self.x
        x2 = self.y + self.vector.y

        normal = Vector2(x2-x1, y2-y1)
        unit_normal = normal.normalize()

        center = self.center()

        return Segment(center.point, unit_normal)

    def center(self):
        x_center = (self.x + self.x + self.vector.x) / 2
        y_center = (self.y + self.y + self.vector.y) / 2

        return Point(Vector2(x_center, y_center))

    def intersection(self, other):
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.vector.x
        y2 = self.y + self.vector.y

        x3 = other.x
        y3 = other.y
        x4 = other.x + other.vector.x
        y4 = other.y + other.vector.y

        a1 = y2 - y1
        b1 = x1 - x2
        c1 = (x2 * y1) - (x1 * y2)

        r3 = ((a1 * x3) + (b1 * y3) + c1)
        r4 = ((a1 * x4) + (b1 * y4) + c1)

        same_sign = ((r3 > 0 and r4 > 0) or (r3 < 0 and r4 < 0))
        if r3 != 0 and r4 != 0 and same_sign:
            return False

        a2 = y4 - y3
        b2 = x3 - x4
        c2 = (x4 * y3) - (x3 * y4)

        r1 = ((a2 * x1) + (b2 * y1) + c2)
        r2 = ((a2 * x2) + (b2 * y2) + c2)

        same_sign = ((r1 > 0 and r2 > 0) or (r1 < 0 and r2 < 0))
        if r1 != 0 and r2 != 0 and same_sign:
            return False

        denom = (a1 * b2) - (a2 * b1)
        if denom == 0:
            # Colinear
            return False

        offset = abs(denom) / 2

        num = (b1 * c2) - (b2 * c1)
        if num < 0:
            int_x = (num - offset) / denom
        else:
            int_x = (num + offset) / denom

        num = (a2 * c1) - (a1 * c2)
        if num < 0:
            int_y = (num - offset) / denom
        else:
            int_y = (num + offset) / denom

        return Point(Vector2(int_x, int_y))

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
