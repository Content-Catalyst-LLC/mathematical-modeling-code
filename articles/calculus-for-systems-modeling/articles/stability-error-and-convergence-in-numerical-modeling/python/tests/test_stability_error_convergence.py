from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from stability_error_convergence.cli import (
    convergence_audit,
    exact_solution,
    simulate,
    stability_amplification_factor,
)

def test_exact_solution_initial_value():
    assert exact_solution(0.0, 100.0, 0.35) == 100.0

def test_simulate_positive():
    assert simulate(100.0, 0.35, 0.5, 20.0) > 0

def test_convergence_audit_records():
    records = convergence_audit()
    assert len(records) == 4
    assert records[-1].step_size == 0.125

def test_stability_amplification_factor():
    assert stability_amplification_factor(0.1, -1.0) == 0.9
