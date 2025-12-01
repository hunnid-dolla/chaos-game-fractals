"""Тесты для класса FractalImage."""

from src.core import Color
from src.image import FractalImage

WIDTH = 10
HEIGHT = 20
EXPECTED_PIXELS = 200
BIG_SIZE = 100
SMALL_SIZE = 2
COLOR_MAX = 255.0
COLOR_HALF = 127.5


def test_image_initialization() -> None:
    """Проверка инициализации изображения."""
    img = FractalImage(WIDTH, HEIGHT)
    assert img.width == WIDTH
    assert img.height == HEIGHT
    assert len(img.pixels) == EXPECTED_PIXELS
    assert img.pixels[0].counter == 0


def test_image_contains() -> None:
    """Проверка границ изображения."""
    img = FractalImage(BIG_SIZE, BIG_SIZE)
    assert img.contains(0, 0)
    assert img.contains(BIG_SIZE - 1, BIG_SIZE - 1)
    assert not img.contains(-1, 0)
    assert not img.contains(BIG_SIZE, BIG_SIZE // 2)


def test_pixel_hit() -> None:
    """Проверка попадания в пиксель."""
    img = FractalImage(SMALL_SIZE, SMALL_SIZE)
    pixel = img.pixel_at(0, 0)
    pixel.hit(Color(255, 0, 0))

    assert pixel.counter == 1
    assert pixel.r == COLOR_MAX
    assert pixel.g == 0.0
    assert pixel.b == 0.0

    pixel.hit(Color(0, 0, 255))
    assert pixel.counter == 2
    assert pixel.r == COLOR_HALF
    assert pixel.b == COLOR_HALF
