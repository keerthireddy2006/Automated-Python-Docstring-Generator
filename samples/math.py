"""Math utilities for basic operations."""


def add(x, y):
    """Add two numbers."""
    return x + y


def multiply(x, y):
    """Multiply two numbers."""
    return x * y


def power(base, exp):
    """Raise base to the power of exp."""
    return base**exp


class MathHelper:
    """Helper class for advanced math operations."""

    def factorial(self, n):
        """Calculate factorial of n."""
        if n == 0:
            return 1
        return n * self.factorial(n - 1)

    def is_even(self, num):
        """Check if number is even."""
        return num % 2 == 0


def divide(a, b):
    """Divide a by b."""
    return a / b
