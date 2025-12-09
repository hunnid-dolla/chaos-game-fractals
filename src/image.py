"""Класс для хранения изображения (холст)."""

import numpy as np


class FractalImage:
    """Холст для отрисовки фрактала на основе NumPy."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        # Массив цветов (Height, Width, 3 цвета RGB)
        self.data = np.zeros((height, width, 3), dtype=np.float32)
        # Массив счетчиков попаданий (Height, Width)
        self.counter = np.zeros((height, width), dtype=np.uint32)

    def contains(self, x: int, y: int) -> bool:
        """Проверяет, попадают ли координаты в границы изображения."""
        return 0 <= x < self.width and 0 <= y < self.height
