"""Limits and the formal basis of calculus companion workflow."""

from .core import (
    LimitExperiment,
    forward_difference,
    central_difference,
    richardson_extrapolation,
    estimate_order,
    convergence_study,
    epsilon_band_review,
)

__all__ = [
    "LimitExperiment",
    "forward_difference",
    "central_difference",
    "richardson_extrapolation",
    "estimate_order",
    "convergence_study",
    "epsilon_band_review",
]
