from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from state_space_geometry.cli import build_audit, dot, norm1, norm2, norminf, subtract


def test_dot():
    assert dot([1.0, 2.0], [3.0, 4.0]) == 11.0


def test_norms():
    x = [2.0, -1.5, -0.3]
    assert round(norm1(x), 6) == 3.8
    assert round(norm2(x), 6) == 2.517936
    assert round(norminf(x), 6) == 2.0


def test_subtract():
    assert subtract([12.0, 4.0, 0.8], [10.0, 5.5, 1.1]) == [2.0, -1.5, -0.30000000000000004]


def test_build_audit():
    audit = build_audit()
    assert audit.system_name == "three_indicator_state_space_geometry_audit"
    assert audit.norm_1 == 3.8
    assert audit.euclidean_distance > 0
    assert audit.weighted_distance > 0
