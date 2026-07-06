from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from case_study_infrastructure_interdependence.cli import build_audit


def test_infrastructure_audit_scenario():
    audit = build_audit()
    assert audit.sector_count == 5
    assert audit.initial_shock_sector == "power"
    assert audit.initial_shock_magnitude == 0.40


def test_dependency_burden_and_downstream_loss():
    audit = build_audit()
    assert audit.highest_dependency_burden_sector == "power"
    assert audit.highest_dependency_burden == 2.4
    assert audit.largest_downstream_loss_sector == "health"
    assert audit.largest_downstream_loss == 0.32


def test_total_downstream_loss_and_warning():
    audit = build_audit()
    assert audit.total_estimated_downstream_loss == 0.96
    assert "exploratory planning" in audit.interpretation_warning
