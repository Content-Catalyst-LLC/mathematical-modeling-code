from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
from statistics import mean


@dataclass(frozen=True)
class UnitRecord:
    key: str
    quantity_type: str
    unit: str
    dimension: str
    expected_range: str
    review_question: str
    status: str


@dataclass(frozen=True)
class ScaleScenario:
    name: str
    initial_storage_m3: float
    capacity_m3: float
    inflow_m3_per_day: float
    demand_m3_per_day: float
    loss_rate_per_day: float
    delta_t_days: float
    periods: int
    description: str = ""


def validate_scenario(scenario: ScaleScenario) -> None:
    if scenario.initial_storage_m3 < 0:
        raise ValueError("initial storage must be nonnegative.")
    if scenario.capacity_m3 <= 0:
        raise ValueError("capacity must be positive.")
    if scenario.initial_storage_m3 > scenario.capacity_m3:
        raise ValueError("initial storage cannot exceed capacity.")
    if scenario.inflow_m3_per_day < 0 or scenario.demand_m3_per_day < 0:
        raise ValueError("flows must be nonnegative.")
    if not 0 <= scenario.loss_rate_per_day <= 1:
        raise ValueError("loss rate must be between 0 and 1 per day.")
    if scenario.delta_t_days <= 0:
        raise ValueError("time step must be positive.")
    if scenario.periods < 1:
        raise ValueError("periods must be at least 1.")


def simulate_scale_scenario(scenario: ScaleScenario) -> list[dict[str, object]]:
    validate_scenario(scenario)
    storage = scenario.initial_storage_m3
    rows: list[dict[str, object]] = []

    for period in range(scenario.periods + 1):
        inflow_volume = scenario.delta_t_days * scenario.inflow_m3_per_day
        demand_volume = scenario.delta_t_days * scenario.demand_m3_per_day
        loss_volume = scenario.delta_t_days * scenario.loss_rate_per_day * storage
        raw_next = storage + inflow_volume - demand_volume - loss_volume
        shortage = max(0.0, -raw_next)
        overflow = max(0.0, raw_next - scenario.capacity_m3)
        next_storage = min(scenario.capacity_m3, max(0.0, raw_next))
        storage_fraction = next_storage / scenario.capacity_m3

        rows.append({
            "scenario": scenario.name,
            "period": period,
            "storage_m3": round(storage, 8),
            "inflow_volume_m3": round(inflow_volume, 8),
            "demand_volume_m3": round(demand_volume, 8),
            "loss_volume_m3": round(loss_volume, 8),
            "raw_next_storage_m3": round(raw_next, 8),
            "next_storage_m3": round(next_storage, 8),
            "storage_fraction": round(storage_fraction, 8),
            "shortage_m3": round(shortage, 8),
            "overflow_m3": round(overflow, 8),
            "domain_valid": 0.0 <= next_storage <= scenario.capacity_m3,
        })

        storage = next_storage

    return rows


def summarize_scale_scenario(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Cannot summarize empty rows.")

    storage = [float(row["storage_m3"]) for row in rows]
    fractions = [float(row["storage_fraction"]) for row in rows]
    shortages = [float(row["shortage_m3"]) for row in rows]
    overflows = [float(row["overflow_m3"]) for row in rows]
    domain_flags = [bool(row["domain_valid"]) for row in rows]

    return {
        "scenario": str(rows[0]["scenario"]),
        "final_storage_m3": round(storage[-1], 8),
        "mean_storage_m3": round(mean(storage), 8),
        "min_storage_fraction": round(min(fractions), 8),
        "max_storage_fraction": round(max(fractions), 8),
        "shortage_periods": sum(1 for value in shortages if value > 0),
        "overflow_periods": sum(1 for value in overflows if value > 0),
        "domain_violations": sum(1 for value in domain_flags if not value),
        "total_shortage_m3": round(sum(shortages), 8),
        "total_overflow_m3": round(sum(overflows), 8),
    }


def unit_risk_score(record: UnitRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.quantity_type} {record.unit} {record.review_question}".lower()
    for term in ["flow", "rate", "time step", "dimensionless", "capacity", "conversion"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_unit_records(path: Path) -> list[UnitRecord]:
    records: list[UnitRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                UnitRecord(
                    key=row["key"],
                    quantity_type=row["quantity_type"],
                    unit=row["unit"],
                    dimension=row["dimension"],
                    expected_range=row["expected_range"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_scale_scenarios(path: Path) -> list[ScaleScenario]:
    scenarios: list[ScaleScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                ScaleScenario(
                    name=row["scenario"],
                    initial_storage_m3=float(row["initial_storage_m3"]),
                    capacity_m3=float(row["capacity_m3"]),
                    inflow_m3_per_day=float(row["inflow_m3_per_day"]),
                    demand_m3_per_day=float(row["demand_m3_per_day"]),
                    loss_rate_per_day=float(row["loss_rate_per_day"]),
                    delta_t_days=float(row["delta_t_days"]),
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


def build_dimensional_audit_card(
    units: list[UnitRecord],
    summaries: list[dict[str, object]],
) -> dict[str, object]:
    unit_rows = [
        {
            **asdict(record),
            "unit_risk_score": unit_risk_score(record),
        }
        for record in units
    ]

    return {
        "article": "Dimensional Analysis, Units, and Scale",
        "unit_register": unit_rows,
        "scenario_summaries": summaries,
        "high_priority_unit_records": [
            row for row in unit_rows if float(row["unit_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "stocks and capacities share units",
            "flows are multiplied by the model time step",
            "loss-rate unit matches the time step",
            "dimensionless storage fraction remains between zero and one",
            "shortage and overflow are reported with units",
        ],
    }
