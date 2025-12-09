"""Тесты для класса FractalImage."""

import numpy as np

from src.core import Color
from src.image import FractalImage

WIDTH = 10
HEIGHT = 20
BIG_SIZE = 100
SMALL_SIZE = 2
COLOR_MAX = 255.0


def test_image_initialization() -> None:
    """Проверка инициализации изображения."""
    img = FractalImage(WIDTH, HEIGHT)
    assert img.width == WIDTH
    assert img.height == HEIGHT
    assert img.data.shape == (HEIGHT, WIDTH, 3)
    assert img.counter.shape == (HEIGHT, WIDTH)
    assert np.all(img.counter == 0)


def test_image_contains() -> None:
    """Проверка границ изображения."""
    img = FractalImage(BIG_SIZE, BIG_SIZE)
    assert img.contains(0, 0)
    assert img.contains(BIG_SIZE - 1, BIG_SIZE - 1)
    assert not img.contains(-1, 0)
    assert not img.contains(BIG_SIZE, BIG_SIZE // 2)


def test_manual_data_modification() -> None:
    """Проверка записи данных в массив."""
    img = FractalImage(SMALL_SIZE, SMALL_SIZE)
    # Имитация попадания
    img.data[0, 0] += [255.0, 0.0, 0.0]
    img.counter[0, 0] += 1

    assert img.counter[0, 0] == 1
    assert np.array_equal(img.data[0, 0], [255.0, 0.0, 0.0])
