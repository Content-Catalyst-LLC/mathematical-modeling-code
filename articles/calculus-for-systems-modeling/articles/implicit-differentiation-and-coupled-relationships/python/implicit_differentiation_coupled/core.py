from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class ImplicitAudit:
    parameter: float
    equilibrium_state: float
    constraint_value: float
    partial_state: float
    partial_parameter: float
    implicit_sensitivity: float
    finite_difference_check: float
    absolute_error: float
    warning: str


def equilibrium_state(parameter: float) -> float:
    return (-parameter + (parameter**2 + 40.0) ** 0.5) / 2.0


def constraint(x: float, p: float) -> float:
    return x**2 + p * x - 10.0


def partial_state(x: float, p: float) -> float:
    return 2.0 * x + p


def partial_parameter(x: float, p: float) -> float:
    return x


def implicit_sensitivity(x: float, p: float, threshold: float = 1e-8) -> float:
    gx = partial_state(x, p)
    if abs(gx) < threshold:
        raise ValueError("regularity failure: partial derivative with respect to state is near zero")
    return -partial_parameter(x, p) / gx


def finite_difference_sensitivity(p: float, h: float = 1e-5) -> float:
    return (equilibrium_state(p + h) - equilibrium_state(p - h)) / (2.0 * h)


def audit_parameter(p: float) -> ImplicitAudit:
    x = equilibrium_state(p)
    gx = partial_state(x, p)
    gp = partial_parameter(x, p)
    sens = implicit_sensitivity(x, p)
    fd = finite_difference_sensitivity(p)
    error = abs(sens - fd)
    warning = ""
    if abs(gx) < 1e-4:
        warning = "near singular state Jacobian; sensitivity may be unstable"
    elif error > 1e-5:
        warning = "finite-difference check differs from implicit derivative"

    return ImplicitAudit(
        parameter=p,
        equilibrium_state=x,
        constraint_value=constraint(x, p),
        partial_state=gx,
        partial_parameter=gp,
        implicit_sensitivity=sens,
        finite_difference_check=fd,
        absolute_error=error,
        warning=warning,
    )


def implicit_audits(parameters: list[float]) -> list[ImplicitAudit]:
    return [audit_parameter(p) for p in parameters]


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
