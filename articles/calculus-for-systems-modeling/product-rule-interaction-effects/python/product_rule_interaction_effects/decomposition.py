from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import math
from statistics import mean


@dataclass(frozen=True)
class ProductRuleRow:
    time: float
    factor_a: float
    factor_b: float
    product_y: float
    a_prime: float
    b_prime: float
    direct_y_prime: float
    contribution_from_a: float
    contribution_from_b: float
    product_rule_y_prime: float
    residual: float


def central_difference(values: list[float], time: list[float]) -> list[float]:
    if len(values) != len(time):
        raise ValueError("values and time must have the same length")
    if len(values) < 3:
        raise ValueError("at least three points are required")

    derivative = [0.0] * len(values)
    derivative[0] = (values[1] - values[0]) / (time[1] - time[0])
    derivative[-1] = (values[-1] - values[-2]) / (time[-1] - time[-2])

    for i in range(1, len(values) - 1):
        derivative[i] = (values[i + 1] - values[i - 1]) / (time[i + 1] - time[i - 1])

    return derivative


def build_synthetic_series(n: int = 401) -> tuple[list[float], list[float], list[float]]:
    if n < 3:
        raise ValueError("n must be at least 3")

    time = [20.0 * i / (n - 1) for i in range(n)]
    factor_a = [100.0 + 4.0 * t + 8.0 * math.sin(0.4 * t) for t in time]
    factor_b = [1.2 + 0.03 * t + 0.15 * math.cos(0.25 * t) for t in time]
    return time, factor_a, factor_b


def decompose_product_rule(time: list[float], factor_a: list[float], factor_b: list[float]) -> list[ProductRuleRow]:
    if not (len(time) == len(factor_a) == len(factor_b)):
        raise ValueError("time, factor_a, and factor_b must have the same length")

    product_y = [a * b for a, b in zip(factor_a, factor_b)]
    a_prime = central_difference(factor_a, time)
    b_prime = central_difference(factor_b, time)
    direct_y_prime = central_difference(product_y, time)

    rows: list[ProductRuleRow] = []
    for t, a, b, y, da, db, dy in zip(time, factor_a, factor_b, product_y, a_prime, b_prime, direct_y_prime):
        contribution_from_a = da * b
        contribution_from_b = a * db
        product_rule_y_prime = contribution_from_a + contribution_from_b
        residual = dy - product_rule_y_prime
        rows.append(ProductRuleRow(t, a, b, y, da, db, dy, contribution_from_a, contribution_from_b, product_rule_y_prime, residual))
    return rows


def summarize(rows: list[ProductRuleRow]) -> dict[str, float]:
    if not rows:
        raise ValueError("rows cannot be empty")

    return {
        "max_abs_residual": max(abs(row.residual) for row in rows),
        "mean_abs_residual": mean(abs(row.residual) for row in rows),
        "mean_abs_contribution_from_a": mean(abs(row.contribution_from_a) for row in rows),
        "mean_abs_contribution_from_b": mean(abs(row.contribution_from_b) for row in rows),
        "mean_direct_y_prime": mean(row.direct_y_prime for row in rows),
    }


def write_rows_csv(path: Path, rows: list[ProductRuleRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(ProductRuleRow.__dataclass_fields__.keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_summary_csv(path: Path, summary: dict[str, float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        for metric, value in summary.items():
            writer.writerow({"metric": metric, "value": value})


def run_default_workflow(base_dir: Path | None = None) -> dict[str, float]:
    root = base_dir or Path(".")
    time, factor_a, factor_b = build_synthetic_series()
    rows = decompose_product_rule(time, factor_a, factor_b)
    summary = summarize(rows)

    write_rows_csv(root / "outputs" / "tables" / "product_rule_decomposition_python.csv", rows)
    write_summary_csv(root / "outputs" / "tables" / "product_rule_summary_python.csv", summary)

    return summary
