from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import random
import statistics


@dataclass(frozen=True)
class MonteCarloRecord:
    key: str
    component_type: str
    uncertainty_structure: str
    interpretation: str
    review_question: str
    status: str


@dataclass(frozen=True)
class MonteCarloScenario:
    scenario: str
    initial_stock_min: float
    initial_stock_max: float
    growth_rate_min: float
    growth_rate_max: float
    extraction_min: float
    extraction_max: float
    shock_probability_min: float
    shock_probability_max: float
    shock_fraction: float
    carrying_capacity: float
    steps: int
    replications: int
    depletion_threshold: float
    seed: int


def validate_scenario(scenario: MonteCarloScenario) -> None:
    pairs = [
        ("initial_stock", scenario.initial_stock_min, scenario.initial_stock_max),
        ("growth_rate", scenario.growth_rate_min, scenario.growth_rate_max),
        ("extraction", scenario.extraction_min, scenario.extraction_max),
        ("shock_probability", scenario.shock_probability_min, scenario.shock_probability_max),
    ]
    for name, lower, upper in pairs:
        if lower > upper:
            raise ValueError(f"{name}_min must be <= {name}_max.")
    if scenario.initial_stock_min < 0 or scenario.growth_rate_min < 0 or scenario.extraction_min < 0:
        raise ValueError("Stock, growth, and extraction ranges must be nonnegative.")
    if not 0 <= scenario.shock_probability_min <= 1 or not 0 <= scenario.shock_probability_max <= 1:
        raise ValueError("Shock probability range must be within [0, 1].")
    if not 0 <= scenario.shock_fraction <= 1:
        raise ValueError("shock_fraction must be within [0, 1].")
    if scenario.carrying_capacity <= 0:
        raise ValueError("carrying_capacity must be positive.")
    if scenario.steps < 1 or scenario.replications < 1:
        raise ValueError("steps and replications must be positive.")


def simulate_once(scenario: MonteCarloScenario, rng: random.Random, replication: int) -> dict[str, object]:
    validate_scenario(scenario)

    initial_stock = rng.uniform(scenario.initial_stock_min, scenario.initial_stock_max)
    growth_rate = rng.uniform(scenario.growth_rate_min, scenario.growth_rate_max)
    extraction = rng.uniform(scenario.extraction_min, scenario.extraction_max)
    shock_probability = rng.uniform(scenario.shock_probability_min, scenario.shock_probability_max)

    stock = initial_stock
    min_stock = stock

    for _ in range(scenario.steps):
        growth = growth_rate * stock * (1.0 - stock / scenario.carrying_capacity)
        shock = stock * scenario.shock_fraction if rng.random() < shock_probability else 0.0
        stock = max(0.0, stock + growth - extraction - shock)
        min_stock = min(min_stock, stock)

    return {
        "scenario": scenario.scenario,
        "replication": replication,
        "sampled_initial_stock": round(initial_stock, 8),
        "sampled_growth_rate": round(growth_rate, 8),
        "sampled_extraction": round(extraction, 8),
        "sampled_shock_probability": round(shock_probability, 8),
        "final_stock": round(stock, 8),
        "minimum_stock": round(min_stock, 8),
        "depleted": int(stock <= scenario.depletion_threshold),
    }


def run_monte_carlo(scenario: MonteCarloScenario) -> list[dict[str, object]]:
    rng = random.Random(scenario.seed)
    return [
        simulate_once(scenario, rng, replication)
        for replication in range(1, scenario.replications + 1)
    ]


def quantile(values: list[float], probability: float) -> float:
    if not values:
        raise ValueError("Cannot compute quantile of empty values.")
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["scenario"]), []).append(row)

    output: list[dict[str, object]] = []
    for scenario, scenario_rows in sorted(grouped.items()):
        values = [float(row["final_stock"]) for row in scenario_rows]
        output.append({
            "scenario": scenario,
            "replications": len(values),
            "mean_final_stock": round(statistics.mean(values), 8),
            "median_final_stock": round(quantile(values, 0.50), 8),
            "p05_final_stock": round(quantile(values, 0.05), 8),
            "p95_final_stock": round(quantile(values, 0.95), 8),
            "min_final_stock": round(min(values), 8),
            "max_final_stock": round(max(values), 8),
            "depletion_probability": round(sum(int(row["depleted"]) for row in scenario_rows) / len(scenario_rows), 8),
        })
    return output


def convergence_rows(rows: list[dict[str, object]], checkpoints: list[int]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["scenario"]), []).append(row)

    output: list[dict[str, object]] = []
    for scenario, scenario_rows in sorted(grouped.items()):
        ordered = sorted(scenario_rows, key=lambda row: int(row["replication"]))
        for checkpoint in checkpoints:
            subset = ordered[: min(checkpoint, len(ordered))]
            values = [float(row["final_stock"]) for row in subset]
            output.append({
                "scenario": scenario,
                "replications_used": len(subset),
                "running_mean_final_stock": round(statistics.mean(values), 8),
                "running_depletion_probability": round(sum(int(row["depleted"]) for row in subset) / len(subset), 8),
            })
    return output


def simple_sensitivity_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["scenario"]), []).append(row)

    output: list[dict[str, object]] = []
    for scenario, scenario_rows in sorted(grouped.items()):
        depleted_rows = [row for row in scenario_rows if int(row["depleted"]) == 1]
        nondepleted_rows = [row for row in scenario_rows if int(row["depleted"]) == 0]
        for field in ["sampled_initial_stock", "sampled_growth_rate", "sampled_extraction", "sampled_shock_probability"]:
            depleted_mean = statistics.mean(float(row[field]) for row in depleted_rows) if depleted_rows else None
            nondepleted_mean = statistics.mean(float(row[field]) for row in nondepleted_rows) if nondepleted_rows else None
            difference = None if depleted_mean is None or nondepleted_mean is None else depleted_mean - nondepleted_mean
            output.append({
                "scenario": scenario,
                "input_field": field,
                "mean_when_depleted": None if depleted_mean is None else round(depleted_mean, 8),
                "mean_when_not_depleted": None if nondepleted_mean is None else round(nondepleted_mean, 8),
                "difference_depleted_minus_not_depleted": None if difference is None else round(difference, 8),
            })
    return output


def monte_carlo_risk_score(record: MonteCarloRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.component_type} {record.uncertainty_structure} {record.review_question}".lower()
    for term in ["distribution", "sampling", "threshold", "seed", "convergence", "risk", "uncertainty", "dependence"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_records(path: Path) -> list[MonteCarloRecord]:
    records: list[MonteCarloRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                MonteCarloRecord(
                    key=row["key"],
                    component_type=row["component_type"],
                    uncertainty_structure=row["uncertainty_structure"],
                    interpretation=row["interpretation"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_scenarios(path: Path) -> list[MonteCarloScenario]:
    scenarios: list[MonteCarloScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenario = MonteCarloScenario(
                scenario=row["scenario"],
                initial_stock_min=float(row["initial_stock_min"]),
                initial_stock_max=float(row["initial_stock_max"]),
                growth_rate_min=float(row["growth_rate_min"]),
                growth_rate_max=float(row["growth_rate_max"]),
                extraction_min=float(row["extraction_min"]),
                extraction_max=float(row["extraction_max"]),
                shock_probability_min=float(row["shock_probability_min"]),
                shock_probability_max=float(row["shock_probability_max"]),
                shock_fraction=float(row["shock_fraction"]),
                carrying_capacity=float(row["carrying_capacity"]),
                steps=int(row["steps"]),
                replications=int(row["replications"]),
                depletion_threshold=float(row["depletion_threshold"]),
                seed=int(row["seed"]),
            )
            validate_scenario(scenario)
            scenarios.append(scenario)
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


def build_monte_carlo_audit_card(
    records: list[MonteCarloRecord],
    scenarios: list[MonteCarloScenario],
    summary_rows: list[dict[str, object]],
    convergence: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {**asdict(record), "monte_carlo_risk_score": monte_carlo_risk_score(record)}
        for record in records
    ]

    return {
        "article": "Monte Carlo Simulation and Uncertainty Propagation",
        "scenario_count": len(scenarios),
        "scenarios": [asdict(scenario) for scenario in scenarios],
        "model_register": register_rows,
        "output_summary": summary_rows,
        "convergence_diagnostics": convergence,
        "high_priority_uncertainty_records": [
            row for row in register_rows if float(row["monte_carlo_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "input distributions are documented",
            "replications and random seeds are recorded",
            "output distributions include quantiles",
            "threshold probabilities are reported",
            "convergence diagnostics are preserved",
        ],
    }
