from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class ImproperIntegralAudit:
    cutoff: float
    truncated_value: float
    reference_value: float
    tail_error: float
    method: str
    convergence_interpretation: str
    warning: str


@dataclass(frozen=True)
class SingularEndpointAudit:
    epsilon: float
    truncated_value: float
    reference_value: float
    excluded_endpoint_error: float
    method: str
    convergence_interpretation: str
    warning: str


def tail_function(x: float) -> float:
    return math.exp(-0.4 * x)


def exact_tail_reference() -> float:
    return 1.0 / 0.4


def singular_function(x: float) -> float:
    return 1.0 / math.sqrt(x)


def exact_singular_reference() -> float:
    return 2.0


def trapezoid_function(func, a: float, b: float, n: int = 4000) -> float:
    if b <= a:
        raise ValueError("Upper bound must exceed lower bound.")
    if n <= 0:
        raise ValueError("n must be positive.")
    dx = (b - a) / n
    total = 0.0
    for i in range(n):
        x0 = a + i * dx
        x1 = x0 + dx
        total += 0.5 * (func(x0) + func(x1)) * dx
    return total


def audit_infinite_cutoffs(cutoffs: list[float]) -> list[ImproperIntegralAudit]:
    reference = exact_tail_reference()
    rows: list[ImproperIntegralAudit] = []
    for cutoff in cutoffs:
        truncated = trapezoid_function(tail_function, 0.0, cutoff)
        tail_error = reference - truncated
        warning = ""
        if abs(tail_error) > 0.05:
            warning = "tail contribution remains material at this cutoff"
        rows.append(
            ImproperIntegralAudit(
                cutoff=cutoff,
                truncated_value=truncated,
                reference_value=reference,
                tail_error=tail_error,
                method="trapezoidal truncation audit",
                convergence_interpretation="exponential decay produces finite infinite-horizon accumulation",
                warning=warning,
            )
        )
    return rows


def audit_singular_epsilons(epsilons: list[float]) -> list[SingularEndpointAudit]:
    reference = exact_singular_reference()
    rows: list[SingularEndpointAudit] = []
    for epsilon in epsilons:
        truncated = trapezoid_function(singular_function, epsilon, 1.0)
        error = reference - truncated
        warning = ""
        if abs(error) > 0.05:
            warning = "excluded singular endpoint contribution remains material"
        rows.append(
            SingularEndpointAudit(
                epsilon=epsilon,
                truncated_value=truncated,
                reference_value=reference,
                excluded_endpoint_error=error,
                method="trapezoidal singular-endpoint audit",
                convergence_interpretation="x^(-1/2) has finite accumulation near zero",
                warning=warning,
            )
        )
    return rows


def p_tail_classification(p: float) -> str:
    if p > 1.0:
        return "convergent tail"
    if p == 1.0:
        return "divergent harmonic boundary"
    return "divergent slow tail"


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
