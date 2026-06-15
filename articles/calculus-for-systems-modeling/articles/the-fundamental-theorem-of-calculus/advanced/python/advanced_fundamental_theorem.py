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


def residual_tolerance_check(residual: float, tolerance: float = 1e-2) -> ConditionCheck:
    passed = abs(residual) <= tolerance
    return ConditionCheck("rate-state residual tolerance", residual, passed, "" if passed else "accumulated rate does not match endpoint difference within tolerance")


def interval_length_check(length: float) -> ConditionCheck:
    passed = length > 0.0
    return ConditionCheck("positive interval length", length, passed, "" if passed else "FTC audit requires a nonzero interval")


def unit_consistency_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("unit consistency documented", flag, passed, "" if passed else "rate units and state units are not reconciled")


def baseline_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("baseline state documented", flag, passed, "" if passed else "state reconstruction lacks a baseline")


def grid_step_check(max_dt: float, threshold: float = 0.5) -> ConditionCheck:
    passed = max_dt <= threshold
    return ConditionCheck("grid spacing", max_dt, passed, "" if passed else "coarse grid may distort accumulated rate")


def sample_checks() -> list[ConditionCheck]:
    return [
        residual_tolerance_check(1e-4),
        residual_tolerance_check(5e-2),
        interval_length_check(2.0),
        interval_length_check(0.0),
        unit_consistency_check(1.0),
        unit_consistency_check(0.0),
        baseline_check(1.0),
        baseline_check(0.0),
        grid_step_check(0.25),
        grid_step_check(2.0),
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
