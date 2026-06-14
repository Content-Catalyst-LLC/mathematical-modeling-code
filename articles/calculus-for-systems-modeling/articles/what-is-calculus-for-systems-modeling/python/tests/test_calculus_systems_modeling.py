from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from what_is_calculus_for_systems_modeling.core import (
    SystemScenario,
    simulate_logistic,
    summarize_runs,
)


def test_simulation_has_initial_and_final_rows():
    scenario = SystemScenario("test", 10.0, 0.2, 100.0, 0.1, 10)
    rows = simulate_logistic(scenario)
    assert rows[0]["step"] == 0
    assert rows[-1]["step"] == 10


def test_summary_contains_final_state():
    scenario = SystemScenario("test", 10.0, 0.2, 100.0, 0.1, 10)
    summary = summarize_runs(simulate_logistic(scenario))
    assert summary[0]["scenario"] == "test"
    assert summary[0]["final_state"] > 0
