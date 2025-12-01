"""Вспомогательные функции для генерации и математики."""

import random

from src.core import AffineCoefficients, Color


def generate_affine_coefficients(count: int) -> list[AffineCoefficients]:
    """Генерирует набор случайных аффинных коэффициентов.

    Коэффициенты подбираются так, чтобы преобразование было сжимающим.
    """
    coefficients = []
    for _ in range(count):
        while True:
            # Генерируем случайные коэффициенты в диапазоне [-1, 1]
            a = random.uniform(-1, 1)
            b = random.uniform(-1, 1)
            c = random.uniform(-1, 1)
            d = random.uniform(-1, 1)
            e = random.uniform(-1, 1)
            f = random.uniform(-1, 1)

            # Проверка на сжимаемость (достаточное условие сходимости IFS)
            if (
                (a**2 + d**2 < 1)
                and (b**2 + e**2 < 1)
                and (a**2 + b**2 + d**2 + e**2 < 1 + (a * e - b * d) ** 2)
            ):
                color = Color(
                    r=random.randint(0, 255),
                    g=random.randint(0, 255),
                    b=random.randint(0, 255),
                )
                coefficients.append(AffineCoefficients(a, b, c, d, e, f, color))
                break
    return coefficients
