from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class FutureModelingDirection:
    key: str
    direction_name: str
    modeling_area: str
    complexity_relevance: float
    technical_maturity: float
    governance_need: float
    uncertainty_pressure: float
    human_judgment_need: float


def load_future_modeling_directions(path: Path) -> list[FutureModelingDirection]:
    directions: list[FutureModelingDirection] = []
    with path.open("r", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            directions.append(FutureModelingDirection(
                key=row["key"],
                direction_name=row["direction_name"],
                modeling_area=row["modeling_area"],
                complexity_relevance=float(row["complexity_relevance"]),
                technical_maturity=float(row["technical_maturity"]),
                governance_need=float(row["governance_need"]),
                uncertainty_pressure=float(row["uncertainty_pressure"]),
                human_judgment_need=float(row["human_judgment_need"]),
            ))
    if not directions:
        raise ValueError("Future modeling direction register cannot be empty.")
    return directions


def direction_priority(row: FutureModelingDirection) -> dict[str, object]:
    future_priority_score = (
        0.25 * row.complexity_relevance
        + 0.20 * row.technical_maturity
        + 0.20 * row.governance_need
        + 0.20 * row.uncertainty_pressure
        + 0.15 * row.human_judgment_need
    )
    if row.governance_need >= 0.85 or row.human_judgment_need >= 0.90:
        review_class = "governance_priority"
    elif row.uncertainty_pressure >= 0.85:
        review_class = "uncertainty_priority"
    elif future_priority_score >= 0.78:
        review_class = "strategic_priority"
    else:
        review_class = "monitor"
    return {
        **asdict(row),
        "future_priority_score": round(future_priority_score, 8),
        "review_class": review_class,
        "requires_governance_plan": row.governance_need >= 0.80,
        "requires_uncertainty_brief": row.uncertainty_pressure >= 0.75,
        "requires_human_judgment_protocol": row.human_judgment_need >= 0.80,
    }


def portfolio_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Future modeling portfolio summary requires rows.")
    scores = [float(row["future_priority_score"]) for row in rows]
    highest = max(rows, key=lambda row: float(row["future_priority_score"]))
    return {
        "highest_priority_direction": highest["direction_name"],
        "mean_future_priority_score": round(statistics.mean(scores), 8),
        "max_future_priority_score": round(max(scores), 8),
        "governance_plan_count": sum(1 for row in rows if bool(row["requires_governance_plan"])),
        "uncertainty_brief_count": sum(1 for row in rows if bool(row["requires_uncertainty_brief"])),
        "human_judgment_protocol_count": sum(1 for row in rows if bool(row["requires_human_judgment_protocol"])),
        "direction_count": len(rows),
    }


def build_future_modeling_review_card(direction_rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "article": "Future Directions in Mathematical Modeling",
        "portfolio_summary": portfolio_summary(direction_rows),
        "future_modeling_directions": direction_rows,
        "use_limit": "This workflow supports strategic review of future modeling directions; it does not rank methods as universally superior or replace domain-specific validation, governance, stakeholder review, or human judgment.",
        "diagnostic_checks": [
            "future modeling directions are explicitly registered",
            "complexity relevance is scored",
            "technical maturity is scored",
            "governance need is scored",
            "uncertainty pressure is scored",
            "human judgment need is scored",
            "governance and uncertainty requirements are flagged",
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
