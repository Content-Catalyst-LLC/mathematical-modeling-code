from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from symbolic_model_inspection.cli import domain_warning, fallback_records, sympy_records

def test_fallback_records_include_derivative():
    records = fallback_records()
    items = {record.item for record in records}
    assert "first_derivative" in items
    assert "equilibria" in items

def test_domain_warning():
    assert "K" in domain_warning("r*x*(1 - x/K)")

def test_sympy_records_returns_records():
    records = sympy_records()
    assert len(records) >= 6
    assert any(record.item == "jacobian" for record in records)
