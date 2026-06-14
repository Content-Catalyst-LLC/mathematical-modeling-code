from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class SystemScenario:
    scenario: str
    initial_state: float
    rate: float
    capacity: float
    dt: float
    steps: int
    interpretation: str = ""


def validate_scenario(item: SystemScenario) -> None:
    if item.initial_state < 0:
        raise ValueError("initial_state must be nonnegative.")
    if item.rate < 0:
        raise ValueError("rate must be nonnegative.")
    if item.capacity <= 0:
        raise ValueError("capacity must be positive.")
    if item.dt <= 0:
        raise ValueError("dt must be positive.")
    if item.steps < 1:
        raise ValueError("steps must be positive.")


def simulate_logistic(item: SystemScenario) -> list[dict[str, object]]:
    """Simulate dS/dt = rS(1 - S/K) with Euler's method."""
    validate_scenario(item)
    state = item.initial_state
    rows: list[dict[str, object]] = []

    for step in range(item.steps + 1):
        time = step * item.dt
        rows.append(
            {
                "scenario": item.scenario,
                "step": step,
                "time": round(time, 10),
                "state": round(state, 10),
                "rate": item.rate,
                "capacity": item.capacity,
                "interpretation": item.interpretation,
            }
        )

        if step == item.steps:
            break

        derivative = item.rate * state * (1.0 - state / item.capacity)
        state = max(0.0, state + derivative * item.dt)

    return rows


def summarize_runs(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["scenario"]), []).append(row)

    output: list[dict[str, object]] = []
    for scenario, values in sorted(grouped.items()):
        final = max(values, key=lambda row: int(row["step"]))
        output.append(
            {
                "scenario": scenario,
                "final_state": round(float(final["state"]), 10),
                "max_state": round(max(float(row["state"]) for row in values), 10),
                "steps": int(final["step"]),
                "rate": final["rate"],
                "capacity": final["capacity"],
                "interpretation": final["interpretation"],
            }
        )

    return output


def load_scenarios(path: Path) -> list[SystemScenario]:
    scenarios: list[SystemScenario] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            item = SystemScenario(
                scenario=row["scenario"],
                initial_state=float(row["initial_state"]),
                rate=float(row["rate"]),
                capacity=float(row["capacity"]),
                dt=float(row["dt"]),
                steps=int(row["steps"]),
                interpretation=row.get("interpretation", ""),
            )
            validate_scenario(item)
            scenarios.append(item)
    return scenarios


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def scenario_manifest(scenarios: list[SystemScenario], summary: list[dict[str, object]]) -> dict[str, object]:
    return {
        "article": "What Is Calculus for Systems Modeling?",
        "model": "dS/dt = rS(1 - S/K)",
        "method": "Euler approximation",
        "scenarios": [asdict(item) for item in scenarios],
        "summary": summary,
        "interpretive_warning": "Educational synthetic workflow. Do not treat as empirical model validation.",
    }
