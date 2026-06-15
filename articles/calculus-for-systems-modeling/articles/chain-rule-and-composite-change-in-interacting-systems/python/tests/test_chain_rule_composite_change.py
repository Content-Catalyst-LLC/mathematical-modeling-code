from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from chain_rule_composite_change.core import chain_rule_audit, chain_rule_audits


def test_chain_rule_matches_finite_difference():
    row = chain_rule_audit(10.0)
    assert row.absolute_error < 1e-5


def test_component_product_matches_total():
    row = chain_rule_audit(10.0)
    product = (
        row.d_temperature_d_forcing
        * row.d_forcing_d_concentration
        * row.d_concentration_d_emissions
        * row.emissions_rate
    )
    assert abs(product - row.total_derivative) < 1e-12


def test_multiple_audits_created():
    rows = chain_rule_audits([0.0, 10.0, 20.0])
    assert len(rows) == 3
