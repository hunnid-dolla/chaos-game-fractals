"""Логика рендеринга фрактала (алгоритм Chaos Game)."""

import random

from src.core import AffineCoefficients, Point
from src.image import FractalImage
from src.transformations import Transformation


class Renderer:
    """Отвечает за генерацию изображения."""

    def render(
        self,
        image: FractalImage,
        coefficients: list[AffineCoefficients],
        transformations: list[Transformation],
        samples: int,
        iter_per_sample: int,
    ) -> None:
        """Запускает процесс рендеринга.

        Args:
            image: Холст для рисования.
            coefficients: Список аффинных коэффициентов (с цветами).
            transformations: Список применяемых вариаций.
            samples: Количество начальных точек (потоков "сэмплов").
            iter_per_sample: Количество итераций для каждой точки.

        """

        aspect = image.width / image.height
        world_x_min, world_x_max = -aspect, aspect
        world_y_min, world_y_max = -1.0, 1.0

        for _ in range(samples):
            # 1. Выбираем случайную стартовую точку
            current_point = Point(
                random.uniform(world_x_min, world_x_max),
                random.uniform(world_y_min, world_y_max),
            )

            # 2. Запускаем итерации
            for step in range(-20, iter_per_sample):
                # Выбираем случайное аффинное преобразование
                coeff = random.choice(coefficients)

                # Применяем линейное преобразование
                x = coeff.a * current_point.x + coeff.b * current_point.y + coeff.c
                y = coeff.d * current_point.x + coeff.e * current_point.y + coeff.f

                # Применяем нелинейные трансформации
                new_x, new_y = 0.0, 0.0
                p_aff = Point(x, y)

                for transform in transformations:
                    p_res = transform.apply(p_aff)
                    new_x += p_res.x
                    new_y += p_res.y

                current_point = Point(new_x, new_y)

                if step < 0:
                    continue

                # 3. Рисуем точку
                screen_x = int(
                    (current_point.x - world_x_min)
                    / (world_x_max - world_x_min)
                    * image.width
                )
                screen_y = int(
                    (current_point.y - world_y_min)
                    / (world_y_max - world_y_min)
                    * image.height
                )

                if image.contains(screen_x, screen_y):
                    pixel = image.pixel_at(screen_x, screen_y)
                    pixel.hit(coeff.color)
