"""Тесты для математических трансформаций."""

import math

import pytest

from src.core import Point
from src.transformations import (
    HorseshoeTransformation,
    LinearTransformation,
    SinusoidalTransformation,
    SphericalTransformation,
    SwirlTransformation,
)


def test_linear_transformation():
    t = LinearTransformation()
    p = Point(1.0, 2.0)
    res = t.apply(p)
    assert res.x == 1.0
    assert res.y == 2.0


def test_sinusoidal_transformation():
    t = SinusoidalTransformation()
    p = Point(math.pi / 2, 0)
    res = t.apply(p)
    assert math.isclose(res.x, 1.0)
    assert math.isclose(res.y, 0.0)


def test_spherical_transformation():
    t = SphericalTransformation()
    p = Point(2.0, 0.0)
    res = t.apply(p)
    # r^2 = 4. x_new = 2/4 = 0.5
    assert math.isclose(res.x, 0.5)
    assert math.isclose(res.y, 0.0)


def test_spherical_transformation_zero():
    t = SphericalTransformation()
    p = Point(0.0, 0.0)
    res = t.apply(p)
    assert res.x == 0.0
    assert res.y == 0.0


def test_swirl_transformation():
    t = SwirlTransformation()
    # r^2 = 1 + 0 = 1. sin(1), cos(1)
    p = Point(1.0, 0.0)
    res = t.apply(p)
    # x = 1*sin(1) - 0 = sin(1)
    # y = 1*cos(1) + 0 = cos(1)
    assert math.isclose(res.x, math.sin(1.0))
    assert math.isclose(res.y, math.cos(1.0))


def test_horseshoe_transformation():
    t = HorseshoeTransformation()
    p = Point(3.0, 4.0)  # r = 5
    res = t.apply(p)
    inv_r = 1.0 / 5.0
    expected_x = inv_r * (3.0 - 4.0) * (3.0 + 4.0)  # 1/5 * (-1) * 7 = -1.4
    expected_y = inv_r * 2 * 3.0 * 4.0  # 1/5 * 24 = 4.8
    assert math.isclose(res.x, expected_x)
    assert math.isclose(res.y, expected_y)
