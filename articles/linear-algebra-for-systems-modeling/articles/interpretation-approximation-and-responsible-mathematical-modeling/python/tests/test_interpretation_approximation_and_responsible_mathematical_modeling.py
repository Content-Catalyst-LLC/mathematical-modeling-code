from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from interpretation_approximation_and_responsible_mathematical_modeling.cli import build_audit


def test_responsible_modeling_audit_claim_type():
    audit = build_audit()
    assert audit.claim_type == "exploratory_decision_support_not_causal_proof"


def test_audit_has_validation_boundary():
    audit = build_audit()
    assert "stated_data_range" in audit.validation_status


def test_audit_warns_against_unreviewed_decision_authority():
    audit = build_audit()
    assert "unreviewed decision authority" in audit.interpretation_boundary
