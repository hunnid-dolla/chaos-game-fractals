"""Тесты для математических трансформаций."""

import math

from src.core import Point
from src.transformations import (
    HorseshoeTransformation,
    LinearTransformation,
    SinusoidalTransformation,
    SphericalTransformation,
    SwirlTransformation,
)


def test_linear_transformation() -> None:
    """Тест линейной трансформации."""
    t = LinearTransformation()
    p = Point(1.0, 2.0)
    res = t.apply(p)
    assert res.x == 1.0
    assert res.y == 2.0


def test_sinusoidal_transformation() -> None:
    """Тест синусоидальной трансформации."""
    t = SinusoidalTransformation()
    p = Point(math.pi / 2, 0)
    res = t.apply(p)
    assert math.isclose(res.x, 1.0)
    assert math.isclose(res.y, 0.0)


def test_spherical_transformation() -> None:
    """Тест сферической трансформации."""
    t = SphericalTransformation()
    p = Point(2.0, 0.0)
    res = t.apply(p)
    assert math.isclose(res.x, 0.5)
    assert math.isclose(res.y, 0.0)


def test_spherical_transformation_zero() -> None:
    """Тест сферической трансформации (нулевая точка)."""
    t = SphericalTransformation()
    p = Point(0.0, 0.0)
    res = t.apply(p)
    assert res.x == 0.0
    assert res.y == 0.0


def test_swirl_transformation() -> None:
    """Тест трансформации 'вихрь'."""
    t = SwirlTransformation()
    p = Point(1.0, 0.0)
    res = t.apply(p)
    assert math.isclose(res.x, math.sin(1.0))
    assert math.isclose(res.y, math.cos(1.0))


def test_horseshoe_transformation() -> None:
    """Тест трансформации 'подкова'."""
    t = HorseshoeTransformation()
    p = Point(3.0, 4.0)
    res = t.apply(p)
    inv_r = 1.0 / 5.0
    expected_x = inv_r * (3.0 - 4.0) * (3.0 + 4.0)
    expected_y = inv_r * 2 * 3.0 * 4.0
    assert math.isclose(res.x, expected_x)
    assert math.isclose(res.y, expected_y)
