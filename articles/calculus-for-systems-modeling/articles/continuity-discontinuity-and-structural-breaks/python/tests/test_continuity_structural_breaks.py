from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from continuity_structural_breaks.core import classify_break, diagnose_breaks, piecewise_system, summarize_flags


def test_piecewise_system_has_jump_at_break():
    assert piecewise_system(4.75) < piecewise_system(5.0)


def test_classify_break_detects_level_and_slope():
    assert classify_break(1.2, 0.8) == "level_and_slope_break"


def test_diagnose_breaks_flags_structural_break():
    xs = [i * 0.25 for i in range(41)]
    ys = [piecewise_system(x) for x in xs]
    rows = diagnose_breaks(xs, ys)
    flags = {row.flag for row in rows}
    assert "level_and_slope_break" in flags or "possible_jump" in flags


def test_summary_counts_all_rows():
    xs = [i * 0.25 for i in range(41)]
    ys = [piecewise_system(x) for x in xs]
    rows = diagnose_breaks(xs, ys)
    summary = summarize_flags(rows)
    assert sum(item["count"] for item in summary) == len(rows)
