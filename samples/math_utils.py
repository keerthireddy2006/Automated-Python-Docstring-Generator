def add_numbers(x, y):
    return x + y


def multiply_numbers(x, y):
    return x * y


class MathHelper:
    def power(self, base, exponent):
        return base**exponent

    def factorial(self, n):
        if n == 0:
            return 1
        return n * self.factorial(n - 1)


def is_even(num):
    return num % 2 == 0
