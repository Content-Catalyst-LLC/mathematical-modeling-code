"""Companion workflow for model comparison and selection."""

from .core import (
    ModelCandidate,
    SelectionRecord,
    load_candidates,
    load_records,
    model_rows,
    comparison_score,
    overfit_gap,
    selection_risk_score,
    build_selection_audit_card,
)

__all__ = [
    "ModelCandidate",
    "SelectionRecord",
    "load_candidates",
    "load_records",
    "model_rows",
    "comparison_score",
    "overfit_gap",
    "selection_risk_score",
    "build_selection_audit_card",
]
