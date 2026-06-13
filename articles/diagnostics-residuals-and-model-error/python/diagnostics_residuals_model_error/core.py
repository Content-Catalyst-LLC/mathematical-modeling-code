from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math
import statistics


@dataclass(frozen=True)
class DiagnosticObservation:
    time: int
    group: str
    observed_value: float
    predicted_value: float
    decision_threshold: float


@dataclass(frozen=True)
class DiagnosticRecord:
    key: str
    diagnostic_layer: str
    modeling_role: str
    review_question: str
    status: str


def load_observations(path: Path) -> list[DiagnosticObservation]:
    observations: list[DiagnosticObservation] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            observations.append(
                DiagnosticObservation(
                    time=int(row["time"]),
                    group=row["group"],
                    observed_value=float(row["observed_value"]),
                    predicted_value=float(row["predicted_value"]),
                    decision_threshold=float(row["decision_threshold"]),
                )
            )
    if not observations:
        raise ValueError("Diagnostic observations cannot be empty.")
    return observations


def load_records(path: Path) -> list[DiagnosticRecord]:
    records: list[DiagnosticRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                DiagnosticRecord(
                    key=row["key"],
                    diagnostic_layer=row["diagnostic_layer"],
                    modeling_role=row["modeling_role"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def residual_rows(data: list[DiagnosticObservation]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in data:
        residual = item.observed_value - item.predicted_value
        near_threshold = abs(item.observed_value - item.decision_threshold) <= 3.0
        decision_disagreement = (
            item.observed_value < item.decision_threshold
        ) != (
            item.predicted_value < item.decision_threshold
        )
        rows.append({
            **asdict(item),
            "residual": round(residual, 8),
            "absolute_error": round(abs(residual), 8),
            "squared_error": round(residual * residual, 8),
            "near_threshold": near_threshold,
            "decision_disagreement": decision_disagreement,
        })
    return rows


def error_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Error summary requires at least one row.")

    residuals = [float(row["residual"]) for row in rows]
    abs_errors = [float(row["absolute_error"]) for row in rows]
    sq_errors = [float(row["squared_error"]) for row in rows]

    return {
        "mean_error": round(statistics.mean(residuals), 8),
        "mae": round(sum(abs_errors) / len(abs_errors), 8),
        "rmse": round(math.sqrt(sum(sq_errors) / len(sq_errors)), 8),
        "median_absolute_error": round(statistics.median(abs_errors), 8),
        "max_absolute_error": round(max(abs_errors), 8),
        "n": len(rows),
    }


def group_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["group"]), []).append(row)

    output: list[dict[str, object]] = []
    for group, values in sorted(grouped.items()):
        summary = error_summary(values)
        output.append({"group": group, **summary})
    return output


def flag_outliers(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    abs_errors = [float(row["absolute_error"]) for row in rows]
    median_error = statistics.median(abs_errors)
    threshold = max(2.5, 2.0 * median_error)

    flagged: list[dict[str, object]] = []
    for row in rows:
        if float(row["absolute_error"]) >= threshold:
            flagged.append({**row, "outlier_threshold": round(threshold, 8)})
    return flagged


def diagnostic_risk_score(record: DiagnosticRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.diagnostic_layer} {record.modeling_role} {record.review_question}".lower()
    for term in ["bias", "threshold", "group", "outlier", "structural", "decision", "uncertainty"]:
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


def build_diagnostic_assessment_card(
    rows: list[dict[str, object]],
    register_rows: list[dict[str, object]],
) -> dict[str, object]:
    overall = error_summary(rows)
    by_group = group_summary(rows)
    outliers = flag_outliers(rows)
    threshold_rows = [row for row in rows if bool(row["near_threshold"])]

    return {
        "article": "Diagnostics, Residuals, and Model Error",
        "overall_error_summary": overall,
        "group_summary": by_group,
        "threshold_case_count": len(threshold_rows),
        "decision_disagreement_count": sum(1 for row in rows if bool(row["decision_disagreement"])),
        "outlier_count": len(outliers),
        "diagnostic_register": register_rows,
        "use_limit": "Diagnostic evidence is purpose-specific and should be interpreted against model scope, uncertainty, and decision consequences.",
        "diagnostic_checks": [
            "residuals are preserved",
            "bias metrics are reported",
            "group summaries are exported",
            "threshold cases are identified",
            "outliers are flagged",
            "model-form review remains required when residuals show structure",
        ],
    }
