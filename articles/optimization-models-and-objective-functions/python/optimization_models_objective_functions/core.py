from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class Program:
    name: str
    benefit_per_unit: float
    cost_per_unit: float
    lower_bound: int
    upper_bound: int


@dataclass(frozen=True)
class OptimizationScenario:
    name: str
    budget: float
    equity_floor: int
    description: str = ""


@dataclass(frozen=True)
class OptimizationRecord:
    key: str
    component_type: str
    expression: str
    interpretation: str
    review_question: str
    status: str


def validate_program(program: Program) -> None:
    if program.cost_per_unit <= 0:
        raise ValueError("cost_per_unit must be positive.")
    if program.upper_bound < program.lower_bound:
        raise ValueError("upper_bound must be at least lower_bound.")
    if program.lower_bound < 0:
        raise ValueError("lower_bound must be nonnegative.")


def validate_scenario(scenario: OptimizationScenario) -> None:
    if scenario.budget < 0:
        raise ValueError("budget must be nonnegative.")
    if scenario.equity_floor < 0:
        raise ValueError("equity_floor must be nonnegative.")


def evaluate_choice(
    allocation: tuple[int, ...],
    program_list: list[Program],
    scenario: OptimizationScenario,
) -> dict[str, object]:
    total_cost = sum(x * p.cost_per_unit for x, p in zip(allocation, program_list))
    total_benefit = sum(x * p.benefit_per_unit for x, p in zip(allocation, program_list))
    equity_ok = all(x >= scenario.equity_floor for x in allocation)
    bounds_ok = all(p.lower_bound <= x <= p.upper_bound for x, p in zip(allocation, program_list))
    budget_ok = total_cost <= scenario.budget
    feasible = equity_ok and bounds_ok and budget_ok

    row: dict[str, object] = {
        "scenario": scenario.name,
        "total_cost": round(total_cost, 4),
        "total_benefit": round(total_benefit, 4),
        "budget": scenario.budget,
        "equity_floor": scenario.equity_floor,
        "budget_ok": budget_ok,
        "bounds_ok": bounds_ok,
        "equity_ok": equity_ok,
        "feasible": feasible,
    }

    for x, program in zip(allocation, program_list):
        row[f"allocation_{program.name}"] = x

    return row


def enumerate_choices(program_list: list[Program], scenario: OptimizationScenario) -> list[dict[str, object]]:
    for program in program_list:
        validate_program(program)
    validate_scenario(scenario)
    ranges = [range(program.lower_bound, program.upper_bound + 1) for program in program_list]
    return [evaluate_choice(choice, program_list, scenario) for choice in product(*ranges)]


def best_feasible(rows: list[dict[str, object]]) -> dict[str, object]:
    feasible_rows = [row for row in rows if bool(row["feasible"])]
    if not feasible_rows:
        return {"status": "infeasible"}
    best = max(feasible_rows, key=lambda row: float(row["total_benefit"]))
    return {"status": "optimal_in_enumerated_feasible_set", **best}


def optimization_risk_score(record: OptimizationRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.component_type} {record.expression} {record.review_question}".lower()
    for term in ["objective", "constraint", "equity", "cost", "distributional", "controllable", "solver"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_programs(path: Path) -> list[Program]:
    rows: list[Program] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                Program(
                    name=row["program"],
                    benefit_per_unit=float(row["benefit_per_unit"]),
                    cost_per_unit=float(row["cost_per_unit"]),
                    lower_bound=int(row["lower_bound"]),
                    upper_bound=int(row["upper_bound"]),
                )
            )
    return rows


def load_scenarios(path: Path) -> list[OptimizationScenario]:
    rows: list[OptimizationScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                OptimizationScenario(
                    name=row["scenario"],
                    budget=float(row["budget"]),
                    equity_floor=int(row["equity_floor"]),
                    description=row.get("description", ""),
                )
            )
    return rows


def load_optimization_records(path: Path) -> list[OptimizationRecord]:
    records: list[OptimizationRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                OptimizationRecord(
                    key=row["key"],
                    component_type=row["component_type"],
                    expression=row["expression"],
                    interpretation=row["interpretation"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


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


def build_optimization_audit_card(
    records: list[OptimizationRecord],
    solution_summaries: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {
            **asdict(record),
            "optimization_risk_score": optimization_risk_score(record),
        }
        for record in records
    ]

    return {
        "article": "Optimization Models and Objective Functions",
        "optimization_register": register_rows,
        "solution_summaries": solution_summaries,
        "high_priority_optimization_records": [
            row for row in register_rows if float(row["optimization_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "decision variables are controllable",
            "objective function is documented",
            "constraints are explicit",
            "feasible alternatives are preserved",
            "optimal solution is framed as conditional decision support",
        ],
    }
