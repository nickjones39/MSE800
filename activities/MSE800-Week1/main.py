def fibonacci_series(limit):
    """Return a list of Fibonacci values up to (and including) limit."""
    series = []
    a, b = 0, 1
    while a <= limit:
        series.append(a)
        a, b = b, a + b
    return series


def factorial(n):
    """Return n! (n factorial). Defined as 1 for n = 0."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def get_valid_number():
    """Prompt until the user enters a non-negative whole number, then return it."""
    while True:
        entry = input("Enter a number (N): ").strip()
        try:
            n = int(entry)
        except ValueError:
            print("  Please enter a whole number (e.g. 10).")
            continue
        if n < 0:
            print("  Please enter a non-negative number (0 or greater).")
            continue
        return n


def main():
    n = get_valid_number()

    print(f"Fibonacci series up to {n}: {fibonacci_series(n)}")
    print(f"Factorial of {n}: {factorial(n)}")


if __name__ == "__main__":
    main()