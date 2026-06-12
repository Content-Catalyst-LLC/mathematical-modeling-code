from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"python"))
from variables_parameters_constraints.core import *

def test_bounds():
    assert bounded_update(120,100)==100
    assert bounded_update(-1,100)==0

def test_simulation():
    rows=simulate_resource(ResourceScenario("test",80,100,8,6,0.015,20))
    assert len(rows)==21
    assert all(0 <= float(r["stock"]) <= 100 for r in rows)

def test_summary_fields():
    summary=summarize_resource(simulate_resource(ResourceScenario("test",80,100,8,6,0.015,20)))
    assert "shortage_periods" in summary and "overflow_periods" in summary

def test_component_score():
    c=ModelComponent("lambda","loss rate","parameter","losses","[0,1]","assumed","How sensitive are outputs?","review")
    assert component_risk_score(c)>0
