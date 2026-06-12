from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math
import statistics


@dataclass(frozen=True)
class ValidationRecord:
    key: str
    validation_layer: str
    modeling_role: str
    assessment_question: str
    status: str


@dataclass(frozen=True)
class ValidationObservation:
    time: int
    observed_value: float
    predicted_value: float
    scenario: str


def load_records(path: Path) -> list[ValidationRecord]:
    records: list[ValidationRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                ValidationRecord(
                    key=row["key"],
                    validation_layer=row["validation_layer"],
                    modeling_role=row["modeling_role"],
                    assessment_question=row["assessment_question"],
                    status=row["status"],
                )
            )
    return records


def load_observations(path: Path) -> list[ValidationObservation]:
    rows: list[ValidationObservation] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                ValidationObservation(
                    time=int(row["time"]),
                    observed_value=float(row["observed_value"]),
                    predicted_value=float(row["predicted_value"]),
                    scenario=row["scenario"],
                )
            )
    if not rows:
        raise ValueError("Validation observations cannot be empty.")
    return rows


def error_rows(data: list[ValidationObservation]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for obs in data:
        residual = obs.observed_value - obs.predicted_value
        rows.append({
            "time": obs.time,
            "scenario": obs.scenario,
            "observed_value": obs.observed_value,
            "predicted_value": obs.predicted_value,
            "residual": round(residual, 8),
            "absolute_error": round(abs(residual), 8),
            "squared_error": round(residual * residual, 8),
        })
    return rows


def metric_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Metric summary requires at least one row.")

    residuals = [float(row["residual"]) for row in rows]
    abs_errors = [float(row["absolute_error"]) for row in rows]
    squared_errors = [float(row["squared_error"]) for row in rows]

    rmse = math.sqrt(sum(squared_errors) / len(squared_errors))
    mae = sum(abs_errors) / len(abs_errors)
    bias = statistics.mean(residuals)
    max_abs_error = max(abs_errors)

    return {
        "rmse": round(rmse, 8),
        "mae": round(mae, 8),
        "bias": round(bias, 8),
        "max_abs_error": round(max_abs_error, 8),
        "n": len(rows),
    }


def scenario_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["scenario"]), []).append(row)

    output: list[dict[str, object]] = []
    for scenario, values in sorted(grouped.items()):
        summary = metric_summary(values)
        output.append({"scenario": scenario, **summary})
    return output


def classify_fitness(summary: dict[str, object]) -> str:
    rmse = float(summary["rmse"])
    max_abs_error = float(summary["max_abs_error"])

    if rmse <= 1.25 and max_abs_error <= 2.0:
        return "adequate_for_scenario_screening"
    if rmse <= 2.5:
        return "limited_use_requires_review"
    return "not_adequate_without_revision"


def validation_risk_score(record: ValidationRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.validation_layer} {record.modeling_role} {record.assessment_question}".lower()
    for term in ["conceptual", "data", "residual", "uncertainty", "decision", "verification", "purpose", "benchmark"]:
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


def build_model_assessment_card(
    records: list[ValidationRecord],
    overall: dict[str, object],
    scenario_rows: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {**asdict(record), "validation_risk_score": validation_risk_score(record)}
        for record in records
    ]

    return {
        "article": "Validation and Model Assessment",
        "overall_metrics": overall,
        "fitness_for_purpose": classify_fitness(overall),
        "scenario_summary": scenario_rows,
        "validation_register": register_rows,
        "high_priority_validation_records": [
            row for row in register_rows if float(row["validation_risk_score"]) >= 8.0
        ],
        "use_limit": "Assessment is educational and does not authorize operational decision use without domain-specific review.",
        "diagnostic_checks": [
            "validation observations are separated from calibration logic",
            "residual and error metrics are exported",
            "scenario-level diagnostics are preserved",
            "fitness-for-purpose judgment is conditional",
            "uncertainty and decision-use review remain required",
        ],
    }
