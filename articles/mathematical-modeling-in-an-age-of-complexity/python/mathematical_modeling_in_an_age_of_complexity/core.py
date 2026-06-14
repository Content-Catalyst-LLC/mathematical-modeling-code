from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class ComplexityModelRecord:
    key: str
    model_role: str
    model_family: str
    complexity_feature: str
    decision_context: str
    status: str


@dataclass(frozen=True)
class ComplexityScenario:
    key: str
    scenario_name: str
    stress_level: float
    interdependence_level: float
    uncertainty_level: float
    resilience_score: float
    equity_score: float
    adaptability_score: float


def load_complexity_model_records(path: Path) -> list[ComplexityModelRecord]:
    records: list[ComplexityModelRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                ComplexityModelRecord(
                    key=row["key"],
                    model_role=row["model_role"],
                    model_family=row["model_family"],
                    complexity_feature=row["complexity_feature"],
                    decision_context=row["decision_context"],
                    status=row["status"],
                )
            )
    if not records:
        raise ValueError("Complexity model register cannot be empty.")
    return records


def load_complexity_scenarios(path: Path) -> list[ComplexityScenario]:
    scenarios: list[ComplexityScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                ComplexityScenario(
                    key=row["key"],
                    scenario_name=row["scenario_name"],
                    stress_level=float(row["stress_level"]),
                    interdependence_level=float(row["interdependence_level"]),
                    uncertainty_level=float(row["uncertainty_level"]),
                    resilience_score=float(row["resilience_score"]),
                    equity_score=float(row["equity_score"]),
                    adaptability_score=float(row["adaptability_score"]),
                )
            )
    if not scenarios:
        raise ValueError("Complexity scenario table cannot be empty.")
    return scenarios


def evaluate_scenario(scenario: ComplexityScenario) -> dict[str, object]:
    fragility_score = (
        0.35 * scenario.stress_level
        + 0.30 * scenario.interdependence_level
        + 0.25 * scenario.uncertainty_level
        + 0.10 * (1.0 - scenario.adaptability_score)
    )

    robust_value = (
        0.40 * scenario.resilience_score
        + 0.30 * scenario.equity_score
        + 0.30 * scenario.adaptability_score
        - 0.20 * fragility_score
    )

    if fragility_score >= 0.70:
        review_class = "high_complexity_risk"
    elif fragility_score >= 0.50:
        review_class = "complexity_review_required"
    else:
        review_class = "standard_monitoring"

    return {
        **asdict(scenario),
        "fragility_score": round(fragility_score, 8),
        "robust_value": round(robust_value, 8),
        "review_class": review_class,
        "requires_adaptive_trigger": scenario.uncertainty_level >= 0.60,
        "requires_interdependence_review": scenario.interdependence_level >= 0.65,
        "requires_equity_review": scenario.equity_score < 0.60,
    }


def model_priority(record: ComplexityModelRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.model_role} {record.model_family} {record.complexity_feature} {record.decision_context}".lower()
    for term in ["uncertainty", "cascading", "adaptive", "robust", "interdependence", "emergence"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def complexity_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Complexity summary requires at least one scenario.")
    fragility_scores = [float(row["fragility_score"]) for row in rows]
    robust_values = [float(row["robust_value"]) for row in rows]
    highest_risk = max(rows, key=lambda row: float(row["fragility_score"]))
    best_robust = max(rows, key=lambda row: float(row["robust_value"]))
    return {
        "highest_fragility_scenario": highest_risk["scenario_name"],
        "best_robust_value_scenario": best_robust["scenario_name"],
        "mean_fragility_score": round(statistics.mean(fragility_scores), 8),
        "mean_robust_value": round(statistics.mean(robust_values), 8),
        "max_fragility_score": round(max(fragility_scores), 8),
        "scenario_count": len(rows),
    }


def build_complexity_model_review_card(
    model_rows: list[dict[str, object]],
    scenario_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Mathematical Modeling in an Age of Complexity",
        "complexity_summary": complexity_summary(scenario_rows),
        "complexity_model_register": model_rows,
        "scenario_review": scenario_rows,
        "use_limit": "This workflow supports complexity modeling literacy, scenario comparison, and governance review; it does not replace domain expertise, stakeholder deliberation, monitoring, or accountable decision-making.",
        "diagnostic_checks": [
            "multiple model roles are represented",
            "complexity features are explicit",
            "scenarios include stress and uncertainty",
            "fragility and robust value are compared",
            "adaptive triggers are flagged",
            "equity and interdependence review are preserved",
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
