from typing import Union

class Calculator:
    def add(self, x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Both arguments must be numbers")
        return x + y

    def divide(self, x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Both arguments must be numbers")
        return x / y

class A:
    x = 1
