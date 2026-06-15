from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class RuleAudit:
    rule: str
    model_structure: str
    x: float
    derivative_value: float
    component_a: float
    component_b: float
    warning: str


def population(t: float) -> float:
    return 100.0 * math.exp(0.01 * t)


def population_rate(t: float) -> float:
    return 0.01 * population(t)


def affluence(t: float) -> float:
    return 2.0 * math.exp(0.02 * t)


def affluence_rate(t: float) -> float:
    return 0.02 * affluence(t)


def product_rule_impact(t: float) -> RuleAudit:
    a = population_rate(t) * affluence(t)
    b = population(t) * affluence_rate(t)
    return RuleAudit("product_rule", "impact = population * affluence", t, a + b, a, b, "")


def resource(t: float) -> float:
    return 1000.0 - 10.0 * t


def quotient_rule_resource_per_capita(t: float) -> RuleAudit:
    denom = population(t) ** 2
    numerator_effect = -10.0 * population(t)
    denominator_effect = resource(t) * population_rate(t)
    derivative = (numerator_effect - denominator_effect) / denom
    warning = "denominator near zero" if abs(population(t)) < 1e-8 else ""
    return RuleAudit("quotient_rule", "resource_per_capita = resource / population", t, derivative, numerator_effect / denom, -denominator_effect / denom, warning)


def emissions(t: float) -> float:
    return 50.0 * math.exp(0.015 * t)


def emissions_rate(t: float) -> float:
    return 0.015 * emissions(t)


def chain_rule_climate_pathway(t: float) -> RuleAudit:
    e = emissions(t)
    c = 0.5 * e
    outer = 1.0 / (1.0 + c)
    inner = 0.5 * emissions_rate(t)
    return RuleAudit("chain_rule", "forcing = forcing(concentration(emissions(t)))", t, outer * inner, outer, inner, "")


def sum_rule_total_rate(t: float) -> RuleAudit:
    a = population_rate(t)
    b = affluence_rate(t)
    return RuleAudit("sum_rule", "total_driver = population + affluence", t, a + b, a, b, "")


def structural_audit(times: list[float]) -> list[RuleAudit]:
    rows: list[RuleAudit] = []
    for t in times:
        rows.extend([sum_rule_total_rate(t), product_rule_impact(t), quotient_rule_resource_per_capita(t), chain_rule_climate_pathway(t)])
    return rows


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
