"""Task 5: Extending a Point class to a Vector class."""

# Task 5
import math


class Point:
    """Represents a point in 2D space."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other):
        if not isinstance(other, Point):
            raise TypeError("distance_to expects a Point or subclass of Point")
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Vector(Point):
    """Represents a vector in 2D space."""

    def __str__(self):
        return f"Vector<{self.x}, {self.y}>"

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)


if __name__ == "__main__":
    point_a = Point(1, 2)
    point_b = Point(4, 6)
    vector_a = Vector(2, 3)
    vector_b = Vector(5, -1)

    print(point_a)
    print(point_b)
    print(f"point_a == point_b: {point_a == point_b}")
    print(f"Distance between points: {point_a.distance_to(point_b):.2f}")

    print(vector_a)
    print(vector_b)
    print(f"vector_a + vector_b = {vector_a + vector_b}")
    print(f"Distance between vectors: {vector_a.distance_to(vector_b):.2f}")
