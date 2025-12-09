"""Основные структуры данных для генерации фрактала."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    """Точка в двумерном пространстве."""

    x: float
    y: float


@dataclass
class Color:
    """Цвет в формате RGB."""

    r: int
    g: int
    b: int

    def to_tuple(self) -> tuple[int, int, int]:
        """Возвращает кортеж (r, g, b)."""
        return self.r, self.g, self.b


@dataclass(frozen=True)
class AffineCoefficients:
    """Коэффициенты для аффинного преобразования.

    x_new = ax + by + c, y_new = dx + ey + f.
    """

    a: float
    b: float
    c: float
    d: float
    e: float
    f: float
    color: Color  # Цвет, ассоциированный с этим преобразованием


@dataclass
class Pixel:
    """Пиксель аккумулятора изображения."""

    counter: int = 0
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0

    def hit(self, color: Color) -> None:
        """Обновляет состояние пикселя при попадании в него."""
        if self.counter == 0:
            self.r = float(color.r)
            self.g = float(color.g)
            self.b = float(color.b)
        else:
            # Усреднение цвета
            self.r = (self.r + color.r) / 2
            self.g = (self.g + color.g) / 2
            self.b = (self.b + color.b) / 2
        self.counter += 1


@dataclass(frozen=True)
class RenderContext:
    """Контекст рендеринга, объединяющий параметры генерации."""

    width: int
    height: int
    samples: int
    iters: int
    symmetry: int
    seed: int
