from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from mechanistic_explanation_limits_formalism.cli import (
    build_mechanism_records,
    build_formal_records,
    build_claim_records,
)

def test_mechanism_records_present():
    assert len(build_mechanism_records()) >= 3

def test_formal_records_present():
    assert len(build_formal_records()) >= 3

def test_claim_types_present():
    claim_types = {record.claim_type for record in build_claim_records()}
    assert "mechanistic" in claim_types
    assert "exploratory" in claim_types

def test_warnings_present():
    assert all(record.warning for record in build_mechanism_records())
