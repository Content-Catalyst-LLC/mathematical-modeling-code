from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))
from numerical_integration.cli import left_rectangle_step, trapezoid_step, simpson_one_third, numerical_integration_audit

def test_basic_steps():
    assert abs(left_rectangle_step(2.0, 0.5) - 1.0) < 1e-12
    assert abs(trapezoid_step(2.0, 4.0, 0.5) - 1.5) < 1e-12
    assert abs(simpson_one_third(1.0, 4.0, 1.0, 0.5) - 3.0) < 1e-12

def test_audit():
    records = numerical_integration_audit(0.0, 10.0, 0.1)
    assert len(records) == 101
