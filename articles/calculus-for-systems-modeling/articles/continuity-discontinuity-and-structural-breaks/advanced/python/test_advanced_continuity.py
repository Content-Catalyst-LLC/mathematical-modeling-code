from __future__ import annotations

from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_continuity import (
    classify_break,
    diagnose_breaks,
    invariant_review,
    jump_function,
    piecewise_system,
    regularity_examples,
)


def test_jump_function_has_jump_at_zero() -> None:
    assert jump_function(-0.1) != jump_function(0.0)


def test_classify_break_level_and_slope() -> None:
    assert classify_break(1.2, 0.8) == "level_and_slope_break"


def test_piecewise_diagnostics_flag_break() -> None:
    xs = [i * 0.25 for i in range(41)]
    ys = [piecewise_system(x) for x in xs]
    rows = diagnose_breaks(xs, ys)
    flags = {row.flag for row in rows}
    assert "level_and_slope_break" in flags or "possible_jump" in flags


def test_regularities_include_continuous_not_differentiable_example() -> None:
    examples = regularity_examples()
    assert any(item.example == "|x|" and item.continuous and not item.differentiable_everywhere for item in examples)


def test_invariant_review_detects_invalid_values() -> None:
    reviews = invariant_review([0.0, 0.5, 1.0, -0.1, 1.2], 0.0, 1.0)
    failures = [item for item in reviews if not item.inside]
    assert len(failures) == 2


if __name__ == "__main__":
    test_jump_function_has_jump_at_zero()
    test_classify_break_level_and_slope()
    test_piecewise_diagnostics_flag_break()
    test_regularities_include_continuous_not_differentiable_example()
    test_invariant_review_detects_invalid_values()
    print("advanced continuity checks passed")
