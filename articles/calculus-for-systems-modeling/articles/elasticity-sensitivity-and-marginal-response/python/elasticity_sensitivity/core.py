from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class ElasticityAudit:
    x: float
    value: float
    derivative: float
    elasticity: float | None
    finite_difference_derivative: float
    absolute_error: float
    response_class: str
    warning: str


def response_function(x: float) -> float:
    if x < -1.0:
        raise ValueError("response_function requires x >= -1")
    return 10.0 * math.sqrt(x + 1.0)


def analytic_derivative(x: float) -> float:
    if x <= -1.0:
        raise ValueError("analytic_derivative requires x > -1")
    return 5.0 / math.sqrt(x + 1.0)


def finite_difference_derivative(x: float, h: float = 1e-5) -> float:
    if x - h < -1.0:
        raise ValueError("finite difference would leave model domain")
    return (response_function(x + h) - response_function(x - h)) / (2.0 * h)


def classify_response(elasticity: float | None) -> str:
    if elasticity is None:
        return "elasticity undefined"
    if abs(elasticity) < 1.0:
        return "inelastic local response"
    if abs(elasticity) == 1.0:
        return "unit elastic local response"
    return "elastic local response"


def audit_point(x: float) -> ElasticityAudit:
    y = response_function(x)
    derivative = analytic_derivative(x)
    finite_difference = finite_difference_derivative(x)
    error = abs(derivative - finite_difference)

    warnings: list[str] = []
    elasticity = None

    if x == 0.0:
        warnings.append("input is zero; proportional input change requires care")
    if y == 0.0:
        warnings.append("output is zero; elasticity undefined")
    if x != 0.0 and y != 0.0:
        elasticity = (x / y) * derivative
    if error > 1e-5:
        warnings.append("finite-difference check differs from analytic derivative")
    if x < 0.1:
        warnings.append("near-zero baseline; normalize with caution")

    return ElasticityAudit(
        x=x,
        value=y,
        derivative=derivative,
        elasticity=elasticity,
        finite_difference_derivative=finite_difference,
        absolute_error=error,
        response_class=classify_response(elasticity),
        warning="; ".join(warnings),
    )


def audits(points: list[float]) -> list[ElasticityAudit]:
    return [audit_point(x) for x in points]


def to_dicts(rows: list[object]) -> list[dict[str, object]]:
    return [asdict(row) for row in rows]


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
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
