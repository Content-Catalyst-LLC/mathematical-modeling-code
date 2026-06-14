from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class ModelGovernanceRecord:
    key: str
    model_name: str
    model_purpose: str
    risk_tier: str
    validation_status: str
    use_limit_status: str
    monitoring_status: str
    model_owner: str
    decision_owner: str


@dataclass(frozen=True)
class GovernanceRiskCase:
    key: str
    model_name: str
    error_risk: float
    uncertainty_level: float
    consequence_level: float
    scope_misuse_risk: float
    accountability_gap: float


def load_governance_register(path: Path) -> list[ModelGovernanceRecord]:
    records: list[ModelGovernanceRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(ModelGovernanceRecord(**row))
    if not records:
        raise ValueError("Model governance register cannot be empty.")
    return records


def load_governance_risk_cases(path: Path) -> list[GovernanceRiskCase]:
    cases: list[GovernanceRiskCase] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            cases.append(
                GovernanceRiskCase(
                    key=row["key"],
                    model_name=row["model_name"],
                    error_risk=float(row["error_risk"]),
                    uncertainty_level=float(row["uncertainty_level"]),
                    consequence_level=float(row["consequence_level"]),
                    scope_misuse_risk=float(row["scope_misuse_risk"]),
                    accountability_gap=float(row["accountability_gap"]),
                )
            )
    if not cases:
        raise ValueError("Governance risk case table cannot be empty.")
    return cases


def governance_priority(record: ModelGovernanceRecord) -> float:
    score = {"low": 1.0, "medium": 3.0, "high": 6.0, "critical": 9.0}.get(
        record.risk_tier.lower(),
        4.0,
    )
    if record.validation_status != "validated_with_limits":
        score += 2.0
    if record.use_limit_status not in {"approved", "approved_with_limits"}:
        score += 2.0
    if record.monitoring_status != "active":
        score += 1.5
    if not record.model_owner or not record.decision_owner:
        score += 3.0
    return round(score, 8)


def evaluate_governance_risk(case: GovernanceRiskCase) -> dict[str, object]:
    governance_risk_score = (
        0.20 * case.error_risk
        + 0.20 * case.uncertainty_level
        + 0.25 * case.consequence_level
        + 0.20 * case.scope_misuse_risk
        + 0.15 * case.accountability_gap
    )

    if governance_risk_score >= 0.70:
        review_class = "escalation_required"
    elif governance_risk_score >= 0.55:
        review_class = "governance_review_required"
    else:
        review_class = "standard_monitoring"

    return {
        **asdict(case),
        "governance_risk_score": round(governance_risk_score, 8),
        "review_class": review_class,
        "requires_uncertainty_brief": case.uncertainty_level >= 0.60,
        "requires_use_limit_review": case.scope_misuse_risk >= 0.45,
        "requires_accountability_review": case.accountability_gap >= 0.30,
    }


def governance_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Governance summary requires at least one row.")
    scores = [float(row["governance_risk_score"]) for row in rows]
    highest = max(rows, key=lambda row: float(row["governance_risk_score"]))
    escalation_count = sum(1 for row in rows if row["review_class"] == "escalation_required")
    return {
        "highest_risk_model": highest["model_name"],
        "mean_governance_risk_score": round(statistics.mean(scores), 8),
        "max_governance_risk_score": round(max(scores), 8),
        "escalation_count": escalation_count,
        "case_count": len(rows),
    }


def build_model_governance_card(
    register_rows: list[dict[str, object]],
    risk_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Model Governance and Accountability",
        "governance_summary": governance_summary(risk_rows),
        "model_governance_register": register_rows,
        "model_governance_risk_review": risk_rows,
        "use_limit": "This workflow supports model governance review and accountability documentation; it does not replace domain validation, legal review, ethical review, stakeholder engagement, or accountable decision ownership.",
        "diagnostic_checks": [
            "model purpose is recorded",
            "risk tier is recorded",
            "validation status is recorded",
            "use-limit status is recorded",
            "monitoring status is recorded",
            "model owner and decision owner are recorded",
            "risk review flags uncertainty, use-limit, and accountability review needs",
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
