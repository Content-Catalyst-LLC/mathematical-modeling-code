from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import random
from statistics import mean, pstdev


@dataclass(frozen=True)
class ProbabilityModelRecord:
    key: str
    model_component: str
    distribution_or_rule: str
    interpretation: str
    review_question: str
    status: str


@dataclass(frozen=True)
class RiskScenario:
    name: str
    demand_mu: float
    demand_sigma: float
    supply_mean: float
    supply_sd: float
    reserve: float
    simulations: int
    seed: int
    description: str = ""


def validate_scenario(scenario: RiskScenario) -> None:
    if scenario.demand_sigma <= 0:
        raise ValueError("demand_sigma must be positive.")
    if scenario.supply_mean <= 0:
        raise ValueError("supply_mean must be positive.")
    if scenario.supply_sd <= 0:
        raise ValueError("supply_sd must be positive.")
    if scenario.reserve < 0:
        raise ValueError("reserve must be nonnegative.")
    if scenario.simulations < 100:
        raise ValueError("simulations must be at least 100.")


def quantile(values: list[float], probability: float) -> float:
    if not values:
        raise ValueError("Cannot compute quantile of empty list.")
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round(probability * (len(ordered) - 1))))
    return ordered[index]


def simulate_risk(scenario: RiskScenario) -> tuple[list[dict[str, object]], dict[str, object]]:
    validate_scenario(scenario)
    rng = random.Random(scenario.seed)

    rows: list[dict[str, object]] = []
    shortages: list[float] = []

    for run in range(1, scenario.simulations + 1):
        demand = rng.lognormvariate(scenario.demand_mu, scenario.demand_sigma)
        supply = max(0.0, rng.gauss(scenario.supply_mean, scenario.supply_sd))
        available = supply + scenario.reserve
        shortage = max(0.0, demand - available)

        rows.append({
            "scenario": scenario.name,
            "run": run,
            "demand": round(demand, 8),
            "supply": round(supply, 8),
            "reserve": round(scenario.reserve, 8),
            "available_supply": round(available, 8),
            "shortage": round(shortage, 8),
            "shortage_event": shortage > 0,
        })
        shortages.append(shortage)

    shortage_events = [value > 0 for value in shortages]
    summary = {
        "scenario": scenario.name,
        "simulations": scenario.simulations,
        "shortage_probability": round(sum(shortage_events) / scenario.simulations, 8),
        "expected_shortage": round(mean(shortages), 8),
        "shortage_sd": round(pstdev(shortages), 8),
        "shortage_q50": round(quantile(shortages, 0.50), 8),
        "shortage_q90": round(quantile(shortages, 0.90), 8),
        "shortage_q95": round(quantile(shortages, 0.95), 8),
        "shortage_q99": round(quantile(shortages, 0.99), 8),
        "max_shortage": round(max(shortages), 8),
    }

    return rows, summary


def probability_risk_score(record: ProbabilityModelRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.model_component} {record.distribution_or_rule} {record.review_question}".lower()
    for term in ["tail", "distribution", "shortage", "risk", "normal", "probability", "evidence", "simulation"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_probability_records(path: Path) -> list[ProbabilityModelRecord]:
    records: list[ProbabilityModelRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                ProbabilityModelRecord(
                    key=row["key"],
                    model_component=row["model_component"],
                    distribution_or_rule=row["distribution_or_rule"],
                    interpretation=row["interpretation"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_risk_scenarios(path: Path) -> list[RiskScenario]:
    scenarios: list[RiskScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                RiskScenario(
                    name=row["scenario"],
                    demand_mu=float(row["demand_mu"]),
                    demand_sigma=float(row["demand_sigma"]),
                    supply_mean=float(row["supply_mean"]),
                    supply_sd=float(row["supply_sd"]),
                    reserve=float(row["reserve"]),
                    simulations=int(row["simulations"]),
                    seed=int(row["seed"]),
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


def build_probability_audit_card(
    records: list[ProbabilityModelRecord],
    scenario_summaries: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {
            **asdict(record),
            "probability_risk_score": probability_risk_score(record),
        }
        for record in records
    ]

    return {
        "article": "Probabilistic and Stochastic Models",
        "probability_model_register": register_rows,
        "scenario_summaries": scenario_summaries,
        "high_priority_probability_records": [
            row for row in register_rows if float(row["probability_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "distribution choices are justified",
            "tail risk is reported",
            "shortage probability and severity are separated",
            "random seed and simulation count are documented",
            "uncertainty is communicated as conditional on assumptions",
        ],
    }
