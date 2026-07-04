from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from numerical_stability_and_conditioning.cli import build_audits


def test_two_audit_cases_exist():
    audits = build_audits()
    assert len(audits) == 2
    assert {audit.matrix_case for audit in audits} == {"well_conditioned_system", "ill_conditioned_system"}


def test_ill_conditioned_case_has_larger_condition_number():
    audits = {audit.matrix_case: audit for audit in build_audits()}
    assert audits["ill_conditioned_system"].condition_number_proxy > audits["well_conditioned_system"].condition_number_proxy


def test_residuals_small_but_conditioning_differs():
    audits = build_audits()
    for audit in audits:
        assert audit.residual_norm < 1e-7
    assert any(audit.stability_status == "review_required_ill_conditioned" for audit in audits)
