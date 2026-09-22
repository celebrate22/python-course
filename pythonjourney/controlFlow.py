
"""FizzBuzz, prime checker, and a Go-style (value, error) function."""

from typing import Optional, Tuple


def fizzbuzz(n: int) -> None:
    """Print numbers 1..n, replacing multiples of 3/5 with Fizz/Buzz."""
    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


def is_prime(n: int) -> bool:
    """Return True if n is a prime number."""
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def divide(a: float, b: float) -> Tuple[Optional[float], Optional[str]]:
    """Return (result, error) instead of raising, Go-style.

    Python normally signals failure with exceptions, but this mirrors
    Go's (value, error) return convention if that's what you want.
    """
    if b == 0:
        return None, "division by zero"
    return a / b, None


def main():
    print("--- fizzbuzz(15) ---")
    fizzbuzz(15)

    print("\n--- is_prime ---")
    for n in [1, 2, 17, 18, 29]:
        print(f"{n} prime? {is_prime(n)}")

    print("\n--- divide ---")
    result, err = divide(10, 2)
    if err:
        print("Error:", err)
    else:
        print("10 / 2 =", result)

    result, err = divide(5, 0)
    if err:
        print("Error:", err)


if __name__ == "__main__":
    main()
