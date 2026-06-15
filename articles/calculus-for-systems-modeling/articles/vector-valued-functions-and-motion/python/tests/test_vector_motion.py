from pathlib import Path
import sys
import math

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from vector_motion.cli import audit_trajectory, acceleration, distance, position, velocity

def test_position_origin():
    assert position(0.0) == (0.0, 0.0)

def test_velocity_at_zero():
    assert velocity(0.0) == (1.0, 1.0)

def test_acceleration_at_zero():
    assert acceleration(0.0) == (0.0, 0.0)

def test_distance():
    assert distance((0.0, 0.0), (3.0, 4.0)) == 5.0

def test_audit_positive_arc_length():
    record = audit_trajectory(0.5, "test")
    assert record.approximate_arc_length > 0
    assert record.path_efficiency >= 0
