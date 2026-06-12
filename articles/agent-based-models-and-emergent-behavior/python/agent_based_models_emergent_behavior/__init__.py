"""Companion workflow for agent-based models and emergent behavior."""

from .core import (
    Agent,
    AgentRuleRecord,
    SimulationScenario,
    load_records,
    load_scenarios,
    run_replication,
    summarize_runs,
    rule_risk_score,
    build_abm_audit_card,
)

__all__ = [
    "Agent",
    "AgentRuleRecord",
    "SimulationScenario",
    "load_records",
    "load_scenarios",
    "run_replication",
    "summarize_runs",
    "rule_risk_score",
    "build_abm_audit_card",
]
