"""Точка входа в генератор фрактального пламени."""

import logging
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from src.config import parse_args
from src.core import AffineCoefficients
from src.image import FractalImage
from src.image_processor import ImageProcessor
from src.renderer import Renderer
from src.transformations import TRANSFORMATIONS_MAP, Transformation
from src.utils import generate_affine_coefficients

# Настройка логирования
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
    seed: float,
) -> FractalImage:
    """
    Задача для отдельного процесса.
    Создает свой экземпляр изображения и рендерит часть точек.
    """

    import random

    random.seed(seed)

    image = FractalImage(width, height)
    renderer = Renderer()
    renderer.render(image, coeffs, transforms, samples, iters)
    return image


def merge_images(base: FractalImage, layer: FractalImage) -> None:
    """Объединяет (суммирует) два изображения."""
    for i, pixel_layer in enumerate(layer.pixels):
        if pixel_layer.counter > 0:
            pixel_base = base.pixels[i]
            # Если в базовом пикселе еще ничего не было
            if pixel_base.counter == 0:
                pixel_base.r = pixel_layer.r
                pixel_base.g = pixel_layer.g
                pixel_base.b = pixel_layer.b
                pixel_base.counter = pixel_layer.counter
            else:
                # Если уже было, усредняем цвет и суммируем попадания
                pixel_base.r = (pixel_base.r + pixel_layer.r) / 2
                pixel_base.g = (pixel_base.g + pixel_layer.g) / 2
                pixel_base.b = (pixel_base.b + pixel_layer.b) / 2
                pixel_base.counter += pixel_layer.counter


def main() -> None:
    """Основная функция запуска."""
    start_time = time.time()
    logger.info("Starting Fractal Flame Generator...")

    # 1. Загрузка конфигурации
    try:
        config = parse_args()
    except Exception as e:
        logger.error(f"Failed to parse configuration: {e}")
        sys.exit(1)

    logger.info(
        f"Config loaded. Size: {config.size.width}x{config.size.height}, "
        f"Threads: {config.threads}, Iterations: {config.iteration_count}"
    )

    # 2. Подготовка ресурсов
    affine_coefficients = generate_affine_coefficients(20)

    # Собираем список активных трансформаций
    active_transformations = []
    for func_conf in config.functions:
        if func_conf.name in TRANSFORMATIONS_MAP:
            active_transformations.append(TRANSFORMATIONS_MAP[func_conf.name])

    if not active_transformations:
        logger.error("No valid transformations specified.")
        sys.exit(1)

    # 3. Запуск рендеринга (Многопоточность)
    total_samples = config.samples  # Берем из конфига

    if total_samples < config.threads:
        total_samples = config.threads
        
    samples_per_thread = total_samples // config.threads

    final_image = FractalImage(config.size.width, config.size.height)
    futures = []

    logger.info(f"Launching {config.threads} worker process(es)...")

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
                )
            )

        # Сбор результатов
        completed_count = 0
        for future in as_completed(futures):
            try:
                part_image = future.result()
                merge_images(final_image, part_image)
                completed_count += 1
                logger.info(
                    f"Progress: {completed_count}/{config.threads} threads finished."
                )
            except Exception as e:
                logger.error(f"Thread failed with error: {e}")

    render_time = time.time() - start_time
    logger.info(f"Rendering completed in {render_time:.2f} seconds.")

    # 4. Сохранение результата
    try:
        processor = ImageProcessor()
        processor.save(
            final_image,
            config.output_path,
            gamma=config.gamma,
            enable_gamma_correction=config.gamma_correction,
        )
        logger.info(f"Image saved to {config.output_path}")
    except Exception as e:
        logger.error(f"Failed to save image: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
