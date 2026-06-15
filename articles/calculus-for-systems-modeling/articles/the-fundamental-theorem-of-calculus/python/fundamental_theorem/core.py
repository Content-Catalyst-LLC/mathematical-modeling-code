from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class FundamentalTheoremAudit:
    interval_start: float
    interval_end: float
    state_start: float
    state_end: float
    endpoint_difference: float
    accumulated_rate: float
    residual: float
    method: str
    unit_check: str
    warning: str


def state(t: float) -> float:
    return 50.0 + 2.0 * t + 3.0 * math.sin(t)


def rate(t: float) -> float:
    return 2.0 + 3.0 * math.cos(t)


def trapezoid_integral(times: list[float]) -> float:
    if len(times) < 2:
        raise ValueError("At least two time points are required.")
    total = 0.0
    for previous, current in zip(times[:-1], times[1:]):
        dt = current - previous
        if dt <= 0:
            raise ValueError("Times must be strictly increasing.")
        total += 0.5 * (rate(previous) + rate(current)) * dt
    return total


def left_rectangle_integral(times: list[float]) -> float:
    if len(times) < 2:
        raise ValueError("At least two time points are required.")
    total = 0.0
    for previous, current in zip(times[:-1], times[1:]):
        dt = current - previous
        if dt <= 0:
            raise ValueError("Times must be strictly increasing.")
        total += rate(previous) * dt
    return total


def audit(times: list[float]) -> FundamentalTheoremAudit:
    a = times[0]
    b = times[-1]
    state_start = state(a)
    state_end = state(b)
    endpoint_difference = state_end - state_start
    accumulated_rate = trapezoid_integral(times)
    residual = endpoint_difference - accumulated_rate

    warnings: list[str] = []
    if abs(residual) > 1e-2:
        warnings.append("endpoint difference and accumulated rate do not closely match")
    if max(times[i + 1] - times[i] for i in range(len(times) - 1)) > 0.5:
        warnings.append("large grid step; refine integration")

    return FundamentalTheoremAudit(
        interval_start=a,
        interval_end=b,
        state_start=state_start,
        state_end=state_end,
        endpoint_difference=endpoint_difference,
        accumulated_rate=accumulated_rate,
        residual=residual,
        method="trapezoidal approximation",
        unit_check="rate units times time units = state units",
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
