"""Логика рендеринга фрактала (алгоритм Chaos Game)."""

import numpy as np

from src.core import AffineCoefficients, Point, RenderContext
from src.image import FractalImage
from src.transformations import Transformation


class Renderer:
    """Отвечает за генерацию изображения с использованием векторизации."""

    def render(
        self,
        image: FractalImage,
        coefficients: list[AffineCoefficients],
        transformations: list[Transformation],
        ctx: RenderContext,
    ) -> None:
        """Запускает процесс рендеринга (векторизованная версия)."""
        rng = np.random.default_rng(ctx.seed)

        aspect = image.width / image.height
        scale = 10.0  # Коэффициент масштаба
        world_x_min, world_x_max = -aspect * scale, aspect * scale
        world_y_min, world_y_max = -1.0 * scale, 1.0 * scale

        coeffs_a = np.array([c.a for c in coefficients])
        coeffs_b = np.array([c.b for c in coefficients])
        coeffs_c = np.array([c.c for c in coefficients])
        coeffs_d = np.array([c.d for c in coefficients])
        coeffs_e = np.array([c.e for c in coefficients])
        coeffs_f = np.array([c.f for c in coefficients])

        coeffs_colors = np.array(
            [[c.color.r, c.color.g, c.color.b] for c in coefficients]
        )

        current_x = rng.uniform(world_x_min, world_x_max, ctx.samples)
        current_y = rng.uniform(world_y_min, world_y_max, ctx.samples)

        for step in range(-20, ctx.iters):
            indices = rng.integers(0, len(coefficients), ctx.samples)

            a = coeffs_a[indices]
            b = coeffs_b[indices]
            c = coeffs_c[indices]
            d = coeffs_d[indices]
            e = coeffs_e[indices]
            f = coeffs_f[indices]

            next_x = a * current_x + b * current_y + c
            next_y = d * current_x + e * current_y + f

            final_x = np.zeros_like(next_x)
            final_y = np.zeros_like(next_y)

            p_aff = Point(next_x, next_y)

            for transform in transformations:
                p_res = transform.apply(p_aff)
                final_x += p_res.x
                final_y += p_res.y

            current_x = final_x
            current_y = final_y

            if step < 0:
                continue

            for s in range(ctx.symmetry):
                theta = s * (2 * np.pi / ctx.symmetry)

                rot_x = current_x * np.cos(theta) - current_y * np.sin(theta)
                rot_y = current_x * np.sin(theta) + current_y * np.cos(theta)

                raw_screen_x = (
                    (rot_x - world_x_min) / (world_x_max - world_x_min) * image.width
                )
                raw_screen_y = (
                    (rot_y - world_y_min) / (world_y_max - world_y_min) * image.height
                )

                valid_mask = (
                    np.isfinite(raw_screen_x)
                    & np.isfinite(raw_screen_y)
                    & (raw_screen_x >= 0)
                    & (raw_screen_x < image.width)
                    & (raw_screen_y >= 0)
                    & (raw_screen_y < image.height)
                )

                valid_x = raw_screen_x[valid_mask].astype(int)
                valid_y = raw_screen_y[valid_mask].astype(int)
                valid_colors = coeffs_colors[indices[valid_mask]]

                np.add.at(image.data, (valid_y, valid_x), valid_colors)
                np.add.at(image.counter, (valid_y, valid_x), 1)
