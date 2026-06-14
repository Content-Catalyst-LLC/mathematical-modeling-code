from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math
from typing import Iterable


@dataclass(frozen=True)
class BreakDiagnostic:
    x: float
    y: float
    left_slope: float | None
    right_slope: float | None
    slope_change: float | None
    level_jump: float | None
    flag: str


@dataclass(frozen=True)
class RegularityExample:
    example: str
    continuous: bool
    uniformly_continuous: bool | None
    lipschitz: bool | None
    differentiable_everywhere: bool
    note: str


@dataclass(frozen=True)
class InvariantReview:
    value: float
    lower: float
    upper: float
    inside: bool
    issue: str


def piecewise_system(x: float) -> float:
    if x < 5.0:
        return 2.0 + 0.5 * x
    return 6.0 + 1.4 * (x - 5.0)


def removable_discontinuity(x: float) -> float:
    if x == 1.0:
        raise ValueError("undefined at removable discontinuity")
    return (x * x - 1.0) / (x - 1.0)


def jump_function(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0


def oscillatory_function(x: float) -> float:
    if x == 0.0:
        raise ValueError("undefined at essential discontinuity")
    return math.sin(1.0 / x)


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

    output: list[BreakDiagnostic] = []
    for i, x in enumerate(xs):
        if i == 0 or i == len(xs) - 1:
            output.append(BreakDiagnostic(x, ys[i], None, None, None, None, "ok"))
            continue

        left_slope = (ys[i] - ys[i - 1]) / (xs[i] - xs[i - 1])
        right_slope = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])
        slope_change = abs(right_slope - left_slope)
        level_jump = abs(ys[i] - ys[i - 1])
        output.append(
            BreakDiagnostic(
                x=x,
                y=ys[i],
                left_slope=left_slope,
                right_slope=right_slope,
                slope_change=slope_change,
                level_jump=level_jump,
                flag=classify_break(level_jump, slope_change),
            )
        )

    return output


def regularity_examples() -> list[RegularityExample]:
    return [
        RegularityExample("|x|", True, True, True, False, "Continuous everywhere, not differentiable at 0."),
        RegularityExample("x^2 on R", True, False, None, True, "Continuous but not uniformly continuous on unbounded domain."),
        RegularityExample("step function", False, False, False, False, "Jump discontinuity at threshold."),
        RegularityExample("sin(1/x)", False, False, False, False, "Essential oscillatory discontinuity at 0."),
        RegularityExample("piecewise structural break", False, False, False, False, "Synthetic level and slope break at x=5."),
    ]


def invariant_review(values: Iterable[float], lower: float, upper: float) -> list[InvariantReview]:
    if lower > upper:
        raise ValueError("lower must be <= upper.")
    output: list[InvariantReview] = []
    for value in values:
        inside = lower <= value <= upper
        output.append(
            InvariantReview(
                value=value,
                lower=lower,
                upper=upper,
                inside=inside,
                issue="" if inside else "value outside invariant interval",
            )
        )
    return output


def records_to_dicts(records: list[object]) -> list[dict[str, object]]:
    return [asdict(record) for record in records]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
