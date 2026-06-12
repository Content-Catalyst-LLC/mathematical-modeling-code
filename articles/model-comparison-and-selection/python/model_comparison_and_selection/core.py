from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class ModelCandidate:
    model_id: str
    model_family: str
    calibration_rmse: float
    validation_rmse: float
    parameter_count: int
    interpretability_score: float
    robustness_score: float
    decision_relevance_score: float


@dataclass(frozen=True)
class SelectionRecord:
    key: str
    selection_layer: str
    modeling_role: str
    review_question: str
    status: str


def load_candidates(path: Path) -> list[ModelCandidate]:
    models: list[ModelCandidate] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            models.append(
                ModelCandidate(
                    model_id=row["model_id"],
                    model_family=row["model_family"],
                    calibration_rmse=float(row["calibration_rmse"]),
                    validation_rmse=float(row["validation_rmse"]),
                    parameter_count=int(row["parameter_count"]),
                    interpretability_score=float(row["interpretability_score"]),
                    robustness_score=float(row["robustness_score"]),
                    decision_relevance_score=float(row["decision_relevance_score"]),
                )
            )
    if not models:
        raise ValueError("Candidate model table cannot be empty.")
    return models


def load_records(path: Path) -> list[SelectionRecord]:
    records: list[SelectionRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                SelectionRecord(
                    key=row["key"],
                    selection_layer=row["selection_layer"],
                    modeling_role=row["modeling_role"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def complexity_penalty(parameter_count: int) -> float:
    if parameter_count < 0:
        raise ValueError("parameter_count cannot be negative.")
    return 0.08 * parameter_count


def comparison_score(model: ModelCandidate) -> float:
    return round(
        model.validation_rmse
        + complexity_penalty(model.parameter_count)
        - 0.35 * model.interpretability_score
        - 0.40 * model.robustness_score
        - 0.35 * model.decision_relevance_score,
        8,
    )


def overfit_gap(model: ModelCandidate) -> float:
    return round(model.validation_rmse - model.calibration_rmse, 8)


def model_rows(models: list[ModelCandidate]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for model in models:
        gap = overfit_gap(model)
        rows.append({
            **asdict(model),
            "overfit_gap": gap,
            "complexity_penalty": round(complexity_penalty(model.parameter_count), 8),
            "comparison_score": comparison_score(model),
            "overfit_flag": gap > 1.0,
        })
    return sorted(rows, key=lambda row: float(row["comparison_score"]))


def selection_risk_score(record: SelectionRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.selection_layer} {record.modeling_role} {record.review_question}".lower()
    for term in ["alternative", "validation", "complexity", "uncertainty", "decision", "robust", "interpret"]:
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


def build_selection_audit_card(
    ranked_rows: list[dict[str, object]],
    register_rows: list[dict[str, object]],
) -> dict[str, object]:
    selected = ranked_rows[0]
    return {
        "article": "Model Comparison and Selection",
        "selected_model": selected,
        "ranking_method": "Validation error plus complexity penalty minus interpretability, robustness, and decision-relevance credits.",
        "overfit_warning_models": [row for row in ranked_rows if bool(row["overfit_flag"])],
        "selection_register": register_rows,
        "use_limit": "Selection is purpose-specific and should not be generalized beyond the comparison criteria.",
        "diagnostic_checks": [
            "candidate models include a baseline",
            "validation error is separated from calibration error",
            "complexity penalty is visible",
            "overfit gap is reported",
            "interpretability and decision relevance are included",
            "alternative models are preserved rather than erased",
        ],
    }
