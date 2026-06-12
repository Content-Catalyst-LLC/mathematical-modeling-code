from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import random
import statistics


@dataclass(frozen=True)
class AgentRuleRecord:
    key: str
    component_type: str
    rule_or_structure: str
    interpretation: str
    review_question: str
    status: str


@dataclass
class Agent:
    agent_id: int
    threshold: float
    adopted: bool


@dataclass(frozen=True)
class SimulationScenario:
    scenario: str
    agent_count: int
    initial_adopters: int
    adoption_threshold_low: float
    adoption_threshold_high: float
    steps: int
    replications: int


def validate_scenario(scenario: SimulationScenario) -> None:
    if scenario.agent_count <= 0:
        raise ValueError("agent_count must be positive.")
    if not 0 <= scenario.initial_adopters <= scenario.agent_count:
        raise ValueError("initial_adopters must be between 0 and agent_count.")
    if not 0 <= scenario.adoption_threshold_low <= scenario.adoption_threshold_high <= 1:
        raise ValueError("threshold bounds must be within [0, 1].")
    if scenario.steps < 1 or scenario.replications < 1:
        raise ValueError("steps and replications must be positive.")


def make_agents(scenario: SimulationScenario, rng: random.Random) -> list[Agent]:
    validate_scenario(scenario)
    agents = [
        Agent(
            agent_id=i,
            threshold=rng.uniform(scenario.adoption_threshold_low, scenario.adoption_threshold_high),
            adopted=False,
        )
        for i in range(scenario.agent_count)
    ]
    for index in rng.sample(range(scenario.agent_count), scenario.initial_adopters):
        agents[index].adopted = True
    return agents


def neighbors(agent_id: int, agent_count: int) -> list[int]:
    return [
        (agent_id - 2) % agent_count,
        (agent_id - 1) % agent_count,
        (agent_id + 1) % agent_count,
        (agent_id + 2) % agent_count,
    ]


def adoption_share(agents: list[Agent]) -> float:
    return sum(1 for agent in agents if agent.adopted) / len(agents)


def step(agents: list[Agent]) -> int:
    agent_count = len(agents)
    next_adopted = [agent.adopted for agent in agents]

    for agent in agents:
        if agent.adopted:
            continue
        local_neighbors = neighbors(agent.agent_id, agent_count)
        adopted_neighbors = sum(1 for idx in local_neighbors if agents[idx].adopted)
        neighbor_share = adopted_neighbors / len(local_neighbors)
        if neighbor_share >= agent.threshold:
            next_adopted[agent.agent_id] = True

    changes = 0
    for agent, new_state in zip(agents, next_adopted):
        if agent.adopted != new_state:
            changes += 1
        agent.adopted = new_state

    return changes


def run_replication(scenario: SimulationScenario, seed: int) -> list[dict[str, object]]:
    rng = random.Random(seed)
    agents = make_agents(scenario, rng)
    rows: list[dict[str, object]] = []

    for t in range(scenario.steps + 1):
        rows.append({
            "scenario": scenario.scenario,
            "seed": seed,
            "step": t,
            "adoption_share": round(adoption_share(agents), 8),
            "adopted_count": sum(1 for agent in agents if agent.adopted),
        })
        if t < scenario.steps:
            changes = step(agents)
            if changes == 0:
                for remaining in range(t + 1, scenario.steps + 1):
                    rows.append({
                        "scenario": scenario.scenario,
                        "seed": seed,
                        "step": remaining,
                        "adoption_share": round(adoption_share(agents), 8),
                        "adopted_count": sum(1 for agent in agents if agent.adopted),
                    })
                break
    return rows


def summarize_runs(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    max_step_by_scenario: dict[str, int] = {}
    for row in rows:
        scenario = str(row["scenario"])
        max_step_by_scenario[scenario] = max(max_step_by_scenario.get(scenario, 0), int(row["step"]))

    grouped: dict[str, list[float]] = {}
    for row in rows:
        scenario = str(row["scenario"])
        if int(row["step"]) == max_step_by_scenario[scenario]:
            grouped.setdefault(scenario, []).append(float(row["adoption_share"]))

    summaries: list[dict[str, object]] = []
    for scenario, values in sorted(grouped.items()):
        summaries.append({
            "scenario": scenario,
            "replications": len(values),
            "mean_final_adoption": round(statistics.mean(values), 8),
            "min_final_adoption": round(min(values), 8),
            "max_final_adoption": round(max(values), 8),
            "stdev_final_adoption": round(statistics.pstdev(values), 8),
        })
    return summaries


def rule_risk_score(record: AgentRuleRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.component_type} {record.rule_or_structure} {record.review_question}".lower()
    for term in ["threshold", "behavior", "interaction", "binary", "replication", "emergent", "schedule"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_records(path: Path) -> list[AgentRuleRecord]:
    records: list[AgentRuleRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                AgentRuleRecord(
                    key=row["key"],
                    component_type=row["component_type"],
                    rule_or_structure=row["rule_or_structure"],
                    interpretation=row["interpretation"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_scenarios(path: Path) -> list[SimulationScenario]:
    scenarios: list[SimulationScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scenarios.append(
                SimulationScenario(
                    scenario=row["scenario"],
                    agent_count=int(row["agent_count"]),
                    initial_adopters=int(row["initial_adopters"]),
                    adoption_threshold_low=float(row["adoption_threshold_low"]),
                    adoption_threshold_high=float(row["adoption_threshold_high"]),
                    steps=int(row["steps"]),
                    replications=int(row["replications"]),
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


def build_abm_audit_card(
    records: list[AgentRuleRecord],
    scenarios: list[SimulationScenario],
    summary_rows: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {
            **asdict(record),
            "rule_risk_score": rule_risk_score(record),
        }
        for record in records
    ]
    return {
        "article": "Agent-Based Models and Emergent Behavior",
        "scenarios": [asdict(scenario) for scenario in scenarios],
        "model_register": register_rows,
        "ensemble_summary": summary_rows,
        "high_priority_abm_records": [
            row for row in register_rows if float(row["rule_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "agent states are documented",
            "behavior rules are interpretable",
            "interaction structure is explicit",
            "replications are run with recorded seeds",
            "emergent outcomes are summarized across ensembles",
        ],
    }
