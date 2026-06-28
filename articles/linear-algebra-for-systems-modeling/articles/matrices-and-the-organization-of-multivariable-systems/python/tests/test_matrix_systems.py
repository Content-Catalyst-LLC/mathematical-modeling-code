from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from matrix_systems.cli import build_audit, is_symmetric, matrix_rank, sample_matrix


def test_sample_matrix_is_symmetric():
    assert is_symmetric(sample_matrix()) is True


def test_matrix_rank_is_full_for_sample():
    assert matrix_rank(sample_matrix()) == 4


def test_audit_fields():
    audit = build_audit()
    assert audit.row_count == 4
    assert audit.column_count == 4
    assert audit.nonzero_entries == 8
    assert audit.symmetric is True
    assert "directional" in audit.interpretation_warning
