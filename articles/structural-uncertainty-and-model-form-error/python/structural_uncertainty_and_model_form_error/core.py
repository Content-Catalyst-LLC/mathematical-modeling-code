from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class ModelForm:
    key: str
    model_family: str
    structural_assumption: str
    review_question: str


@dataclass(frozen=True)
class StructuralRecord:
    key: str
    structural_layer: str
    modeling_role: str
    review_question: str
    status: str


def load_model_forms(path: Path) -> list[ModelForm]:
    forms: list[ModelForm] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            forms.append(
                ModelForm(
                    key=row["key"],
                    model_family=row["model_family"],
                    structural_assumption=row["structural_assumption"],
                    review_question=row["review_question"],
                )
            )
    if not forms:
        raise ValueError("Model-form table cannot be empty.")
    return forms


def load_records(path: Path) -> list[StructuralRecord]:
    records: list[StructuralRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                StructuralRecord(
                    key=row["key"],
                    structural_layer=row["structural_layer"],
                    modeling_role=row["modeling_role"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def simulate_model(form_key: str, years: int = 10) -> float:
    stock = 80.0
    carrying_capacity = 120.0
    extraction_rate = 0.12
    growth_rate = 0.08
    fixed_loss = 5.8
    critical_threshold = 55.0

    for _ in range(years):
        if form_key == "linear_decline":
            stock = max(0.0, stock - fixed_loss)
        elif form_key == "proportional_decline":
            stock = max(0.0, stock - extraction_rate * stock)
        elif form_key == "logistic_recovery":
            growth = growth_rate * stock * (1.0 - stock / carrying_capacity)
            extraction = extraction_rate * stock
            stock = max(0.0, stock + growth - extraction)
        elif form_key == "threshold_shift":
            if stock < critical_threshold:
                stock = max(0.0, stock - 1.6 * extraction_rate * stock)
            else:
                stock = max(0.0, stock - extraction_rate * stock)
        else:
            raise ValueError(f"Unknown model form: {form_key}")

    return round(stock, 8)


def comparison_rows(forms: list[ModelForm], threshold: float = 45.0) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for form in forms:
        output = simulate_model(form.key)
        rows.append({
            **asdict(form),
            "projected_stock": output,
            "below_threshold": output < threshold,
            "distance_to_threshold": round(output - threshold, 8),
        })
    return rows


def structural_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Structural summary requires at least one model form.")

    outputs = [float(row["projected_stock"]) for row in rows]
    threshold_flags = [bool(row["below_threshold"]) for row in rows]

    return {
        "mean_output": round(statistics.mean(outputs), 8),
        "min_output": round(min(outputs), 8),
        "max_output": round(max(outputs), 8),
        "structural_spread": round(max(outputs) - min(outputs), 8),
        "threshold_disagreement": len(set(threshold_flags)) > 1,
        "model_count": len(rows),
    }


def structural_risk_score(record: StructuralRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.structural_layer} {record.modeling_role} {record.review_question}".lower()
    for term in ["family", "functional", "boundary", "aggregation", "threshold", "regime", "scale"]:
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


def build_structural_uncertainty_assessment_card(
    rows: list[dict[str, object]],
    register_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Structural Uncertainty and Model Form Error",
        "structural_summary": structural_summary(rows),
        "model_form_comparison": rows,
        "structural_register": register_rows,
        "use_limit": "Structural uncertainty remains when plausible model forms support different outputs, thresholds, or decisions.",
        "diagnostic_checks": [
            "multiple plausible model forms are compared",
            "structural spread is reported",
            "threshold disagreement is flagged",
            "boundary and aggregation choices are reviewed",
            "model-form uncertainty is not reduced to parameter uncertainty",
        ],
    }
