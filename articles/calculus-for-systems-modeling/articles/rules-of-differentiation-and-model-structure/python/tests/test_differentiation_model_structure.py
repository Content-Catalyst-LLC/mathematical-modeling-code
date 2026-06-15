from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from differentiation_model_structure.core import product_rule_impact, quotient_rule_resource_per_capita, structural_audit


def test_product_rule_components_sum_to_derivative():
    row = product_rule_impact(10.0)
    assert abs((row.component_a + row.component_b) - row.derivative_value) < 1e-10


def test_quotient_rule_has_ratio_structure():
    row = quotient_rule_resource_per_capita(10.0)
    assert row.rule == "quotient_rule"
    assert "resource_per_capita" in row.model_structure


def test_structural_audit_includes_core_rules():
    rows = structural_audit([0.0, 10.0])
    rules = {row.rule for row in rows}
    assert {"sum_rule", "product_rule", "quotient_rule", "chain_rule"}.issubset(rules)
