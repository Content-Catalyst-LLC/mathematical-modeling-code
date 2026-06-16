from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from sensitivity_robustness_parameter_dependence.cli import (
    build_parameter_records,
    build_sensitivity_records,
    logistic_final,
)

def test_parameter_records_present():
    assert len(build_parameter_records()) >= 3

def test_sensitivity_records_present():
    assert len(build_sensitivity_records()) >= 3

def test_logistic_final_positive():
    assert logistic_final(10, 0.35, 100, 20) > 0

def test_robustness_notes_available():
    assert all(record.robustness_note in {"stable", "sensitive"} for record in build_sensitivity_records())
