from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class FunctionalModel:
    model_key: str
    model_name: str
    functional_form: str
    interpretation: str


def linear_model(x: float, a: float = 10.0, b: float = 2.0) -> float:
    return a + b * x


def exponential_model(x: float, a: float = 10.0, b: float = 0.18) -> float:
    return a * math.exp(b * x)


def logistic_model(x: float, capacity: float = 100.0, rate: float = 0.75, midpoint: float = 5.0) -> float:
    return capacity / (1.0 + math.exp(-rate * (x - midpoint)))


def threshold_model(x: float, threshold: float = 5.0, low: float = 20.0, high: float = 80.0) -> float:
    return low if x < threshold else high


def evaluate_models(x_values: list[float]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for x in x_values:
        rows.append({
            "x": x,
            "model": "linear_growth",
            "functional_form": "y = a + bx",
            "value": linear_model(x),
            "interpretation": "constant marginal change",
        })
        rows.append({
            "x": x,
            "model": "exponential_growth",
            "functional_form": "y = a exp(bx)",
            "value": exponential_model(x),
            "interpretation": "compounding change",
        })
        rows.append({
            "x": x,
            "model": "logistic_growth",
            "functional_form": "y = K / (1 + exp(-r(x-c)))",
            "value": logistic_model(x),
            "interpretation": "bounded growth toward capacity",
        })
        rows.append({
            "x": x,
            "model": "threshold_response",
            "functional_form": "piecewise threshold",
            "value": threshold_model(x),
            "interpretation": "regime-dependent response",
        })

    return rows


def summarize_results(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["model"]), []).append(row)

    summary: list[dict[str, object]] = []
    for model, values in sorted(grouped.items()):
        ordered = sorted(values, key=lambda item: float(item["x"]))
        summary.append({
            "model": model,
            "minimum_value": round(min(float(item["value"]) for item in ordered), 8),
            "maximum_value": round(max(float(item["value"]) for item in ordered), 8),
            "final_value": round(float(ordered[-1]["value"]), 8),
            "functional_form": ordered[0]["functional_form"],
            "interpretation": ordered[0]["interpretation"],
        })

    return summary


def load_x_values(path: Path) -> list[float]:
    values: list[float] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            values.append(float(row["x"]))
    return values


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


def build_manifest(summary: list[dict[str, object]]) -> dict[str, object]:
    return {
        "article": "Functions, Variables, and Mathematical Representation",
        "series": "Calculus for Systems Modeling",
        "models_compared": len(summary),
        "summary": summary,
        "interpretive_warning": "Synthetic teaching example. Functional forms are representation choices, not empirical claims.",
    }
