from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class ModelFailureRecord:
    key: str
    failure_mode: str
    model_stage: str
    ethical_issue: str
    likely_cause: str
    review_status: str


@dataclass(frozen=True)
class ModelRiskCase:
    key: str
    model_name: str
    intended_use: str
    severity: float
    likelihood: float
    detectability_gap: float
    uncertainty_level: float
    equity_concern: float
    accountability_gap: float


def load_failure_records(path: Path) -> list[ModelFailureRecord]:
    records: list[ModelFailureRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                ModelFailureRecord(
                    key=row["key"],
                    failure_mode=row["failure_mode"],
                    model_stage=row["model_stage"],
                    ethical_issue=row["ethical_issue"],
                    likely_cause=row["likely_cause"],
                    review_status=row["review_status"],
                )
            )
    if not records:
        raise ValueError("Model failure register cannot be empty.")
    return records


def load_risk_cases(path: Path) -> list[ModelRiskCase]:
    cases: list[ModelRiskCase] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            cases.append(
                ModelRiskCase(
                    key=row["key"],
                    model_name=row["model_name"],
                    intended_use=row["intended_use"],
                    severity=float(row["severity"]),
                    likelihood=float(row["likelihood"]),
                    detectability_gap=float(row["detectability_gap"]),
                    uncertainty_level=float(row["uncertainty_level"]),
                    equity_concern=float(row["equity_concern"]),
                    accountability_gap=float(row["accountability_gap"]),
                )
            )
    if not cases:
        raise ValueError("Model ethics risk case table cannot be empty.")
    return cases


def ethical_risk_score(case: ModelRiskCase) -> float:
    score = (
        1.8 * case.severity
        + 1.3 * case.likelihood
        + 1.2 * case.detectability_gap
        + 1.1 * case.uncertainty_level
        + 1.5 * case.equity_concern
        + 1.6 * case.accountability_gap
    )
    return round(score, 8)


def evaluate_risk_case(case: ModelRiskCase) -> dict[str, object]:
    score = ethical_risk_score(case)
    if score >= 6.0:
        review_class = "high_ethics_review_required"
    elif score >= 4.0:
        review_class = "governance_review_required"
    else:
        review_class = "standard_review"

    return {
        **asdict(case),
        "ethical_risk_score": score,
        "review_class": review_class,
        "requires_use_limit_statement": True,
        "requires_human_decision_owner": case.accountability_gap >= 0.40,
        "requires_equity_review": case.equity_concern >= 0.50,
    }


def failure_priority(record: ModelFailureRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.review_status.lower(),
        4.0,
    )
    text = f"{record.failure_mode} {record.ethical_issue} {record.likely_cause}".lower()
    for term in ["accountability", "bias", "validation", "uncertainty", "boundary", "precision", "scope"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def ethics_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Ethics summary requires at least one model risk case.")
    scores = [float(row["ethical_risk_score"]) for row in rows]
    high_review = sum(1 for row in rows if row["review_class"] == "high_ethics_review_required")
    highest = max(rows, key=lambda row: float(row["ethical_risk_score"]))
    return {
        "highest_risk_model": highest["model_name"],
        "mean_ethical_risk_score": round(statistics.mean(scores), 8),
        "max_ethical_risk_score": round(max(scores), 8),
        "min_ethical_risk_score": round(min(scores), 8),
        "high_ethics_review_count": high_review,
        "case_count": len(rows),
    }


def build_model_ethics_governance_card(
    failure_rows: list[dict[str, object]],
    risk_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Limits, Failure, and the Ethics of Modeling",
        "ethics_summary": ethics_summary(risk_rows),
        "failure_register": failure_rows,
        "risk_review": risk_rows,
        "use_limit": "This workflow supports model ethics review and failure-mode analysis; it does not certify a model for consequential deployment or replace domain, legal, institutional, stakeholder, or ethical review.",
        "diagnostic_checks": [
            "model purpose is explicit",
            "failure modes are registered",
            "uncertainty and false precision are reviewed",
            "equity concern is scored",
            "accountability gap is scored",
            "use limits and decision ownership are required",
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
