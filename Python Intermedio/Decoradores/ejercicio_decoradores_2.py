def validate_numbers(func):
    def wrapper(*args, **kwargs):
        for value in args:
            if not isinstance(value, (int, float)):
                raise TypeError("All parameters must be numbers.")

        for value in kwargs.values():
            if not isinstance(value, (int, float)):
                raise TypeError("All parameters must be numbers.")

        return func(*args, **kwargs)

    return wrapper


@validate_numbers
def multiply(a, b):
    return a * b


try:
    print(multiply(5, 3))
except TypeError as ex:
    print(f"Error: {ex}")

try:
    print(multiply(5, "3"))
except TypeError as ex:
    print(f"Error: {ex}")