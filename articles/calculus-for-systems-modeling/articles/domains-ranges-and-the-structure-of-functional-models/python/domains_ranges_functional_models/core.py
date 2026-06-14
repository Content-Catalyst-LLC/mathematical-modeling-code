from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class Scenario:
    scenario: str
    initial_state: float
    rate: float
    capacity: float
    time_horizon: float
    interpretation: str = ""


def validate_domain(item: Scenario) -> list[str]:
    issues: list[str] = []
    if item.initial_state < 0:
        issues.append("initial_state must be nonnegative")
    if item.rate < 0:
        issues.append("rate must be nonnegative")
    if item.capacity <= 0:
        issues.append("capacity must be positive")
    if item.time_horizon < 0:
        issues.append("time_horizon must be nonnegative")
    if item.capacity > 0 and item.initial_state > item.capacity:
        issues.append("initial_state exceeds capacity")
    return issues


def bounded_growth_value(item: Scenario) -> float:
    issues = validate_domain(item)
    if issues:
        raise ValueError("; ".join(issues))
    exponent = -item.rate * item.time_horizon
    denominator = 1.0 + ((item.capacity - item.initial_state) / item.initial_state) * math.exp(exponent)
    return item.capacity / denominator


def validate_range(value: float, capacity: float) -> list[str]:
    issues: list[str] = []
    if value < 0:
        issues.append("output is negative")
    if value > capacity:
        issues.append("output exceeds capacity")
    return issues


def evaluate_scenarios(scenarios: list[Scenario]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in scenarios:
        domain_issues = validate_domain(item)
        if domain_issues:
            rows.append({"scenario": item.scenario, "status": "domain_review", "value": "", "issues": "; ".join(domain_issues), "interpretation": item.interpretation})
            continue
        value = bounded_growth_value(item)
        range_issues = validate_range(value, item.capacity)
        rows.append({"scenario": item.scenario, "status": "ok" if not range_issues else "range_review", "value": round(value, 8), "issues": "; ".join(range_issues), "interpretation": item.interpretation})
    return rows


def summarize_validation(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    counts: dict[str, int] = {}
    for row in rows:
        status = str(row["status"])
        counts[status] = counts.get(status, 0) + 1
    return [{"status": status, "count": count} for status, count in sorted(counts.items())]


def load_scenarios(path: Path) -> list[Scenario]:
    scenarios: list[Scenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(Scenario(row["scenario"], float(row["initial_state"]), float(row["rate"]), float(row["capacity"]), float(row["time_horizon"]), row.get("interpretation", "")))
    return scenarios


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


def build_manifest(scenarios: list[Scenario], results: list[dict[str, object]]) -> dict[str, object]:
    return {
        "article": "Domains, Ranges, and the Structure of Functional Models",
        "series": "Calculus for Systems Modeling",
        "model": "bounded growth with explicit domain and range validation",
        "scenarios": [asdict(item) for item in scenarios],
        "validation_summary": summarize_validation(results),
        "interpretive_warning": "Synthetic teaching workflow. Domain and range checks support interpretation but do not validate empirical accuracy."
    }
