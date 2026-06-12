from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
from statistics import mean


@dataclass(frozen=True)
class StateVariable:
    key: str
    state_type: str
    unit: str
    interpretation: str
    update_role: str
    observability: str
    review_question: str
    status: str


@dataclass(frozen=True)
class RepresentationScenario:
    name: str
    representation: str
    initial_storage: float
    initial_demand: float
    initial_condition: float
    capacity: float
    inflow: float
    loss_rate: float
    demand_response: float
    condition_decay: float
    periods: int
    description: str = ""


def validate_scenario(scenario: RepresentationScenario) -> None:
    if scenario.initial_storage < 0:
        raise ValueError("initial_storage must be nonnegative.")
    if scenario.capacity <= 0:
        raise ValueError("capacity must be positive.")
    if scenario.initial_storage > scenario.capacity:
        raise ValueError("initial_storage cannot exceed capacity.")
    if scenario.initial_demand < 0:
        raise ValueError("initial_demand must be nonnegative.")
    if not 0 <= scenario.initial_condition <= 1:
        raise ValueError("initial_condition must be between 0 and 1.")
    if scenario.inflow < 0:
        raise ValueError("inflow must be nonnegative.")
    if not 0 <= scenario.loss_rate <= 1:
        raise ValueError("loss_rate must be between 0 and 1.")
    if scenario.periods < 1:
        raise ValueError("periods must be at least 1.")
    if scenario.representation not in {"storage_only", "adaptive_demand", "condition_aware"}:
        raise ValueError("representation must be storage_only, adaptive_demand, or condition_aware.")


def simulate_representation(scenario: RepresentationScenario) -> list[dict[str, object]]:
    validate_scenario(scenario)

    storage = scenario.initial_storage
    demand = scenario.initial_demand
    condition = scenario.initial_condition
    rows: list[dict[str, object]] = []

    for period in range(scenario.periods + 1):
        effective_loss_rate = scenario.loss_rate
        if scenario.representation == "condition_aware":
            effective_loss_rate = scenario.loss_rate * (1.0 + (1.0 - condition))

        losses = effective_loss_rate * storage
        raw_next_storage = storage + scenario.inflow - demand - losses
        shortage = max(0.0, -raw_next_storage)
        overflow = max(0.0, raw_next_storage - scenario.capacity)
        next_storage = min(scenario.capacity, max(0.0, raw_next_storage))

        rows.append({
            "scenario": scenario.name,
            "representation": scenario.representation,
            "period": period,
            "storage": round(storage, 8),
            "demand": round(demand, 8),
            "condition": round(condition, 8),
            "effective_loss_rate": round(effective_loss_rate, 8),
            "raw_next_storage": round(raw_next_storage, 8),
            "next_storage": round(next_storage, 8),
            "shortage": round(shortage, 8),
            "overflow": round(overflow, 8),
            "domain_valid": 0.0 <= next_storage <= scenario.capacity and 0.0 <= condition <= 1.0,
        })

        if scenario.representation in {"adaptive_demand", "condition_aware"}:
            demand = max(0.0, demand - scenario.demand_response * shortage)

        if scenario.representation == "condition_aware":
            stress = shortage + overflow
            condition = max(0.0, condition - scenario.condition_decay * stress)

        storage = next_storage

    return rows


def summarize_representation(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Cannot summarize empty rows.")

    storage = [float(row["storage"]) for row in rows]
    demand = [float(row["demand"]) for row in rows]
    condition = [float(row["condition"]) for row in rows]
    shortages = [float(row["shortage"]) for row in rows]
    overflows = [float(row["overflow"]) for row in rows]
    domain_flags = [bool(row["domain_valid"]) for row in rows]

    return {
        "scenario": str(rows[0]["scenario"]),
        "representation": str(rows[0]["representation"]),
        "final_storage": round(storage[-1], 8),
        "mean_storage": round(mean(storage), 8),
        "final_demand": round(demand[-1], 8),
        "final_condition": round(condition[-1], 8),
        "shortage_periods": sum(1 for value in shortages if value > 0),
        "overflow_periods": sum(1 for value in overflows if value > 0),
        "domain_violations": sum(1 for value in domain_flags if not value),
        "total_shortage": round(sum(shortages), 8),
        "total_overflow": round(sum(overflows), 8),
    }


def state_risk_score(record: StateVariable) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.state_type} {record.observability} {record.review_question}".lower()
    for term in ["latent", "proxy", "partially", "backlog", "capacity", "hidden", "adaptive"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_state_variables(path: Path) -> list[StateVariable]:
    records: list[StateVariable] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                StateVariable(
                    key=row["key"],
                    state_type=row["state_type"],
                    unit=row["unit"],
                    interpretation=row["interpretation"],
                    update_role=row["update_role"],
                    observability=row["observability"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_representation_scenarios(path: Path) -> list[RepresentationScenario]:
    scenarios: list[RepresentationScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                RepresentationScenario(
                    name=row["scenario"],
                    representation=row["representation"],
                    initial_storage=float(row["initial_storage"]),
                    initial_demand=float(row["initial_demand"]),
                    initial_condition=float(row["initial_condition"]),
                    capacity=float(row["capacity"]),
                    inflow=float(row["inflow"]),
                    loss_rate=float(row["loss_rate"]),
                    demand_response=float(row["demand_response"]),
                    condition_decay=float(row["condition_decay"]),
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


def build_state_audit_card(
    state_variables: list[StateVariable],
    summaries: list[dict[str, object]],
) -> dict[str, object]:
    state_rows = [
        {
            **asdict(record),
            "state_risk_score": state_risk_score(record),
        }
        for record in state_variables
    ]

    return {
        "article": "State Variables and System Representation",
        "state_register": state_rows,
        "scenario_summaries": summaries,
        "high_priority_state_records": [
            row for row in state_rows if float(row["state_risk_score"]) >= 8.0
        ],
        "representation_review_questions": [
            "Does the state contain enough information to update the system?",
            "Which variables are state, input, output, parameter, or derived diagnostic?",
            "Are hidden or proxy states clearly documented?",
            "Does aggregation hide important state variation?",
            "Do conclusions change under alternative state representations?",
        ],
    }
