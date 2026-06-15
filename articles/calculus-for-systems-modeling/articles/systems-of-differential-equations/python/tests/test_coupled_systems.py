from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from coupled_systems.cli import (
    coexistence_equilibrium,
    predator_prey_rates,
    simulate_predator_prey,
)

def test_predator_prey_rates():
    prey_rate, predator_rate = predator_prey_rates(40.0, 9.0, 0.7, 0.05, 0.02, 0.5)
    assert abs(prey_rate - 10.0) < 1e-12
    assert abs(predator_rate - 2.7) < 1e-12

def test_coexistence_equilibrium():
    prey_star, predator_star = coexistence_equilibrium(0.7, 0.05, 0.02, 0.5)
    assert prey_star == 25.0
    assert abs(predator_star - 14.0) < 1e-12

def test_simulation_length():
    assert len(simulate_predator_prey(40.0, 9.0, 0.7, 0.05, 0.02, 0.5, 0.01, 10)) == 11

def test_record_warning():
    record = simulate_predator_prey(40.0, 9.0, 0.7, 0.05, 0.02, 0.5, 0.01, 1)[0]
    assert "well-mixed" in record.warning
