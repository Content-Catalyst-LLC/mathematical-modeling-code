from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_improper_integrals import (
    convergence_evidence_check,
    limiting_process_check,
    model_domain_check,
    p_tail_check,
    truncation_sensitivity_check,
)


def test_missing_limiting_process_fails():
    assert limiting_process_check(0.0).passed is False


def test_missing_convergence_evidence_fails():
    assert convergence_evidence_check(0.0).passed is False


def test_material_tail_error_fails():
    assert truncation_sensitivity_check(0.2).passed is False


def test_p_tail_boundary_fails():
    assert p_tail_check(1.0).passed is False


def test_missing_model_domain_fails():
    assert model_domain_check(0.0).passed is False


if __name__ == "__main__":
    test_missing_limiting_process_fails()
    test_missing_convergence_evidence_fails()
    test_material_tail_error_fails()
    test_p_tail_boundary_fails()
    test_missing_model_domain_fails()
    print("advanced improper-integral checks passed")
