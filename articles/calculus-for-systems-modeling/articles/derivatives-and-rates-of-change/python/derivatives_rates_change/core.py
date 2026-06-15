from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class RateDiagnostic:
    method: str
    x0: float
    h: float
    estimate: float
    exact: float
    absolute_error: float
    relative_rate: float | None
    warning: str


@dataclass(frozen=True)
class VectorFieldRecord:
    state: float
    parameter: float
    rate: float
    inside_invariant_domain: bool
    warning: str


def system_response(x: float) -> float:
    return math.exp(0.2 * x)


def exact_derivative(x: float) -> float:
    return 0.2 * math.exp(0.2 * x)


def average_rate(a: float, b: float) -> float:
    if a == b:
        raise ValueError("average rate requires a nonzero interval")
    return (system_response(b) - system_response(a)) / (b - a)


def forward_difference(x: float, h: float) -> float:
    if h <= 0:
        raise ValueError("h must be positive")
    return (system_response(x + h) - system_response(x)) / h


def backward_difference(x: float, h: float) -> float:
    if h <= 0:
        raise ValueError("h must be positive")
    return (system_response(x) - system_response(x - h)) / h


def central_difference(x: float, h: float) -> float:
    if h <= 0:
        raise ValueError("h must be positive")
    return (system_response(x + h) - system_response(x - h)) / (2.0 * h)


def elasticity(derivative: float, x: float) -> float | None:
    y = system_response(x)
    if x == 0 or y == 0:
        return None
    return (x / y) * derivative


def rate_diagnostics(x0: float, h_values: list[float]) -> list[RateDiagnostic]:
    exact = exact_derivative(x0)
    rows: list[RateDiagnostic] = []
    for h in h_values:
        estimates = {
            "average_rate_right": average_rate(x0, x0 + h),
            "forward_difference": forward_difference(x0, h),
            "backward_difference": backward_difference(x0, h),
            "central_difference": central_difference(x0, h),
        }
        for method, estimate in estimates.items():
            rows.append(
                RateDiagnostic(
                    method=method,
                    x0=x0,
                    h=h,
                    estimate=estimate,
                    exact=exact,
                    absolute_error=abs(estimate - exact),
                    relative_rate=elasticity(estimate, x0),
                    warning="step-size and domain review required" if h < 1e-8 else "",
                )
            )
    return rows


def estimate_order(error_large: float, error_small: float, ratio: float = 2.0) -> float:
    if error_large <= 0 or error_small <= 0:
        return float("nan")
    return math.log(error_large / error_small) / math.log(ratio)


def convergence_orders(rows: list[RateDiagnostic]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for method in sorted({row.method for row in rows}):
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


def logistic_rate(state: float, r: float = 0.6, carrying_capacity: float = 1.0) -> float:
    return r * state * (1.0 - state / carrying_capacity)


def vector_field_records(states: list[float]) -> list[VectorFieldRecord]:
    rows: list[VectorFieldRecord] = []
    for state in states:
        inside = 0.0 <= state <= 1.0
        rows.append(VectorFieldRecord(state, 0.6, logistic_rate(state), inside, "" if inside else "state outside invariant domain [0,1]"))
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
