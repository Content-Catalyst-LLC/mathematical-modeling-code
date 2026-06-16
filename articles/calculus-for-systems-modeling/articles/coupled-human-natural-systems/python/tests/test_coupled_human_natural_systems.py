from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from coupled_human_natural_systems.cli import (
    regeneration, extraction, adaptive_effort_step, natural_stock_step,
    distributional_burden, threshold_warning, simulate_coupled_system,
    build_scenarios, build_diagnostics
)

def test_regeneration_positive():
    assert regeneration(80, 0.08, 100) > 0

def test_extraction_positive():
    assert extraction(0.003, 12, 80) > 0

def test_adaptive_effort_not_negative():
    assert adaptive_effort_step(1, 1, 1, 10, 1) >= 0

def test_natural_stock_step_not_negative():
    assert natural_stock_step(1, 0.08, 100, 20, 20, 1) >= 0

def test_distributional_burden():
    assert distributional_burden(0.6, 1.4, 0.2) > 0

def test_threshold_warning():
    assert threshold_warning(25, 30) == "below_threshold_review_required"

def test_simulation_record():
    record = simulate_coupled_system("test", 0.08, 100, 0.003, 12, 0.6, 0.2, 0.25, 80, 1.2, 0.1, 0.25, 4)
    assert record.final_natural_stock >= 0

def test_scenarios_present():
    names = {record.scenario_name for record in build_scenarios()}
    assert "baseline_coupled_resource" in names
    assert "restoration_and_adaptation" in names

def test_diagnostics_present():
    assert len(build_diagnostics()) == 4
