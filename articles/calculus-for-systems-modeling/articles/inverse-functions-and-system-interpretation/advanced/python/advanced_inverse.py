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


def derivative_invertibility_check(value: float, threshold: float = 1e-8) -> ConditionCheck:
    passed = abs(value) > threshold
    return ConditionCheck("nonzero derivative for local inverse", value, passed, "" if passed else "forward derivative is zero or near zero")


def jacobian_conditioning_check(condition_number: float, threshold: float = 1e8) -> ConditionCheck:
    passed = condition_number < threshold
    return ConditionCheck("Jacobian conditioning", condition_number, passed, "" if passed else "inverse map may be unstable under output noise")


def domain_check(value: float, lower: float) -> ConditionCheck:
    passed = value > lower
    return ConditionCheck("domain validity", value, passed, "" if passed else "recovered input is outside admissible domain")


def residual_check(residual: float, threshold: float = 1e-8) -> ConditionCheck:
    passed = abs(residual) <= threshold
    return ConditionCheck("forward consistency residual", residual, passed, "" if passed else "forward check does not reproduce target output")


def sample_checks() -> list[ConditionCheck]:
    return [
        derivative_invertibility_check(0.5),
        derivative_invertibility_check(0.0),
        jacobian_conditioning_check(100.0),
        jacobian_conditioning_check(1e10),
        domain_check(0.2, -1.0),
        domain_check(-2.0, -1.0),
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
