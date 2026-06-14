from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math
from typing import Callable, Iterable


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
class DerivativeDiagnostic:
    function_name: str
    x0: float
    h: float
    forward: float
    backward: float
    central: float
    one_sided_gap: float
    kink_flag: bool


@dataclass(frozen=True)
class InvariantReview:
    value: float
    lower: float
    upper: float
    inside: bool
    issue: str


def smooth_response(x: float) -> float:
    return math.exp(0.2 * x)


def smooth_derivative(x: float) -> float:
    return 0.2 * math.exp(0.2 * x)


def kink_response(x: float) -> float:
    return abs(x)


def saturation_response(x: float) -> float:
    return min(max(x, 0.0), 1.0)


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
    h_values: Iterable[float],
) -> list[LocalApproximationRecord]:
    output: list[LocalApproximationRecord] = []
    for h in h_values:
        if h == 0:
            continue
        actual_change = f(x0 + h) - f(x0)
        linear_prediction = derivative_at_x0 * h
        error = abs(actual_change - linear_prediction)
        output.append(
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
    return output


def derivative_diagnostics(
    function_name: str,
    f: RealFunction,
    x0: float,
    h_values: Iterable[float],
    gap_threshold: float = 0.5,
) -> list[DerivativeDiagnostic]:
    output: list[DerivativeDiagnostic] = []
    for h in h_values:
        if h <= 0:
            continue
        fwd = forward_difference(f, x0, h)
        bwd = backward_difference(f, x0, h)
        cen = central_difference(f, x0, h)
        gap = abs(fwd - bwd)
        output.append(
            DerivativeDiagnostic(
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
    return output


def invariant_review(values: Iterable[float], lower: float, upper: float) -> list[InvariantReview]:
    if lower > upper:
        raise ValueError("lower must be <= upper.")
    output: list[InvariantReview] = []
    for value in values:
        inside = lower <= value <= upper
        output.append(
            InvariantReview(
                value=value,
                lower=lower,
                upper=upper,
                inside=inside,
                issue="" if inside else "value outside invariant interval",
            )
        )
    return output


def records_to_dicts(records: list[object]) -> list[dict[str, object]]:
    return [asdict(record) for record in records]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
