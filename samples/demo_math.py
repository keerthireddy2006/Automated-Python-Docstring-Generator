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
