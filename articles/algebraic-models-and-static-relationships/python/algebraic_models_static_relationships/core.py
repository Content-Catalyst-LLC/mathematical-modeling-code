from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class AlgebraicRelationship:
    key: str
    relationship_type: str
    expression: str
    interpretation: str
    domain_or_constraint: str
    review_question: str
    status: str


@dataclass(frozen=True)
class AllocationScenario:
    name: str
    budget: float
    cost_a: float
    cost_b: float
    benefit_a: float
    benefit_b: float
    allocation_a: float
    allocation_b: float
    capacity_a: float
    capacity_b: float
    description: str = ""


def validate_scenario(scenario: AllocationScenario) -> None:
    numeric_fields = asdict(scenario)
    for key, value in numeric_fields.items():
        if key in {"name", "description"}:
            continue
        if float(value) < 0:
            raise ValueError(f"{key} must be nonnegative.")
    if scenario.budget <= 0:
        raise ValueError("budget must be positive.")
    if scenario.cost_a <= 0 or scenario.cost_b <= 0:
        raise ValueError("costs must be positive.")


def evaluate_scenario(scenario: AllocationScenario) -> dict[str, object]:
    validate_scenario(scenario)

    total_cost = scenario.cost_a * scenario.allocation_a + scenario.cost_b * scenario.allocation_b
    total_benefit = scenario.benefit_a * scenario.allocation_a + scenario.benefit_b * scenario.allocation_b

    budget_slack = scenario.budget - total_cost
    capacity_slack_a = scenario.capacity_a - scenario.allocation_a
    capacity_slack_b = scenario.capacity_b - scenario.allocation_b

    feasible = (
        budget_slack >= 0
        and capacity_slack_a >= 0
        and capacity_slack_b >= 0
        and scenario.allocation_a >= 0
        and scenario.allocation_b >= 0
    )

    benefit_per_cost = total_benefit / total_cost if total_cost > 0 else 0.0

    return {
        "scenario": scenario.name,
        "budget": round(scenario.budget, 8),
        "total_cost": round(total_cost, 8),
        "total_benefit": round(total_benefit, 8),
        "benefit_per_cost": round(benefit_per_cost, 8),
        "budget_slack": round(budget_slack, 8),
        "capacity_slack_a": round(capacity_slack_a, 8),
        "capacity_slack_b": round(capacity_slack_b, 8),
        "feasible": feasible,
        "constraint_status": "feasible" if feasible else "constraint violation",
        "description": scenario.description,
    }


def relationship_risk_score(record: AlgebraicRelationship) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.relationship_type} {record.expression} {record.review_question}".lower()
    for term in ["constraint", "objective", "budget", "capacity", "equity", "domain", "units", "ratio"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_relationships(path: Path) -> list[AlgebraicRelationship]:
    relationships: list[AlgebraicRelationship] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            relationships.append(
                AlgebraicRelationship(
                    key=row["key"],
                    relationship_type=row["relationship_type"],
                    expression=row["expression"],
                    interpretation=row["interpretation"],
                    domain_or_constraint=row["domain_or_constraint"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return relationships


def load_scenarios(path: Path) -> list[AllocationScenario]:
    scenarios: list[AllocationScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                AllocationScenario(
                    name=row["scenario"],
                    budget=float(row["budget"]),
                    cost_a=float(row["cost_a"]),
                    cost_b=float(row["cost_b"]),
                    benefit_a=float(row["benefit_a"]),
                    benefit_b=float(row["benefit_b"]),
                    allocation_a=float(row["allocation_a"]),
                    allocation_b=float(row["allocation_b"]),
                    capacity_a=float(row["capacity_a"]),
                    capacity_b=float(row["capacity_b"]),
                    description=row.get("description", ""),
                )
            )
    return scenarios


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def build_algebraic_audit_card(
    relationships: list[AlgebraicRelationship],
    scenario_summaries: list[dict[str, object]],
) -> dict[str, object]:
    relationship_rows = [
        {
            **asdict(record),
            "relationship_risk_score": relationship_risk_score(record),
        }
        for record in relationships
    ]

    return {
        "article": "Algebraic Models and Static Relationships",
        "relationships": relationship_rows,
        "scenario_summaries": scenario_summaries,
        "high_priority_relationships": [
            row for row in relationship_rows if float(row["relationship_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "equations have stated interpretation",
            "units and domains are visible",
            "constraints are checked separately from objectives",
            "ratios report numerator and denominator meaning",
            "static conclusions are not overextended to dynamic behavior",
        ],
    }
