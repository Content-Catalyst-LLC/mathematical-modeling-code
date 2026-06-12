from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
from statistics import mean


@dataclass(frozen=True)
class ModelAssumption:
    key: str
    statement: str
    assumption_type: str
    role: str
    risk_if_false: str
    sensitivity_test: str
    review_status: str


@dataclass(frozen=True)
class ResourceScenario:
    name: str
    initial_stock: float
    capacity: float
    inflow: float
    demand: float
    loss_rate: float
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
    if scenario.periods < 1:
        raise ValueError("periods must be at least 1.")


def bounded_update(stock: float, inflow: float, demand: float, losses: float, capacity: float) -> float:
    return min(capacity, max(0.0, stock + inflow - demand - losses))


def simulate_resource(scenario: ResourceScenario) -> list[dict[str, float | str | int]]:
    validate_scenario(scenario)
    stock = float(scenario.initial_stock)
    rows: list[dict[str, float | str | int]] = []

    for period in range(scenario.periods + 1):
        losses = scenario.loss_rate * stock
        shortage = max(0.0, scenario.demand + losses - (stock + scenario.inflow))
        stock_margin = stock / scenario.capacity

        rows.append({
            "scenario": scenario.name,
            "period": period,
            "stock": round(stock, 8),
            "inflow": round(scenario.inflow, 8),
            "demand": round(scenario.demand, 8),
            "losses": round(losses, 8),
            "shortage": round(shortage, 8),
            "capacity": round(scenario.capacity, 8),
            "stock_margin": round(stock_margin, 8),
        })

        stock = bounded_update(stock, scenario.inflow, scenario.demand, losses, scenario.capacity)

    return rows


def summarize_resource(rows: list[dict[str, float | str | int]]) -> dict[str, float | str | int]:
    if not rows:
        raise ValueError("Cannot summarize empty rows.")

    stocks = [float(row["stock"]) for row in rows]
    shortages = [float(row["shortage"]) for row in rows]
    shortage_periods = sum(1 for value in shortages if value > 0)

    return {
        "scenario": str(rows[0]["scenario"]),
        "final_stock": round(stocks[-1], 8),
        "mean_stock": round(mean(stocks), 8),
        "min_stock": round(min(stocks), 8),
        "max_stock": round(max(stocks), 8),
        "shortage_periods": shortage_periods,
        "total_shortage": round(sum(shortages), 8),
        "shortage_risk": round(shortage_periods / len(rows), 8),
        "minimum_stock_margin": round(min(stocks) / float(rows[0]["capacity"]), 8),
    }


def assumption_risk_score(assumption: ModelAssumption) -> float:
    status_weight = {
        "active": 1.0,
        "review": 5.0,
        "revise": 8.0,
        "archive": 2.0,
    }.get(assumption.review_status.lower(), 4.0)

    type_weight = {
        "abstraction": 2.0,
        "boundary": 2.5,
        "scale": 2.0,
        "functional_form": 3.0,
        "parameter": 2.5,
        "uncertainty": 3.0,
        "computational": 1.5,
        "interpretive": 3.0,
    }.get(assumption.assumption_type.lower(), 2.0)

    risk_text = assumption.risk_if_false.lower()
    penalty = 0.0
    for term in ["hidden", "understated", "severity", "access", "spatial", "uncertainty"]:
        if term in risk_text:
            penalty += 0.75

    return round(status_weight + type_weight + penalty, 8)


def load_assumptions(path: Path) -> list[ModelAssumption]:
    assumptions: list[ModelAssumption] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            assumptions.append(
                ModelAssumption(
                    key=row["key"],
                    statement=row["statement"],
                    assumption_type=row["assumption_type"],
                    role=row["role"],
                    risk_if_false=row["risk_if_false"],
                    sensitivity_test=row["sensitivity_test"],
                    review_status=row["review_status"],
                )
            )
    return assumptions


def load_scenarios(path: Path) -> list[ResourceScenario]:
    scenarios: list[ResourceScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                ResourceScenario(
                    name=row["scenario"],
                    initial_stock=float(row["initial_stock"]),
                    capacity=float(row["capacity"]),
                    inflow=float(row["inflow"]),
                    demand=float(row["demand"]),
                    loss_rate=float(row["loss_rate"]),
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


def build_model_design_card(
    assumptions: list[ModelAssumption],
    summaries: list[dict[str, float | str | int]],
) -> dict[str, object]:
    assumption_rows = [
        {
            **asdict(assumption),
            "assumption_risk_score": assumption_risk_score(assumption),
        }
        for assumption in assumptions
    ]

    return {
        "article": "Assumptions, Simplification, and Model Design",
        "formal_model": "S[t+1] = min(K, max(0, S[t] + I[t] - D[t] - L[t]))",
        "model_design_purpose": "Demonstrate assumption-aware simplification and model design review.",
        "assumptions": assumption_rows,
        "scenario_summaries": summaries,
        "high_priority_assumptions": [
            row for row in assumption_rows if float(row["assumption_risk_score"]) >= 8.0
        ],
        "revision_triggers": [
            "high assumption risk score",
            "shortage periods in stress scenarios",
            "conclusion sensitive to low inflow",
            "omitted heterogeneity affects intended use",
            "validation evidence does not support design assumptions",
        ],
    }
