from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
from statistics import mean


@dataclass(frozen=True)
class BoundaryChoice:
    key: str
    boundary_type: str
    included: str
    excluded: str
    risk_if_excluded: str
    review_question: str
    status: str


@dataclass(frozen=True)
class ResourceScenario:
    name: str
    boundary_version: str
    initial_stock: float
    capacity: float
    inflow: float
    demand: float
    loss_rate: float
    policy_savings: float
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
    if scenario.policy_savings < 0:
        raise ValueError("policy_savings must be nonnegative.")
    if scenario.periods < 1:
        raise ValueError("periods must be at least 1.")


def bounded_update(stock: float, inflow: float, demand: float, losses: float, capacity: float) -> float:
    return min(capacity, max(0.0, stock + inflow - demand - losses))


def simulate_resource(scenario: ResourceScenario) -> list[dict[str, float | str | int]]:
    validate_scenario(scenario)
    stock = scenario.initial_stock
    rows: list[dict[str, float | str | int]] = []

    for period in range(scenario.periods + 1):
        effective_demand = max(0.0, scenario.demand - scenario.policy_savings)
        losses = scenario.loss_rate * stock
        shortage = max(0.0, effective_demand + losses - (stock + scenario.inflow))
        stock_margin = stock / scenario.capacity

        rows.append({
            "scenario": scenario.name,
            "boundary_version": scenario.boundary_version,
            "period": period,
            "stock": round(stock, 8),
            "inflow": round(scenario.inflow, 8),
            "demand": round(scenario.demand, 8),
            "effective_demand": round(effective_demand, 8),
            "policy_savings": round(scenario.policy_savings, 8),
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
        "boundary_version": str(rows[0]["boundary_version"]),
        "final_stock": round(stocks[-1], 8),
        "mean_stock": round(mean(stocks), 8),
        "min_stock": round(min(stocks), 8),
        "max_stock": round(max(stocks), 8),
        "shortage_periods": shortage_periods,
        "total_shortage": round(sum(shortages), 8),
        "shortage_risk": round(shortage_periods / len(rows), 8),
        "minimum_stock_margin": round(min(stocks) / float(rows[0]["capacity"]), 8),
    }


def boundary_risk_score(choice: BoundaryChoice) -> float:
    score = {
        "active": 1.0,
        "review": 5.0,
        "revise": 8.0,
        "archive": 2.0,
    }.get(choice.status.lower(), 4.0)

    text = f"{choice.excluded} {choice.risk_if_excluded}".lower()
    for term in ["hidden", "understated", "overstated", "equity", "extreme", "long-term", "vulnerable", "distributional"]:
        if term in text:
            score += 1.0

    if choice.boundary_type.lower() in {"decision", "population", "uncertainty"}:
        score += 1.5

    return round(score, 8)


def load_boundaries(path: Path) -> list[BoundaryChoice]:
    boundaries: list[BoundaryChoice] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            boundaries.append(
                BoundaryChoice(
                    key=row["key"],
                    boundary_type=row["boundary_type"],
                    included=row["included"],
                    excluded=row["excluded"],
                    risk_if_excluded=row["risk_if_excluded"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return boundaries


def load_scenarios(path: Path) -> list[ResourceScenario]:
    scenarios: list[ResourceScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                ResourceScenario(
                    name=row["scenario"],
                    boundary_version=row["boundary_version"],
                    initial_stock=float(row["initial_stock"]),
                    capacity=float(row["capacity"]),
                    inflow=float(row["inflow"]),
                    demand=float(row["demand"]),
                    loss_rate=float(row["loss_rate"]),
                    policy_savings=float(row["policy_savings"]),
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


def build_boundary_card(
    boundaries: list[BoundaryChoice],
    summaries: list[dict[str, float | str | int]],
) -> dict[str, object]:
    boundary_rows = [
        {
            **asdict(boundary),
            "boundary_risk_score": boundary_risk_score(boundary),
        }
        for boundary in boundaries
    ]

    return {
        "article": "Model Boundaries, Scale, and Scope",
        "formal_model": "S[t+1] = min(K, max(0, S[t] + I[t] - D[t] - L[t]))",
        "boundary_versions": sorted({str(row["boundary_version"]) for row in summaries}),
        "boundary_register": boundary_rows,
        "scenario_summaries": summaries,
        "high_priority_boundaries": [
            row for row in boundary_rows if float(row["boundary_risk_score"]) >= 8.0
        ],
        "revision_triggers": [
            "boundary risk score above threshold",
            "scenario conclusion changes after boundary expansion",
            "time horizon does not match decision horizon",
            "scale of output does not match scale of affected users",
            "model is used beyond stated scope",
        ],
    }
