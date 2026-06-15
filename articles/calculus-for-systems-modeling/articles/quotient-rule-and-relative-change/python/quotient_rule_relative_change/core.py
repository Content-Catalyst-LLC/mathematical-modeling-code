from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class QuotientAudit:
    t: float
    numerator: float
    denominator: float
    ratio: float
    numerator_rate: float
    denominator_rate: float
    numerator_effect: float
    denominator_effect: float
    quotient_derivative: float
    numerator_relative_rate: float
    denominator_relative_rate: float
    ratio_relative_rate: float
    warning: str


def resource_stock(t: float) -> float:
    return 1000.0 * math.exp(-0.01 * t)


def resource_stock_rate(t: float) -> float:
    return -0.01 * resource_stock(t)


def population(t: float) -> float:
    return 100.0 * math.exp(0.02 * t)


def population_rate(t: float) -> float:
    return 0.02 * population(t)


def quotient_audit(t: float, threshold: float = 1e-8) -> QuotientAudit:
    f = resource_stock(t)
    g = population(t)
    fp = resource_stock_rate(t)
    gp = population_rate(t)

    if abs(g) <= threshold:
        raise ValueError("denominator too close to zero")

    ratio = f / g
    numerator_effect = fp / g
    denominator_effect = -(f * gp) / (g ** 2)
    derivative = numerator_effect + denominator_effect

    return QuotientAudit(
        t=t,
        numerator=f,
        denominator=g,
        ratio=ratio,
        numerator_rate=fp,
        denominator_rate=gp,
        numerator_effect=numerator_effect,
        denominator_effect=denominator_effect,
        quotient_derivative=derivative,
        numerator_relative_rate=fp / f,
        denominator_relative_rate=gp / g,
        ratio_relative_rate=derivative / ratio,
        warning="small denominator; ratio derivative may be unstable" if abs(g) < 1.0 else "",
    )


def quotient_audits(times: list[float]) -> list[QuotientAudit]:
    return [quotient_audit(t) for t in times]


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
