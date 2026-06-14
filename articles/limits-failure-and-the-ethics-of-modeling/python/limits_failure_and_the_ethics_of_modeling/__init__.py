"""Companion workflow for limits, failure, and the ethics of modeling."""

from .core import (
    ModelFailureRecord,
    ModelRiskCase,
    load_failure_records,
    load_risk_cases,
    evaluate_risk_case,
    failure_priority,
    ethics_summary,
    build_model_ethics_governance_card,
)

__all__ = [
    "ModelFailureRecord",
    "ModelRiskCase",
    "load_failure_records",
    "load_risk_cases",
    "evaluate_risk_case",
    "failure_priority",
    "ethics_summary",
    "build_model_ethics_governance_card",
]
