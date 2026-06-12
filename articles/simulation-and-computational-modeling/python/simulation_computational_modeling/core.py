from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import random
import statistics


@dataclass(frozen=True)
class SimulationRecord:
    key: str
    component_type: str
    computational_structure: str
    interpretation: str
    review_question: str
    status: str


@dataclass(frozen=True)
class Scenario:
    scenario: str
    initial_stock: float
    growth_rate: float
    carrying_capacity: float
    extraction: float
    shock_probability: float
    shock_fraction: float
    steps: int
    replications: int


def validate_scenario(scenario: Scenario) -> None:
    if scenario.initial_stock < 0:
        raise ValueError("initial_stock must be nonnegative.")
    if scenario.growth_rate < 0:
        raise ValueError("growth_rate must be nonnegative.")
    if scenario.carrying_capacity <= 0:
        raise ValueError("carrying_capacity must be positive.")
    if scenario.extraction < 0:
        raise ValueError("extraction must be nonnegative.")
    if not 0 <= scenario.shock_probability <= 1:
        raise ValueError("shock_probability must be in [0, 1].")
    if not 0 <= scenario.shock_fraction <= 1:
        raise ValueError("shock_fraction must be in [0, 1].")
    if scenario.steps < 1 or scenario.replications < 1:
        raise ValueError("steps and replications must be positive.")


def extraction_for_step(scenario: Scenario, stock: float) -> float:
    if scenario.scenario == "adaptive_policy" and stock < 40.0:
        return scenario.extraction * 0.35
    return scenario.extraction


def simulate(scenario: Scenario, seed: int) -> list[dict[str, object]]:
    validate_scenario(scenario)
    rng = random.Random(seed)
    stock = scenario.initial_stock
    rows: list[dict[str, object]] = []

    for step in range(scenario.steps + 1):
        rows.append({
            "scenario": scenario.scenario,
            "seed": seed,
            "step": step,
            "resource_stock": round(stock, 8),
            "depleted": int(stock <= 5.0),
        })

        if step == scenario.steps:
            break

        growth = scenario.growth_rate * stock * (1.0 - stock / scenario.carrying_capacity)
        extraction = extraction_for_step(scenario, stock)
        shock = stock * scenario.shock_fraction if rng.random() < scenario.shock_probability else 0.0
        stock = max(0.0, stock + growth - extraction - shock)

    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    max_step_by_scenario: dict[str, int] = {}
    for row in rows:
        scenario = str(row["scenario"])
        max_step_by_scenario[scenario] = max(max_step_by_scenario.get(scenario, 0), int(row["step"]))

    grouped: dict[str, list[float]] = {}
    for row in rows:
        scenario = str(row["scenario"])
        if int(row["step"]) == max_step_by_scenario[scenario]:
            grouped.setdefault(scenario, []).append(float(row["resource_stock"]))

    output: list[dict[str, object]] = []
    for scenario, values in sorted(grouped.items()):
        output.append({
            "scenario": scenario,
            "replications": len(values),
            "mean_final_stock": round(statistics.mean(values), 8),
            "min_final_stock": round(min(values), 8),
            "max_final_stock": round(max(values), 8),
            "stdev_final_stock": round(statistics.pstdev(values), 8),
            "depletion_probability": round(sum(1 for value in values if value <= 5.0) / len(values), 8),
        })

    return output


def simulation_risk_score(record: SimulationRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.component_type} {record.computational_structure} {record.review_question}".lower()
    for term in ["update", "time", "random", "seed", "ensemble", "uncertainty", "numerical", "decision"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_records(path: Path) -> list[SimulationRecord]:
    records: list[SimulationRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                SimulationRecord(
                    key=row["key"],
                    component_type=row["component_type"],
                    computational_structure=row["computational_structure"],
                    interpretation=row["interpretation"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_scenarios(path: Path) -> list[Scenario]:
    scenarios: list[Scenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenario = Scenario(
                scenario=row["scenario"],
                initial_stock=float(row["initial_stock"]),
                growth_rate=float(row["growth_rate"]),
                carrying_capacity=float(row["carrying_capacity"]),
                extraction=float(row["extraction"]),
                shock_probability=float(row["shock_probability"]),
                shock_fraction=float(row["shock_fraction"]),
                steps=int(row["steps"]),
                replications=int(row["replications"]),
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


def build_simulation_audit_card(
    records: list[SimulationRecord],
    scenarios: list[Scenario],
    summary_rows: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {**asdict(record), "simulation_risk_score": simulation_risk_score(record)}
        for record in records
    ]
    return {
        "article": "Simulation and Computational Modeling",
        "scenario_count": len(scenarios),
        "scenarios": [asdict(scenario) for scenario in scenarios],
        "model_register": register_rows,
        "scenario_summary": summary_rows,
        "high_priority_simulation_records": [
            row for row in register_rows if float(row["simulation_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "state variables are documented",
            "update rules match the mathematical specification",
            "random seeds and replications are recorded",
            "scenario definitions are explicit",
            "uncertainty and sensitivity are summarized",
        ],
    }
