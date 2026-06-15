from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'python'))
from separable_equations.cli import exponential_solution, exponential_rate, logistic_solution, logistic_rate, simulate_exponential, simulate_logistic

def test_exponential_solution_initial(): assert exponential_solution(0.0, 10.0, 0.25) == 10.0
def test_exponential_rate(): assert exponential_rate(10.0, 0.25) == 2.5
def test_logistic_solution_initial(): assert abs(logistic_solution(0.0, 10.0, 0.25, 100.0) - 10.0) < 1e-12
def test_logistic_rate(): assert abs(logistic_rate(10.0, 0.25, 100.0) - 2.25) < 1e-12
def test_lengths():
    assert len(simulate_exponential(10.0, 0.25, 0.1, 10)) == 11
    assert len(simulate_logistic(10.0, 0.25, 100.0, 0.1, 10)) == 11
