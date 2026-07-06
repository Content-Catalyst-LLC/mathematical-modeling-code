from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from scaling_normalization_and_comparative_structure.cli import build_audit


def test_standardization_balances_column_norms():
    audit = build_audit()
    assert abs(audit.standardized_column_norm_1 - audit.standardized_column_norm_2) < 1e-10


def test_row_and_unit_normalization_work():
    audit = build_audit()
    assert abs(audit.first_row_sum_after_row_normalization - 1.0) < 1e-10
    assert abs(audit.first_row_norm_after_unit_normalization - 1.0) < 1e-10


def test_scaling_improves_condition_proxy():
    audit = build_audit()
    assert audit.standardized_condition_proxy < audit.raw_condition_proxy
