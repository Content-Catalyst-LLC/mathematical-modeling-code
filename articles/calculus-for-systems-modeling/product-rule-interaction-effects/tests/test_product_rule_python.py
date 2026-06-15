from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from product_rule_interaction_effects.decomposition import build_synthetic_series, decompose_product_rule, summarize


def test_product_rule_residual_is_small():
    time, a, b = build_synthetic_series(401)
    rows = decompose_product_rule(time, a, b)
    summary = summarize(rows)
    assert summary["mean_abs_residual"] < 0.02
