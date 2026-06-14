from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class PolicyModelRecord:
    key: str
    policy_domain: str
    model_role: str
    model_family: str
    public_question: str
    status: str


@dataclass(frozen=True)
class PolicyOption:
    key: str
    option_name: str
    projected_benefit: float
    total_cost: float
    implementation_feasibility: float
    equity_score: float
    uncertainty_width: float
    public_risk: float


def load_policy_model_records(path: Path) -> list[PolicyModelRecord]:
    records: list[PolicyModelRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                PolicyModelRecord(
                    key=row["key"],
                    policy_domain=row["policy_domain"],
                    model_role=row["model_role"],
                    model_family=row["model_family"],
                    public_question=row["public_question"],
                    status=row["status"],
                )
            )
    if not records:
        raise ValueError("Policy model register cannot be empty.")
    return records


def load_policy_options(path: Path) -> list[PolicyOption]:
    options: list[PolicyOption] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            options.append(
                PolicyOption(
                    key=row["key"],
                    option_name=row["option_name"],
                    projected_benefit=float(row["projected_benefit"]),
                    total_cost=float(row["total_cost"]),
                    implementation_feasibility=float(row["implementation_feasibility"]),
                    equity_score=float(row["equity_score"]),
                    uncertainty_width=float(row["uncertainty_width"]),
                    public_risk=float(row["public_risk"]),
                )
            )
    if not options:
        raise ValueError("Policy option table cannot be empty.")
    return options


def evaluate_policy_option(option: PolicyOption, budget_limit: float = 40.0) -> dict[str, object]:
    budget_violation = option.total_cost > budget_limit
    uncertainty_penalty = 0.22 * option.uncertainty_width
    risk_penalty = 30.0 * option.public_risk
    feasibility_bonus = 18.0 * option.implementation_feasibility
    equity_bonus = 24.0 * option.equity_score
    budget_penalty = 14.0 if budget_violation else 0.0

    public_value_score = (
        option.projected_benefit
        + feasibility_bonus
        + equity_bonus
        - option.total_cost
        - uncertainty_penalty
        - risk_penalty
        - budget_penalty
    )

    review_class = "requires_budget_review" if budget_violation else "within_budget"
    if option.equity_score < 0.65:
        review_class = "requires_equity_review"
    if option.public_risk > 0.38:
        review_class = "requires_risk_review"

    return {
        **asdict(option),
        "budget_limit": budget_limit,
        "budget_margin": round(budget_limit - option.total_cost, 8),
        "budget_violation": budget_violation,
        "public_value_score": round(public_value_score, 8),
        "review_class": review_class,
    }


def policy_priority(record: PolicyModelRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.model_role} {record.model_family} {record.public_question}".lower()
    for term in ["equity", "governance", "allocation", "risk", "uncertainty", "public", "decision"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def policy_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Policy summary requires at least one option.")
    scores = [float(row["public_value_score"]) for row in rows]
    violations = sum(1 for row in rows if bool(row["budget_violation"]))
    best = max(rows, key=lambda row: float(row["public_value_score"]))
    return {
        "best_scored_option": best["option_name"],
        "mean_public_value_score": round(statistics.mean(scores), 8),
        "max_public_value_score": round(max(scores), 8),
        "min_public_value_score": round(min(scores), 8),
        "budget_violation_count": violations,
        "option_count": len(rows),
    }


def build_policy_decision_support_card(
    register_rows: list[dict[str, object]],
    option_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Mathematical Modeling in Policy and Public Systems",
        "policy_summary": policy_summary(option_rows),
        "policy_model_register": register_rows,
        "policy_option_review": option_rows,
        "use_limit": "This workflow supports policy option review and public reasoning; it does not automate public decisions or replace legal, ethical, stakeholder, and institutional judgment.",
        "diagnostic_checks": [
            "policy purpose is stated",
            "model role is separated from decision authority",
            "budget constraints are explicit",
            "equity score is reviewed",
            "public risk is reviewed",
            "uncertainty width is reported",
            "governance and accountability remain required",
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
