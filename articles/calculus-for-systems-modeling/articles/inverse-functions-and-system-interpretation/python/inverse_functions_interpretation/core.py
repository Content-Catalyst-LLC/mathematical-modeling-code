from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class InverseAudit:
    target_output: float
    recovered_input: float
    forward_check: float
    residual: float
    forward_derivative: float
    inverse_sensitivity: float
    domain_valid: bool
    warning: str


def forward_model(x: float) -> float:
    if x <= -1.0:
        raise ValueError("forward model domain requires x > -1")
    return math.log1p(x)


def forward_derivative(x: float) -> float:
    if x <= -1.0:
        raise ValueError("forward derivative domain requires x > -1")
    return 1.0 / (1.0 + x)


def inverse_model(y: float) -> float:
    return math.exp(y) - 1.0


def inverse_audit(target_output: float) -> InverseAudit:
    x = inverse_model(target_output)
    y_check = forward_model(x)
    residual = y_check - target_output
    derivative = forward_derivative(x)
    inverse_sensitivity = 1.0 / derivative
    domain_valid = x > -1.0

    warning = ""
    if not domain_valid:
        warning = "recovered input outside domain"
    elif abs(derivative) < 1e-6:
        warning = "small forward derivative; inverse may be unstable"
    elif abs(residual) > 1e-8:
        warning = "forward check does not reproduce target output"

    return InverseAudit(
        target_output=target_output,
        recovered_input=x,
        forward_check=y_check,
        residual=residual,
        forward_derivative=derivative,
        inverse_sensitivity=inverse_sensitivity,
        domain_valid=domain_valid,
        warning=warning,
    )


def inverse_audits(outputs: list[float]) -> list[InverseAudit]:
    return [inverse_audit(y) for y in outputs]


def to_dicts(rows: list[object]) -> list[dict[str, object]]:
    return [asdict(row) for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
