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


def interval_length_check(length: float) -> ConditionCheck:
    passed = length > 0.0
    return ConditionCheck("positive interval length", length, passed, "" if passed else "definite integral requires a nonzero oriented interval for total-change interpretation")


def unit_consistency_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("unit consistency documented", flag, passed, "" if passed else "integrand units and integration variable units are not documented")


def sign_convention_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("sign convention documented", flag, passed, "" if passed else "signed accumulation may be confused with total activity")


def numerical_method_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("numerical method documented", flag, passed, "" if passed else "approximate total change lacks method documentation")


def grid_size_check(max_dt: float, threshold: float = 1.0) -> ConditionCheck:
    passed = max_dt <= threshold
    return ConditionCheck("grid spacing", max_dt, passed, "" if passed else "coarse grid may miss bursts, peaks, or discontinuities")


def sample_checks() -> list[ConditionCheck]:
    return [
        interval_length_check(4.0),
        interval_length_check(0.0),
        unit_consistency_check(1.0),
        unit_consistency_check(0.0),
        sign_convention_check(1.0),
        sign_convention_check(0.0),
        numerical_method_check(1.0),
        numerical_method_check(0.0),
        grid_size_check(0.5),
        grid_size_check(2.0),
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
