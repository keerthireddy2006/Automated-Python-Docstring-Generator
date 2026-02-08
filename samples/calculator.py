"""Module containing a simple calculator and greeting functions."""


class Calculator:
    """A simple calculator class for basic arithmetic operations."""

    def add(self, a: int, b: int) -> int:
        """Add two numbers and return the result.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b
        """
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Subtract b from a and return the result."""
        return a - b

    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    def divide(self, a: int, b: int) -> float:
        """Divide a by b.

        Raises:
            ZeroDivisionError: If b is zero
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b


def greet(name: str) -> str:
    """Return a greeting message for the given name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(5, 3))
