from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import platform
import random
import sys


@dataclass(frozen=True)
class WorkflowRecord:
    key: str
    workflow_stage: str
    computational_object: str
    modeling_role: str
    review_question: str
    status: str


@dataclass(frozen=True)
class ResourceScenario:
    scenario: str
    initial_stock: float
    growth_rate: float
    carrying_capacity: float
    extraction: float
    shock_probability: float
    shock_fraction: float
    steps: int
    seed: int


def validate_scenario(scenario: ResourceScenario) -> None:
    if scenario.initial_stock < 0:
        raise ValueError("initial_stock must be nonnegative.")
    if scenario.growth_rate < 0:
        raise ValueError("growth_rate must be nonnegative.")
    if scenario.carrying_capacity <= 0:
        raise ValueError("carrying_capacity must be positive.")
    if scenario.extraction < 0:
        raise ValueError("extraction must be nonnegative.")
    if not 0 <= scenario.shock_probability <= 1:
        raise ValueError("shock_probability must be in [0, 1].")
    if not 0 <= scenario.shock_fraction <= 1:
        raise ValueError("shock_fraction must be in [0, 1].")
    if scenario.steps < 1:
        raise ValueError("steps must be positive.")


def simulate(scenario: ResourceScenario) -> list[dict[str, object]]:
    validate_scenario(scenario)
    rng = random.Random(scenario.seed)
    stock = scenario.initial_stock
    rows: list[dict[str, object]] = []

    for step in range(scenario.steps + 1):
        rows.append({
            "scenario": scenario.scenario,
            "step": step,
            "resource_stock": round(stock, 8),
            "seed": scenario.seed,
        })

        if step == scenario.steps:
            break

        growth = scenario.growth_rate * stock * (1.0 - stock / scenario.carrying_capacity)
        shock = stock * scenario.shock_fraction if rng.random() < scenario.shock_probability else 0.0
        stock = max(0.0, stock + growth - scenario.extraction - shock)

    return rows


def summarize_trajectories(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["scenario"]), []).append(row)

    output: list[dict[str, object]] = []
    for scenario, values in sorted(grouped.items()):
        final = max(values, key=lambda item: int(item["step"]))
        minimum = min(float(item["resource_stock"]) for item in values)
        output.append({
            "scenario": scenario,
            "final_stock": round(float(final["resource_stock"]), 8),
            "minimum_stock": round(minimum, 8),
            "steps": len(values) - 1,
            "seed": final["seed"],
        })
    return output


def workflow_risk_score(record: WorkflowRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.workflow_stage} {record.computational_object} {record.review_question}".lower()
    for term in ["schema", "manifest", "configuration", "execution", "audit", "reproduce", "validation", "output"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def hash_file(path: Path) -> str:
    if not path.exists():
        return "missing"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def load_records(path: Path) -> list[WorkflowRecord]:
    records: list[WorkflowRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                WorkflowRecord(
                    key=row["key"],
                    workflow_stage=row["workflow_stage"],
                    computational_object=row["computational_object"],
                    modeling_role=row["modeling_role"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_scenarios(path: Path) -> list[ResourceScenario]:
    scenarios: list[ResourceScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenario = ResourceScenario(
                scenario=row["scenario"],
                initial_stock=float(row["initial_stock"]),
                growth_rate=float(row["growth_rate"]),
                carrying_capacity=float(row["carrying_capacity"]),
                extraction=float(row["extraction"]),
                shock_probability=float(row["shock_probability"]),
                shock_fraction=float(row["shock_fraction"]),
                steps=int(row["steps"]),
                seed=int(row["seed"]),
            )
            validate_scenario(scenario)
            scenarios.append(scenario)
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


def build_run_manifest(
    article: str,
    scenarios: list[ResourceScenario],
    output_paths: dict[str, Path],
) -> dict[str, object]:
    return {
        "article": article,
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "scenarios": [asdict(scenario) for scenario in scenarios],
        "outputs": {key: str(path) for key, path in output_paths.items()},
        "output_hashes": {f"{key}_sha256": hash_file(path) for key, path in output_paths.items()},
    }


def build_output_index(output_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = []
    for key, path in sorted(output_paths.items()):
        rows.append({
            "output_key": key,
            "path": str(path),
            "exists": path.exists(),
            "sha256": hash_file(path),
        })
    return rows


def build_workflow_audit_card(
    records: list[WorkflowRecord],
    scenarios: list[ResourceScenario],
    summary_rows: list[dict[str, object]],
    output_paths: dict[str, Path],
) -> dict[str, object]:
    register_rows = [
        {**asdict(record), "workflow_risk_score": workflow_risk_score(record)}
        for record in records
    ]

    return {
        "article": "Scientific Computing for Modeling Workflows",
        "scenario_count": len(scenarios),
        "workflow_register": register_rows,
        "summary": summary_rows,
        "output_index": build_output_index(output_paths),
        "high_priority_workflow_records": [
            row for row in register_rows if float(row["workflow_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "inputs and configuration are documented",
            "model execution is reproducible",
            "outputs are indexed and hashed",
            "run environment is recorded",
            "workflow governance artifacts are generated",
        ],
    }
