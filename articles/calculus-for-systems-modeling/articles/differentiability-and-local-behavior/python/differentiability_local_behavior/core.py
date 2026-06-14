from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math
from typing import Callable


RealFunction = Callable[[float], float]


@dataclass(frozen=True)
class LocalApproximationRecord:
    function_name: str
    x0: float
    h: float
    actual_change: float
    linear_prediction: float
    absolute_error: float
    error_over_h: float


@dataclass(frozen=True)
class FiniteDifferenceRecord:
    function_name: str
    x0: float
    h: float
    forward: float
    backward: float
    central: float
    one_sided_gap: float
    kink_flag: bool


def smooth_response(x: float) -> float:
    return math.exp(0.2 * x)


def smooth_derivative(x: float) -> float:
    return 0.2 * math.exp(0.2 * x)


def kink_response(x: float) -> float:
    return abs(x)


def forward_difference(f: RealFunction, x: float, h: float) -> float:
    if h <= 0:
        raise ValueError("h must be positive")
    return (f(x + h) - f(x)) / h


def backward_difference(f: RealFunction, x: float, h: float) -> float:
    if h <= 0:
        raise ValueError("h must be positive")
    return (f(x) - f(x - h)) / h


def central_difference(f: RealFunction, x: float, h: float) -> float:
    if h <= 0:
        raise ValueError("h must be positive")
    return (f(x + h) - f(x - h)) / (2.0 * h)


def local_linearization_error(
    function_name: str,
    f: RealFunction,
    derivative_at_x0: float,
    x0: float,
    h_values: list[float],
) -> list[LocalApproximationRecord]:
    rows: list[LocalApproximationRecord] = []
    for h in h_values:
        if h == 0:
            continue
        actual_change = f(x0 + h) - f(x0)
        linear_prediction = derivative_at_x0 * h
        error = abs(actual_change - linear_prediction)
        rows.append(
            LocalApproximationRecord(
                function_name=function_name,
                x0=x0,
                h=h,
                actual_change=actual_change,
                linear_prediction=linear_prediction,
                absolute_error=error,
                error_over_h=error / abs(h),
            )
        )
    return rows


def finite_difference_diagnostics(
    function_name: str,
    f: RealFunction,
    x0: float,
    h_values: list[float],
    gap_threshold: float = 0.5,
) -> list[FiniteDifferenceRecord]:
    rows: list[FiniteDifferenceRecord] = []
    for h in h_values:
        if h <= 0:
            continue
        fwd = forward_difference(f, x0, h)
        bwd = backward_difference(f, x0, h)
        cen = central_difference(f, x0, h)
        gap = abs(fwd - bwd)
        rows.append(
            FiniteDifferenceRecord(
                function_name=function_name,
                x0=x0,
                h=h,
                forward=fwd,
                backward=bwd,
                central=cen,
                one_sided_gap=gap,
                kink_flag=gap > gap_threshold,
            )
        )
    return rows


def load_h_values(path: Path) -> list[float]:
    with path.open("r", encoding="utf-8") as handle:
        return [float(row["h"]) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def to_dicts(rows: list[object]) -> list[dict[str, object]]:
    return [asdict(row) for row in rows]
