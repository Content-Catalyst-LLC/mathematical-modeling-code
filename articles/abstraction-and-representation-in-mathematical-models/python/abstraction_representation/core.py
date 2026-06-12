from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
from statistics import mean


@dataclass(frozen=True)
class RepresentationChoice:
    target_feature: str
    abstraction: str
    formal_representation: str
    preserved_structure: str
    omitted_detail: str
    review_question: str
    status: str


@dataclass(frozen=True)
class StockFlowScenario:
    name: str
    initial_stock: float
    capacity: float
    inflow: float
    demand: float
    loss_rate: float
    periods: int
    description: str = ""


def validate_scenario(scenario: StockFlowScenario) -> None:
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


def simulate_stock_flow(scenario: StockFlowScenario) -> list[dict[str, float | str | int]]:
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


def summarize_stock_flow(rows: list[dict[str, float | str | int]]) -> dict[str, float | str | int]:
    if not rows:
        raise ValueError("Cannot summarize empty rows.")

    stocks = [float(row["stock"]) for row in rows]
    shortages = [float(row["shortage"]) for row in rows]

    return {
        "scenario": str(rows[0]["scenario"]),
        "final_stock": round(stocks[-1], 8),
        "mean_stock": round(mean(stocks), 8),
        "min_stock": round(min(stocks), 8),
        "max_stock": round(max(stocks), 8),
        "shortage_periods": sum(1 for value in shortages if value > 0),
        "total_shortage": round(sum(shortages), 8),
        "minimum_stock_margin": round(min(stocks) / float(rows[0]["capacity"]), 8),
    }


def representation_risk_score(choice: RepresentationChoice) -> float:
    score = 0.0
    status_weights = {
        "active": 1.0,
        "review": 5.0,
        "revise": 8.0,
        "archive": 2.0,
    }
    score += status_weights.get(choice.status.lower(), 4.0)

    omitted_words = [word for word in choice.omitted_detail.replace(",", " ").split() if word.strip()]
    score += min(10.0, len(omitted_words) * 0.4)

    if "stochastic" in choice.omitted_detail.lower() or "quality" in choice.omitted_detail.lower():
        score += 2.0
    if "ownership" in choice.omitted_detail.lower() or "access" in choice.omitted_detail.lower():
        score += 2.0

    return round(score, 8)


def load_representation_choices(path: Path) -> list[RepresentationChoice]:
    choices: list[RepresentationChoice] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            choices.append(
                RepresentationChoice(
                    target_feature=row["target_feature"],
                    abstraction=row["abstraction"],
                    formal_representation=row["formal_representation"],
                    preserved_structure=row["preserved_structure"],
                    omitted_detail=row["omitted_detail"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return choices


def load_scenarios(path: Path) -> list[StockFlowScenario]:
    scenarios: list[StockFlowScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                StockFlowScenario(
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


def build_representation_card(
    choices: list[RepresentationChoice],
    summaries: list[dict[str, float | str | int]],
) -> dict[str, object]:
    choice_rows = [
        {
            **asdict(choice),
            "representation_risk_score": representation_risk_score(choice),
        }
        for choice in choices
    ]

    return {
        "article": "Abstraction and Representation in Mathematical Models",
        "formal_model": "S[t+1] = min(K, max(0, S[t] + I[t] - D[t] - L[t]))",
        "abstraction_map": "World resource system -> aggregate stock-flow representation",
        "represented_features": [choice.target_feature for choice in choices],
        "representation_choices": choice_rows,
        "scenario_summaries": summaries,
        "review_questions": [choice.review_question for choice in choices],
        "known_limits": [choice.omitted_detail for choice in choices],
        "revision_triggers": [
            "high representation risk score",
            "shortage periods under stress scenarios",
            "omitted detail directly affects intended use",
            "representation not adequate for validation purpose",
            "proxy variable used as if it were the target concept",
        ],
    }
