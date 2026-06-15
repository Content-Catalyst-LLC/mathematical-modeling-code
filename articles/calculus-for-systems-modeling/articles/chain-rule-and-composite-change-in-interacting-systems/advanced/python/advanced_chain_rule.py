from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class ConditionCheck:
    condition: str
    value: str
    passed: bool
    warning: str


def domain_compatibility_check(inner_value: float, lower: float, upper: float) -> ConditionCheck:
    passed = lower <= inner_value <= upper
    return ConditionCheck("domain compatibility", f"{inner_value} in [{lower}, {upper}]", passed, "" if passed else "inner value outside outer function domain")


def differentiable_links_check(flags: list[bool]) -> ConditionCheck:
    passed = all(flags)
    return ConditionCheck("differentiable links", str(flags), passed, "" if passed else "at least one pathway link is not differentiable")


def local_validity_check(distance_from_operating_point: float, tolerance: float = 1.0) -> ConditionCheck:
    passed = abs(distance_from_operating_point) <= tolerance
    return ConditionCheck("local validity", str(distance_from_operating_point), passed, "" if passed else "local derivative may be overextended")


def implementation_warning_check(has_conditionals: bool) -> ConditionCheck:
    passed = not has_conditionals
    return ConditionCheck("automatic differentiation implementation", str(has_conditionals), passed, "" if passed else "implementation contains branches or conditionals requiring review")


def sample_checks() -> list[ConditionCheck]:
    return [
        domain_compatibility_check(0.5, 0.0, 1.0),
        domain_compatibility_check(1.5, 0.0, 1.0),
        differentiable_links_check([True, True, True]),
        differentiable_links_check([True, False, True]),
        local_validity_check(0.2),
        local_validity_check(5.0),
        implementation_warning_check(False),
        implementation_warning_check(True),
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
