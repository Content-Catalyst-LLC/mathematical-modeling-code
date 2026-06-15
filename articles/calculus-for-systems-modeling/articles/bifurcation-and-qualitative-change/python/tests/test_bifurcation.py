from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from bifurcation.cli import (
    build_saddle_node_records,
    classify_scalar_stability,
    pitchfork_equilibria,
    saddle_node_derivative,
    saddle_node_equilibria,
    transcritical_equilibria,
)

def test_saddle_node_equilibria_absent_and_present():
    assert saddle_node_equilibria(-1.0) == []
    assert saddle_node_equilibria(0.0) == [0.0]
    assert saddle_node_equilibria(4.0) == [-2.0, 2.0]

def test_saddle_node_derivative():
    assert saddle_node_derivative(2.0) == -4.0

def test_classify_stability():
    assert classify_scalar_stability(-0.1) == "locally_stable"
    assert classify_scalar_stability(0.1) == "locally_unstable"
    assert classify_scalar_stability(0.0) == "inconclusive_at_critical_value"

def test_transcritical_equilibria():
    assert transcritical_equilibria(3.0) == [0.0, 3.0]

def test_pitchfork_equilibria():
    assert pitchfork_equilibria(-1.0) == [0.0]
    assert pitchfork_equilibria(4.0) == [0.0, -2.0, 2.0]

def test_records_include_absent_and_present():
    records = build_saddle_node_records(-1, 1)
    statuses = {record.branch_status for record in records}
    assert "equilibrium_absent" in statuses
    assert "critical_branch" in statuses
    assert "equilibrium_present" in statuses
