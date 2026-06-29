from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from markov_transition_matrices.cli import build_audit, evolve, is_nonnegative, row_sum_error


def test_row_sum_and_nonnegative():
    P = [[0.82, 0.16, 0.02], [0.10, 0.76, 0.14], [0.03, 0.22, 0.75]]
    assert row_sum_error(P) == 0.0
    assert is_nonnegative(P)


def test_evolve_conserves_probability():
    P = [[0.82, 0.16, 0.02], [0.10, 0.76, 0.14], [0.03, 0.22, 0.75]]
    pi = [0.60, 0.30, 0.10]
    result = evolve(pi, P, 10)
    assert abs(sum(result) - 1.0) < 1e-12


def test_build_audit():
    audit = build_audit()
    assert audit.system_name == "infrastructure_condition_transition_audit"
    assert audit.orientation == "row_stochastic_row_vector_update_pi_next_equals_pi_P"
    assert audit.nonnegative
    assert audit.row_sum_error == 0.0
