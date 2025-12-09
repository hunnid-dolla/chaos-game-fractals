"""Модуль для обработки и сохранения изображений."""

import numpy as np
from PIL import Image

from src.image import FractalImage


class ImageProcessor:
    """Класс для постобработки и сохранения фрактального изображения."""

    def save(
        self,
        image: FractalImage,
        output_path: str,
        gamma: float = 2.2,
        *,
        enable_gamma_correction: bool = True,
    ) -> None:
        """Сохраняет изображение в файл с применением гамма-коррекции."""
        with np.errstate(divide="ignore", invalid="ignore"):
            # 1. Получаем карту частот (сколько раз попали в каждый пиксель)
            counts = image.counter

            # Если изображение пустое, сохраняем черный квадрат
            if np.max(counts) == 0:
                img = Image.new("RGB", (image.width, image.height))
                img.save(output_path, "PNG")
                return

            # 2. Логарифмическая коррекция яркости (Log-Density)
            safe_counts = np.maximum(counts, 1)
            log_counts = np.log10(safe_counts)

            # Нормируем карту яркости от 0 до 1
            max_log = np.max(log_counts)
            alpha = log_counts / max_log

            # 3. Вычисляем средний цвет
            alpha_expanded = alpha[:, :, np.newaxis]
            counts_expanded = safe_counts[:, :, np.newaxis]

            # Средний цвет
            avg_color = image.data / counts_expanded

            # 4. Итоговый цвет = Средний цвет * Яркость
            normalized_data = avg_color * alpha_expanded

            # Дополнительное усиление насыщенности
            normalized_data *= 1.2

        # 5. Гамма-коррекция
        if enable_gamma_correction:
            normalized_data /= 255.0
            # Защита от отрицательных значений перед pow
            normalized_data = np.maximum(normalized_data, 0)
            normalized_data = np.power(normalized_data, 1.0 / gamma)
            normalized_data *= 255.0

        # Обрезаем значения 0..255
        final_data = np.clip(normalized_data, 0, 255).astype(np.uint8)

        img = Image.fromarray(final_data, "RGB")
        img.save(output_path, "PNG")
