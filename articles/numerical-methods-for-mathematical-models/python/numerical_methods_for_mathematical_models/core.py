from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class NumericalRecord:
    key: str
    component_type: str
    numerical_structure: str
    interpretation: str
    review_question: str
    status: str


@dataclass(frozen=True)
class SolverScenario:
    scenario: str
    initial_stock: float
    growth_rate: float
    carrying_capacity: float
    extraction: float
    horizon: float
    step_size: float


def validate_scenario(scenario: SolverScenario) -> None:
    if scenario.initial_stock < 0:
        raise ValueError("initial_stock must be nonnegative.")
    if scenario.growth_rate < 0:
        raise ValueError("growth_rate must be nonnegative.")
    if scenario.carrying_capacity <= 0:
        raise ValueError("carrying_capacity must be positive.")
    if scenario.extraction < 0:
        raise ValueError("extraction must be nonnegative.")
    if scenario.horizon <= 0 or scenario.step_size <= 0:
        raise ValueError("horizon and step_size must be positive.")


def derivative(stock: float, growth_rate: float, carrying_capacity: float, extraction: float) -> float:
    return growth_rate * stock * (1.0 - stock / carrying_capacity) - extraction


def run_euler(scenario: SolverScenario) -> list[dict[str, object]]:
    validate_scenario(scenario)
    steps = int(round(scenario.horizon / scenario.step_size))
    stock = scenario.initial_stock
    rows: list[dict[str, object]] = []

    for index in range(steps + 1):
        time = index * scenario.step_size
        rows.append({
            "scenario": scenario.scenario,
            "step_size": scenario.step_size,
            "index": index,
            "time": round(time, 8),
            "resource_stock": round(stock, 8),
        })

        if index == steps:
            break

        stock = stock + scenario.step_size * derivative(
            stock,
            scenario.growth_rate,
            scenario.carrying_capacity,
            scenario.extraction,
        )
        stock = max(0.0, stock)

    return rows


def convergence_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[float, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(float(row["step_size"]), []).append(row)

    final_rows = []
    for step_size, step_rows in sorted(grouped.items(), reverse=True):
        final = max(step_rows, key=lambda item: int(item["index"]))
        final_rows.append({
            "step_size": step_size,
            "final_stock": float(final["resource_stock"]),
        })

    reference = min(final_rows, key=lambda row: float(row["step_size"]))["final_stock"]

    output = []
    for row in sorted(final_rows, key=lambda item: float(item["step_size"])):
        output.append({
            "step_size": row["step_size"],
            "final_stock": round(row["final_stock"], 8),
            "absolute_difference_from_finest_step": round(abs(row["final_stock"] - reference), 8),
        })

    return output


def numerical_risk_score(record: NumericalRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.component_type} {record.numerical_structure} {record.review_question}".lower()
    for term in ["step", "convergence", "stability", "discretization", "constraint", "error", "solver"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_records(path: Path) -> list[NumericalRecord]:
    records: list[NumericalRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                NumericalRecord(
                    key=row["key"],
                    component_type=row["component_type"],
                    numerical_structure=row["numerical_structure"],
                    interpretation=row["interpretation"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_scenarios(path: Path) -> list[SolverScenario]:
    scenarios: list[SolverScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenario = SolverScenario(
                scenario=row["scenario"],
                initial_stock=float(row["initial_stock"]),
                growth_rate=float(row["growth_rate"]),
                carrying_capacity=float(row["carrying_capacity"]),
                extraction=float(row["extraction"]),
                horizon=float(row["horizon"]),
                step_size=float(row["step_size"]),
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


def build_numerical_audit_card(
    records: list[NumericalRecord],
    scenarios: list[SolverScenario],
    convergence_rows: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {**asdict(record), "numerical_risk_score": numerical_risk_score(record)}
        for record in records
    ]

    return {
        "article": "Numerical Methods for Mathematical Models",
        "method": "Euler time stepping",
        "scenario_count": len(scenarios),
        "scenarios": [asdict(scenario) for scenario in scenarios],
        "model_register": register_rows,
        "convergence_summary": convergence_rows,
        "high_priority_numerical_records": [
            row for row in register_rows if float(row["numerical_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "step size is documented",
            "convergence is checked",
            "state constraints are explicit",
            "numerical approximation is separated from model claim",
            "outputs include diagnostics",
        ],
    }
