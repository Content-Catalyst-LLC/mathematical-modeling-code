from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class AIAssistanceRecord:
    key: str
    modeling_stage: str
    ai_role: str
    artifact_type: str
    provenance_required: bool
    human_review_required: bool
    status: str


@dataclass(frozen=True)
class HumanJudgmentCase:
    key: str
    judgment_point: str
    decision_context: str
    evidence_strength: float
    uncertainty_level: float
    consequence_level: float
    automation_bias_risk: float
    accountability_clarity: float


def _parse_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    return value.strip().lower() in {"true", "1", "yes", "y"}


def load_ai_assistance_records(path: Path) -> list[AIAssistanceRecord]:
    records: list[AIAssistanceRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                AIAssistanceRecord(
                    key=row["key"],
                    modeling_stage=row["modeling_stage"],
                    ai_role=row["ai_role"],
                    artifact_type=row["artifact_type"],
                    provenance_required=_parse_bool(row["provenance_required"]),
                    human_review_required=_parse_bool(row["human_review_required"]),
                    status=row["status"],
                )
            )
    if not records:
        raise ValueError("AI assistance register cannot be empty.")
    return records


def load_human_judgment_cases(path: Path) -> list[HumanJudgmentCase]:
    cases: list[HumanJudgmentCase] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            cases.append(
                HumanJudgmentCase(
                    key=row["key"],
                    judgment_point=row["judgment_point"],
                    decision_context=row["decision_context"],
                    evidence_strength=float(row["evidence_strength"]),
                    uncertainty_level=float(row["uncertainty_level"]),
                    consequence_level=float(row["consequence_level"]),
                    automation_bias_risk=float(row["automation_bias_risk"]),
                    accountability_clarity=float(row["accountability_clarity"]),
                )
            )
    if not cases:
        raise ValueError("Human judgment case table cannot be empty.")
    return cases


def review_priority(record: AIAssistanceRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    if record.provenance_required:
        score += 1.0
    if record.human_review_required:
        score += 1.0
    if record.artifact_type in {"model_script", "diagnostic_report", "public_summary", "use_limit_statement"}:
        score += 1.0
    return round(score, 8)


def evaluate_judgment_case(case: HumanJudgmentCase) -> dict[str, object]:
    risk_score = (
        0.25 * (1.0 - case.evidence_strength)
        + 0.25 * case.uncertainty_level
        + 0.25 * case.consequence_level
        + 0.15 * case.automation_bias_risk
        + 0.10 * (1.0 - case.accountability_clarity)
    )

    if risk_score >= 0.65:
        review_class = "escalation_required"
    elif risk_score >= 0.50:
        review_class = "human_review_required"
    else:
        review_class = "standard_review"

    return {
        **asdict(case),
        "judgment_risk_score": round(risk_score, 8),
        "review_class": review_class,
        "requires_use_limit_statement": case.consequence_level >= 0.70,
        "requires_uncertainty_brief": case.uncertainty_level >= 0.60,
        "requires_accountability_owner": case.accountability_clarity < 0.70,
    }


def judgment_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Judgment summary requires at least one row.")
    risk_scores = [float(row["judgment_risk_score"]) for row in rows]
    highest = max(rows, key=lambda row: float(row["judgment_risk_score"]))
    escalation_count = sum(1 for row in rows if row["review_class"] == "escalation_required")
    return {
        "highest_risk_judgment_point": highest["judgment_point"],
        "mean_judgment_risk_score": round(statistics.mean(risk_scores), 8),
        "max_judgment_risk_score": round(max(risk_scores), 8),
        "escalation_count": escalation_count,
        "case_count": len(rows),
    }


def build_ai_assisted_modeling_governance_card(
    assistance_rows: list[dict[str, object]],
    judgment_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "AI-Assisted Modeling and Human Judgment",
        "judgment_summary": judgment_summary(judgment_rows),
        "ai_assistance_register": assistance_rows,
        "human_judgment_review": judgment_rows,
        "use_limit": "This workflow supports AI-assisted modeling review, provenance tracking, and human judgment governance; it does not permit AI-generated artifacts to serve as final decision authority without human review, validation, and accountability.",
        "diagnostic_checks": [
            "AI assistance role is recorded",
            "artifact type is recorded",
            "provenance requirement is explicit",
            "human review requirement is explicit",
            "judgment risk is scored",
            "use-limit and uncertainty briefs are flagged",
            "accountability owner requirement is preserved",
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
