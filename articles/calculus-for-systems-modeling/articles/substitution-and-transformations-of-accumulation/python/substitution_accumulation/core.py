from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class SubstitutionAudit:
    original_start: float
    original_end: float
    transformed_start: float
    transformed_end: float
    direct_integral: float
    transformed_integral: float
    residual: float
    method: str
    unit_check: str
    warning: str


def g(x: float) -> float:
    return x * x + 1.0


def g_prime(x: float) -> float:
    return 2.0 * x


def f(u: float) -> float:
    return math.sqrt(u)


def transformed_integrand_x(x: float) -> float:
    return f(g(x)) * g_prime(x)


def grid(a: float, b: float, n: int) -> list[float]:
    if n <= 0:
        raise ValueError("n must be positive.")
    return [a + (b - a) * i / n for i in range(n + 1)]


def trapezoid_integral(values: list[float], points: list[float]) -> float:
    if len(values) != len(points):
        raise ValueError("Values and points must have the same length.")
    if len(points) < 2:
        raise ValueError("At least two grid points are required.")
    total = 0.0
    for i in range(len(points) - 1):
        step = points[i + 1] - points[i]
        if step <= 0:
            raise ValueError("Grid points must be strictly increasing.")
        total += 0.5 * (values[i] + values[i + 1]) * step
    return total


def audit_substitution(a: float, b: float, n: int = 400) -> SubstitutionAudit:
    if a >= b:
        raise ValueError("Original interval must satisfy a < b.")

    x_points = grid(a, b, n)
    direct_values = [transformed_integrand_x(x) for x in x_points]
    direct = trapezoid_integral(direct_values, x_points)

    u_start = g(a)
    u_end = g(b)
    if u_start >= u_end:
        raise ValueError("Transformed interval is not increasing; use orientation-aware or piecewise handling.")

    u_points = grid(u_start, u_end, n)
    u_values = [f(u) for u in u_points]
    transformed = trapezoid_integral(u_values, u_points)

    residual = direct - transformed
    warnings: list[str] = []
    if abs(residual) > 1e-3:
        warnings.append("direct and transformed accumulation differ beyond tolerance")
    if min(g_prime(x) for x in x_points) <= 0:
        warnings.append("check monotonicity over interval")
    if abs(u_end - u_start) == abs(b - a):
        warnings.append("scale factor may be hidden by special interval geometry")

    return SubstitutionAudit(
        original_start=a,
        original_end=b,
        transformed_start=u_start,
        transformed_end=u_end,
        direct_integral=direct,
        transformed_integral=transformed,
        residual=residual,
        method="trapezoidal comparison",
        unit_check="f(u) du equals f(g(x)) g_prime(x) dx",
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
