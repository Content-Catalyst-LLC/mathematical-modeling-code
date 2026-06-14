from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from differentiability_local_behavior.core import (
    finite_difference_diagnostics,
    kink_response,
    local_linearization_error,
    smooth_derivative,
    smooth_response,
)


def test_smooth_local_linearization_error_decreases_relative_to_h():
    rows = local_linearization_error("smooth", smooth_response, smooth_derivative(5.0), 5.0, [0.5, 0.25, 0.125])
    assert rows[-1].error_over_h < rows[0].error_over_h


def test_kink_has_large_one_sided_gap():
    rows = finite_difference_diagnostics("kink", kink_response, 0.0, [1.0, 0.5, 0.25])
    assert all(row.kink_flag for row in rows)


def test_smooth_has_small_one_sided_gap_for_small_h():
    rows = finite_difference_diagnostics("smooth", smooth_response, 5.0, [0.25, 0.125, 0.0625])
    assert rows[-1].one_sided_gap < rows[0].one_sided_gap
