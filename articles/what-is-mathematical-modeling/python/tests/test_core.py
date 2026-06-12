from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
PY_ROOT = ARTICLE_ROOT / "python"
sys.path.insert(0, str(PY_ROOT))

from what_is_mathematical_modeling.core import LogisticModel, simulate_euler, simulate_rk4, sensitivity_oat


def test_logistic_model_outputs_nonnegative():
    model = LogisticModel("test", 10.0, 0.35, 100.0, 0.1, 20)
    result = simulate_euler(model)
    assert all(float(row["state"]) >= 0 for row in result.rows)


def test_rk4_converges_toward_capacity():
    model = LogisticModel("test", 10.0, 0.35, 100.0, 0.1, 200)
    result = simulate_rk4(model)
    assert result.final_state > 90.0
    assert result.final_state <= 101.0


def test_sensitivity_has_expected_rows():
    model = LogisticModel("test", 10.0, 0.35, 100.0, 0.1, 50)
    rows = sensitivity_oat(model)
    assert len(rows) == 6
