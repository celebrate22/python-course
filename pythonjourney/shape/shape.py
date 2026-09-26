from abc import ABC, abstractmethod
import math

class InvalidDimensionError(ValueError):
    """Custom exception raised when shape dimensions are zero or negative."""
    def __init__(self, shape_type: str, message: str):
        self.shape_type = shape_type
        self.message = message
        super().__init__(f"[{shape_type} Error]: {message}")


class Shape(ABC):
    """Shape is an abstract base class with an area method."""
    @abstractmethod
    def area(self) -> float:
        pass


class Rectangle(Shape):
    """Rectangle holds width and height and validates dimensions."""
    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            raise InvalidDimensionError("Rectangle", "Width and height must be greater than zero.")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Circle(Shape):
    """Circle holds radius and validates dimensions."""
    def __init__(self, radius: float):
        if radius <= 0:
            raise InvalidDimensionError("Circle", "Radius must be greater than zero.")
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius * self.radius
