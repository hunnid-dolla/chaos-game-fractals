"""Класс для хранения изображения (холст)."""

from src.core import Color, Pixel


class FractalImage:
    """Холст для отрисовки фрактала."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Одномерный массив пикселей
        self.pixels: list[Pixel] = [Pixel() for _ in range(width * height)]

    def contains(self, x: int, y: int) -> bool:
        """Проверяет, попадают ли координаты в границы изображения."""
        return 0 <= x < self.width and 0 <= y < self.height

    def pixel_at(self, x: int, y: int) -> Pixel:
        """Возвращает пиксель по координатам (x, y)."""
        return self.pixels[y * self.width + x]
