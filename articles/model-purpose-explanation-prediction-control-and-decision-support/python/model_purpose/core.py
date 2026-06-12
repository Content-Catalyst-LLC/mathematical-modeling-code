from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
from statistics import mean


@dataclass(frozen=True)
class PurposeRecord:
    purpose: str
    primary_question: str
    design_emphasis: str
    validation_standard: str
    uncertainty_format: str
    misuse_risk: str
    supported_use_status: str


@dataclass(frozen=True)
class ResourceScenario:
    name: str
    purpose: str
    initial_stock: float
    capacity: float
    inflow: float
    demand: float
    loss_rate: float
    control_action: float
    periods: int
    description: str = ""


def validate_scenario(scenario: ResourceScenario) -> None:
    if scenario.initial_stock < 0:
        raise ValueError("initial_stock must be nonnegative.")
    if scenario.capacity <= 0:
        raise ValueError("capacity must be positive.")
    if scenario.initial_stock > scenario.capacity:
        raise ValueError("initial_stock cannot exceed capacity.")
    if scenario.inflow < 0 or scenario.demand < 0:
        raise ValueError("inflow and demand must be nonnegative.")
    if scenario.loss_rate < 0:
        raise ValueError("loss_rate must be nonnegative.")
    if scenario.control_action < 0:
        raise ValueError("control_action must be nonnegative.")
    if scenario.periods < 1:
        raise ValueError("periods must be at least 1.")


def bounded_update(stock: float, inflow: float, demand: float, losses: float, capacity: float) -> float:
    return min(capacity, max(0.0, stock + inflow - demand - losses))


def simulate_resource(scenario: ResourceScenario) -> list[dict[str, float | str | int]]:
    validate_scenario(scenario)
    stock = scenario.initial_stock
    rows: list[dict[str, float | str | int]] = []

    for period in range(scenario.periods + 1):
        effective_demand = max(0.0, scenario.demand - scenario.control_action)
        losses = scenario.loss_rate * stock
        shortage = max(0.0, effective_demand + losses - (stock + scenario.inflow))
        stock_margin = stock / scenario.capacity

        rows.append({
            "scenario": scenario.name,
            "purpose": scenario.purpose,
            "period": period,
            "stock": round(stock, 8),
            "inflow": round(scenario.inflow, 8),
            "demand": round(scenario.demand, 8),
            "effective_demand": round(effective_demand, 8),
            "control_action": round(scenario.control_action, 8),
            "losses": round(losses, 8),
            "shortage": round(shortage, 8),
            "capacity": round(scenario.capacity, 8),
            "stock_margin": round(stock_margin, 8),
        })

        stock = bounded_update(stock, scenario.inflow, effective_demand, losses, scenario.capacity)

    return rows


def summarize_resource(rows: list[dict[str, float | str | int]]) -> dict[str, float | str | int]:
    if not rows:
        raise ValueError("Cannot summarize empty rows.")

    stocks = [float(row["stock"]) for row in rows]
    shortages = [float(row["shortage"]) for row in rows]
    shortage_periods = sum(1 for value in shortages if value > 0)

    return {
        "scenario": str(rows[0]["scenario"]),
        "purpose": str(rows[0]["purpose"]),
        "final_stock": round(stocks[-1], 8),
        "mean_stock": round(mean(stocks), 8),
        "min_stock": round(min(stocks), 8),
        "max_stock": round(max(stocks), 8),
        "shortage_periods": shortage_periods,
        "total_shortage": round(sum(shortages), 8),
        "shortage_risk": round(shortage_periods / len(rows), 8),
        "minimum_stock_margin": round(min(stocks) / float(rows[0]["capacity"]), 8),
    }


def purpose_risk_score(record: PurposeRecord) -> float:
    score = {
        "supported": 1.0,
        "exploratory": 4.0,
        "review": 5.0,
        "revise": 8.0,
        "prohibited": 10.0,
    }.get(record.supported_use_status.lower(), 4.0)

    misuse = record.misuse_risk.lower()
    for term in ["automated", "substitution", "beyond validation", "complete value", "forecast", "cause"]:
        if term in misuse:
            score += 1.25

    if record.purpose.lower() in {"control", "decision_support", "optimization"}:
        score += 1.0

    return round(score, 8)


def load_purpose_records(path: Path) -> list[PurposeRecord]:
    records: list[PurposeRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                PurposeRecord(
                    purpose=row["purpose"],
                    primary_question=row["primary_question"],
                    design_emphasis=row["design_emphasis"],
                    validation_standard=row["validation_standard"],
                    uncertainty_format=row["uncertainty_format"],
                    misuse_risk=row["misuse_risk"],
                    supported_use_status=row["supported_use_status"],
                )
            )
    return records


def load_scenarios(path: Path) -> list[ResourceScenario]:
    scenarios: list[ResourceScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                ResourceScenario(
                    name=row["scenario"],
                    purpose=row["purpose"],
                    initial_stock=float(row["initial_stock"]),
                    capacity=float(row["capacity"]),
                    inflow=float(row["inflow"]),
                    demand=float(row["demand"]),
                    loss_rate=float(row["loss_rate"]),
                    control_action=float(row["control_action"]),
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


def build_model_purpose_card(
    purposes: list[PurposeRecord],
    summaries: list[dict[str, float | str | int]],
) -> dict[str, object]:
    purpose_rows = [
        {
            **asdict(purpose),
            "purpose_risk_score": purpose_risk_score(purpose),
        }
        for purpose in purposes
    ]

    return {
        "article": "Model Purpose: Explanation, Prediction, Control, and Decision Support",
        "formal_model": "S[t+1] = min(K, max(0, S[t] + I[t] - D[t] - L[t]))",
        "purpose_register": purpose_rows,
        "scenario_summaries": summaries,
        "high_priority_purposes": [
            row for row in purpose_rows if float(row["purpose_risk_score"]) >= 8.0
        ],
        "purpose_drift_triggers": [
            "teaching model used for operational decision",
            "scenario model interpreted as forecast",
            "predictive model interpreted as causal explanation",
            "optimization output treated as complete value judgment",
            "decision support used as decision substitution",
        ],
    }
