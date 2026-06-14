from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class InterpretationRecord:
    key: str
    interpretation_layer: str
    model_role: str
    decision_question: str
    status: str


@dataclass(frozen=True)
class DecisionOption:
    key: str
    option_name: str
    expected_stock: float
    lower_bound: float
    upper_bound: float
    implementation_burden: float
    consequence_if_wrong: float
    description: str


def load_interpretation_records(path: Path) -> list[InterpretationRecord]:
    records: list[InterpretationRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                InterpretationRecord(
                    key=row["key"],
                    interpretation_layer=row["interpretation_layer"],
                    model_role=row["model_role"],
                    decision_question=row["decision_question"],
                    status=row["status"],
                )
            )
    if not records:
        raise ValueError("Interpretation register cannot be empty.")
    return records


def load_decision_options(path: Path) -> list[DecisionOption]:
    options: list[DecisionOption] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            options.append(
                DecisionOption(
                    key=row["key"],
                    option_name=row["option_name"],
                    expected_stock=float(row["expected_stock"]),
                    lower_bound=float(row["lower_bound"]),
                    upper_bound=float(row["upper_bound"]),
                    implementation_burden=float(row["implementation_burden"]),
                    consequence_if_wrong=float(row["consequence_if_wrong"]),
                    description=row["description"],
                )
            )
    if not options:
        raise ValueError("Decision options table cannot be empty.")
    return options


def evaluate_option(option: DecisionOption, threshold: float = 45.0) -> dict[str, object]:
    crosses_threshold = option.lower_bound < threshold
    threshold_margin = option.expected_stock - threshold
    robustness_class = "robust" if option.lower_bound >= threshold else "fragile"
    decision_score = (
        option.expected_stock
        - 0.8 * option.implementation_burden
        - 1.2 * option.consequence_if_wrong
        - (8.0 if crosses_threshold else 0.0)
    )

    return {
        **asdict(option),
        "threshold": threshold,
        "threshold_margin": round(threshold_margin, 8),
        "crosses_threshold_under_uncertainty": crosses_threshold,
        "robustness_class": robustness_class,
        "decision_score": round(decision_score, 8),
    }


def interpretation_priority(record: InterpretationRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.interpretation_layer} {record.model_role} {record.decision_question}".lower()
    for term in ["threshold", "decision", "uncertainty", "values", "governance", "owner"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def decision_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Decision summary requires at least one option.")
    scores = [float(row["decision_score"]) for row in rows]
    fragile_count = sum(1 for row in rows if row["robustness_class"] == "fragile")
    best = max(rows, key=lambda row: float(row["decision_score"]))

    return {
        "best_scored_option": best["option_name"],
        "mean_score": round(statistics.mean(scores), 8),
        "max_score": round(max(scores), 8),
        "min_score": round(min(scores), 8),
        "fragile_option_count": fragile_count,
        "option_count": len(rows),
    }


def build_decision_support_review_card(
    interpretation_rows: list[dict[str, object]],
    option_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Model Interpretation and Decision-Making",
        "decision_summary": decision_summary(option_rows),
        "interpretation_register": interpretation_rows,
        "decision_options": option_rows,
        "use_limit": "This workflow supports interpretation and decision review; it does not automate the final decision.",
        "diagnostic_checks": [
            "model output is separated from decision",
            "threshold risk is reviewed",
            "uncertainty is connected to action",
            "tradeoffs are documented",
            "decision ownership remains human or institutional",
            "monitoring and update triggers are required",
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
