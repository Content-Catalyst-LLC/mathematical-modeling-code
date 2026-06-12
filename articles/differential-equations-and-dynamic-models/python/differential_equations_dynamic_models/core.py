from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
from statistics import mean


@dataclass(frozen=True)
class DynamicModelRecord:
    key: str
    component_type: str
    expression: str
    interpretation: str
    units_or_domain: str
    review_question: str
    status: str


@dataclass(frozen=True)
class DynamicScenario:
    name: str
    initial_storage: float
    capacity: float
    inflow_rate: float
    demand_rate: float
    loss_rate: float
    dt: float
    horizon: float
    description: str = ""


def validate_scenario(scenario: DynamicScenario) -> None:
    if scenario.initial_storage < 0:
        raise ValueError("initial_storage must be nonnegative.")
    if scenario.capacity <= 0:
        raise ValueError("capacity must be positive.")
    if scenario.initial_storage > scenario.capacity:
        raise ValueError("initial_storage cannot exceed capacity.")
    if scenario.inflow_rate < 0 or scenario.demand_rate < 0:
        raise ValueError("flow rates must be nonnegative.")
    if scenario.loss_rate < 0:
        raise ValueError("loss_rate must be nonnegative.")
    if scenario.dt <= 0:
        raise ValueError("time step must be positive.")
    if scenario.horizon <= 0:
        raise ValueError("time horizon must be positive.")


def derivative(storage: float, scenario: DynamicScenario) -> float:
    return scenario.inflow_rate - scenario.demand_rate - scenario.loss_rate * storage


def simulate_euler(scenario: DynamicScenario) -> list[dict[str, object]]:
    validate_scenario(scenario)

    storage = scenario.initial_storage
    time = 0.0
    steps = int(round(scenario.horizon / scenario.dt))
    rows: list[dict[str, object]] = []

    for step in range(steps + 1):
        rate = derivative(storage, scenario)
        raw_next = storage + scenario.dt * rate
        shortage = max(0.0, -raw_next)
        overflow = max(0.0, raw_next - scenario.capacity)
        next_storage = min(scenario.capacity, max(0.0, raw_next))

        rows.append({
            "scenario": scenario.name,
            "step": step,
            "time": round(time, 8),
            "storage": round(storage, 8),
            "rate_of_change": round(rate, 8),
            "raw_next_storage": round(raw_next, 8),
            "next_storage": round(next_storage, 8),
            "shortage": round(shortage, 8),
            "overflow": round(overflow, 8),
            "domain_valid": 0.0 <= next_storage <= scenario.capacity,
        })

        storage = next_storage
        time += scenario.dt

    return rows


def summarize_trajectory(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Cannot summarize empty rows.")

    storage = [float(row["storage"]) for row in rows]
    rates = [float(row["rate_of_change"]) for row in rows]
    shortages = [float(row["shortage"]) for row in rows]
    overflows = [float(row["overflow"]) for row in rows]
    domain_flags = [bool(row["domain_valid"]) for row in rows]

    return {
        "scenario": str(rows[0]["scenario"]),
        "final_storage": round(storage[-1], 8),
        "mean_storage": round(mean(storage), 8),
        "min_storage": round(min(storage), 8),
        "max_storage": round(max(storage), 8),
        "mean_rate_of_change": round(mean(rates), 8),
        "shortage_periods": sum(1 for value in shortages if value > 0),
        "overflow_periods": sum(1 for value in overflows if value > 0),
        "domain_violations": sum(1 for value in domain_flags if not value),
        "total_shortage": round(sum(shortages), 8),
        "total_overflow": round(sum(overflows), 8),
    }


def dynamic_risk_score(record: DynamicModelRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.component_type} {record.expression} {record.review_question}".lower()
    for term in ["boundary", "units", "rate", "capacity", "numerically", "initial", "time step"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_model_records(path: Path) -> list[DynamicModelRecord]:
    records: list[DynamicModelRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                DynamicModelRecord(
                    key=row["key"],
                    component_type=row["component_type"],
                    expression=row["expression"],
                    interpretation=row["interpretation"],
                    units_or_domain=row["units_or_domain"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_dynamic_scenarios(path: Path) -> list[DynamicScenario]:
    scenarios: list[DynamicScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                DynamicScenario(
                    name=row["scenario"],
                    initial_storage=float(row["initial_storage"]),
                    capacity=float(row["capacity"]),
                    inflow_rate=float(row["inflow_rate"]),
                    demand_rate=float(row["demand_rate"]),
                    loss_rate=float(row["loss_rate"]),
                    dt=float(row["dt"]),
                    horizon=float(row["horizon"]),
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


def build_dynamic_audit_card(
    records: list[DynamicModelRecord],
    scenario_summaries: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {
            **asdict(record),
            "dynamic_risk_score": dynamic_risk_score(record),
        }
        for record in records
    ]

    return {
        "article": "Differential Equations and Dynamic Models",
        "model_register": register_rows,
        "scenario_summaries": scenario_summaries,
        "high_priority_dynamic_records": [
            row for row in register_rows if float(row["dynamic_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "rate equations have stated units",
            "initial conditions are documented",
            "time step is explicit",
            "domain boundaries are enforced",
            "dynamic conclusions are not reduced to endpoint values",
        ],
    }
