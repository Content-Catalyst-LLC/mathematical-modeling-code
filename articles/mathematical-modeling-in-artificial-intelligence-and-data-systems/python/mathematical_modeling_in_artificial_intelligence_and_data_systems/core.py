from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class AIModelRecord:
    key: str
    model_role: str
    model_family: str
    data_domain: str
    decision_context: str
    status: str


@dataclass(frozen=True)
class ModelCandidate:
    key: str
    model_name: str
    validation_score: float
    calibration_error: float
    subgroup_error_gap: float
    drift_score: float
    interpretability_score: float
    privacy_risk: float
    deployment_criticality: float


def load_ai_model_records(path: Path) -> list[AIModelRecord]:
    records: list[AIModelRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                AIModelRecord(
                    key=row["key"],
                    model_role=row["model_role"],
                    model_family=row["model_family"],
                    data_domain=row["data_domain"],
                    decision_context=row["decision_context"],
                    status=row["status"],
                )
            )
    if not records:
        raise ValueError("AI model register cannot be empty.")
    return records


def load_model_candidates(path: Path) -> list[ModelCandidate]:
    candidates: list[ModelCandidate] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            candidates.append(
                ModelCandidate(
                    key=row["key"],
                    model_name=row["model_name"],
                    validation_score=float(row["validation_score"]),
                    calibration_error=float(row["calibration_error"]),
                    subgroup_error_gap=float(row["subgroup_error_gap"]),
                    drift_score=float(row["drift_score"]),
                    interpretability_score=float(row["interpretability_score"]),
                    privacy_risk=float(row["privacy_risk"]),
                    deployment_criticality=float(row["deployment_criticality"]),
                )
            )
    if not candidates:
        raise ValueError("Model candidate table cannot be empty.")
    return candidates


def evaluate_candidate(candidate: ModelCandidate) -> dict[str, object]:
    penalty = (
        1.8 * candidate.calibration_error
        + 1.5 * candidate.subgroup_error_gap
        + 1.2 * candidate.drift_score
        + 1.4 * candidate.privacy_risk
        + 0.7 * candidate.deployment_criticality
        - 0.5 * candidate.interpretability_score
    )

    governance_score = candidate.validation_score - penalty

    requires_review = (
        candidate.calibration_error > 0.08
        or candidate.subgroup_error_gap > 0.12
        or candidate.drift_score > 0.20
        or candidate.privacy_risk > 0.15
        or candidate.interpretability_score < 0.50
    )

    review_class = "deployment_candidate" if not requires_review else "requires_governance_review"
    if candidate.deployment_criticality > 0.75 and requires_review:
        review_class = "high_stakes_review_required"

    return {
        **asdict(candidate),
        "governance_score": round(governance_score, 8),
        "requires_review": requires_review,
        "review_class": review_class,
    }


def model_priority(record: AIModelRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.model_role} {record.model_family} {record.decision_context}".lower()
    for term in ["ranking", "generation", "monitoring", "governance", "risk", "visibility", "accountability"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def deployment_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Deployment summary requires at least one model candidate.")
    scores = [float(row["governance_score"]) for row in rows]
    review_count = sum(1 for row in rows if bool(row["requires_review"]))
    best = max(rows, key=lambda row: float(row["governance_score"]))
    return {
        "best_governed_candidate": best["model_name"],
        "mean_governance_score": round(statistics.mean(scores), 8),
        "max_governance_score": round(max(scores), 8),
        "min_governance_score": round(min(scores), 8),
        "review_required_count": review_count,
        "candidate_count": len(rows),
    }


def build_ai_model_governance_card(
    register_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Mathematical Modeling in Artificial Intelligence and Data Systems",
        "deployment_summary": deployment_summary(candidate_rows),
        "ai_model_register": register_rows,
        "candidate_review": candidate_rows,
        "use_limit": "This workflow supports AI model governance review; it does not certify a model for deployment, automate high-stakes decisions, or replace domain, legal, security, privacy, and ethics review.",
        "diagnostic_checks": [
            "model purpose is stated",
            "data domain is documented",
            "validation score is not the only criterion",
            "calibration error is reviewed",
            "subgroup error gap is reviewed",
            "drift score is reviewed",
            "privacy risk is reviewed",
            "interpretability and human review remain required",
        ],
    }


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
