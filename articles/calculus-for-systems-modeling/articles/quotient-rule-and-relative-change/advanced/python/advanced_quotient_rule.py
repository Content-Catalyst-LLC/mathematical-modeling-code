from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class ConditionCheck:
    condition: str
    value: float
    passed: bool
    warning: str


def denominator_check(value: float, threshold: float = 1e-8) -> ConditionCheck:
    passed = abs(value) > threshold
    return ConditionCheck("nonzero denominator", value, passed, "" if passed else "denominator is zero or near zero")


def positivity_check(value: float) -> ConditionCheck:
    passed = value > 0
    return ConditionCheck("positive quantity for logarithmic relative-rate interpretation", value, passed, "" if passed else "relative-rate logarithmic interpretation requires positivity")


def relative_rate_identity(n_rel: float, d_rel: float, ratio_rel: float, tolerance: float = 1e-10) -> ConditionCheck:
    residual = ratio_rel - (n_rel - d_rel)
    passed = abs(residual) <= tolerance
    return ConditionCheck("relative-rate identity", residual, passed, "" if passed else "R'/R does not match f'/f - g'/g within tolerance")


def sample_checks() -> list[ConditionCheck]:
    return [
        denominator_check(100.0),
        denominator_check(0.0),
        positivity_check(10.0),
        positivity_check(-2.0),
        relative_rate_identity(-0.01, 0.02, -0.03),
        relative_rate_identity(-0.01, 0.02, -0.02),
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def to_dicts(rows: list[object]) -> list[dict[str, object]]:
    return [asdict(row) for row in rows]
