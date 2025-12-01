"""Тесты конфигурации."""

from src.config import AppConfig, SizeConfig


def test_default_config():
    config = AppConfig()
    assert config.size.width == 1920
    assert config.iteration_count == 2500
    assert len(config.functions) == 4


def test_custom_size_config():
    config = AppConfig(size=SizeConfig(width=800, height=600))
    assert config.size.width == 800
    assert config.size.height == 600


def test_custom_params():
    config = AppConfig(threads=8, seed=123.45)
    assert config.threads == 8
    assert config.seed == 123.45
