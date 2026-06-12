from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
from statistics import mean
from typing import Iterable


@dataclass(frozen=True)
class ModelingQuestion:
    article_slug: str
    real_world_context: str
    modeling_purpose: str
    central_question: str
    intended_use: str
    decision_context: str


@dataclass(frozen=True)
class Assumption:
    key: str
    statement: str
    role: str
    risk_if_false: str
    sensitivity_test: str
    review_status: str


@dataclass(frozen=True)
class ReservoirScenario:
    name: str
    initial_storage: float
    capacity: float
    base_inflow: float
    base_demand: float
    demand_growth: float
    loss_rate: float
    periods: int
    description: str = ""


def validate_scenario(scenario: ReservoirScenario) -> None:
    if scenario.initial_storage < 0:
        raise ValueError("initial_storage must be nonnegative.")
    if scenario.capacity <= 0:
        raise ValueError("capacity must be positive.")
    if scenario.initial_storage > scenario.capacity:
        raise ValueError("initial_storage cannot exceed capacity.")
    if scenario.periods < 1:
        raise ValueError("periods must be at least 1.")
    if scenario.loss_rate < 0:
        raise ValueError("loss_rate must be nonnegative.")
    if scenario.base_demand < 0 or scenario.base_inflow < 0:
        raise ValueError("base demand and inflow must be nonnegative.")


def bounded_storage_update(storage: float, inflow: float, demand: float, losses: float, capacity: float) -> float:
    return min(capacity, max(0.0, storage + inflow - demand - losses))


def simulate_reservoir(scenario: ReservoirScenario) -> list[dict[str, float | str | int]]:
    validate_scenario(scenario)
    storage = float(scenario.initial_storage)
    rows: list[dict[str, float | str | int]] = []

    for period in range(scenario.periods + 1):
        demand = scenario.base_demand * ((1.0 + scenario.demand_growth) ** period)
        inflow = scenario.base_inflow
        losses = scenario.loss_rate * storage
        shortage = max(0.0, demand + losses - (storage + inflow))
        storage_margin = storage / scenario.capacity if scenario.capacity else 0.0

        rows.append({
            "scenario": scenario.name,
            "period": period,
            "storage": round(storage, 8),
            "inflow": round(inflow, 8),
            "demand": round(demand, 8),
            "losses": round(losses, 8),
            "shortage": round(shortage, 8),
            "capacity": round(scenario.capacity, 8),
            "storage_margin": round(storage_margin, 8),
        })

        storage = bounded_storage_update(storage, inflow, demand, losses, scenario.capacity)

    return rows


def summarize_scenario(rows: list[dict[str, float | str | int]]) -> dict[str, float | str | int]:
    if not rows:
        raise ValueError("Cannot summarize empty rows.")

    storage_values = [float(row["storage"]) for row in rows]
    shortages = [float(row["shortage"]) for row in rows]
    shortage_periods = sum(1 for value in shortages if value > 0)
    low_storage_periods = sum(1 for value in storage_values if value < 0.25 * float(rows[0]["capacity"]))

    return {
        "scenario": str(rows[0]["scenario"]),
        "final_storage": round(storage_values[-1], 8),
        "mean_storage": round(mean(storage_values), 8),
        "min_storage": round(min(storage_values), 8),
        "max_storage": round(max(storage_values), 8),
        "shortage_periods": shortage_periods,
        "low_storage_periods": low_storage_periods,
        "total_shortage": round(sum(shortages), 8),
        "shortage_risk": round(shortage_periods / len(rows), 8),
        "minimum_storage_margin": round(min(storage_values) / float(rows[0]["capacity"]), 8),
    }


def scenario_stress_index(summary: dict[str, float | str | int]) -> float:
    shortage_risk = float(summary["shortage_risk"])
    total_shortage = float(summary["total_shortage"])
    low_storage_periods = float(summary["low_storage_periods"])
    minimum_margin = float(summary["minimum_storage_margin"])
    return round(
        100.0 * shortage_risk
        + 1.5 * low_storage_periods
        + 0.10 * total_shortage
        + max(0.0, 0.30 - minimum_margin) * 80.0,
        8,
    )


def load_scenarios(path: Path) -> list[ReservoirScenario]:
    scenarios: list[ReservoirScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                ReservoirScenario(
                    name=row["scenario"],
                    initial_storage=float(row["initial_storage"]),
                    capacity=float(row["capacity"]),
                    base_inflow=float(row["base_inflow"]),
                    base_demand=float(row["base_demand"]),
                    demand_growth=float(row["demand_growth"]),
                    loss_rate=float(row["loss_rate"]),
                    periods=int(row["periods"]),
                    description=row.get("description", ""),
                )
            )
    return scenarios


def load_assumptions(path: Path) -> list[Assumption]:
    assumptions: list[Assumption] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            assumptions.append(
                Assumption(
                    key=row["key"],
                    statement=row["statement"],
                    role=row["role"],
                    risk_if_false=row["risk_if_false"],
                    sensitivity_test=row["sensitivity_test"],
                    review_status=row["review_status"],
                )
            )
    return assumptions


def load_observations(path: Path) -> list[dict[str, float]]:
    observations: list[dict[str, float]] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            observations.append({
                "period": float(row["period"]),
                "observed_storage": float(row["observed_storage"]),
            })
    return observations


def compare_to_observations(
    simulated_rows: list[dict[str, float | str | int]],
    observations: Iterable[dict[str, float]],
) -> list[dict[str, float | str]]:
    by_period = {int(row["period"]): float(row["storage"]) for row in simulated_rows}
    scenario = str(simulated_rows[0]["scenario"])
    residual_rows: list[dict[str, float | str]] = []

    for observation in observations:
        period = int(observation["period"])
        observed = float(observation["observed_storage"])
        predicted = by_period.get(period)
        if predicted is None:
            continue
        residual_rows.append({
            "scenario": scenario,
            "period": float(period),
            "observed_storage": round(observed, 8),
            "predicted_storage": round(predicted, 8),
            "residual": round(observed - predicted, 8),
            "absolute_residual": round(abs(observed - predicted), 8),
        })
    return residual_rows


def residual_summary(rows: list[dict[str, float | str]]) -> dict[str, float | str]:
    if not rows:
        return {"status": "no residuals"}
    residuals = [float(row["residual"]) for row in rows]
    abs_residuals = [abs(value) for value in residuals]
    return {
        "status": "computed",
        "n": float(len(rows)),
        "bias": round(mean(residuals), 8),
        "mae": round(mean(abs_residuals), 8),
        "max_abs_residual": round(max(abs_residuals), 8),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write for {path}.")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def build_modeling_process_card(
    question: ModelingQuestion,
    assumptions: list[Assumption],
    summaries: list[dict[str, float | str | int]],
) -> dict[str, object]:
    ranked = sorted(
        [
            {**summary, "stress_index": scenario_stress_index(summary)}
            for summary in summaries
        ],
        key=lambda row: float(row["stress_index"]),
        reverse=True,
    )

    return {
        "article": "The Modeling Process: From World to Formal Representation",
        "question": asdict(question),
        "formal_model": "S[t+1] = min(K, max(0, S[t] + I[t] - D[t] - L[t]))",
        "variables": ["S_t", "I_t", "D_t", "L_t"],
        "parameters": ["K", "base_inflow", "base_demand", "demand_growth", "loss_rate"],
        "constraints": ["0 <= S_t <= K"],
        "outputs": ["storage", "shortage", "shortage_risk", "stress_index"],
        "assumptions": [asdict(item) for item in assumptions],
        "ranked_scenarios": ranked,
        "revision_triggers": [
            "high residual bias",
            "shortage risk above tolerance",
            "conclusion sensitive to uncertain inflow",
            "assumption status requires review",
            "model output does not answer the intended use",
        ],
    }
