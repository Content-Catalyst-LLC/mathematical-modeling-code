from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class EcologyModelRecord:
    key: str
    domain: str
    model_role: str
    model_family: str
    sustainability_question: str
    status: str


@dataclass(frozen=True)
class ResourceScenario:
    key: str
    scenario_name: str
    initial_stock: float
    growth_rate: float
    carrying_capacity: float
    extraction: float
    climate_stress: float
    years: int
    minimum_stock: float


def load_ecology_model_records(path: Path) -> list[EcologyModelRecord]:
    records: list[EcologyModelRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                EcologyModelRecord(
                    key=row["key"],
                    domain=row["domain"],
                    model_role=row["model_role"],
                    model_family=row["model_family"],
                    sustainability_question=row["sustainability_question"],
                    status=row["status"],
                )
            )
    if not records:
        raise ValueError("Ecology model register cannot be empty.")
    return records


def load_resource_scenarios(path: Path) -> list[ResourceScenario]:
    scenarios: list[ResourceScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                ResourceScenario(
                    key=row["key"],
                    scenario_name=row["scenario_name"],
                    initial_stock=float(row["initial_stock"]),
                    growth_rate=float(row["growth_rate"]),
                    carrying_capacity=float(row["carrying_capacity"]),
                    extraction=float(row["extraction"]),
                    climate_stress=float(row["climate_stress"]),
                    years=int(row["years"]),
                    minimum_stock=float(row["minimum_stock"]),
                )
            )
    if not scenarios:
        raise ValueError("Resource scenario table cannot be empty.")
    return scenarios


def simulate_resource(scenario: ResourceScenario) -> list[dict[str, float]]:
    stock = scenario.initial_stock
    trajectory: list[dict[str, float]] = []
    effective_growth = scenario.growth_rate * (1.0 - scenario.climate_stress)

    for year in range(scenario.years + 1):
        resilience_margin = stock - scenario.minimum_stock
        trajectory.append(
            {
                "year": float(year),
                "stock": round(stock, 8),
                "resilience_margin": round(resilience_margin, 8),
            }
        )
        regeneration = effective_growth * stock * (1.0 - stock / scenario.carrying_capacity)
        stock = max(0.0, stock + regeneration - scenario.extraction)

    return trajectory


def evaluate_scenario(scenario: ResourceScenario) -> dict[str, object]:
    trajectory = simulate_resource(scenario)
    final_stock = trajectory[-1]["stock"]
    minimum_observed_stock = min(point["stock"] for point in trajectory)
    minimum_resilience_margin = min(point["resilience_margin"] for point in trajectory)
    threshold_breach = any(point["stock"] < scenario.minimum_stock for point in trajectory)

    review_class = "threshold_breach" if threshold_breach else "above_threshold"
    if minimum_resilience_margin < 50.0 and not threshold_breach:
        review_class = "low_resilience_margin"

    return {
        **asdict(scenario),
        "effective_growth_rate": round(scenario.growth_rate * (1.0 - scenario.climate_stress), 8),
        "final_stock": round(final_stock, 8),
        "minimum_observed_stock": round(minimum_observed_stock, 8),
        "minimum_resilience_margin": round(minimum_resilience_margin, 8),
        "threshold_breach": threshold_breach,
        "review_class": review_class,
    }


def ecology_priority(record: EcologyModelRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.model_role} {record.model_family} {record.sustainability_question}".lower()
    for term in ["threshold", "resilience", "climate", "biodiversity", "governance", "sustainability"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def sustainability_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Sustainability summary requires at least one scenario.")
    final_stocks = [float(row["final_stock"]) for row in rows]
    breaches = sum(1 for row in rows if bool(row["threshold_breach"]))
    best = max(rows, key=lambda row: float(row["minimum_resilience_margin"]))
    return {
        "best_resilience_scenario": best["scenario_name"],
        "mean_final_stock": round(statistics.mean(final_stocks), 8),
        "min_final_stock": round(min(final_stocks), 8),
        "max_final_stock": round(max(final_stocks), 8),
        "scenario_spread": round(max(final_stocks) - min(final_stocks), 8),
        "threshold_breach_count": breaches,
        "scenario_count": len(rows),
    }


def build_sustainability_review_card(
    register_rows: list[dict[str, object]],
    scenario_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Mathematical Modeling in Ecology and Sustainability",
        "sustainability_summary": sustainability_summary(scenario_rows),
        "ecology_model_register": register_rows,
        "scenario_review": scenario_rows,
        "use_limit": "This workflow supports ecological scenario interpretation and sustainability review; it is illustrative and does not replace field evidence, local knowledge, professional ecological assessment, or governance review.",
        "diagnostic_checks": [
            "resource stock and regeneration are represented",
            "climate stress is included as a scenario factor",
            "minimum ecological threshold is explicit",
            "resilience margin is computed",
            "threshold breach is flagged",
            "governance and monitoring remain required",
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
