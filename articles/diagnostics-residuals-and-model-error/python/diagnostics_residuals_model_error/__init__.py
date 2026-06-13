"""Companion workflow for diagnostics, residuals, and model error."""

from .core import (
    DiagnosticObservation,
    DiagnosticRecord,
    load_observations,
    load_records,
    residual_rows,
    error_summary,
    group_summary,
    flag_outliers,
    diagnostic_risk_score,
    build_diagnostic_assessment_card,
)

__all__ = [
    "DiagnosticObservation",
    "DiagnosticRecord",
    "load_observations",
    "load_records",
    "residual_rows",
    "error_summary",
    "group_summary",
    "flag_outliers",
    "diagnostic_risk_score",
    "build_diagnostic_assessment_card",
]
