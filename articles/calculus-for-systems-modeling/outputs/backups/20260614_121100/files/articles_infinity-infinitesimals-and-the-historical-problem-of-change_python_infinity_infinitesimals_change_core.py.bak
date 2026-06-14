from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class ApproximationRecord:
    function_name: str
    x: float
    h: float
    estimate: float
    exact_value: float
    absolute_error: float


def system_response(x: float) -> float:
    """Synthetic smooth response function for derivative approximation."""
    return math.exp(0.2 * x)


def exact_derivative(x: float) -> float:
    return 0.2 * math.exp(0.2 * x)


def difference_quotient(x: float, h: float) -> float:
    if h <= 0:
        raise ValueError("h must be positive.")
    return (system_response(x + h) - system_response(x)) / h


def run_approximations(x: float, h_values: list[float]) -> list[ApproximationRecord]:
    exact = exact_derivative(x)
    records: list[ApproximationRecord] = []

    for h in h_values:
        estimate = difference_quotient(x, h)
        records.append(
            ApproximationRecord(
                function_name="exp(0.2x)",
                x=x,
                h=h,
                estimate=estimate,
                exact_value=exact,
                absolute_error=abs(estimate - exact),
            )
        )

    return records


def summarize_approximations(records: list[ApproximationRecord]) -> list[dict[str, object]]:
    if not records:
        return []

    best = min(records, key=lambda item: item.absolute_error)
    worst = max(records, key=lambda item: item.absolute_error)

    return [
        {
            "summary_key": "best_step",
            "h": best.h,
            "estimate": round(best.estimate, 12),
            "absolute_error": round(best.absolute_error, 12),
        },
        {
            "summary_key": "worst_step",
            "h": worst.h,
            "estimate": round(worst.estimate, 12),
            "absolute_error": round(worst.absolute_error, 12),
        },
    ]


def load_step_sizes(path: Path) -> list[float]:
    values: list[float] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            values.append(float(row["h"]))
    return values


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def build_manifest(records: list[ApproximationRecord]) -> dict[str, object]:
    return {
        "article": "Infinity, Infinitesimals, and the Historical Problem of Change",
        "series": "Calculus for Systems Modeling",
        "model": "difference quotient convergence for exp(0.2x)",
        "records": [asdict(item) for item in records],
        "summary": summarize_approximations(records),
        "interpretive_warning": "Synthetic teaching workflow. Convergence behavior in this smooth example does not guarantee empirical model validity.",
    }
