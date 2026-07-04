from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from matrix_operations_across_modeling_languages.cli import cross_language_audit


def test_cross_language_audit_basic_fields():
    audit, y, product, solution = cross_language_audit()
    assert audit.matrix_shape == "3x3"
    assert audit.vector_shape == "3"
    assert audit.solve_residual_norm < 1e-9


def test_matrix_outputs_have_expected_shapes():
    audit, y, product, solution = cross_language_audit()
    assert len(y) == 3
    assert len(solution) == 3
    assert len(product) == 3
    assert len(product[0]) == 3


def test_diagnostics_reasonable():
    audit, y, product, solution = cross_language_audit()
    assert audit.determinant > 0
    assert audit.condition_number > 1
