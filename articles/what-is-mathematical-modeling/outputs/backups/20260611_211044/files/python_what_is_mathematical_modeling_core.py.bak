from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from pathlib import Path
import csv
import json
import math
import random
from statistics import mean, pstdev
from typing import Callable, Iterable


@dataclass(frozen=True)
class LogisticModel:
    """Bounded-growth mathematical model.

    dx/dt = r * x * (1 - x / K)

    This is a compact example of a nonlinear dynamic model with a state
    variable, parameters, assumptions, and numerical implementation choices.
    """

    name: str
    initial_state: float
    growth_rate: float
    carrying_capacity: float
    time_step: float
    steps: int

    def validate(self) -> None:
        if self.initial_state < 0:
            raise ValueError("initial_state must be nonnegative.")
        if self.carrying_capacity <= 0:
            raise ValueError("carrying_capacity must be positive.")
        if self.time_step <= 0:
            raise ValueError("time_step must be positive.")
        if self.steps < 1:
            raise ValueError("steps must be at least 1.")
        if self.initial_state > 10 * self.carrying_capacity:
            raise ValueError("initial_state is implausibly high relative to carrying_capacity.")


@dataclass(frozen=True)
class SimulationResult:
    model: LogisticModel
    method: str
    rows: list[dict[str, float | str | int]]

    @property
    def final_state(self) -> float:
        return float(self.rows[-1]["state"])

    @property
    def max_state(self) -> float:
        return max(float(row["state"]) for row in self.rows)

    @property
    def min_state(self) -> float:
        return min(float(row["state"]) for row in self.rows)


def logistic_derivative(x: float, growth_rate: float, carrying_capacity: float) -> float:
    return growth_rate * x * (1.0 - x / carrying_capacity)


def simulate_euler(model: LogisticModel) -> SimulationResult:
    model.validate()
    x = float(model.initial_state)
    rows: list[dict[str, float | str | int]] = []

    for step in range(model.steps + 1):
        time = step * model.time_step
        rows.append({
            "scenario": model.name,
            "method": "euler",
            "step": step,
            "time": round(time, 10),
            "state": round(x, 10),
            "growth_rate": model.growth_rate,
            "carrying_capacity": model.carrying_capacity,
            "time_step": model.time_step,
        })
        dxdt = logistic_derivative(x, model.growth_rate, model.carrying_capacity)
        x = max(0.0, x + dxdt * model.time_step)

    return SimulationResult(model=model, method="euler", rows=rows)


def simulate_rk4(model: LogisticModel) -> SimulationResult:
    model.validate()
    x = float(model.initial_state)
    dt = model.time_step
    r = model.growth_rate
    k_cap = model.carrying_capacity
    rows: list[dict[str, float | str | int]] = []

    for step in range(model.steps + 1):
        time = step * dt
        rows.append({
            "scenario": model.name,
            "method": "rk4",
            "step": step,
            "time": round(time, 10),
            "state": round(x, 10),
            "growth_rate": r,
            "carrying_capacity": k_cap,
            "time_step": dt,
        })

        k1 = logistic_derivative(x, r, k_cap)
        k2 = logistic_derivative(x + 0.5 * dt * k1, r, k_cap)
        k3 = logistic_derivative(x + 0.5 * dt * k2, r, k_cap)
        k4 = logistic_derivative(x + dt * k3, r, k_cap)
        x = max(0.0, x + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4))

    return SimulationResult(model=model, method="rk4", rows=rows)


def run_scenarios(base: LogisticModel) -> list[SimulationResult]:
    scenarios = [
        base,
        replace(base, name="low_growth", growth_rate=base.growth_rate * 0.65),
        replace(base, name="high_growth", growth_rate=base.growth_rate * 1.35),
        replace(base, name="lower_capacity", carrying_capacity=base.carrying_capacity * 0.70),
        replace(base, name="higher_capacity", carrying_capacity=base.carrying_capacity * 1.40),
    ]

    results: list[SimulationResult] = []
    for scenario in scenarios:
        results.append(simulate_euler(scenario))
        results.append(simulate_rk4(scenario))
    return results


def read_observations(path: Path) -> list[tuple[float, float]]:
    observations: list[tuple[float, float]] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            observations.append((float(row["time"]), float(row["observed_state"])))
    return observations


def interpolate_rows(rows: list[dict[str, float | str | int]], time: float) -> float:
    if time <= float(rows[0]["time"]):
        return float(rows[0]["state"])
    if time >= float(rows[-1]["time"]):
        return float(rows[-1]["state"])

    for left, right in zip(rows, rows[1:]):
        t0 = float(left["time"])
        t1 = float(right["time"])
        if t0 <= time <= t1:
            x0 = float(left["state"])
            x1 = float(right["state"])
            if t1 == t0:
                return x0
            weight = (time - t0) / (t1 - t0)
            return x0 + weight * (x1 - x0)

    return float(rows[-1]["state"])


def residuals_against_observations(
    result: SimulationResult,
    observations: list[tuple[float, float]],
) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for time, observed in observations:
        predicted = interpolate_rows(result.rows, time)
        rows.append({
            "scenario": result.model.name,
            "method": result.method,
            "time": round(time, 10),
            "observed": round(observed, 10),
            "predicted": round(predicted, 10),
            "residual": round(observed - predicted, 10),
        })
    return rows


def residual_diagnostics(residual_rows: list[dict[str, float | str]]) -> dict[str, float]:
    residual_values = [float(row["residual"]) for row in residual_rows]
    if not residual_values:
        raise ValueError("No residuals supplied.")

    mse = mean([value * value for value in residual_values])
    mae = mean([abs(value) for value in residual_values])
    bias = mean(residual_values)
    rmse = math.sqrt(mse)

    return {
        "n": float(len(residual_values)),
        "bias": round(bias, 10),
        "mae": round(mae, 10),
        "rmse": round(rmse, 10),
        "residual_std_population": round(pstdev(residual_values), 10),
        "max_abs_residual": round(max(abs(value) for value in residual_values), 10),
    }


def calibrate_grid_search(
    base: LogisticModel,
    observations: list[tuple[float, float]],
    growth_rates: Iterable[float],
    carrying_capacities: Iterable[float],
) -> list[dict[str, float | str]]:
    candidates: list[dict[str, float | str]] = []

    for growth_rate in growth_rates:
        for carrying_capacity in carrying_capacities:
            candidate = replace(
                base,
                name=f"calibrated_r_{growth_rate:.4f}_k_{carrying_capacity:.2f}",
                growth_rate=growth_rate,
                carrying_capacity=carrying_capacity,
            )
            result = simulate_rk4(candidate)
            residual_rows = residuals_against_observations(result, observations)
            diag = residual_diagnostics(residual_rows)
            candidates.append({
                "growth_rate": round(growth_rate, 8),
                "carrying_capacity": round(carrying_capacity, 8),
                "rmse": diag["rmse"],
                "mae": diag["mae"],
                "bias": diag["bias"],
            })

    return sorted(candidates, key=lambda row: float(row["rmse"]))


def sensitivity_oat(
    base: LogisticModel,
    perturbation: float = 0.10,
    output_function: Callable[[SimulationResult], float] | None = None,
) -> list[dict[str, float | str]]:
    if output_function is None:
        output_function = lambda result: result.final_state

    baseline_result = simulate_rk4(base)
    baseline_output = output_function(baseline_result)

    rows: list[dict[str, float | str]] = []
    for parameter_name in ["growth_rate", "carrying_capacity", "initial_state"]:
        base_value = float(getattr(base, parameter_name))
        for direction, multiplier in [("down", 1.0 - perturbation), ("up", 1.0 + perturbation)]:
            modified = replace(base, name=f"{parameter_name}_{direction}", **{parameter_name: base_value * multiplier})
            result = simulate_rk4(modified)
            output = output_function(result)
            rows.append({
                "parameter": parameter_name,
                "direction": direction,
                "base_value": round(base_value, 10),
                "modified_value": round(base_value * multiplier, 10),
                "baseline_output": round(baseline_output, 10),
                "modified_output": round(output, 10),
                "absolute_change": round(output - baseline_output, 10),
                "relative_change": round((output - baseline_output) / baseline_output if baseline_output else 0.0, 10),
            })
    return rows


def monte_carlo_uncertainty(
    base: LogisticModel,
    n: int = 250,
    seed: int = 42,
) -> list[dict[str, float | int]]:
    rng = random.Random(seed)
    rows: list[dict[str, float | int]] = []

    for run_id in range(n):
        growth_rate = max(0.001, rng.gauss(base.growth_rate, base.growth_rate * 0.12))
        carrying_capacity = max(1.0, rng.gauss(base.carrying_capacity, base.carrying_capacity * 0.08))
        initial_state = max(0.001, rng.gauss(base.initial_state, max(base.initial_state * 0.10, 0.01)))

        model = replace(
            base,
            name=f"mc_{run_id:04d}",
            growth_rate=growth_rate,
            carrying_capacity=carrying_capacity,
            initial_state=initial_state,
        )
        result = simulate_rk4(model)
        rows.append({
            "run_id": run_id,
            "growth_rate": round(growth_rate, 10),
            "carrying_capacity": round(carrying_capacity, 10),
            "initial_state": round(initial_state, 10),
            "final_state": round(result.final_state, 10),
            "max_state": round(result.max_state, 10),
        })

    return rows


def summarize_results(results: list[SimulationResult]) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for result in results:
        values = [float(row["state"]) for row in result.rows]
        rows.append({
            "scenario": result.model.name,
            "method": result.method,
            "initial_state": result.model.initial_state,
            "growth_rate": result.model.growth_rate,
            "carrying_capacity": result.model.carrying_capacity,
            "time_step": result.model.time_step,
            "steps": result.model.steps,
            "final_state": round(result.final_state, 10),
            "mean_state": round(mean(values), 10),
            "min_state": round(min(values), 10),
            "max_state": round(max(values), 10),
        })
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write for {path}")

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def model_card(base: LogisticModel) -> dict[str, object]:
    return {
        "article": "What Is Mathematical Modeling?",
        "model_family": "nonlinear dynamic model",
        "equation": "dx/dt = r*x*(1 - x/K)",
        "purpose": [
            "demonstrate model framing",
            "compare numerical methods",
            "support scenario analysis",
            "illustrate calibration and uncertainty",
        ],
        "assumptions": [
            "state is nonnegative",
            "growth rate is constant within each run",
            "carrying capacity is constant within each run",
            "spatial heterogeneity is omitted",
            "process and observation noise are omitted unless explicitly modeled",
        ],
        "baseline_parameters": asdict(base),
        "limitations": [
            "not calibrated to a real empirical system",
            "not valid for extrapolation beyond the stated demonstration purpose",
            "does not include structural model-form uncertainty beyond scenario testing",
        ],
    }
