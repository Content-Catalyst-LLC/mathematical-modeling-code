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


def regularity_check(value: float, threshold: float = 1e-8) -> ConditionCheck:
    passed = abs(value) > threshold
    return ConditionCheck("regularity condition", value, passed, "" if passed else "partial derivative or Jacobian block is singular or near singular")


def conditioning_check(condition_number: float, threshold: float = 1e8) -> ConditionCheck:
    passed = condition_number < threshold
    return ConditionCheck("Jacobian conditioning", condition_number, passed, "" if passed else "Jacobian is ill-conditioned")


def branch_distance_check(distance: float, threshold: float = 1.0) -> ConditionCheck:
    passed = abs(distance) <= threshold
    return ConditionCheck("local branch validity", distance, passed, "" if passed else "local derivative may be overextended from its branch")


def residual_check(residual: float, threshold: float = 1e-8) -> ConditionCheck:
    passed = abs(residual) <= threshold
    return ConditionCheck("constraint residual", residual, passed, "" if passed else "constraint residual is too large")


def sample_checks() -> list[ConditionCheck]:
    return [
        regularity_check(2.0),
        regularity_check(0.0),
        conditioning_check(100.0),
        conditioning_check(1e10),
        branch_distance_check(0.2),
        branch_distance_check(3.0),
        residual_check(1e-10),
        residual_check(1e-2),
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
