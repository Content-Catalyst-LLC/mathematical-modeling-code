from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class GeneralizationModel:
    model_id: str
    model_family: str
    training_rmse: float
    validation_rmse: float
    parameter_count: int
    complexity_score: float
    interpretability_score: float


@dataclass(frozen=True)
class GeneralizationRecord:
    key: str
    generalization_layer: str
    modeling_role: str
    review_question: str
    status: str


def load_models(path: Path) -> list[GeneralizationModel]:
    models: list[GeneralizationModel] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            models.append(
                GeneralizationModel(
                    model_id=row["model_id"],
                    model_family=row["model_family"],
                    training_rmse=float(row["training_rmse"]),
                    validation_rmse=float(row["validation_rmse"]),
                    parameter_count=int(row["parameter_count"]),
                    complexity_score=float(row["complexity_score"]),
                    interpretability_score=float(row["interpretability_score"]),
                )
            )
    if not models:
        raise ValueError("Generalization model table cannot be empty.")
    return models


def load_records(path: Path) -> list[GeneralizationRecord]:
    records: list[GeneralizationRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                GeneralizationRecord(
                    key=row["key"],
                    generalization_layer=row["generalization_layer"],
                    modeling_role=row["modeling_role"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def overfit_gap(model: GeneralizationModel) -> float:
    return round(model.validation_rmse - model.training_rmse, 8)


def classify_model(model: GeneralizationModel) -> str:
    gap = overfit_gap(model)

    if model.training_rmse >= 3.0 and model.validation_rmse >= 3.0:
        return "likely_underfit"
    if gap >= 1.0 and model.training_rmse <= 1.0:
        return "likely_overfit"
    if model.validation_rmse <= 1.5 and gap <= 0.6:
        return "generalizes_reasonably"
    return "requires_review"


def generalization_score(model: GeneralizationModel) -> float:
    return round(
        model.validation_rmse
        + 0.20 * model.complexity_score
        + 0.08 * model.parameter_count
        - 0.20 * model.interpretability_score,
        8,
    )


def model_rows(models: list[GeneralizationModel]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for model in models:
        rows.append({
            **asdict(model),
            "overfit_gap": overfit_gap(model),
            "generalization_score": generalization_score(model),
            "classification": classify_model(model),
        })
    return sorted(rows, key=lambda row: float(row["generalization_score"]))


def generalization_risk_score(record: GeneralizationRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.generalization_layer} {record.modeling_role} {record.review_question}".lower()
    for term in ["training", "validation", "overfit", "underfit", "complexity", "shift", "decision"]:
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


def build_generalization_assessment_card(
    ranked_rows: list[dict[str, object]],
    register_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Overfitting, Underfitting, and Model Generalization",
        "selected_for_review": ranked_rows[0],
        "overfit_warning_models": [row for row in ranked_rows if row["classification"] == "likely_overfit"],
        "underfit_warning_models": [row for row in ranked_rows if row["classification"] == "likely_underfit"],
        "generalization_register": register_rows,
        "use_limit": "Generalization assessment is conditional on validation design, evidence quality, and use context.",
        "diagnostic_checks": [
            "training and validation error are separated",
            "overfit gap is reported",
            "underfit conditions are flagged",
            "complexity is reviewed",
            "distribution shift remains a scope concern",
            "decision thresholds require separate review",
        ],
    }
