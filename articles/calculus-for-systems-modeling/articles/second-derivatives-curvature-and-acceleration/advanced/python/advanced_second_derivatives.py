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


def smoothness_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("twice differentiability", flag, passed, "" if passed else "second derivative claim lacks smoothness support")


def inflection_sign_change_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("inflection sign change", flag, passed, "" if passed else "f''=0 alone does not prove inflection")


def finite_difference_error_check(value: float, threshold: float = 1e-5) -> ConditionCheck:
    passed = abs(value) <= threshold
    return ConditionCheck("finite-difference second-derivative error", value, passed, "" if passed else "second derivative estimate is unstable or inaccurate")


def noise_review_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("noise and smoothing review", flag, passed, "" if passed else "noise or smoothing assumptions are not documented")


def sample_checks() -> list[ConditionCheck]:
    return [
        smoothness_check(1.0),
        smoothness_check(0.0),
        inflection_sign_change_check(1.0),
        inflection_sign_change_check(0.0),
        finite_difference_error_check(1e-8),
        finite_difference_error_check(1e-2),
        noise_review_check(1.0),
        noise_review_check(0.0),
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
