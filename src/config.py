"""Модуль конфигурации приложения."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError

from src.transformations import TRANSFORMATIONS_MAP

AFFINE_COEFFS_COUNT = 6


class SizeConfig(BaseModel):
    """Конфигурация размера изображения."""

    width: int = 1920
    height: int = 1080


class TransformationConfig(BaseModel):
    """Конфигурация одной трансформации."""

    name: str
    weight: float


class AffineParams(BaseModel):
    """Коэффициенты аффинного преобразования."""

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
    samples: int = 20_000
    output_path: str = "result.png"
    threads: int = 1
    seed: int = 5
    symmetry: int = 1
    functions: list[TransformationConfig] = Field(
        default_factory=lambda: [
            TransformationConfig(name="linear", weight=1.0),
            TransformationConfig(name="swirl", weight=1.0),
            TransformationConfig(name="horseshoe", weight=1.0),
            TransformationConfig(name="sinusoidal", weight=1.0),
        ]
    )
    affine_params: list[AffineParams] | None = None
    gamma_correction: bool = True
    gamma: float = 2.2


def _load_json_config(path: str) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        print(f"Config file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _parse_functions(functions_str: str) -> list[dict[str, Any]]:
    funcs = []
    for item in functions_str.split(","):
        name, weight = item.split(":")
        if name not in TRANSFORMATIONS_MAP:
            print(f"Unknown transformation: {name}", file=sys.stderr)
            sys.exit(1)
        funcs.append({"name": name, "weight": float(weight)})
    return funcs


def _parse_affine_params(params_str: str) -> list[dict[str, float]]:
    """Парсит строку формата a,b,c,d,e,f/a,b..."""
    result = []
    groups = params_str.split("/")
    for group in groups:
        parts = group.split(",")
        if len(parts) != AFFINE_COEFFS_COUNT:
            print(f"Invalid affine params format: {group}", file=sys.stderr)
            sys.exit(1)
        try:
            coeffs = [float(p) for p in parts]
            result.append(
                {
                    "a": coeffs[0],
                    "b": coeffs[1],
                    "c": coeffs[2],
                    "d": coeffs[3],
                    "e": coeffs[4],
                    "f": coeffs[5],
                }
            )
        except ValueError:
            print(f"Invalid number in affine params: {group}", file=sys.stderr)
            sys.exit(1)
    return result


def _update_config_from_args(
    config_data: dict[str, Any], args: argparse.Namespace
) -> None:
    simple_mappings = {
        "iteration_count": "iteration_count",
        "samples": "samples",
        "output_path": "output_path",
        "threads": "threads",
        "seed": "seed",
        "gamma_correction": "gamma_correction",
        "gamma": "gamma",
        "symmetry": "symmetry",
    }

    for arg_name, config_key in simple_mappings.items():
        val = getattr(args, arg_name)
        if val is not None:
            config_data[config_key] = val

    if args.width:
        config_data.setdefault("size", {})["width"] = args.width
    if args.height:
        config_data.setdefault("size", {})["height"] = args.height

    if args.functions:
        config_data["functions"] = _parse_functions(args.functions)

    if args.affine_params:
        config_data["affine_params"] = _parse_affine_params(args.affine_params)


def parse_args() -> AppConfig:
    """Парсит аргументы CLI и объединяет их с конфигом."""
    parser = argparse.ArgumentParser(
        description="Fractal Flame Generator", add_help=False
    )
    parser.add_argument("--help", action="help", help="Show this help message and exit")
    parser.add_argument("--config", type=str, help="Path to JSON config file")
    parser.add_argument("-w", "--width", type=int, help="Image width")
    parser.add_argument("-h", "--height", type=int, help="Image height")
    parser.add_argument(
        "-i", "--iteration-count", type=int, help="Iterations per pixel"
    )
    parser.add_argument("-s", "--samples", type=int, help="Number of starting points")
    parser.add_argument("-o", "--output-path", type=str, help="Output file path")
    parser.add_argument("-t", "--threads", type=int, help="Number of threads")
    parser.add_argument("--seed", type=int, help="Random seed (long)")
    parser.add_argument(
        "-sym", "--symmetry", type=int, help="Symmetry level (rotations)"
    )
    parser.add_argument(
        "-ap",
        "--affine-params",
        type=str,
        help="Affine params a,b,c,d,e,f/...",
    )
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
    config_data: dict[str, Any] = AppConfig().model_dump()

    if args.config:
        config_data.update(_load_json_config(args.config))

    _update_config_from_args(config_data, args)

    try:
        return AppConfig(**config_data)
    except (ValidationError, ValueError) as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
