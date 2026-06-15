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


def initial_stock_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("initial stock documented", flag, passed, "" if passed else "ending-stock claim lacks documented initial condition")


def sign_convention_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("sign convention documented", flag, passed, "" if passed else "net-flow sign convention is ambiguous")


def gross_flow_reporting_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("gross flows reported", flag, passed, "" if passed else "net change may hide large offsetting activity")


def exposure_window_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("exposure window documented", flag, passed, "" if passed else "cumulative exposure lacks measurement window")


def unit_consistency_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("unit consistency documented", flag, passed, "" if passed else "rate-time units do not reconcile with stock or exposure units")


def sample_checks() -> list[ConditionCheck]:
    return [
        initial_stock_check(1.0),
        initial_stock_check(0.0),
        sign_convention_check(1.0),
        sign_convention_check(0.0),
        gross_flow_reporting_check(1.0),
        gross_flow_reporting_check(0.0),
        exposure_window_check(1.0),
        exposure_window_check(0.0),
        unit_consistency_check(1.0),
        unit_consistency_check(0.0),
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
