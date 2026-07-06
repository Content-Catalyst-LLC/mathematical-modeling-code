from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from representation_choices_and_model_assumptions.cli import build_audit


def test_audit_records_matrix_meaning():
    audit = build_audit()
    assert audit.matrix_shape == "3x2"
    assert audit.row_meaning == "infrastructure_zones"


def test_standardized_norms_are_balanced():
    audit = build_audit()
    assert abs(audit.standardized_column_norm_1 - audit.standardized_column_norm_2) < 1e-10


def test_zero_meaning_is_not_missingness():
    audit = build_audit()
    assert "not_missingness" in audit.zero_meaning
