"""Simple example module with complete docstrings."""


def greet(name: str) -> str:
    """Greet a person by name.

    Args:
        name: The person's name

    Returns:
        A friendly greeting message
    """
    return f"Hello, {name}!"


def square(number: float) -> float:
    """Calculate the square of a number.

    Args:
        number: The input number

    Returns:
        The square of the number
    """
    return number * number


class Counter:
    """A simple counter class."""

    def __init__(self):
        """Initialize counter to zero."""
        self.count = 0

    def increment(self) -> None:
        """Increment the counter by 1."""
        self.count += 1

    def get_count(self) -> int:
        """Get the current count.

        Returns:
            Current value of the counter
        """
        return self.count


# Presentation demo comment
# Added comment for demo
