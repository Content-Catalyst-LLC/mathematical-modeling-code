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


def residual_tolerance_check(residual: float, tolerance: float = 1e-3) -> ConditionCheck:
    passed = abs(residual) <= tolerance
    return ConditionCheck("direct-transformed residual tolerance", residual, passed, "" if passed else "direct and transformed accumulation differ beyond tolerance")


def scale_factor_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("scale factor documented", flag, passed, "" if passed else "substitution lacks documented differential scale factor")


def transformed_bounds_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("transformed bounds documented", flag, passed, "" if passed else "definite integral uses changed variable without transformed bounds")


def unit_consistency_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("unit consistency documented", flag, passed, "" if passed else "units do not show preservation of accumulated quantity")


def monotonicity_check(min_derivative: float) -> ConditionCheck:
    passed = min_derivative > 0.0
    return ConditionCheck("monotonicity over interval", min_derivative, passed, "" if passed else "transformation may require piecewise treatment or orientation review")


def sample_checks() -> list[ConditionCheck]:
    return [
        residual_tolerance_check(1e-5),
        residual_tolerance_check(1e-1),
        scale_factor_check(1.0),
        scale_factor_check(0.0),
        transformed_bounds_check(1.0),
        transformed_bounds_check(0.0),
        unit_consistency_check(1.0),
        unit_consistency_check(0.0),
        monotonicity_check(0.2),
        monotonicity_check(-0.2),
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
