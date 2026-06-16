from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from parameter_sweeps_sensitivity.cli import (
    build_grid_sweep,
    final_output,
    finite_difference_sensitivity,
    logistic_solution,
)

def test_logistic_solution_initial_value():
    assert logistic_solution(0.0, 10.0, 0.35, 100.0) == 10.0

def test_final_output_positive():
    assert final_output(0.35, 100.0) > 0.0

def test_grid_sweep_size():
    records = build_grid_sweep()
    assert len(records) == 20

def test_sensitivity_parameter_names():
    record = finite_difference_sensitivity("growth_rate")
    assert record.parameter == "growth_rate"
    assert record.finite_difference_sensitivity > 0.0
