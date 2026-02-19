"""Demo math module with complete docstrings for testing CI and pre-commit."""


def add(a: float, b: float) -> float:
    """Add two numbers.

    Args:
        a (float): First number
        b (float): Second number

    Returns:
        float: Sum of a and b
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a.

    Args:
        a (float): Number to subtract from
        b (float): Number to subtract

    Returns:
        float: Result of a - b
    """
    return a - b


class SimpleMath:
    """Simple math operations class for testing class docstrings."""

    def __init__(self, initial_value: float = 0.0) -> None:
        """Initialize with an initial value.

        Args:
            initial_value (float, optional): Starting value. Defaults to 0.0.
        """
        self.value = initial_value

    def multiply_by(self, factor: float) -> None:
        """Multiply current value by a factor.

        Args:
            factor (float): Multiplier
        """
        self.value *= factor

    def get_value(self) -> float:
        """Return the current value.

        Returns:
            float: Current calculated value
        """
        return self.value
