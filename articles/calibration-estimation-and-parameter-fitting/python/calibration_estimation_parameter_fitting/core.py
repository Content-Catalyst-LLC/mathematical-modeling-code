from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math
import statistics


@dataclass(frozen=True)
class CalibrationRecord:
    key: str
    calibration_layer: str
    modeling_role: str
    diagnostic_question: str
    status: str


@dataclass(frozen=True)
class Observation:
    time: int
    observed_stock: float
    extraction: float


@dataclass(frozen=True)
class ParameterCandidate:
    growth_rate: float
    carrying_capacity: float


def load_records(path: Path) -> list[CalibrationRecord]:
    records: list[CalibrationRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                CalibrationRecord(
                    key=row["key"],
                    calibration_layer=row["calibration_layer"],
                    modeling_role=row["modeling_role"],
                    diagnostic_question=row["diagnostic_question"],
                    status=row["status"],
                )
            )
    return records


def load_observations(path: Path) -> list[Observation]:
    rows: list[Observation] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                Observation(
                    time=int(row["time"]),
                    observed_stock=float(row["observed_stock"]),
                    extraction=float(row["extraction"]),
                )
            )
    if not rows:
        raise ValueError("Calibration observations cannot be empty.")
    return rows


def load_grid(path: Path) -> dict[str, float]:
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        row = next(reader)
    return {key: float(value) for key, value in row.items()}


def candidate_grid(grid_config: dict[str, float]) -> list[ParameterCandidate]:
    candidates: list[ParameterCandidate] = []
    g = grid_config["growth_rate_min"]
    while g <= grid_config["growth_rate_max"] + 1e-12:
        k = grid_config["carrying_capacity_min"]
        while k <= grid_config["carrying_capacity_max"] + 1e-12:
            candidates.append(ParameterCandidate(round(g, 10), round(k, 10)))
            k += grid_config["carrying_capacity_step"]
        g += grid_config["growth_rate_step"]
    return candidates


def simulate(candidate: ParameterCandidate, data: list[Observation]) -> list[dict[str, float]]:
    if not data:
        raise ValueError("Calibration data cannot be empty.")
    if candidate.growth_rate < 0 or candidate.carrying_capacity <= 0:
        raise ValueError("Invalid parameter candidate.")

    stock = data[0].observed_stock
    rows: list[dict[str, float]] = []

    for index, obs in enumerate(data):
        if index == 0:
            predicted = stock
        else:
            previous = data[index - 1]
            growth = candidate.growth_rate * stock * (1.0 - stock / candidate.carrying_capacity)
            predicted = max(0.0, stock + growth - previous.extraction)
            stock = predicted

        rows.append({
            "time": obs.time,
            "observed_stock": obs.observed_stock,
            "predicted_stock": round(predicted, 8),
            "residual": round(obs.observed_stock - predicted, 8),
        })

    return rows


def score_candidate(candidate: ParameterCandidate, data: list[Observation]) -> dict[str, object]:
    rows = simulate(candidate, data)
    residuals = [float(row["residual"]) for row in rows]
    sse = sum(residual * residual for residual in residuals)
    rmse = math.sqrt(sse / len(residuals))
    mae = sum(abs(residual) for residual in residuals) / len(residuals)
    bias = statistics.mean(residuals)

    return {
        "growth_rate": candidate.growth_rate,
        "carrying_capacity": candidate.carrying_capacity,
        "sse": round(sse, 8),
        "rmse": round(rmse, 8),
        "mae": round(mae, 8),
        "bias": round(bias, 8),
    }


def fit_model(data: list[Observation], candidates: list[ParameterCandidate]) -> tuple[dict[str, object], list[dict[str, object]]]:
    scored = [score_candidate(candidate, data) for candidate in candidates]
    best = min(scored, key=lambda row: float(row["sse"]))
    return best, scored


def calibration_risk_score(record: CalibrationRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.calibration_layer} {record.modeling_role} {record.diagnostic_question}".lower()
    for term in ["data", "loss", "residual", "validation", "parameter", "bounds", "diagnostic", "uncertainty"]:
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


def build_calibration_audit_card(
    records: list[CalibrationRecord],
    best_fit: dict[str, object],
    residual_rows: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {**asdict(record), "calibration_risk_score": calibration_risk_score(record)}
        for record in records
    ]
    residuals = [float(row["residual"]) for row in residual_rows]
    return {
        "article": "Calibration, Estimation, and Parameter Fitting",
        "best_fit": best_fit,
        "residual_summary": {
            "mean_residual": round(statistics.mean(residuals), 8),
            "max_abs_residual": round(max(abs(value) for value in residuals), 8),
            "residual_count": len(residuals),
        },
        "calibration_register": register_rows,
        "high_priority_calibration_records": [
            row for row in register_rows if float(row["calibration_risk_score"]) >= 8.0
        ],
        "diagnostic_checks": [
            "calibration observations are documented",
            "parameter bounds are explicit",
            "objective function is recorded",
            "residuals are exported",
            "best-fit parameters are not treated as final truth",
        ],
    }
