from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class ScientificModelRecord:
    key: str
    scientific_domain: str
    model_role: str
    model_family: str
    evidence_question: str
    status: str


@dataclass(frozen=True)
class PopulationScenario:
    key: str
    growth_rate: float
    carrying_capacity: float
    initial_population: float
    years: int
    observation_noise: float


def load_scientific_model_records(path: Path) -> list[ScientificModelRecord]:
    records: list[ScientificModelRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                ScientificModelRecord(
                    key=row["key"],
                    scientific_domain=row["scientific_domain"],
                    model_role=row["model_role"],
                    model_family=row["model_family"],
                    evidence_question=row["evidence_question"],
                    status=row["status"],
                )
            )
    if not records:
        raise ValueError("Scientific model register cannot be empty.")
    return records


def load_population_scenarios(path: Path) -> list[PopulationScenario]:
    scenarios: list[PopulationScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                PopulationScenario(
                    key=row["key"],
                    growth_rate=float(row["growth_rate"]),
                    carrying_capacity=float(row["carrying_capacity"]),
                    initial_population=float(row["initial_population"]),
                    years=int(row["years"]),
                    observation_noise=float(row["observation_noise"]),
                )
            )
    if not scenarios:
        raise ValueError("Population scenario table cannot be empty.")
    return scenarios


def logistic_population(initial: float, growth_rate: float, carrying_capacity: float, years: int) -> list[dict[str, float]]:
    values: list[dict[str, float]] = []
    population = initial

    for year in range(years + 1):
        values.append({"year": float(year), "population": round(population, 8)})
        population = population + growth_rate * population * (1.0 - population / carrying_capacity)

    return values


def scenario_summary(scenario: PopulationScenario) -> dict[str, object]:
    trajectory = logistic_population(
        initial=scenario.initial_population,
        growth_rate=scenario.growth_rate,
        carrying_capacity=scenario.carrying_capacity,
        years=scenario.years,
    )
    final_population = trajectory[-1]["population"]
    midpoint = scenario.carrying_capacity / 2.0
    crosses_midpoint = any(point["population"] >= midpoint for point in trajectory)

    return {
        **asdict(scenario),
        "final_population": round(final_population, 8),
        "carrying_capacity_half": round(midpoint, 8),
        "crosses_capacity_midpoint": crosses_midpoint,
        "trajectory_points": len(trajectory),
    }


def scientific_priority(record: ScientificModelRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.model_role} {record.model_family} {record.evidence_question}".lower()
    for term in ["uncertainty", "measurement", "comparison", "prediction", "evidence", "mechanism"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def evidence_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Evidence summary requires at least one scenario row.")
    finals = [float(row["final_population"]) for row in rows]
    return {
        "mean_final_population": round(statistics.mean(finals), 8),
        "min_final_population": round(min(finals), 8),
        "max_final_population": round(max(finals), 8),
        "scenario_spread": round(max(finals) - min(finals), 8),
        "scenario_count": len(rows),
    }


def build_scientific_model_evidence_card(
    register_rows: list[dict[str, object]],
    scenario_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Mathematical Modeling in Science",
        "evidence_summary": evidence_summary(scenario_rows),
        "scientific_model_register": register_rows,
        "scenario_summary": scenario_rows,
        "use_limit": "This workflow demonstrates scientific model interpretation; results are illustrative and should not be treated as empirical findings.",
        "diagnostic_checks": [
            "model purpose is stated",
            "scientific domain is named",
            "model family is identified",
            "scenario spread is reported",
            "measurement uncertainty is acknowledged",
            "validation and domain of validity remain explicit",
        ],
    }


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
