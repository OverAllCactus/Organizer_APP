import operator
import re
from typing import Union

Number = Union[int, float]

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def calculate_expression(expr: str, precision: int = 15) -> float:
    """
    Вычисляет арифметическое выражение и округляет результат.
    precision — количество знаков после запятой для округления.
    """
    expr = expr.strip()
    if not expr:
        return 0.0

    if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
        raise ValueError("Недопустимые символы в выражении")

    try:
        result = eval(expr, {"__builtins__": {}}, OPERATORS)
        if not isinstance(result, (int, float)):
            raise ValueError("Результат не является числом")

        return round(float(result), precision)
    except ZeroDivisionError:
        raise ZeroDivisionError("Деление на ноль")
    except Exception as e:
        raise ValueError(f"Ошибка вычисления: {e}")
