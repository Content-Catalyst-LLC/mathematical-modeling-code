from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from long_run_transition_systems.cli import build_audit, evolve, is_nonnegative, l1_distance, row_sum_error, stationary_by_iteration


def test_stochastic_matrix_validation():
    P = [[0.82, 0.16, 0.02], [0.10, 0.76, 0.14], [0.03, 0.22, 0.75]]
    assert row_sum_error(P) == 0.0
    assert is_nonnegative(P)


def test_stationary_estimate_conserves_probability():
    P = [[0.82, 0.16, 0.02], [0.10, 0.76, 0.14], [0.03, 0.22, 0.75]]
    stationary = stationary_by_iteration(P)
    assert abs(sum(stationary) - 1.0) < 1e-12


def test_initial_conditions_get_closer():
    P = [[0.82, 0.16, 0.02], [0.10, 0.76, 0.14], [0.03, 0.22, 0.75]]
    a = [0.80, 0.15, 0.05]
    b = [0.10, 0.25, 0.65]
    assert l1_distance(evolve(a, P, 25), evolve(b, P, 25)) < l1_distance(a, b)


def test_build_audit():
    audit = build_audit()
    assert audit.system_name == "long_run_infrastructure_condition_transition_audit"
    assert audit.nonnegative
    assert audit.row_sum_error == 0.0
