from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class ModelScenario:
    key: str
    model_form: str
    scenario: str
    extraction_multiplier: float
    shock: float
    review_question: str


@dataclass(frozen=True)
class RobustnessRecord:
    key: str
    dependence_layer: str
    modeling_role: str
    review_question: str
    status: str


def load_scenarios(path: Path) -> list[ModelScenario]:
    items: list[ModelScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            items.append(
                ModelScenario(
                    key=row["key"],
                    model_form=row["model_form"],
                    scenario=row["scenario"],
                    extraction_multiplier=float(row["extraction_multiplier"]),
                    shock=float(row["shock"]),
                    review_question=row["review_question"],
                )
            )
    if not items:
        raise ValueError("Robustness scenario table cannot be empty.")
    return items


def load_records(path: Path) -> list[RobustnessRecord]:
    records: list[RobustnessRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                RobustnessRecord(
                    key=row["key"],
                    dependence_layer=row["dependence_layer"],
                    modeling_role=row["modeling_role"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def simulate(form: str, extraction_multiplier: float, shock: float, years: int = 10) -> float:
    stock = 80.0
    carrying_capacity = 120.0
    growth_rate = 0.08
    extraction_rate = 0.12 * extraction_multiplier
    fixed_loss = 5.8 * extraction_multiplier
    critical_threshold = 55.0

    for _ in range(years):
        if form == "linear_decline":
            stock = max(0.0, stock - fixed_loss - shock * stock)
        elif form == "logistic_recovery":
            growth = growth_rate * stock * (1.0 - stock / carrying_capacity)
            extraction = extraction_rate * stock
            stock = max(0.0, stock + growth - extraction - shock * stock)
        elif form == "threshold_shift":
            if stock < critical_threshold:
                stock = max(0.0, stock - 1.6 * extraction_rate * stock - shock * stock)
            else:
                stock = max(0.0, stock - extraction_rate * stock - shock * stock)
        else:
            raise ValueError(f"Unknown model form: {form}")

    return round(stock, 8)


def robustness_rows(items: list[ModelScenario], threshold: float = 45.0) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in items:
        output = simulate(item.model_form, item.extraction_multiplier, item.shock)
        rows.append({
            **asdict(item),
            "projected_stock": output,
            "below_threshold": output < threshold,
            "distance_to_threshold": round(output - threshold, 8),
            "fragility_class": "fragile" if abs(output - threshold) <= 5 else "stable_margin",
        })
    return rows


def robustness_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Robustness summary requires at least one row.")

    outputs = [float(row["projected_stock"]) for row in rows]
    threshold_flags = [bool(row["below_threshold"]) for row in rows]
    fragile_count = sum(1 for row in rows if row["fragility_class"] == "fragile")

    return {
        "mean_output": round(statistics.mean(outputs), 8),
        "min_output": round(min(outputs), 8),
        "max_output": round(max(outputs), 8),
        "robustness_spread": round(max(outputs) - min(outputs), 8),
        "threshold_disagreement": len(set(threshold_flags)) > 1,
        "fragile_case_count": fragile_count,
        "scenario_count": len(rows),
    }


def robustness_risk_score(record: RobustnessRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.dependence_layer} {record.modeling_role} {record.review_question}".lower()
    for term in ["threshold", "scenario", "model", "parameter", "data", "stress", "reverse"]:
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


def build_robustness_fragility_assessment_card(
    rows: list[dict[str, object]],
    register_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Robustness, Fragility, and Model Dependence",
        "robustness_summary": robustness_summary(rows),
        "robustness_matrix": rows,
        "robustness_register": register_rows,
        "use_limit": "Robustness conclusions depend on the perturbations, model forms, thresholds, and scenarios included in the review.",
        "diagnostic_checks": [
            "model forms are varied",
            "stress scenarios are included",
            "threshold disagreement is flagged",
            "fragility classes are reported",
            "model dependence is not hidden",
            "decision interpretation accounts for robustness evidence",
        ],
    }
