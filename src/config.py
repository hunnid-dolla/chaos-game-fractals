"""Модуль конфигурации приложения."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from src.transformations import TRANSFORMATIONS_MAP


class SizeConfig(BaseModel):
    width: int = 1920
    height: int = 1080


class TransformationConfig(BaseModel):
    name: str
    weight: float


class AffineParams(BaseModel):
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float


class AppConfig(BaseModel):
    """Главная конфигурация приложения."""

    size: SizeConfig = Field(default_factory=SizeConfig)
    iteration_count: int = 2500
    output_path: str = "result.png"
    threads: int = 1
    seed: float = 5.1234
    functions: list[TransformationConfig] = Field(
        default_factory=lambda: [
            TransformationConfig(name="linear", weight=1.0),
            TransformationConfig(name="swirl", weight=1.0),
            TransformationConfig(name="horseshoe", weight=1.0),
            TransformationConfig(name="sinusoidal", weight=1.0),
        ]
    )
    affine_params: AffineParams | None = None
    gamma_correction: bool = True
    gamma: float = 2.2


def parse_args() -> AppConfig:
    """Парсит аргументы CLI и объединяет их с конфигом."""
    parser = argparse.ArgumentParser(
        description="Fractal Flame Generator",
        add_help=False
    )

    parser.add_argument(
        "--help",
        action="help",
        help="Show this help message and exit"
    )

    parser.add_argument("--config", type=str, help="Path to JSON config file")
    parser.add_argument("-w", "--width", type=int, help="Image width")
    parser.add_argument("-h", "--height", type=int, help="Image height")
    parser.add_argument("-i", "--iteration-count", type=int, help="Iterations per pixel")
    parser.add_argument("-o", "--output-path", type=str, help="Output file path")
    parser.add_argument("-t", "--threads", type=int, help="Number of threads")
    parser.add_argument("--seed", type=float, help="Random seed")
    parser.add_argument(
        "-f",
        "--functions",
        type=str,
        help="Transformations format: name:weight,name:weight",
    )
    parser.add_argument(
        "-g",
        "--gamma-correction",
        action=argparse.BooleanOptionalAction,
        help="Enable gamma correction",
    )
    parser.add_argument("--gamma", type=float, help="Gamma value")

    args = parser.parse_args()

    # 1. Загружаем дефолтный конфиг
    config_data: dict[str, Any] = AppConfig().model_dump()

    # 2. Если передан JSON конфиг, обновляем значения из него
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"Config file not found: {args.config}", file=sys.stderr)
            sys.exit(1)
        with config_path.open("r", encoding="utf-8") as f:
            json_config = json.load(f)
            config_data.update(json_config)

    # 3. Аргументы CLI имеют наивысший приоритет
    if args.width:
        config_data.setdefault("size", {})["width"] = args.width
    if args.height:
        config_data.setdefault("size", {})["height"] = args.height
    if args.iteration_count:
        config_data["iteration_count"] = args.iteration_count
    if args.output_path:
        config_data["output_path"] = args.output_path
    if args.threads:
        config_data["threads"] = args.threads
    if args.seed:
        config_data["seed"] = args.seed
    if args.gamma_correction is not None:
        config_data["gamma_correction"] = args.gamma_correction
    if args.gamma:
        config_data["gamma"] = args.gamma

    if args.functions:
        funcs = []
        for item in args.functions.split(","):
            name, weight = item.split(":")
            if name not in TRANSFORMATIONS_MAP:
                print(f"Unknown transformation: {name}", file=sys.stderr)
                sys.exit(1)
            funcs.append({"name": name, "weight": float(weight)})
        config_data["functions"] = funcs

    # Валидация через Pydantic
    try:
        return AppConfig(**config_data)
    except Exception as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)