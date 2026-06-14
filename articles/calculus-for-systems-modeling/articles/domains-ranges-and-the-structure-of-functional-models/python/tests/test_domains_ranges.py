from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from domains_ranges_functional_models.core import Scenario, bounded_growth_value, evaluate_scenarios, validate_domain


def test_valid_scenario_has_no_domain_issues():
    assert validate_domain(Scenario("baseline", 10.0, 0.2, 100.0, 20.0)) == []


def test_negative_initial_state_is_invalid():
    assert "initial_state must be nonnegative" in validate_domain(Scenario("bad", -1.0, 0.2, 100.0, 20.0))


def test_bounded_growth_output_in_range():
    value = bounded_growth_value(Scenario("baseline", 10.0, 0.2, 100.0, 20.0))
    assert 0 <= value <= 100


def test_evaluate_scenarios_flags_invalid_items():
    rows = evaluate_scenarios([Scenario("baseline", 10.0, 0.2, 100.0, 20.0), Scenario("bad", -1.0, 0.2, 100.0, 20.0)])
    statuses = {row["scenario"]: row["status"] for row in rows}
    assert statuses["baseline"] == "ok"
    assert statuses["bad"] == "domain_review"
