from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math
import random
from statistics import mean


@dataclass(frozen=True)
class RelationshipRecord:
    key: str
    relationship_type: str
    expression: str
    interpretation: str
    structural_assumption: str
    review_question: str
    status: str


@dataclass(frozen=True)
class StructureScenario:
    name: str
    structure: str
    initial_stock: float
    capacity: float
    inflow: float
    demand: float
    loss_rate: float
    feedback_strength: float
    periods: int
    description: str = ""


def validate_scenario(scenario: StructureScenario) -> None:
    if scenario.initial_stock < 0:
        raise ValueError("initial_stock must be nonnegative.")
    if scenario.capacity <= 0:
        raise ValueError("capacity must be positive.")
    if scenario.initial_stock > scenario.capacity:
        raise ValueError("initial_stock cannot exceed capacity.")
    if scenario.inflow < 0 or scenario.demand < 0:
        raise ValueError("inflow and demand must be nonnegative.")
    if not 0 <= scenario.loss_rate <= 1:
        raise ValueError("loss_rate must be between 0 and 1.")
    if scenario.feedback_strength < 0:
        raise ValueError("feedback_strength must be nonnegative.")
    if scenario.periods < 1:
        raise ValueError("periods must be at least 1.")


def simulate_structure(scenario: StructureScenario, seed: int = 42) -> list[dict[str, float | str | int]]:
    validate_scenario(scenario)
    rng = random.Random(seed)
    stock = scenario.initial_stock
    demand = scenario.demand
    rows: list[dict[str, float | str | int]] = []

    for period in range(scenario.periods + 1):
        inflow = scenario.inflow

        if scenario.structure == "stochastic":
            shock = rng.gauss(0.0, 0.18)
            inflow = scenario.inflow * math.exp(shock)

        if scenario.structure == "threshold":
            if stock < 0.35 * scenario.capacity:
                demand = max(0.0, demand - scenario.feedback_strength * 2.0)
            else:
                demand = scenario.demand

        losses = scenario.loss_rate * stock
        raw_next_stock = stock + inflow - demand - losses
        shortage = max(0.0, -raw_next_stock)
        overflow = max(0.0, raw_next_stock - scenario.capacity)

        if scenario.structure in {"constrained", "feedback", "stochastic", "threshold"}:
            next_stock = min(scenario.capacity, max(0.0, raw_next_stock))
        else:
            next_stock = raw_next_stock

        rows.append({
            "scenario": scenario.name,
            "structure": scenario.structure,
            "period": period,
            "stock": round(stock, 8),
            "inflow": round(inflow, 8),
            "demand": round(demand, 8),
            "losses": round(losses, 8),
            "raw_next_stock": round(raw_next_stock, 8),
            "next_stock": round(next_stock, 8),
            "shortage": round(shortage, 8),
            "overflow": round(overflow, 8),
            "capacity": round(scenario.capacity, 8),
        })

        if scenario.structure == "feedback":
            demand = max(0.0, demand - scenario.feedback_strength * shortage)

        stock = next_stock

    return rows


def summarize_structure(rows: list[dict[str, float | str | int]]) -> dict[str, float | str | int]:
    if not rows:
        raise ValueError("Cannot summarize empty rows.")

    stocks = [float(row["stock"]) for row in rows]
    shortages = [float(row["shortage"]) for row in rows]
    overflows = [float(row["overflow"]) for row in rows]

    return {
        "scenario": str(rows[0]["scenario"]),
        "structure": str(rows[0]["structure"]),
        "final_stock": round(stocks[-1], 8),
        "mean_stock": round(mean(stocks), 8),
        "min_stock": round(min(stocks), 8),
        "max_stock": round(max(stocks), 8),
        "shortage_periods": sum(1 for value in shortages if value > 0),
        "overflow_periods": sum(1 for value in overflows if value > 0),
        "total_shortage": round(sum(shortages), 8),
        "total_overflow": round(sum(overflows), 8),
    }


def structure_risk_score(record: RelationshipRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.relationship_type} {record.structural_assumption} {record.review_question}".lower()

    for term in ["feedback", "stochastic", "constraint", "shortage", "overflow", "threshold", "domain", "delayed"]:
        if term in text:
            score += 1.0

    return round(score, 8)


def load_relationships(path: Path) -> list[RelationshipRecord]:
    records: list[RelationshipRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                RelationshipRecord(
                    key=row["key"],
                    relationship_type=row["relationship_type"],
                    expression=row["expression"],
                    interpretation=row["interpretation"],
                    structural_assumption=row["structural_assumption"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_scenarios(path: Path) -> list[StructureScenario]:
    scenarios: list[StructureScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                StructureScenario(
                    name=row["scenario"],
                    structure=row["structure"],
                    initial_stock=float(row["initial_stock"]),
                    capacity=float(row["capacity"]),
                    inflow=float(row["inflow"]),
                    demand=float(row["demand"]),
                    loss_rate=float(row["loss_rate"]),
                    feedback_strength=float(row["feedback_strength"]),
                    periods=int(row["periods"]),
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


def build_structural_diagnostics_card(
    relationships: list[RelationshipRecord],
    summaries: list[dict[str, float | str | int]],
) -> dict[str, object]:
    relationship_rows = [
        {
            **asdict(item),
            "structure_risk_score": structure_risk_score(item),
        }
        for item in relationships
    ]

    return {
        "article": "Functional Relationships and Mathematical Structure",
        "relationship_register": relationship_rows,
        "scenario_summaries": summaries,
        "high_priority_relationships": [
            row for row in relationship_rows if float(row["structure_risk_score"]) >= 8.0
        ],
        "structural_review_questions": [
            "Does the functional form match the intended mechanism?",
            "Does the model need linear, nonlinear, dynamic, stochastic, networked, or constrained structure?",
            "Do constraints hide shortage or overflow?",
            "Does feedback occur immediately, with delay, or not at all?",
            "Does uncertainty require probability, scenarios, or robust analysis?",
        ],
    }
