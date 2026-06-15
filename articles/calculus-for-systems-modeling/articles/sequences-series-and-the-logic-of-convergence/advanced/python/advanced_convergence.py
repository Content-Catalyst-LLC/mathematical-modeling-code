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


def sequence_defined_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("sequence definition documented", flag, passed, "" if passed else "convergence claim lacks a defined sequence or series")


def stopping_rule_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("stopping rule documented", flag, passed, "" if passed else "computation stopped without a documented stopping rule")


def remainder_bound_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("remainder bound documented", flag, passed, "" if passed else "finite approximation lacks a tail or error estimate")


def latest_term_test(last_term: float, tail_bound: float | None) -> ConditionCheck:
    passed = tail_bound is not None
    return ConditionCheck("latest term not used as tail proof", last_term, passed, "" if passed else "small latest term alone does not bound the full remaining tail")


def absolute_convergence_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("absolute convergence reviewed", flag, passed, "" if passed else "signed convergence may hide large gross activity")


def sample_checks() -> list[ConditionCheck]:
    return [
        sequence_defined_check(1.0),
        sequence_defined_check(0.0),
        stopping_rule_check(1.0),
        stopping_rule_check(0.0),
        remainder_bound_check(1.0),
        remainder_bound_check(0.0),
        latest_term_test(0.0001, 0.001),
        latest_term_test(0.0001, None),
        absolute_convergence_check(1.0),
        absolute_convergence_check(0.0),
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
