"""Professional companion workflow for 'What Is Mathematical Modeling?'."""

from .core import (
    LogisticModel,
    SimulationResult,
    simulate_euler,
    simulate_rk4,
    run_scenarios,
    calibrate_grid_search,
    sensitivity_oat,
    monte_carlo_uncertainty,
    residual_diagnostics,
    load_scenarios,
    build_model_card,
)

__all__ = [
    "LogisticModel",
    "SimulationResult",
    "simulate_euler",
    "simulate_rk4",
    "run_scenarios",
    "calibrate_grid_search",
    "sensitivity_oat",
    "monte_carlo_uncertainty",
    "residual_diagnostics",
    "load_scenarios",
    "build_model_card",
]
