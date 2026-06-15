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


def test_selected_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("convergence test selected", flag, passed, "" if passed else "infinite approximation lacks a named test or bound")


def test_conditions_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("test conditions verified", flag, passed, "" if passed else "selected test conditions were not verified")


def term_test_misuse_check(terms_go_to_zero: float, claimed_convergence_from_terms_only: float) -> ConditionCheck:
    passed = not (terms_go_to_zero == 1.0 and claimed_convergence_from_terms_only == 1.0)
    return ConditionCheck("term test not used backward", claimed_convergence_from_terms_only, passed, "" if passed else "terms going to zero is not sufficient to prove convergence")


def remainder_estimate_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("remainder estimate documented", flag, passed, "" if passed else "finite partial sum lacks tail or error estimate")


def inconclusive_result_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("inconclusive result handled", flag, passed, "" if passed else "inconclusive test result was overread as a conclusion")


def sample_checks() -> list[ConditionCheck]:
    return [
        test_selected_check(1.0),
        test_selected_check(0.0),
        test_conditions_check(1.0),
        test_conditions_check(0.0),
        term_test_misuse_check(1.0, 0.0),
        term_test_misuse_check(1.0, 1.0),
        remainder_estimate_check(1.0),
        remainder_estimate_check(0.0),
        inconclusive_result_check(1.0),
        inconclusive_result_check(0.0),
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
