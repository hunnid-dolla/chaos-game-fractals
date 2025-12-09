"""Математические функции трансформаций (вариации)."""

from abc import ABC, abstractmethod

import numpy as np

from src.core import Point


class Transformation(ABC):
    """Базовый класс для всех трансформаций."""

    @abstractmethod
    def apply(self, point: Point) -> Point:
        """Применяет трансформацию к точке (или массиву точек)."""


class LinearTransformation(Transformation):
    """Линейная трансформация (V0)."""

    def apply(self, point: Point) -> Point:
        """Возвращает точку без изменений."""
        return point


class SinusoidalTransformation(Transformation):
    """Синусоидальная трансформация (V1)."""

    def apply(self, point: Point) -> Point:
        """Применяет синус к координатам."""
        return Point(x=np.sin(point.x), y=np.sin(point.y))


class SphericalTransformation(Transformation):
    """Сферическая трансформация (V2)."""

    def apply(self, point: Point) -> Point:
        """Искажает координаты по сфере."""
        r2 = point.x**2 + point.y**2
        factor = 1.0 / np.where(r2 == 0, 1e-9, r2)
        return Point(x=point.x * factor, y=point.y * factor)


class SwirlTransformation(Transformation):
    """Трансформация 'Вихрь' (V3)."""

    def apply(self, point: Point) -> Point:
        """Закручивает координаты в вихрь."""
        r2 = point.x**2 + point.y**2
        sin_r2 = np.sin(r2)
        cos_r2 = np.cos(r2)
        return Point(
            x=point.x * sin_r2 - point.y * cos_r2,
            y=point.x * cos_r2 + point.y * sin_r2,
        )


class HorseshoeTransformation(Transformation):
    """Трансформация 'Подкова' (V4)."""

    def apply(self, point: Point) -> Point:
        """Искажает координаты в форме подковы."""
        r = np.sqrt(point.x**2 + point.y**2)
        inv_r = 1.0 / np.where(r == 0, 1e-9, r)
        return Point(
            x=inv_r * (point.x - point.y) * (point.x + point.y),
            y=inv_r * 2 * point.x * point.y,
        )


# Реестр доступных функций по имени
TRANSFORMATIONS_MAP: dict[str, Transformation] = {
    "linear": LinearTransformation(),
    "sinusoidal": SinusoidalTransformation(),
    "spherical": SphericalTransformation(),
    "swirl": SwirlTransformation(),
    "horseshoe": HorseshoeTransformation(),
}
