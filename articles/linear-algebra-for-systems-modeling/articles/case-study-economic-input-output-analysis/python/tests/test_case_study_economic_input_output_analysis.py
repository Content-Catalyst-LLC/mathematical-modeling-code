from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from case_study_economic_input_output_analysis.cli import build_audit


def test_input_output_audit_basic_totals():
    audit = build_audit()
    assert audit.sector_count == 3
    assert audit.final_demand_total == 450.0
    assert audit.gross_output_total == 763.099081201887


def test_multiplier_and_shock_results():
    audit = build_audit()
    assert audit.highest_multiplier_sector == "manufacturing"
    assert audit.highest_output_multiplier == 1.951825177111
    assert audit.gross_output_change_total == 48.795629500869


def test_conditioning_and_interpretation_warning():
    audit = build_audit()
    assert audit.leontief_infinity_condition_estimate == 2.147504345667
    assert "Multipliers are not automatic measures" in audit.interpretation_warning
