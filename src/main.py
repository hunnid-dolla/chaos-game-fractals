"""Точка входа в генератор."""

import logging
import sys


def main() -> None:
    """Основная функция запуска."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Fractal Flame Generator started")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Fatal error occurred")
        sys.exit(1)
