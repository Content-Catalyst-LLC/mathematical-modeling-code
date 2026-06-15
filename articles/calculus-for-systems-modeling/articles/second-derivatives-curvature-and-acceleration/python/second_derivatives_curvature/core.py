from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class SecondDerivativeAudit:
    x: float
    value: float
    first_derivative: float
    second_derivative: float
    curvature: float
    concavity: str
    finite_difference_second: float
    absolute_error: float
    warning: str


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def first_derivative(x: float) -> float:
    y = logistic(x)
    return y * (1.0 - y)


def second_derivative(x: float) -> float:
    y = logistic(x)
    return y * (1.0 - y) * (1.0 - 2.0 * y)


def curvature(x: float) -> float:
    fp = first_derivative(x)
    fpp = second_derivative(x)
    return abs(fpp) / ((1.0 + fp**2) ** 1.5)


def finite_difference_second(x: float, h: float = 1e-4) -> float:
    return (logistic(x + h) - 2.0 * logistic(x) + logistic(x - h)) / (h**2)


def classify_concavity(value: float, threshold: float = 1e-8) -> str:
    if value > threshold:
        return "concave up"
    if value < -threshold:
        return "concave down"
    return "near zero curvature candidate"


def audit_point(x: float) -> SecondDerivativeAudit:
    y = logistic(x)
    fp = first_derivative(x)
    fpp = second_derivative(x)
    kappa = curvature(x)
    fd = finite_difference_second(x)
    error = abs(fpp - fd)

    warning = ""
    if abs(fpp) < 1e-8:
        warning = "possible inflection candidate; verify concavity sign change"
    elif error > 1e-5:
        warning = "finite-difference second derivative differs from analytic value"

    return SecondDerivativeAudit(
        x=x,
        value=y,
        first_derivative=fp,
        second_derivative=fpp,
        curvature=kappa,
        concavity=classify_concavity(fpp),
        finite_difference_second=fd,
        absolute_error=error,
        warning=warning,
    )


def second_derivative_audits(points: list[float]) -> list[SecondDerivativeAudit]:
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
