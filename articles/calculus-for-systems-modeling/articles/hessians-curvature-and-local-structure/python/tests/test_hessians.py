from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from hessians.cli import audit_case, classify_hessian, det2, f, gradient, hessian

def test_function_value():
    assert abs(f(2.0, 1.0) - 14.8) < 1e-12

def test_gradient_value():
    assert gradient(2.0, 1.0) == (5.8, 8.8)

def test_hessian_entries():
    assert hessian(2.0, 1.0) == ((2.4, 1.8), (1.8, 6.0))

def test_classification_positive_definite():
    assert classify_hessian(hessian(2.0, 1.0)) == "positive definite"

def test_indefinite_warning():
    record = audit_case(-5.0, 0.0, 0.2, 0.1)
    assert record.classification == "indefinite"
    assert "saddle" in record.warning.lower()
