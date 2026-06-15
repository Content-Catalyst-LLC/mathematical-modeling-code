from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from partial_derivatives.cli import cross_partial_xy, is_feasible, partial_x, partial_y, system_response

def test_system_response():
    assert system_response(2.0, 4.0) == 18.0

def test_partials():
    assert partial_x(2.0, 4.0) == 5.0
    assert partial_y(2.0, 4.0) == 3.0

def test_cross_partial():
    assert cross_partial_xy(2.0, 4.0) == 0.5

def test_infeasible_budget():
    assert not is_feasible(8.0, 4.0)
