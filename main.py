from shapes import Rectangle, Circle, Shape, InvalidDimensionError

def main():
    shapes_list: list[Shape] = []

    # 1. Create a valid Rectangle
    try:
        shapes_list.append(Rectangle(width=4, height=5))
    except InvalidDimensionError as e:
        print(f"Failed to create shape: {e}")

    # 2. Create a valid Circle
    try:
        shapes_list.append(Circle(radius=3))
    except InvalidDimensionError as e:
        print(f"Failed to create shape: {e}")

    # 3. Example: Attempting to create an invalid shape to trigger the custom exception
    try:
        shapes_list.append(Rectangle(width=-2, height=5))
    except InvalidDimensionError as e:
        # This catch is specific to our custom error
        print(f"Caught custom validation error -> Type: {e.shape_type} | Message: {e.message}")

    print("\n--- Calculating Areas ---")
    # Print every area from one loop
    for shape in shapes_list:
        print(f"Area: {shape.area():.2f}")

if __name__ == "__main__":
    main()
