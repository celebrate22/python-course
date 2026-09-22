
"""Simple temperature converter between Celsius, Fahrenheit, and Kelvin."""


def celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32


def celsius_to_kelvin(c: float) -> float:
    return c + 273.15


def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5 / 9


def kelvin_to_celsius(k: float) -> float:
    return k - 273.15


def convert(value: float, unit: str):
    unit = unit.upper()
    if unit == "C":
        c = value
    elif unit == "F":
        c = fahrenheit_to_celsius(value)
    elif unit == "K":
        c = kelvin_to_celsius(value)
    else:
        raise ValueError(f"Unknown unit: {unit}. Use C, F, or K.")

    f = celsius_to_fahrenheit(c)
    k = celsius_to_kelvin(c)
    return c, f, k


def parse_input(raw: str):
    raw = raw.strip().upper()
    if len(raw) < 2:
        raise ValueError("Input too short:")
    value_str, unit = raw[:-1], raw[-1]
    return float(value_str), unit


def main():
    print("Temperature Converter")
    print("Enter a value with its unit:")
    raw = input("> ")

    try:
        value, unit = parse_input(raw)
        c, f, k = convert(value, unit)
        print(f"\n{c:.2f}°C = {f:.2f}°F = {k:.2f}K")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
