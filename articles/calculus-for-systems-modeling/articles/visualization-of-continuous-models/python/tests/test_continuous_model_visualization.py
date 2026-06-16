from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from continuous_model_visualization.cli import (
    build_audit_records,
    build_trajectories,
    logistic_solution,
)

def test_logistic_solution_positive():
    assert logistic_solution(0, 10, 0.35, 100) == 10
    assert logistic_solution(10, 10, 0.35, 100) > 10

def test_trajectories_include_scenarios():
    records = build_trajectories()
    scenarios = {record.scenario for record in records}
    assert scenarios == {"low_growth", "baseline", "high_growth"}
    assert len(records) == 243

def test_audit_records_include_diagnostic_plot():
    records = build_audit_records()
    assert any(record.visual_type == "diagnostic_plot" for record in records)
