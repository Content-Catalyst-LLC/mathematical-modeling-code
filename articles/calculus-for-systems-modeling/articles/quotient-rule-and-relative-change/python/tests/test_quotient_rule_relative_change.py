from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from quotient_rule_relative_change.core import quotient_audit, quotient_audits


def test_components_sum_to_quotient_derivative():
    row = quotient_audit(10.0)
    assert abs((row.numerator_effect + row.denominator_effect) - row.quotient_derivative) < 1e-12


def test_relative_rate_identity():
    row = quotient_audit(10.0)
    assert abs(row.ratio_relative_rate - (row.numerator_relative_rate - row.denominator_relative_rate)) < 1e-12


def test_multiple_audits_created():
    rows = quotient_audits([0.0, 5.0, 10.0])
    assert len(rows) == 3
