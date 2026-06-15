from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))
from functions_several_variables.cli import is_feasible, system_response

def test_system_response():
    assert system_response(2.0, 4.0) == 18.0

def test_feasible_inside():
    assert is_feasible(4.0, 3.0)

def test_infeasible_budget():
    assert not is_feasible(8.0, 4.0)
