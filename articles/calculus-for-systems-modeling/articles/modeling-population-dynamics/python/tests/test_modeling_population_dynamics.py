from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from modeling_population_dynamics.cli import (
    build_parameter_records,
    build_scenarios,
    exponential_population,
    logistic_population,
    per_capita_growth,
)

def test_exponential_growth_positive():
    assert exponential_population(100, 0.08, 10) > 100

def test_logistic_growth_bounded():
    value = logistic_population(100, 0.08, 1000, 40)
    assert 100 < value < 1000

def test_parameter_records_present():
    assert {record.parameter_name for record in build_parameter_records()} == {"N0", "r", "K"}

def test_scenarios_present():
    assert {record.model_type for record in build_scenarios()} == {"exponential", "logistic"}

def test_per_capita_growth():
    assert per_capita_growth(10, 100) == 0.1
