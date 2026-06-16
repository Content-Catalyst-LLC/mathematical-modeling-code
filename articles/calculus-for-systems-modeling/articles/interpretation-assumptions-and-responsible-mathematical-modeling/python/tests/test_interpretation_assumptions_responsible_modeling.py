from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from interpretation_assumptions_responsible_modeling.cli import (
    build_purpose_records,
    build_assumption_records,
    build_claim_boundary_records,
)

def test_purpose_records_present():
    assert len(build_purpose_records()) >= 3

def test_assumption_records_present():
    assert len(build_assumption_records()) >= 4

def test_claim_boundaries_present():
    claim_types = {record.claim_type for record in build_claim_boundary_records()}
    assert "descriptive" in claim_types
    assert "predictive" in claim_types

def test_governance_statuses_valid():
    assert all(record.governance_status in {"active", "review", "revise", "archive"} for record in build_claim_boundary_records())
