"""Точка входа в генератор фрактального пламени."""

import logging
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from src.config import parse_args
from src.core import AffineCoefficients, Color
from src.image import FractalImage
from src.image_processor import ImageProcessor
from src.renderer import Renderer
from src.transformations import TRANSFORMATIONS_MAP, Transformation
from src.utils import generate_affine_coefficients

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def render_task(
    width: int,
    height: int,
    coeffs: list[AffineCoefficients],
    transforms: list[Transformation],
    samples: int,
    iters: int,
    seed: int,
    symmetry: int,
) -> FractalImage:
    """Задача для отдельного процесса.

    Создает свой экземпляр изображения и рендерит часть точек.
    """
    import random

    import numpy as np

    # Переинициализация генераторов случайных чисел для каждого процесса
    random.seed(seed)
    np.random.seed(seed)

    image = FractalImage(width, height)
    renderer = Renderer()
    renderer.render(image, coeffs, transforms, samples, iters, symmetry)
    return image


def merge_images(base: FractalImage, layer: FractalImage) -> None:
    """Объединяет (суммирует) два изображения."""
    # NumPy
    base.data += layer.data
    base.counter += layer.counter


def main() -> None:
    """Основная функция запуска."""
    start_time = time.time()
    logger.info("Starting Fractal Flame Generator...")

    try:
        config = parse_args()
    except Exception:
        logger.exception("Failed to parse configuration")
        sys.exit(1)

    logger.info(
        "Config loaded. Size: %sx%s, Threads: %s, Iterations: %s, Symmetry: %s",
        config.size.width,
        config.size.height,
        config.threads,
        config.iteration_count,
        config.symmetry,
    )

    # Логика аффинных коэффициентов
    if config.affine_params:
        affine_coefficients = []
        for p in config.affine_params:
            # Для заданных вручную коэффициентов генерируем случайный цвет
            color = Color(
                r=random.randint(0, 255),
                g=random.randint(0, 255),
                b=random.randint(0, 255),
            )
            affine_coefficients.append(
                AffineCoefficients(p.a, p.b, p.c, p.d, p.e, p.f, color)
            )
        logger.info("Using %s custom affine transformations", len(affine_coefficients))
    else:
        affine_coefficients = generate_affine_coefficients(20)
        logger.info("Generated 20 random affine transformations")

    active_transformations = [
        TRANSFORMATIONS_MAP[func_conf.name]
        for func_conf in config.functions
        if func_conf.name in TRANSFORMATIONS_MAP
    ]

    if not active_transformations:
        logger.error("No valid transformations specified.")
        sys.exit(1)

    total_samples = config.samples
    # Защита от деления на ноль или слишком малого кол-ва сэмплов
    total_samples = max(total_samples, config.threads)
    samples_per_thread = total_samples // config.threads

    final_image = FractalImage(config.size.width, config.size.height)
    futures = []

    logger.info("Launching %s worker process(es)...", config.threads)

    with ProcessPoolExecutor(max_workers=config.threads) as executor:
        for i in range(config.threads):
            thread_seed = config.seed + i
            futures.append(
                executor.submit(
                    render_task,
                    config.size.width,
                    config.size.height,
                    affine_coefficients,
                    active_transformations,
                    samples_per_thread,
                    config.iteration_count,
                    thread_seed,
                    config.symmetry,
                )
            )

        completed_count = 0
        for future in as_completed(futures):
            try:
                part_image = future.result()
                merge_images(final_image, part_image)
                completed_count += 1
                logger.info(
                    "Progress: %s/%s threads finished.",
                    completed_count,
                    config.threads,
                )
            except Exception:
                logger.exception("Thread failed with error")

    render_time = time.time() - start_time
    logger.info("Rendering completed in %.2f seconds.", render_time)

    try:
        processor = ImageProcessor()
        processor.save(
            final_image,
            config.output_path,
            gamma=config.gamma,
            enable_gamma_correction=config.gamma_correction,
        )
        logger.info("Image saved to %s", config.output_path)
    except Exception:
        logger.exception("Failed to save image")
        sys.exit(1)


if __name__ == "__main__":
    main()
