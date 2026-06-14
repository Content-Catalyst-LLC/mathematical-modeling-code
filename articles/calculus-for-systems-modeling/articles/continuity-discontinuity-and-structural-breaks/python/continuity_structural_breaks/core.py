from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class BreakDiagnostic:
    x: float
    y: float
    left_slope: float | None
    right_slope: float | None
    slope_change: float | None
    level_jump: float | None
    flag: str


def piecewise_system(x: float) -> float:
    """Synthetic system with a level jump and slope break at x=5."""
    if x < 5.0:
        return 2.0 + 0.5 * x
    return 6.0 + 1.4 * (x - 5.0)


def classify_break(level_jump: float, slope_change: float, jump_threshold: float = 1.0, slope_threshold: float = 0.5) -> str:
    if level_jump > jump_threshold and slope_change > slope_threshold:
        return "level_and_slope_break"
    if level_jump > jump_threshold:
        return "possible_jump"
    if slope_change > slope_threshold:
        return "possible_slope_break"
    return "ok"


def diagnose_breaks(xs: list[float], ys: list[float]) -> list[BreakDiagnostic]:
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have same length")
    if len(xs) < 3:
        raise ValueError("at least three points are required")

    rows: list[BreakDiagnostic] = []

    for i, x in enumerate(xs):
        left_slope = None
        right_slope = None
        slope_change = None
        level_jump = None
        flag = "ok"

        if 0 < i < len(xs) - 1:
            left_slope = (ys[i] - ys[i - 1]) / (xs[i] - xs[i - 1])
            right_slope = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])
            slope_change = abs(right_slope - left_slope)
            level_jump = abs(ys[i] - ys[i - 1])
            flag = classify_break(level_jump, slope_change)

        rows.append(BreakDiagnostic(
            x=x,
            y=ys[i],
            left_slope=left_slope,
            right_slope=right_slope,
            slope_change=slope_change,
            level_jump=level_jump,
            flag=flag,
        ))

    return rows


def summarize_flags(rows: list[BreakDiagnostic]) -> list[dict[str, object]]:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.flag] = counts.get(row.flag, 0) + 1
    return [{"flag": flag, "count": count} for flag, count in sorted(counts.items())]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def to_dicts(rows: list[BreakDiagnostic]) -> list[dict[str, object]]:
    return [asdict(row) for row in rows]
