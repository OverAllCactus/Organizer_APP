from typing import Union

Number = Union[int, float]

UNITS_CONFIG = {
    "length": {
        "m": 1.0,
        "cm": 0.01,
        "mm": 0.001,
        "km": 1000.0,
        "ft": 0.3048,
        "in": 0.0254,
    },
    "weight": {
        "kg": 1.0,
        "g": 0.001,
    },
}


def convert(
    value: Number,
    from_unit: str,
    to_unit: str,
    category: str,
) -> float:
    """
    Конвертация через коэффициенты относительно базовой единицы.
    category: 'length' или 'weight'
    """
    cfg = UNITS_CONFIG.get(category)
    if cfg is None:
        raise ValueError(f"Неизвестная категория: {category}")
    if from_unit not in cfg or to_unit not in cfg:
        raise ValueError("Недопустимая единица измерения")

    base_value = value * cfg[from_unit]
    return base_value / cfg[to_unit]