"""Тесты конфигурации."""

from src.config import AppConfig, SizeConfig

DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
DEFAULT_ITERATIONS = 2500
DEFAULT_FUNCTIONS_COUNT = 4
CUSTOM_WIDTH = 800
CUSTOM_HEIGHT = 600
CUSTOM_THREADS = 8
CUSTOM_SEED = 123.45


def test_default_config() -> None:
    """Проверка дефолтной конфигурации."""
    config = AppConfig()
    assert config.size.width == DEFAULT_WIDTH
    assert config.iteration_count == DEFAULT_ITERATIONS
    assert len(config.functions) == DEFAULT_FUNCTIONS_COUNT


def test_custom_size_config() -> None:
    """Проверка кастомного размера."""
    config = AppConfig(size=SizeConfig(width=CUSTOM_WIDTH, height=CUSTOM_HEIGHT))
    assert config.size.width == CUSTOM_WIDTH
    assert config.size.height == CUSTOM_HEIGHT


def test_custom_params() -> None:
    """Проверка кастомных параметров."""
    config = AppConfig(threads=CUSTOM_THREADS, seed=CUSTOM_SEED)
    assert config.threads == CUSTOM_THREADS
    assert config.seed == CUSTOM_SEED
