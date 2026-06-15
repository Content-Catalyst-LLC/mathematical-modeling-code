from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class RelatedRateAudit:
    time: float
    height: float
    height_rate: float
    volume: float
    structural_derivative: float
    inferred_volume_rate: float
    finite_difference_check: float
    absolute_error: float
    warning: str


def volume(height: float, shape_coefficient: float = 12.0) -> float:
    return shape_coefficient * height**2


def d_volume_d_height(height: float, shape_coefficient: float = 12.0) -> float:
    return 2.0 * shape_coefficient * height


def height(time: float) -> float:
    return 2.0 + 0.08 * time


def height_rate(time: float) -> float:
    return 0.08


def finite_difference_volume_rate(time: float, h: float = 1e-4) -> float:
    return (volume(height(time + h)) - volume(height(time - h))) / (2.0 * h)


def audit_time(time: float) -> RelatedRateAudit:
    current_height = height(time)
    current_height_rate = height_rate(time)
    current_volume = volume(current_height)
    structural = d_volume_d_height(current_height)
    inferred_rate = structural * current_height_rate
    fd = finite_difference_volume_rate(time)
    error = abs(inferred_rate - fd)

    warning = ""
    if current_height <= 0:
        warning = "height outside physical domain"
    elif error > 1e-5:
        warning = "finite-difference check differs from related-rate calculation"

    return RelatedRateAudit(
        time=time,
        height=current_height,
        height_rate=current_height_rate,
        volume=current_volume,
        structural_derivative=structural,
        inferred_volume_rate=inferred_rate,
        finite_difference_check=fd,
        absolute_error=error,
        warning=warning,
    )


def related_rate_audits(times: list[float]) -> list[RelatedRateAudit]:
    return [audit_time(t) for t in times]


def to_dicts(rows: list[object]) -> list[dict[str, object]]:
    return [asdict(row) for row in rows]


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
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
