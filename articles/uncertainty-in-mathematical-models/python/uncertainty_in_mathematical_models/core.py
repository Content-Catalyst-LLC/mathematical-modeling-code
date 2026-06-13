from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import random
import statistics


@dataclass(frozen=True)
class UncertainParameter:
    name: str
    low: float
    baseline: float
    high: float
    uncertainty_type: str
    description: str


@dataclass(frozen=True)
class UncertaintyRecord:
    key: str
    uncertainty_layer: str
    modeling_role: str
    review_question: str
    status: str


def load_parameters(path: Path) -> list[UncertainParameter]:
    parameters: list[UncertainParameter] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            parameters.append(
                UncertainParameter(
                    name=row["name"],
                    low=float(row["low"]),
                    baseline=float(row["baseline"]),
                    high=float(row["high"]),
                    uncertainty_type=row["uncertainty_type"],
                    description=row["description"],
                )
            )
    if not parameters:
        raise ValueError("Uncertain parameter table cannot be empty.")
    return parameters


def load_records(path: Path) -> list[UncertaintyRecord]:
    records: list[UncertaintyRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                UncertaintyRecord(
                    key=row["key"],
                    uncertainty_layer=row["uncertainty_layer"],
                    modeling_role=row["modeling_role"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def projection(
    initial_stock: float,
    growth_rate: float,
    carrying_capacity: float,
    extraction_rate: float,
    shock_intensity: float,
    years: int = 10,
) -> float:
    stock = initial_stock
    for _ in range(years):
        growth = growth_rate * stock * (1.0 - stock / carrying_capacity)
        extraction = extraction_rate * stock
        shock = shock_intensity * stock
        stock = max(0.0, stock + growth - extraction - shock)
    return round(stock, 8)


def sample_parameters(parameters: list[UncertainParameter], seed: int = 42, n: int = 1000) -> list[dict[str, float]]:
    rng = random.Random(seed)
    samples: list[dict[str, float]] = []
    for _ in range(n):
        row = {}
        for item in parameters:
            row[item.name] = rng.uniform(item.low, item.high)
        samples.append(row)
    return samples


def propagation_rows(parameters: list[UncertainParameter], threshold: float = 45.0) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, values in enumerate(sample_parameters(parameters), start=1):
        output = projection(**values)
        rows.append({
            "run_id": index,
            **values,
            "projected_stock": output,
            "below_threshold": output < threshold,
        })
    return rows


def quantile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("Cannot compute quantile of empty list.")
    position = probability * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return round(ordered[lower] * (1.0 - weight) + ordered[upper] * weight, 8)


def output_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Output summary requires at least one propagation row.")

    outputs = [float(row["projected_stock"]) for row in rows]
    threshold_count = sum(1 for row in rows if bool(row["below_threshold"]))
    return {
        "mean": round(statistics.mean(outputs), 8),
        "median": round(statistics.median(outputs), 8),
        "p05": quantile(outputs, 0.05),
        "p25": quantile(outputs, 0.25),
        "p75": quantile(outputs, 0.75),
        "p95": quantile(outputs, 0.95),
        "min": round(min(outputs), 8),
        "max": round(max(outputs), 8),
        "threshold_probability": round(threshold_count / len(rows), 8),
        "n": len(rows),
    }


def uncertainty_risk_score(record: UncertaintyRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.uncertainty_layer} {record.modeling_role} {record.review_question}".lower()
    for term in ["parameter", "structural", "scenario", "decision", "threshold", "model"]:
        if term in text:
            score += 1.0
    return round(score, 8)


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


def build_uncertainty_assessment_card(
    rows: list[dict[str, object]],
    register_rows: list[dict[str, object]],
) -> dict[str, object]:
    summary = output_summary(rows)
    return {
        "article": "Uncertainty in Mathematical Models",
        "output_summary": summary,
        "threshold_risk_flag": summary["threshold_probability"] > 0.05,
        "uncertainty_register": register_rows,
        "use_limit": "This uncertainty assessment includes sampled parameter and input uncertainty but does not fully resolve structural uncertainty.",
        "diagnostic_checks": [
            "uncertainty sources are named",
            "parameter ranges are documented",
            "output distribution is summarized",
            "threshold probability is reported",
            "structural uncertainty remains a review obligation",
            "decision interpretation must account for uncertainty",
        ],
    }
