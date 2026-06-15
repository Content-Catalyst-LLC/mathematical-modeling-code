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
    return ConditionCheck("decomposition residual tolerance", residual, passed, "" if passed else "direct and decomposed accumulation differ beyond tolerance")


def unit_consistency_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("unit consistency documented", flag, passed, "" if passed else "direct boundary and residual terms lack shared product units")


def boundary_interpretation_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("boundary term interpreted", flag, passed, "" if passed else "boundary term lacks endpoint interpretation")


def residual_interpretation_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("residual integral interpreted", flag, passed, "" if passed else "residual integral lacks system interpretation")


def causal_claim_check(flag: float) -> ConditionCheck:
    passed = flag == 0.0
    return ConditionCheck("causal overclaim avoided", flag, passed, "" if passed else "decomposition identity is being overread as causal proof")


def sample_checks() -> list[ConditionCheck]:
    return [
        residual_tolerance_check(1e-5),
        residual_tolerance_check(1e-1),
        unit_consistency_check(1.0),
        unit_consistency_check(0.0),
        boundary_interpretation_check(1.0),
        boundary_interpretation_check(0.0),
        residual_interpretation_check(1.0),
        residual_interpretation_check(0.0),
        causal_claim_check(0.0),
        causal_claim_check(1.0),
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
