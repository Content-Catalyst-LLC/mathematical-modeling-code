from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from scientific_computing_modeling_workflows.core import (
    ResourceScenario,
    WorkflowRecord,
    hash_file,
    simulate,
    summarize_trajectories,
    workflow_risk_score,
)


def test_simulate_outputs_all_steps():
    scenario = ResourceScenario("test", 70.0, 0.18, 100.0, 6.0, 0.0, 0.1, 5, 123)
    rows = simulate(scenario)
    assert rows[0]["step"] == 0
    assert rows[-1]["step"] == 5


def test_summarize_trajectories():
    scenario = ResourceScenario("test", 70.0, 0.18, 100.0, 6.0, 0.0, 0.1, 5, 123)
    summary = summarize_trajectories(simulate(scenario))
    assert summary[0]["scenario"] == "test"
    assert summary[0]["steps"] == 5


def test_workflow_risk_score_positive():
    record = WorkflowRecord(
        "run_manifest",
        "reproducibility",
        "manifest_json",
        "Records command environment seed and outputs.",
        "Can another analyst rerun the workflow?",
        "active",
    )
    assert workflow_risk_score(record) > 0


def test_hash_file_missing():
    assert hash_file(Path("definitely_missing_file.txt")) == "missing"
