from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from case_study_state_transition_and_markov_dynamics.cli import build_audit


def test_markov_audit_structure_and_stochastic_check():
    audit = build_audit()
    assert audit.state_count == 4
    assert audit.time_steps == 5
    assert audit.stochastic_check_passed is True


def test_baseline_and_stationary_results():
    audit = build_audit()
    assert audit.highest_probability_state_after_horizon == "normal"
    assert audit.highest_probability_after_horizon == 0.42833125
    assert audit.stationary_highest_probability_state == "normal"
    assert audit.stationary_highest_probability == 0.40602189781


def test_stress_scenario_and_warning():
    audit = build_audit()
    assert audit.baseline_disrupted_probability_after_horizon == 0.1756128125
    assert audit.stress_disrupted_probability_after_horizon == 0.41016825
    assert "memoryless" not in audit.memoryless_warning.lower() or "current state" in audit.memoryless_warning.lower()
