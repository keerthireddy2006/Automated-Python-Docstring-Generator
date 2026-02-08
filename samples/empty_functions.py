"""Module with example functions and class that lack proper docstrings initially."""


def process_data(data):
    """Double the input data."""
    return data * 2


class DataHandler:
    """Handles loading, saving, and transforming data."""

    def load(self, path):
        """Load data from the given path."""
        pass

    def save(self, data, path):
        """Save data to the given path."""
        pass

    def transform(self, x):
        """Add 1 to the input value."""
        return x + 1
