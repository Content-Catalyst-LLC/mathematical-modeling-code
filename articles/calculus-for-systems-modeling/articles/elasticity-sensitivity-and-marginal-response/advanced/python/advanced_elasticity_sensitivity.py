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


def nonzero_input_check(x: float) -> ConditionCheck:
    passed = x != 0.0
    return ConditionCheck("nonzero input for elasticity", x, passed, "" if passed else "elasticity requires careful interpretation at zero input")


def nonzero_output_check(y: float) -> ConditionCheck:
    passed = y != 0.0
    return ConditionCheck("nonzero output for elasticity", y, passed, "" if passed else "elasticity is undefined at zero output")


def positive_log_domain_check(x: float, y: float) -> ConditionCheck:
    passed = x > 0.0 and y > 0.0
    return ConditionCheck("positive log domain", min(x, y), passed, "" if passed else "log-derivative interpretation requires positive input and output")


def finite_difference_error_check(value: float, threshold: float = 1e-5) -> ConditionCheck:
    passed = abs(value) <= threshold
    return ConditionCheck("finite-difference derivative error", value, passed, "" if passed else "finite-difference sensitivity is unstable or inaccurate")


def local_scope_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("local scope stated", flag, passed, "" if passed else "sensitivity claim lacks a stated baseline or local scope")


def sample_checks() -> list[ConditionCheck]:
    return [
        nonzero_input_check(0.0),
        nonzero_input_check(4.0),
        nonzero_output_check(0.0),
        nonzero_output_check(10.0),
        positive_log_domain_check(1.0, 10.0),
        positive_log_domain_check(-1.0, 10.0),
        finite_difference_error_check(1e-8),
        finite_difference_error_check(1e-2),
        local_scope_check(1.0),
        local_scope_check(0.0),
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
