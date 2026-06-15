from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from total_differentials.cli import audit_case, feasible_displacement, f, fx, fy, total_differential

def test_function_value():
    assert f(4.0, 3.0) == 28.0

def test_partials():
    assert fx(4.0, 3.0) == 4.5
    assert fy(4.0, 3.0) == 4.0

def test_total_differential():
    assert abs(total_differential(4.0, 3.0, 0.2, -0.1) - 0.5) < 1e-12

def test_feasible_displacement():
    assert feasible_displacement(4.0, 3.0, 0.2, -0.1)
    assert not feasible_displacement(8.0, 1.0, 1.0, 1.0)

def test_audit_error_nonnegative():
    record = audit_case(4.0, 3.0, 1.0, 1.0)
    assert record.absolute_error >= 0
