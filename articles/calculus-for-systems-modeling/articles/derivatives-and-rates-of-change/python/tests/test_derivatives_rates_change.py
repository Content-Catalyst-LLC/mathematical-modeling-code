from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from derivatives_rates_change.core import (
    central_difference,
    exact_derivative,
    forward_difference,
    rate_diagnostics,
    vector_field_records,
)


def test_central_difference_more_accurate_than_forward():
    x = 5.0
    h = 0.1
    assert abs(central_difference(x, h) - exact_derivative(x)) < abs(forward_difference(x, h) - exact_derivative(x))


def test_rate_diagnostics_include_elasticity():
    rows = rate_diagnostics(5.0, [0.5, 0.25])
    assert any(row.relative_rate is not None for row in rows)


def test_vector_field_flags_invalid_states():
    rows = vector_field_records([-0.1, 0.0, 0.5, 1.1])
    assert sum(not row.inside_invariant_domain for row in rows) == 2
