"""Continuity, discontinuity, and structural-break companion workflow."""

from .core import (
    BreakDiagnostic,
    piecewise_system,
    diagnose_breaks,
    summarize_flags,
)

__all__ = [
    "BreakDiagnostic",
    "piecewise_system",
    "diagnose_breaks",
    "summarize_flags",
]
