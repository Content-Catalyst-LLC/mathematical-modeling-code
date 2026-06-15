from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from jacobians.cli import F, audit_case, determinant_2x2, jacobian

def test_transformation_value():
    assert F(2.0, 1.0) == (5.0, 5.0)

def test_jacobian_entries():
    assert jacobian(2.0, 1.0) == ((4.0, 1.0), (1.0, 5.0))

def test_determinant():
    assert determinant_2x2(((4.0, 1.0), (1.0, 5.0))) == 19.0

def test_audit_nonnegative_error():
    record = audit_case(2.0, 1.0, 0.1, -0.05)
    assert record.error_norm >= 0

def test_singularity_warning_exists():
    record = audit_case(0.0, 0.0, 0.1, 0.1)
    assert "singular" in record.warning.lower()
