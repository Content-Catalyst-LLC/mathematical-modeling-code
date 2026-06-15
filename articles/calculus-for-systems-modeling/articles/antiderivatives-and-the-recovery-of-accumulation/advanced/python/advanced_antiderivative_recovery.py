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


def initial_condition_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("initial condition documented", flag, passed, "" if passed else "recovered accumulation lacks a documented baseline")


def unit_consistency_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("unit consistency documented", flag, passed, "" if passed else "rate-variable accumulation units are not documented")


def time_grid_check(max_dt: float, threshold: float = 2.0) -> ConditionCheck:
    passed = max_dt <= threshold
    return ConditionCheck("time-step size", max_dt, passed, "" if passed else "large time step may distort numerical accumulation")


def missing_flow_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("missing-flow review documented", flag, passed, "" if passed else "missing inflows or outflows may invalidate recovered stock")


def domain_interval_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("domain interval documented", flag, passed, "" if passed else "accumulation interval exceeds or lacks documented model support")


def sample_checks() -> list[ConditionCheck]:
    return [
        initial_condition_check(1.0),
        initial_condition_check(0.0),
        unit_consistency_check(1.0),
        unit_consistency_check(0.0),
        time_grid_check(1.0),
        time_grid_check(5.0),
        missing_flow_check(1.0),
        missing_flow_check(0.0),
        domain_interval_check(1.0),
        domain_interval_check(0.0),
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
