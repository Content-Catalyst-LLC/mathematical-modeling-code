from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from typed_model_records_haskell.cli import (
    ModelParameters,
    ModelState,
    build_output,
    simulate,
    step_logistic,
    validate_parameters,
)

def params():
    return ModelParameters(0.35, 100.0, 10.0, 0.25, 20.0, "test")

def test_validation_passes():
    assert validate_parameters(params()) == []

def test_validation_fails():
    bad = ModelParameters(-0.1, 100.0, 10.0, 0.25, 20.0, "bad")
    assert validate_parameters(bad)

def test_step_advances_time():
    state = step_logistic(params(), ModelState(0.0, 10.0))
    assert state.model_time == 0.25

def test_simulate_has_final_state():
    states = simulate(params())
    assert states[-1].model_time >= 20.0

def test_output_contains_diagnostics():
    output = build_output(params())
    assert len(output.diagnostics) >= 2
