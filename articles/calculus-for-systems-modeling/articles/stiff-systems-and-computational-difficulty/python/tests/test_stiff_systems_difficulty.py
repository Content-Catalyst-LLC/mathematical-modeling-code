from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from stiff_systems_difficulty.cli import (
    exact_solution,
    explicit_euler,
    implicit_euler,
    stiffness_audit,
    stiffness_ratio,
)

def test_exact_solution_initial_value():
    assert exact_solution(0.0, 1.0, -50.0) == 1.0

def test_explicit_instability_factor():
    _, amp = explicit_euler(1.0, -50.0, 0.1, 1.0)
    assert amp > 1.0

def test_implicit_stability_factor():
    _, amp = implicit_euler(1.0, -50.0, 0.1, 1.0)
    assert amp <= 1.0

def test_stiffness_audit_records():
    records = stiffness_audit()
    assert len(records) == 8
    assert any(record.method == "implicit_euler" for record in records)

def test_stiffness_ratio():
    assert stiffness_ratio([-1.0, -50.0]) == 50.0
