from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class FlowRecord:
    step: int
    duration: float
    inflow: float
    outflow: float
    exposure_intensity: float
    population_weight: float


@dataclass(frozen=True)
class StockExposureAudit:
    initial_stock: float
    cumulative_inflow: float
    cumulative_outflow: float
    net_accumulation: float
    ending_stock: float
    cumulative_exposure: float
    population_weighted_exposure: float
    gross_activity: float
    method: str
    unit_check: str
    warning: str


def sample_records() -> list[FlowRecord]:
    return [
        FlowRecord(1, 1.0, 12.0, 6.0, 20.0, 1000.0),
        FlowRecord(2, 1.0, 10.0, 7.0, 18.0, 1100.0),
        FlowRecord(3, 1.0, 9.0, 8.0, 15.0, 1050.0),
        FlowRecord(4, 1.0, 8.0, 9.0, 13.0, 980.0),
        FlowRecord(5, 1.0, 7.0, 9.0, 11.0, 960.0),
    ]


def audit_flow_to_stock(initial_stock: float, records: list[FlowRecord]) -> StockExposureAudit:
    if not records:
        raise ValueError("At least one flow record is required.")
    if any(row.duration <= 0 for row in records):
        raise ValueError("All durations must be positive.")

    cumulative_inflow = sum(row.inflow * row.duration for row in records)
    cumulative_outflow = sum(row.outflow * row.duration for row in records)
    net_accumulation = cumulative_inflow - cumulative_outflow
    ending_stock = initial_stock + net_accumulation
    gross_activity = cumulative_inflow + cumulative_outflow

    cumulative_exposure = sum(row.exposure_intensity * row.duration for row in records)
    population_weighted_exposure = sum(
        row.exposure_intensity * row.population_weight * row.duration
        for row in records
    )

    warnings: list[str] = []
    if ending_stock < 0:
        warnings.append("ending stock is negative; check constraints or sign conventions")
    if gross_activity > 0 and abs(net_accumulation) / gross_activity < 0.05:
        warnings.append("large gross flows nearly cancel; report gross activity separately")
    if cumulative_exposure <= 0:
        warnings.append("cumulative exposure is nonpositive; check exposure intensity and units")

    return StockExposureAudit(
        initial_stock=initial_stock,
        cumulative_inflow=cumulative_inflow,
        cumulative_outflow=cumulative_outflow,
        net_accumulation=net_accumulation,
        ending_stock=ending_stock,
        cumulative_exposure=cumulative_exposure,
        population_weighted_exposure=population_weighted_exposure,
        gross_activity=gross_activity,
        method="discrete time-step accumulation",
        unit_check="flow multiplied by duration gives stock units; intensity multiplied by duration gives exposure units",
        warning="; ".join(warnings),
    )


def to_dicts(rows: list[object]) -> list[dict[str, object]]:
    return [asdict(row) for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
