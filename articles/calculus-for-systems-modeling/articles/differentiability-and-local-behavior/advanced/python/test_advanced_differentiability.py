from __future__ import annotations

from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_differentiability import (
    derivative_diagnostics,
    invariant_review,
    kink_response,
    local_linearization_error,
    smooth_derivative,
    smooth_response,
)


def test_smooth_local_linearization_error_decreases_relative_to_h() -> None:
    rows = local_linearization_error("smooth", smooth_response, smooth_derivative(5.0), 5.0, [0.5, 0.25, 0.125])
    assert rows[-1].error_over_h < rows[0].error_over_h


def test_kink_diagnostics_flag_one_sided_gap() -> None:
    rows = derivative_diagnostics("kink", kink_response, 0.0, [1.0, 0.5, 0.25])
    assert all(row.kink_flag for row in rows)


def test_smooth_diagnostics_gap_decreases() -> None:
    rows = derivative_diagnostics("smooth", smooth_response, 5.0, [0.25, 0.125, 0.0625])
    assert rows[-1].one_sided_gap < rows[0].one_sided_gap


def test_invariant_review_detects_invalid_values() -> None:
    reviews = invariant_review([0.0, 0.5, 1.0, -0.1, 1.2], 0.0, 1.0)
    failures = [item for item in reviews if not item.inside]
    assert len(failures) == 2


if __name__ == "__main__":
    test_smooth_local_linearization_error_decreases_relative_to_h()
    test_kink_diagnostics_flag_one_sided_gap()
    test_smooth_diagnostics_gap_decreases()
    test_invariant_review_detects_invalid_values()
    print("advanced differentiability checks passed")
