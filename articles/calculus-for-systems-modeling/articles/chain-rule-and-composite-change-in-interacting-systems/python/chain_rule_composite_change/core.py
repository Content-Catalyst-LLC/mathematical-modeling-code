from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class ChainRuleAudit:
    t: float
    emissions: float
    concentration: float
    forcing: float
    temperature: float
    emissions_rate: float
    d_concentration_d_emissions: float
    d_forcing_d_concentration: float
    d_temperature_d_forcing: float
    total_derivative: float
    finite_difference_check: float
    absolute_error: float
    warning: str


def emissions(t: float) -> float:
    return 50.0 * math.exp(0.015 * t)


def emissions_rate(t: float) -> float:
    return 0.015 * emissions(t)


def concentration(e: float) -> float:
    return 0.5 * e


def d_concentration_d_emissions(_: float) -> float:
    return 0.5


def forcing(c: float) -> float:
    return math.log(1.0 + c)


def d_forcing_d_concentration(c: float) -> float:
    return 1.0 / (1.0 + c)


def temperature_response(f: float) -> float:
    return 1.2 * f


def d_temperature_d_forcing(_: float) -> float:
    return 1.2


def temperature_pathway(t: float) -> float:
    return temperature_response(forcing(concentration(emissions(t))))


def finite_difference(t: float, h: float = 1e-4) -> float:
    return (temperature_pathway(t + h) - temperature_pathway(t - h)) / (2.0 * h)


def chain_rule_audit(t: float) -> ChainRuleAudit:
    e = emissions(t)
    c = concentration(e)
    f = forcing(c)
    temp = temperature_response(f)
    s1 = emissions_rate(t)
    s2 = d_concentration_d_emissions(e)
    s3 = d_forcing_d_concentration(c)
    s4 = d_temperature_d_forcing(f)
    total = s4 * s3 * s2 * s1
    fd = finite_difference(t)
    error = abs(total - fd)
    return ChainRuleAudit(
        t=t,
        emissions=e,
        concentration=c,
        forcing=f,
        temperature=temp,
        emissions_rate=s1,
        d_concentration_d_emissions=s2,
        d_forcing_d_concentration=s3,
        d_temperature_d_forcing=s4,
        total_derivative=total,
        finite_difference_check=fd,
        absolute_error=error,
        warning="finite-difference check differs from chain-rule derivative" if error > 1e-5 else "",
    )


def chain_rule_audits(times: list[float]) -> list[ChainRuleAudit]:
    return [chain_rule_audit(t) for t in times]


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
