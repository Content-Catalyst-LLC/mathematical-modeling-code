"""Companion workflow for discrete models and recurrence relations."""

from .core import (
    RecurrenceRecord,
    RecurrenceScenario,
    load_recurrence_records,
    load_recurrence_scenarios,
    simulate_recurrence,
    summarize_trajectory,
    recurrence_risk_score,
    build_recurrence_audit_card,
)

__all__ = [
    "RecurrenceRecord",
    "RecurrenceScenario",
    "load_recurrence_records",
    "load_recurrence_scenarios",
    "simulate_recurrence",
    "summarize_trajectory",
    "recurrence_risk_score",
    "build_recurrence_audit_card",
]
