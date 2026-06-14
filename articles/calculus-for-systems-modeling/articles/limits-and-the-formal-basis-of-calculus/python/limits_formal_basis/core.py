from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class LimitExperiment:
    method: str
    x: float
    h: float
    estimate: float
    exact: float
    absolute_error: float


def f(x: float) -> float:
    return math.exp(0.2 * x)


def exact_derivative(x: float) -> float:
    return 0.2 * math.exp(0.2 * x)


def require_positive_h(h: float) -> None:
    if h <= 0:
        raise ValueError("h must be positive")


def forward_difference(x: float, h: float) -> float:
    require_positive_h(h)
    return (f(x + h) - f(x)) / h


def central_difference(x: float, h: float) -> float:
    require_positive_h(h)
    return (f(x + h) - f(x - h)) / (2.0 * h)


def richardson_extrapolation(central_h: float, central_h_over_2: float) -> float:
    return (4.0 * central_h_over_2 - central_h) / 3.0


def estimate_order(error_large: float, error_small: float, ratio: float = 2.0) -> float:
    if error_large <= 0 or error_small <= 0:
        return float("nan")
    if ratio <= 1:
        raise ValueError("ratio must be greater than one")
    return math.log(error_large / error_small) / math.log(ratio)


def convergence_study(x: float, h_values: list[float]) -> list[LimitExperiment]:
    exact = exact_derivative(x)
    rows: list[LimitExperiment] = []

    for h in h_values:
        fd = forward_difference(x, h)
        cd = central_difference(x, h)
        cd_half = central_difference(x, h / 2.0)
        rich = richardson_extrapolation(cd, cd_half)

        rows.append(LimitExperiment("forward_difference", x, h, fd, exact, abs(fd - exact)))
        rows.append(LimitExperiment("central_difference", x, h, cd, exact, abs(cd - exact)))
        rows.append(LimitExperiment("richardson_central", x, h, rich, exact, abs(rich - exact)))

    return rows


def convergence_orders(rows: list[LimitExperiment]) -> list[dict[str, float | str]]:
    output: list[dict[str, float | str]] = []
    methods = sorted({row.method for row in rows})

    for method in methods:
        values = sorted([row for row in rows if row.method == method], key=lambda item: item.h, reverse=True)
        for large, small in zip(values, values[1:]):
            output.append({
                "method": method,
                "h_large": large.h,
                "h_small": small.h,
                "error_large": large.absolute_error,
                "error_small": small.absolute_error,
                "estimated_order": estimate_order(large.absolute_error, small.absolute_error, large.h / small.h),
            })

    return output


def epsilon_band_review(rows: list[LimitExperiment], epsilons: list[float]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for row in rows:
        for epsilon in epsilons:
            output.append({
                "method": row.method,
                "h": row.h,
                "epsilon": epsilon,
                "absolute_error": row.absolute_error,
                "inside_epsilon": row.absolute_error < epsilon,
            })
    return output


def load_step_sizes(path: Path) -> list[float]:
    with path.open("r", encoding="utf-8") as handle:
        return [float(row["h"]) for row in csv.DictReader(handle)]


def load_epsilons(path: Path) -> list[float]:
    with path.open("r", encoding="utf-8") as handle:
        return [float(row["epsilon"]) for row in csv.DictReader(handle)]


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


def to_dicts(rows: list[LimitExperiment]) -> list[dict[str, object]]:
    return [asdict(row) for row in rows]
