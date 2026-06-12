from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
from statistics import mean


@dataclass(frozen=True)
class RecurrenceRecord:
    key: str
    component_type: str
    expression: str
    interpretation: str
    domain_or_step: str
    review_question: str
    status: str


@dataclass(frozen=True)
class RecurrenceScenario:
    name: str
    initial_storage: float
    initial_demand: float
    capacity: float
    inflow: float
    loss_rate: float
    demand_response: float
    periods: int
    adaptive_demand: bool
    description: str = ""


def parse_bool(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def validate_scenario(scenario: RecurrenceScenario) -> None:
    if scenario.initial_storage < 0:
        raise ValueError("initial_storage must be nonnegative.")
    if scenario.capacity <= 0:
        raise ValueError("capacity must be positive.")
    if scenario.initial_storage > scenario.capacity:
        raise ValueError("initial_storage cannot exceed capacity.")
    if scenario.initial_demand < 0:
        raise ValueError("initial_demand must be nonnegative.")
    if scenario.inflow < 0:
        raise ValueError("inflow must be nonnegative.")
    if scenario.loss_rate < 0:
        raise ValueError("loss_rate must be nonnegative.")
    if scenario.demand_response < 0:
        raise ValueError("demand_response must be nonnegative.")
    if scenario.periods < 1:
        raise ValueError("periods must be at least 1.")


def simulate_recurrence(scenario: RecurrenceScenario) -> list[dict[str, object]]:
    validate_scenario(scenario)

    storage = scenario.initial_storage
    demand = scenario.initial_demand
    rows: list[dict[str, object]] = []

    for period in range(scenario.periods + 1):
        raw_next_storage = storage + scenario.inflow - demand - scenario.loss_rate * storage
        shortage = max(0.0, -raw_next_storage)
        overflow = max(0.0, raw_next_storage - scenario.capacity)
        next_storage = min(scenario.capacity, max(0.0, raw_next_storage))

        rows.append({
            "scenario": scenario.name,
            "period": period,
            "storage": round(storage, 8),
            "demand": round(demand, 8),
            "raw_next_storage": round(raw_next_storage, 8),
            "next_storage": round(next_storage, 8),
            "shortage": round(shortage, 8),
            "overflow": round(overflow, 8),
            "adaptive_demand": scenario.adaptive_demand,
            "domain_valid": 0.0 <= next_storage <= scenario.capacity,
        })

        if scenario.adaptive_demand:
            demand = max(0.0, demand - scenario.demand_response * shortage)

        storage = next_storage

    return rows


def summarize_trajectory(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Cannot summarize empty rows.")

    storage = [float(row["storage"]) for row in rows]
    demand = [float(row["demand"]) for row in rows]
    shortages = [float(row["shortage"]) for row in rows]
    overflows = [float(row["overflow"]) for row in rows]
    domain_flags = [bool(row["domain_valid"]) for row in rows]

    return {
        "scenario": str(rows[0]["scenario"]),
        "final_storage": round(storage[-1], 8),
        "mean_storage": round(mean(storage), 8),
        "min_storage": round(min(storage), 8),
        "max_storage": round(max(storage), 8),
        "final_demand": round(demand[-1], 8),
        "shortage_periods": sum(1 for value in shortages if value > 0),
        "overflow_periods": sum(1 for value in overflows if value > 0),
        "domain_violations": sum(1 for value in domain_flags if not value),
        "total_shortage": round(sum(shortages), 8),
        "total_overflow": round(sum(overflows), 8),
    }


def recurrence_risk_score(record: RecurrenceRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.component_type} {record.expression} {record.review_question}".lower()
    for term in ["boundary", "adaptive", "shortage", "clipping", "threshold", "derived", "step"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_recurrence_records(path: Path) -> list[RecurrenceRecord]:
    records: list[RecurrenceRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                RecurrenceRecord(
                    key=row["key"],
                    component_type=row["component_type"],
                    expression=row["expression"],
                    interpretation=row["interpretation"],
                    domain_or_step=row["domain_or_step"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_recurrence_scenarios(path: Path) -> list[RecurrenceScenario]:
    scenarios: list[RecurrenceScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                RecurrenceScenario(
                    name=row["scenario"],
                    initial_storage=float(row["initial_storage"]),
                    initial_demand=float(row["initial_demand"]),
                    capacity=float(row["capacity"]),
                    inflow=float(row["inflow"]),
                    loss_rate=float(row["loss_rate"]),
                    demand_response=float(row["demand_response"]),
                    periods=int(row["periods"]),
                    adaptive_demand=parse_bool(row["adaptive_demand"]),
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


def build_recurrence_audit_card(
    records: list[RecurrenceRecord],
    scenario_summaries: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {
            **asdict(record),
            "recurrence_risk_score": recurrence_risk_score(record),
        }
        for record in records
    ]

    return {
        "article": "Discrete Models and Recurrence Relations",
        "recurrence_register": register_rows,
        "scenario_summaries": scenario_summaries,
        "high_priority_recurrence_records": [
            row for row in register_rows if float(row["recurrence_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "step meaning is documented",
            "update order is explicit",
            "boundary events are reported",
            "recurrence trajectories are preserved",
            "static endpoints are not substituted for dynamic behavior",
        ],
    }
