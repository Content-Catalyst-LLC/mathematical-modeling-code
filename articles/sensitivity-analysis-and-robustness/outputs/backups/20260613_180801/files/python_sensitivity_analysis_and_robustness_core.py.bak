from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class Parameter:
    name: str
    baseline: float
    low: float
    high: float
    uncertainty_label: str


@dataclass(frozen=True)
class SensitivityRecord:
    key: str
    sensitivity_layer: str
    modeling_role: str
    review_question: str
    status: str


def load_parameters(path: Path) -> list[Parameter]:
    parameters: list[Parameter] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            parameters.append(
                Parameter(
                    name=row["name"],
                    baseline=float(row["baseline"]),
                    low=float(row["low"]),
                    high=float(row["high"]),
                    uncertainty_label=row["uncertainty_label"],
                )
            )
    if not parameters:
        raise ValueError("Sensitivity parameter table cannot be empty.")
    return parameters


def load_records(path: Path) -> list[SensitivityRecord]:
    records: list[SensitivityRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                SensitivityRecord(
                    key=row["key"],
                    sensitivity_layer=row["sensitivity_layer"],
                    modeling_role=row["modeling_role"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def resource_projection(
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


def baseline_output(params: list[Parameter]) -> float:
    values = {item.name: item.baseline for item in params}
    return resource_projection(**values)


def sweep_rows(params: list[Parameter], threshold: float = 45.0) -> list[dict[str, object]]:
    baseline_values = {item.name: item.baseline for item in params}
    base_output = resource_projection(**baseline_values)

    rows: list[dict[str, object]] = []
    for item in params:
        for level, value in [("low", item.low), ("baseline", item.baseline), ("high", item.high)]:
            values = dict(baseline_values)
            values[item.name] = value
            output = resource_projection(**values)
            delta = output - base_output
            relative_change = delta / base_output if base_output != 0 else math.nan
            rows.append({
                "parameter": item.name,
                "uncertainty_label": item.uncertainty_label,
                "level": level,
                "value": value,
                "projected_stock": output,
                "delta_from_baseline": round(delta, 8),
                "relative_change": round(relative_change, 8),
                "below_threshold": output < threshold,
            })
    return rows


def sensitivity_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["parameter"]), []).append(row)

    output: list[dict[str, object]] = []
    for parameter, values in grouped.items():
        stocks = [float(row["projected_stock"]) for row in values]
        rel = [abs(float(row["relative_change"])) for row in values]
        output.append({
            "parameter": parameter,
            "min_projected_stock": round(min(stocks), 8),
            "max_projected_stock": round(max(stocks), 8),
            "range_width": round(max(stocks) - min(stocks), 8),
            "max_abs_relative_change": round(max(rel), 8),
            "threshold_crossed": any(bool(row["below_threshold"]) for row in values),
        })
    return sorted(output, key=lambda row: float(row["range_width"]), reverse=True)


def sensitivity_risk_score(record: SensitivityRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.sensitivity_layer} {record.modeling_role} {record.review_question}".lower()
    for term in ["threshold", "stress", "structural", "decision", "data", "uncertainty"]:
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


def build_robustness_assessment_card(
    params: list[Parameter],
    sweep: list[dict[str, object]],
    summary: list[dict[str, object]],
    register_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Sensitivity Analysis and Robustness",
        "baseline_output": baseline_output(params),
        "most_sensitive_parameter": summary[0],
        "threshold_crossing_parameters": [row for row in summary if bool(row["threshold_crossed"])],
        "sensitivity_register": register_rows,
        "parameter_count": len(params),
        "sweep_row_count": len(sweep),
        "use_limit": "Sensitivity results depend on parameter ranges, scenario design, and model structure.",
        "diagnostic_checks": [
            "parameter ranges are documented",
            "baseline output is preserved",
            "sensitivity ranking is exported",
            "threshold crossings are flagged",
            "structural sensitivity remains a review obligation",
            "robustness is interpreted against decision purpose",
        ],
    }
