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


def limiting_process_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("limiting process documented", flag, passed, "" if passed else "improper boundary lacks a defined limiting process")


def convergence_evidence_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("convergence evidence documented", flag, passed, "" if passed else "finite value lacks convergence evidence")


def truncation_sensitivity_check(tail_error: float, tolerance: float = 0.05) -> ConditionCheck:
    passed = abs(tail_error) <= tolerance
    return ConditionCheck("truncation tail error", tail_error, passed, "" if passed else "tail contribution remains material at selected cutoff")


def p_tail_check(p: float) -> ConditionCheck:
    passed = p > 1.0
    return ConditionCheck("p-tail convergence", p, passed, "" if passed else "p-tail integral diverges for p <= 1")


def model_domain_check(flag: float) -> ConditionCheck:
    passed = flag == 1.0
    return ConditionCheck("model validity boundary documented", flag, passed, "" if passed else "limit may extend beyond credible model domain")


def sample_checks() -> list[ConditionCheck]:
    return [
        limiting_process_check(1.0),
        limiting_process_check(0.0),
        convergence_evidence_check(1.0),
        convergence_evidence_check(0.0),
        truncation_sensitivity_check(0.01),
        truncation_sensitivity_check(0.2),
        p_tail_check(2.0),
        p_tail_check(1.0),
        model_domain_check(1.0),
        model_domain_check(0.0),
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
