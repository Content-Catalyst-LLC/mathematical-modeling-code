from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class RecoveryRecord:
    time: float
    net_flow: float
    recovered_stock: float
    method: str
    unit_check: str
    warning: str


def net_flow(t: float) -> float:
    inflow = 12.0 + 0.5 * t
    outflow = 7.0 + 0.2 * t
    return inflow - outflow


def trapezoid_recovery(times: list[float], initial_stock: float) -> list[RecoveryRecord]:
    if len(times) < 2:
        raise ValueError("At least two time points are required.")

    records: list[RecoveryRecord] = [
        RecoveryRecord(
            time=times[0],
            net_flow=net_flow(times[0]),
            recovered_stock=initial_stock,
            method="initial condition",
            unit_check="stock units = initial stock units",
            warning="baseline determines recovered level",
        )
    ]

    stock = initial_stock

    for previous, current in zip(times[:-1], times[1:]):
        dt = current - previous
        if dt <= 0:
            raise ValueError("Times must be strictly increasing.")

        area = 0.5 * (net_flow(previous) + net_flow(current)) * dt
        stock += area

        warnings: list[str] = []
        if dt > 2.0:
            warnings.append("large time step; accumulation may be coarse")
        if stock < 0:
            warnings.append("recovered stock is negative; review baseline and flows")

        records.append(
            RecoveryRecord(
                time=current,
                net_flow=net_flow(current),
                recovered_stock=stock,
                method="trapezoidal accumulation",
                unit_check="flow units times time units = stock units",
                warning="; ".join(warnings),
            )
        )

    return records


def rectangle_recovery(times: list[float], initial_stock: float) -> list[RecoveryRecord]:
    if len(times) < 2:
        raise ValueError("At least two time points are required.")

    records: list[RecoveryRecord] = [
        RecoveryRecord(
            time=times[0],
            net_flow=net_flow(times[0]),
            recovered_stock=initial_stock,
            method="initial condition",
            unit_check="stock units = initial stock units",
            warning="baseline determines recovered level",
        )
    ]

    stock = initial_stock

    for previous, current in zip(times[:-1], times[1:]):
        dt = current - previous
        if dt <= 0:
            raise ValueError("Times must be strictly increasing.")
        stock += net_flow(previous) * dt
        records.append(
            RecoveryRecord(
                time=current,
                net_flow=net_flow(current),
                recovered_stock=stock,
                method="left-rectangle accumulation",
                unit_check="flow units times time units = stock units",
                warning="lower-order method; compare with trapezoidal recovery",
            )
        )

    return records


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
