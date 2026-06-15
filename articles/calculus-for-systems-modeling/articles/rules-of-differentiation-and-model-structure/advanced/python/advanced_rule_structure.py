from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class RuleCheck:
    rule: str
    condition: str
    passed: bool
    warning: str


def quotient_denominator_check(value: float, threshold: float = 1e-8) -> RuleCheck:
    passed = abs(value) > threshold
    return RuleCheck("quotient_rule", "denominator nonzero and not near zero", passed, "" if passed else "denominator near zero")


def chain_link_check(flags: list[bool]) -> RuleCheck:
    passed = all(flags)
    return RuleCheck("chain_rule", "all nested links differentiable", passed, "" if passed else "at least one chain link is not differentiable")


def implicit_regular_check(partial_y: float, threshold: float = 1e-8) -> RuleCheck:
    passed = abs(partial_y) > threshold
    return RuleCheck("implicit_differentiation", "regularity condition F_y != 0", passed, "" if passed else "implicit derivative may be undefined")


def log_positive_check(value: float) -> RuleCheck:
    passed = value > 0
    return RuleCheck("logarithmic_differentiation", "positive argument for logarithm", passed, "" if passed else "logarithmic differentiation requires positive quantity")


def sample_checks() -> list[RuleCheck]:
    return [
        quotient_denominator_check(100.0),
        quotient_denominator_check(0.0),
        chain_link_check([True, True, True]),
        chain_link_check([True, False, True]),
        implicit_regular_check(2.0),
        implicit_regular_check(0.0),
        log_positive_check(5.0),
        log_positive_check(-1.0),
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
