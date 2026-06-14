from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class PublicHealthModelRecord:
    key: str
    domain: str
    model_role: str
    model_family: str
    public_health_question: str
    status: str


@dataclass(frozen=True)
class EpidemicScenario:
    key: str
    scenario_name: str
    population: float
    initial_infectious: float
    initial_recovered: float
    beta: float
    gamma: float
    days: int
    hospital_capacity: float
    hospitalization_rate: float


def load_public_health_model_records(path: Path) -> list[PublicHealthModelRecord]:
    records: list[PublicHealthModelRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                PublicHealthModelRecord(
                    key=row["key"],
                    domain=row["domain"],
                    model_role=row["model_role"],
                    model_family=row["model_family"],
                    public_health_question=row["public_health_question"],
                    status=row["status"],
                )
            )
    if not records:
        raise ValueError("Public health model register cannot be empty.")
    return records


def load_epidemic_scenarios(path: Path) -> list[EpidemicScenario]:
    scenarios: list[EpidemicScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                EpidemicScenario(
                    key=row["key"],
                    scenario_name=row["scenario_name"],
                    population=float(row["population"]),
                    initial_infectious=float(row["initial_infectious"]),
                    initial_recovered=float(row["initial_recovered"]),
                    beta=float(row["beta"]),
                    gamma=float(row["gamma"]),
                    days=int(row["days"]),
                    hospital_capacity=float(row["hospital_capacity"]),
                    hospitalization_rate=float(row["hospitalization_rate"]),
                )
            )
    if not scenarios:
        raise ValueError("Epidemic scenario table cannot be empty.")
    return scenarios


def simulate_sir(scenario: EpidemicScenario) -> list[dict[str, float]]:
    susceptible = scenario.population - scenario.initial_infectious - scenario.initial_recovered
    infectious = scenario.initial_infectious
    recovered = scenario.initial_recovered
    trajectory: list[dict[str, float]] = []

    for day in range(scenario.days + 1):
        hospital_demand = infectious * scenario.hospitalization_rate
        trajectory.append(
            {
                "day": float(day),
                "susceptible": round(susceptible, 8),
                "infectious": round(infectious, 8),
                "recovered": round(recovered, 8),
                "hospital_demand": round(hospital_demand, 8),
            }
        )

        new_infections = scenario.beta * susceptible * infectious / scenario.population
        new_recoveries = scenario.gamma * infectious

        susceptible = max(0.0, susceptible - new_infections)
        infectious = max(0.0, infectious + new_infections - new_recoveries)
        recovered = min(scenario.population, recovered + new_recoveries)

    return trajectory


def evaluate_scenario(scenario: EpidemicScenario) -> dict[str, object]:
    trajectory = simulate_sir(scenario)
    peak_infectious = max(point["infectious"] for point in trajectory)
    peak_hospital_demand = max(point["hospital_demand"] for point in trajectory)
    final_recovered = trajectory[-1]["recovered"]
    estimated_attack_rate = final_recovered / scenario.population
    capacity_breach = peak_hospital_demand > scenario.hospital_capacity
    r0_simple = scenario.beta / scenario.gamma

    review_class = "capacity_breach" if capacity_breach else "within_capacity"
    if r0_simple > 1.5 and not capacity_breach:
        review_class = "high_transmission_review"

    return {
        **asdict(scenario),
        "r0_simple": round(r0_simple, 8),
        "peak_infectious": round(peak_infectious, 8),
        "peak_hospital_demand": round(peak_hospital_demand, 8),
        "capacity_margin": round(scenario.hospital_capacity - peak_hospital_demand, 8),
        "estimated_attack_rate": round(estimated_attack_rate, 8),
        "capacity_breach": capacity_breach,
        "review_class": review_class,
    }


def public_health_priority(record: PublicHealthModelRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.model_role} {record.model_family} {record.public_health_question}".lower()
    for term in ["capacity", "equity", "surveillance", "uncertainty", "transmission", "communication"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def epidemic_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Epidemic summary requires at least one scenario.")
    peaks = [float(row["peak_infectious"]) for row in rows]
    capacity_breaches = sum(1 for row in rows if bool(row["capacity_breach"]))
    best = min(rows, key=lambda row: float(row["peak_hospital_demand"]))
    return {
        "lowest_peak_hospital_demand_scenario": best["scenario_name"],
        "mean_peak_infectious": round(statistics.mean(peaks), 8),
        "max_peak_infectious": round(max(peaks), 8),
        "min_peak_infectious": round(min(peaks), 8),
        "capacity_breach_count": capacity_breaches,
        "scenario_count": len(rows),
    }


def build_public_health_model_review_card(
    register_rows: list[dict[str, object]],
    scenario_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Mathematical Modeling in Public Health and Epidemiology",
        "epidemic_summary": epidemic_summary(scenario_rows),
        "public_health_model_register": register_rows,
        "scenario_review": scenario_rows,
        "use_limit": "This simplified SIR workflow supports public health modeling literacy and scenario review; it does not replace surveillance investigation, clinical evidence, local expertise, ethical review, or public health authority.",
        "diagnostic_checks": [
            "transmission assumptions are explicit",
            "capacity demand is estimated",
            "capacity breach is flagged",
            "scenario comparison is preserved",
            "equity and surveillance review remain required",
            "uncertainty and use limits are stated",
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
