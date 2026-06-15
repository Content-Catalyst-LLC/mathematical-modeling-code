from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class IntegralAudit:
    interval_start: float
    interval_end: float
    method: str
    signed_accumulation: float
    absolute_accumulation: float
    unit_check: str
    interpretation: str
    warning: str


def net_rate(t: float) -> float:
    return 4.0 * math.sin(t / 2.0) + 1.0


def signed_values(times: list[float]) -> list[float]:
    return [net_rate(t) for t in times]


def trapezoid_integral(values: list[float], times: list[float]) -> float:
    if len(values) != len(times):
        raise ValueError("Values and times must have the same length.")
    if len(times) < 2:
        raise ValueError("At least two time points are required.")

    total = 0.0
    for i in range(len(times) - 1):
        dt = times[i + 1] - times[i]
        if dt <= 0:
            raise ValueError("Times must be strictly increasing.")
        total += 0.5 * (values[i] + values[i + 1]) * dt
    return total


def rectangle_integral(values: list[float], times: list[float]) -> float:
    if len(values) != len(times):
        raise ValueError("Values and times must have the same length.")
    if len(times) < 2:
        raise ValueError("At least two time points are required.")

    total = 0.0
    for i in range(len(times) - 1):
        dt = times[i + 1] - times[i]
        if dt <= 0:
            raise ValueError("Times must be strictly increasing.")
        total += values[i] * dt
    return total


def audit_integral(times: list[float]) -> IntegralAudit:
    rates = signed_values(times)
    signed = trapezoid_integral(rates, times)
    absolute = trapezoid_integral([abs(r) for r in rates], times)

    warnings: list[str] = []
    if any(r < 0 for r in rates) and abs(signed) < absolute:
        warnings.append("signed accumulation includes cancellation")
    if max(times[i + 1] - times[i] for i in range(len(times) - 1)) > 1.0:
        warnings.append("large time step; review numerical accuracy")
    if abs(signed) < 0.25 * absolute:
        warnings.append("small net change relative to total activity")

    return IntegralAudit(
        interval_start=times[0],
        interval_end=times[-1],
        method="trapezoidal approximation",
        signed_accumulation=signed,
        absolute_accumulation=absolute,
        unit_check="rate units times time units = accumulated quantity units",
        interpretation="signed accumulation estimates net change; absolute accumulation estimates total activity",
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
