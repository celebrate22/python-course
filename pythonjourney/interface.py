from abc import ABC, abstractmethod
import math

# Define the Shape interface using an abstract base class
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        
    def area(self) -> float:
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
        
    def area(self) -> float:
        return math.pi * (self.radius ** 2)

# Put both shapes in a single list
shapes = [
    Rectangle(4, 5),
    Circle(3)
]

# Print every area from one loop
for shape in shapes:
    print(f"Area: {shape.area():.2f}")
