from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class IntegrationByPartsAudit:
    interval_start: float
    interval_end: float
    direct_integral: float
    boundary_term: float
    residual_integral: float
    decomposed_value: float
    decomposition_residual: float
    method: str
    unit_check: str
    warning: str


def u(x: float) -> float:
    return 1.0 + x


def u_prime(x: float) -> float:
    return 1.0


def v(x: float) -> float:
    return math.exp(-0.3 * x) * math.sin(x)


def v_prime(x: float) -> float:
    return math.exp(-0.3 * x) * (math.cos(x) - 0.3 * math.sin(x))


def grid(a: float, b: float, n: int) -> list[float]:
    if a >= b:
        raise ValueError("Interval must satisfy a < b.")
    if n <= 0:
        raise ValueError("n must be positive.")
    return [a + (b - a) * i / n for i in range(n + 1)]


def trapezoid_integral(values: list[float], points: list[float]) -> float:
    if len(values) != len(points):
        raise ValueError("Values and points must have same length.")
    if len(points) < 2:
        raise ValueError("At least two grid points are required.")
    total = 0.0
    for i in range(len(points) - 1):
        dx = points[i + 1] - points[i]
        if dx <= 0:
            raise ValueError("Grid points must be strictly increasing.")
        total += 0.5 * (values[i] + values[i + 1]) * dx
    return total


def audit_integration_by_parts(a: float, b: float, n: int = 800) -> IntegrationByPartsAudit:
    points = grid(a, b, n)

    direct_values = [u(x) * v_prime(x) for x in points]
    residual_values = [v(x) * u_prime(x) for x in points]

    direct = trapezoid_integral(direct_values, points)
    residual_integral = trapezoid_integral(residual_values, points)
    boundary = u(b) * v(b) - u(a) * v(a)
    decomposed = boundary - residual_integral
    decomposition_residual = direct - decomposed

    warnings: list[str] = []
    if abs(decomposition_residual) > 1e-3:
        warnings.append("decomposition residual exceeds tolerance")
    if n < 200:
        warnings.append("coarse grid may distort decomposition")

    return IntegrationByPartsAudit(
        interval_start=a,
        interval_end=b,
        direct_integral=direct,
        boundary_term=boundary,
        residual_integral=residual_integral,
        decomposed_value=decomposed,
        decomposition_residual=decomposition_residual,
        method="trapezoidal comparison",
        unit_check="u times v units are shared by direct, boundary, and residual terms",
        warning="; ".join(warnings),
    )


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
