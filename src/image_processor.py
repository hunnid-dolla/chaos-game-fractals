"""Модуль для обработки и сохранения изображений."""

import math

from PIL import Image

from src.image import FractalImage


class ImageProcessor:
    """Класс для постобработки и сохранения фрактального изображения."""

    def save(
        self,
        image: FractalImage,
        output_path: str,
        gamma: float = 2.2,
        enable_gamma_correction: bool = True,
    ) -> None:
        """
        Сохраняет изображение в файл с применением гамма-коррекции.

        Args:
            image: Холст с пикселями.
            output_path: Путь для сохранения.
            gamma: Значение гаммы.
            enable_gamma_correction: Включить ли коррекцию.
        """
        # Подготавливаем буфер данных для Pillow
        # Pillow принимает список кортежей
        data = []

        # Предварительно вычисляем обратную гамму для скорости
        inv_gamma = 1.0 / gamma if enable_gamma_correction else 1.0

        for pixel in image.pixels:
            if pixel.counter == 0:
                data.append((0, 0, 0))
                continue

            r, g, b = pixel.r, pixel.g, pixel.b

            # Применяем гамма-коррекцию, если включена
            if enable_gamma_correction:
                r = math.pow(r / 255.0, inv_gamma) * 255.0
                g = math.pow(g / 255.0, inv_gamma) * 255.0
                b = math.pow(b / 255.0, inv_gamma) * 255.0

            # Ограничиваем значения диапазоном
            r = min(max(0, int(r)), 255)
            g = min(max(0, int(g)), 255)
            b = min(max(0, int(b)), 255)

            data.append((r, g, b))

        # Создаем изображение и сохраняем
        img = Image.new("RGB", (image.width, image.height))
        img.putdata(data)
        img.save(output_path, "PNG")
