from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from when_continuous_models_mislead.cli import (
    build_continuity_assumptions,
    build_risk_records,
    build_solver_diagnostics,
)

def test_assumptions_present():
    assert len(build_continuity_assumptions()) >= 3

def test_risks_present():
    risk_names = {record.risk_name for record in build_risk_records()}
    assert "false_smoothness" in risk_names
    assert "solver_confidence" in risk_names

def test_solver_diagnostics_present():
    assert len(build_solver_diagnostics()) >= 3

def test_all_risks_review_status():
    assert all(record.status == "review" for record in build_risk_records())
