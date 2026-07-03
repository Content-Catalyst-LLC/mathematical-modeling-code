from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from simulation_of_high_dimensional_systems.cli import simulation_audit


def test_simulation_audit_basic_fields():
    audit, final_totals, energy, matrix_summary = simulation_audit()
    assert audit.state_dimension == 24
    assert audit.time_steps == 40
    assert audit.ensemble_runs == 250


def test_simulation_outputs_have_expected_shape():
    audit, final_totals, energy, matrix_summary = simulation_audit()
    assert len(final_totals) > 0
    assert len(energy) > 0
    assert len(matrix_summary) == 2


def test_simulation_diagnostics_reasonable():
    audit, final_totals, energy, matrix_summary = simulation_audit()
    assert audit.transition_spectral_radius < 1.0
    assert 0 <= audit.transition_density <= 1
    assert audit.final_state_mean_total > 0
