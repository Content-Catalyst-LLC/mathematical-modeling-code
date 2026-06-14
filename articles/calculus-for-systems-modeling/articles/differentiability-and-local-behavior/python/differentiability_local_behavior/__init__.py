"""Differentiability and local behavior companion workflow."""

from .core import (
    LocalApproximationRecord,
    FiniteDifferenceRecord,
    smooth_response,
    smooth_derivative,
    kink_response,
    central_difference,
    local_linearization_error,
    finite_difference_diagnostics,
)

__all__ = [
    "LocalApproximationRecord",
    "FiniteDifferenceRecord",
    "smooth_response",
    "smooth_derivative",
    "kink_response",
    "central_difference",
    "local_linearization_error",
    "finite_difference_diagnostics",
]
