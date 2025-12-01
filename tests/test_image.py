"""Тесты для класса FractalImage."""

from src.core import Color
from src.image import FractalImage


def test_image_initialization():
    img = FractalImage(10, 20)
    assert img.width == 10
    assert img.height == 20
    assert len(img.pixels) == 200
    assert img.pixels[0].counter == 0


def test_image_contains():
    img = FractalImage(100, 100)
    assert img.contains(0, 0)
    assert img.contains(99, 99)
    assert not img.contains(-1, 0)
    assert not img.contains(100, 50)


def test_pixel_hit():
    img = FractalImage(2, 2)
    # Попадаем в пиксель (0,0) красным цветом
    pixel = img.pixel_at(0, 0)
    pixel.hit(Color(255, 0, 0))

    assert pixel.counter == 1
    assert pixel.r == 255.0
    assert pixel.g == 0.0
    assert pixel.b == 0.0

    # Попадаем второй раз синим цветом
    # (255+0)/2 = 127.5, (0+0)/2 = 0, (0+255)/2 = 127.5
    pixel.hit(Color(0, 0, 255))
    assert pixel.counter == 2
    assert pixel.r == 127.5
    assert pixel.b == 127.5
