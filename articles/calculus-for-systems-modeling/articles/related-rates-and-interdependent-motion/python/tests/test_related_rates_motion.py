from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from related_rates_motion.core import audit_time, related_rate_audits


def test_related_rate_matches_finite_difference():
    row = audit_time(10.0)
    assert row.absolute_error < 1e-5


def test_inferred_rate_matches_structural_times_driver():
    row = audit_time(20.0)
    assert abs(row.inferred_volume_rate - row.structural_derivative * row.height_rate) < 1e-12


def test_multiple_audits_created():
    rows = related_rate_audits([0.0, 5.0, 10.0])
    assert len(rows) == 3
