class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b

    def subtract(self, a: int, b: int) -> int:
        return a - b

    def greet(self, name):
        print(f"Hello, {name}")


class MessageFormatter:
    def format_upper(self, message: str) -> str:
        return message.upper()

    def format_lower(self, message: str) -> str:
        return message.lower()

    def repeat(self, message: str, times: int):
        for _ in range(times):
            print(message)


def say_hello(name: str):
    print("Hello", name)
