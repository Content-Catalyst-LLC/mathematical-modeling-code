from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math
from typing import Callable, Iterable


RealFunction = Callable[[float], float]


@dataclass(frozen=True)
class DifferenceEstimate:
    method: str
    x: float
    h: float
    estimate: float
    exact: float
    absolute_error: float


@dataclass(frozen=True)
class ConvergenceOrder:
    method: str
    h_large: float
    h_small: float
    error_large: float
    error_small: float
    estimated_order: float


@dataclass(frozen=True)
class InvariantReview:
    value: float
    lower: float
    upper: float
    inside: bool
    issue: str


def f(x: float) -> float:
    return math.exp(0.2 * x)


def exact_derivative(x: float) -> float:
    return 0.2 * math.exp(0.2 * x)


def require_positive_h(h: float) -> None:
    if h <= 0:
        raise ValueError("h must be positive.")


def forward_difference(fn: RealFunction, x: float, h: float) -> float:
    require_positive_h(h)
    return (fn(x + h) - fn(x)) / h


def central_difference(fn: RealFunction, x: float, h: float) -> float:
    require_positive_h(h)
    return (fn(x + h) - fn(x - h)) / (2.0 * h)


def richardson_extrapolation(central_h: float, central_h_over_2: float, order: int = 2) -> float:
    factor = float(2 ** order)
    return (factor * central_h_over_2 - central_h) / (factor - 1.0)


def estimate_order(error_large: float, error_small: float, refinement_ratio: float = 2.0) -> float:
    if error_large <= 0 or error_small <= 0:
        raise ValueError("Errors must be positive to estimate convergence order.")
    if refinement_ratio <= 1:
        raise ValueError("Refinement ratio must be greater than one.")
    return math.log(error_large / error_small) / math.log(refinement_ratio)


def convergence_study(x: float = 5.0, h_values: Iterable[float] | None = None) -> list[DifferenceEstimate]:
    if h_values is None:
        h_values = [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625]

    exact = exact_derivative(x)
    rows: list[DifferenceEstimate] = []

    for h in h_values:
        fd = forward_difference(f, x, h)
        cd = central_difference(f, x, h)
        cd_half = central_difference(f, x, h / 2.0)
        rich = richardson_extrapolation(cd, cd_half, order=2)

        rows.append(DifferenceEstimate("forward_difference", x, h, fd, exact, abs(fd - exact)))
        rows.append(DifferenceEstimate("central_difference", x, h, cd, exact, abs(cd - exact)))
        rows.append(DifferenceEstimate("richardson_central", x, h, rich, exact, abs(rich - exact)))

    return rows


def convergence_orders(rows: list[DifferenceEstimate]) -> list[ConvergenceOrder]:
    grouped: dict[str, list[DifferenceEstimate]] = {}
    for row in rows:
        grouped.setdefault(row.method, []).append(row)

    output: list[ConvergenceOrder] = []
    for method, values in grouped.items():
        ordered = sorted(values, key=lambda item: item.h, reverse=True)
        for large, small in zip(ordered, ordered[1:]):
            if large.absolute_error > 0 and small.absolute_error > 0:
                output.append(
                    ConvergenceOrder(
                        method=method,
                        h_large=large.h,
                        h_small=small.h,
                        error_large=large.absolute_error,
                        error_small=small.absolute_error,
                        estimated_order=estimate_order(large.absolute_error, small.absolute_error, large.h / small.h),
                    )
                )
    return output


def roundoff_review(x: float = 5.0) -> list[dict[str, float | str]]:
    h_values = [10.0 ** (-k) for k in range(1, 13)]
    exact = exact_derivative(x)
    output: list[dict[str, float | str]] = []

    previous_error: float | None = None
    for h in h_values:
        estimate = forward_difference(f, x, h)
        error = abs(estimate - exact)
        warning = ""
        if previous_error is not None and error > previous_error:
            warning = "error increased after refinement; possible roundoff or cancellation"
        output.append({"h": h, "estimate": estimate, "absolute_error": error, "warning": warning})
        previous_error = error

    return output


def invariant_review(values: Iterable[float], lower: float, upper: float) -> list[InvariantReview]:
    if lower > upper:
        raise ValueError("lower must be <= upper.")
    reviews: list[InvariantReview] = []
    for value in values:
        inside = lower <= value <= upper
        reviews.append(
            InvariantReview(
                value=value,
                lower=lower,
                upper=upper,
                inside=inside,
                issue="" if inside else "value outside invariant interval",
            )
        )
    return reviews


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
