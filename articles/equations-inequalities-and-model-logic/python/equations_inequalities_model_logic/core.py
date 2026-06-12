from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
from statistics import mean


@dataclass(frozen=True)
class FormalStatement:
    key: str
    statement_type: str
    expression: str
    interpretation: str
    domain_or_condition: str
    review_question: str
    status: str


@dataclass(frozen=True)
class LogicScenario:
    name: str
    initial_stock: float
    capacity: float
    inflow: float
    demand: float
    loss_rate: float
    low_storage_threshold: float
    demand_reduction: float
    periods: int
    description: str = ""


def validate_scenario(scenario: LogicScenario) -> None:
    if scenario.initial_stock < 0:
        raise ValueError("initial_stock must be nonnegative.")
    if scenario.capacity <= 0:
        raise ValueError("capacity must be positive.")
    if scenario.initial_stock > scenario.capacity:
        raise ValueError("initial_stock cannot exceed capacity.")
    if scenario.inflow < 0 or scenario.demand < 0:
        raise ValueError("inflow and demand must be nonnegative.")
    if not 0 <= scenario.loss_rate <= 1:
        raise ValueError("loss_rate must be between 0 and 1.")
    if scenario.low_storage_threshold < 0 or scenario.low_storage_threshold > scenario.capacity:
        raise ValueError("threshold must be within the storage domain.")
    if scenario.demand_reduction < 0:
        raise ValueError("demand_reduction must be nonnegative.")
    if scenario.periods < 1:
        raise ValueError("periods must be at least 1.")


def simulate_logic(scenario: LogicScenario) -> list[dict[str, object]]:
    validate_scenario(scenario)
    stock = scenario.initial_stock
    demand = scenario.demand
    rows: list[dict[str, object]] = []

    for period in range(scenario.periods + 1):
        losses = scenario.loss_rate * stock
        raw_next_stock = stock + scenario.inflow - demand - losses
        shortage = max(0.0, -raw_next_stock)
        overflow = max(0.0, raw_next_stock - scenario.capacity)
        constrained_next_stock = min(scenario.capacity, max(0.0, raw_next_stock))
        low_storage_rule_active = stock < scenario.low_storage_threshold
        domain_valid = 0.0 <= constrained_next_stock <= scenario.capacity

        rows.append({
            "scenario": scenario.name,
            "period": period,
            "stock": round(stock, 8),
            "inflow": round(scenario.inflow, 8),
            "demand": round(demand, 8),
            "losses": round(losses, 8),
            "raw_next_stock": round(raw_next_stock, 8),
            "constrained_next_stock": round(constrained_next_stock, 8),
            "shortage": round(shortage, 8),
            "overflow": round(overflow, 8),
            "low_storage_rule_active": low_storage_rule_active,
            "domain_valid": domain_valid,
        })

        if low_storage_rule_active:
            demand = max(0.0, demand - scenario.demand_reduction)

        stock = constrained_next_stock

    return rows


def summarize_logic(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Cannot summarize empty rows.")

    stocks = [float(row["stock"]) for row in rows]
    shortages = [float(row["shortage"]) for row in rows]
    overflows = [float(row["overflow"]) for row in rows]
    logic_activations = [bool(row["low_storage_rule_active"]) for row in rows]
    domain_flags = [bool(row["domain_valid"]) for row in rows]

    return {
        "scenario": str(rows[0]["scenario"]),
        "final_stock": round(stocks[-1], 8),
        "mean_stock": round(mean(stocks), 8),
        "min_stock": round(min(stocks), 8),
        "max_stock": round(max(stocks), 8),
        "shortage_periods": sum(1 for value in shortages if value > 0),
        "overflow_periods": sum(1 for value in overflows if value > 0),
        "logic_activation_periods": sum(1 for value in logic_activations if value),
        "domain_violations": sum(1 for value in domain_flags if not value),
        "total_shortage": round(sum(shortages), 8),
        "total_overflow": round(sum(overflows), 8),
    }


def statement_risk_score(statement: FormalStatement) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        statement.status.lower(),
        4.0,
    )
    text = f"{statement.statement_type} {statement.expression} {statement.review_question}".lower()
    for term in ["constraint", "threshold", "shortage", "hide", "domain", "if", "max", "min"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_statements(path: Path) -> list[FormalStatement]:
    statements: list[FormalStatement] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            statements.append(
                FormalStatement(
                    key=row["key"],
                    statement_type=row["statement_type"],
                    expression=row["expression"],
                    interpretation=row["interpretation"],
                    domain_or_condition=row["domain_or_condition"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return statements


def load_scenarios(path: Path) -> list[LogicScenario]:
    scenarios: list[LogicScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                LogicScenario(
                    name=row["scenario"],
                    initial_stock=float(row["initial_stock"]),
                    capacity=float(row["capacity"]),
                    inflow=float(row["inflow"]),
                    demand=float(row["demand"]),
                    loss_rate=float(row["loss_rate"]),
                    low_storage_threshold=float(row["low_storage_threshold"]),
                    demand_reduction=float(row["demand_reduction"]),
                    periods=int(row["periods"]),
                    description=row.get("description", ""),
                )
            )
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


def build_logic_audit_card(
    statements: list[FormalStatement],
    summaries: list[dict[str, object]],
) -> dict[str, object]:
    statement_rows = [
        {
            **asdict(statement),
            "statement_risk_score": statement_risk_score(statement),
        }
        for statement in statements
    ]

    return {
        "article": "Equations, Inequalities, and Model Logic",
        "formal_statements": statement_rows,
        "scenario_summaries": summaries,
        "high_priority_statements": [
            row for row in statement_rows if float(row["statement_risk_score"]) >= 8.0
        ],
        "logic_checks": [
            "equations have stated interpretation",
            "inequalities have stated source and domain",
            "conditional rules are visible",
            "domain validity is checked after each update",
            "shortage and overflow are reported rather than silently hidden",
        ],
    }
