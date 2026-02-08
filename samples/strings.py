"""String manipulation utilities and formatter."""


def capitalize_text(text: str) -> str:
    """Convert the first character of the string to uppercase."""
    if not text:
        return ""
    return text[0].upper() + text[1:]


def reverse_string(s: str) -> str:
    """Return the reversed version of the input string."""
    return s[::-1]


class MessageFormatter:
    """Utility class to format text messages in different cases."""

    def format_upper(self, message: str) -> str:
        """Convert message to uppercase."""
        return message.upper()

    def format_lower(self, message: str) -> str:
        """Convert message to lowercase."""
        return message.lower()

    def repeat(self, message: str, times: int = 3) -> str:
        """Repeat the message multiple times."""
        return message * times


def is_palindrome(text: str) -> bool:
    """Check if the given text is a palindrome (ignoring case and spaces)."""
    cleaned = "".join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]
