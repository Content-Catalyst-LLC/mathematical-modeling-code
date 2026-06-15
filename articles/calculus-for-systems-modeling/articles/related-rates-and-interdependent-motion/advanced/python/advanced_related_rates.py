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


def domain_check(value: float, lower: float = 0.0) -> ConditionCheck:
    passed = value > lower
    return ConditionCheck("physical domain", value, passed, "" if passed else "state outside physical domain")


def derivative_conditioning_check(value: float, threshold: float = 1e-8) -> ConditionCheck:
    passed = abs(value) > threshold
    return ConditionCheck("rate-conversion derivative", value, passed, "" if passed else "rate conversion is zero or near singular")


def finite_difference_error_check(value: float, threshold: float = 1e-5) -> ConditionCheck:
    passed = abs(value) <= threshold
    return ConditionCheck("finite-difference error", value, passed, "" if passed else "finite-difference check differs from analytic related rate")


def unit_review_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("unit review", flag, passed, "" if passed else "units not documented or inconsistent")


def sample_checks() -> list[ConditionCheck]:
    return [
        domain_check(2.0),
        domain_check(-1.0),
        derivative_conditioning_check(24.0),
        derivative_conditioning_check(0.0),
        finite_difference_error_check(1e-8),
        finite_difference_error_check(1e-2),
        unit_review_check(1.0),
        unit_review_check(0.0),
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
