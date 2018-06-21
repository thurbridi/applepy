import pygame

WHITE = (255, 255, 255)


class Shape:
    def __init__(self, coord, angle=0):
        self._coord = coord
        self._angle = angle

    @property
    def coord(self):
        return self._coord

    @property
    def x(self):
        return self._coord[0]

    @x.setter
    def x(self, value):
        self._coord.x = value

    @property
    def y(self):
        return self._coord[1]

    @y.setter
    def y(self, value):
        self._coord.y = value

    @property
    def angle(self):
        return self._angle


class Rectangle(Shape):
    def __init__(self, coord, w, h):
        super().__init__(coord)
        self.w = w
        self.h = h

    @property
    def width(self):
        return self.w

    @property
    def height(self):
        return self.h

    def display(self, screen):
        pygame.draw.polygon(
            screen,
            WHITE,
            [
                (self.x, self.y),
                (self.x + self.w, self.y),
                (self.x + self.w, self.y + self.h),
                (self.x, self.y + self.h)
            ], 0)


class Circle(Shape):
    def __init__(self, coord, r):
        super().__init__(coord)
        self.r = r

    def display(self, screen):
        pygame.draw.circle(
            screen, WHITE, (self.x, self.y), self.r, 0)
