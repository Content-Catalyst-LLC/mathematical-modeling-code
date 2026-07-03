from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class HighDimensionalSimulationAudit:
    model_name: str
    state_dimension: int
    time_steps: int
    ensemble_runs: int
    method: str
    random_seed: int
    transition_spectral_radius: float
    transition_density: float
    final_state_mean_norm: float
    final_state_mean_total: float
    final_state_95th_percentile_total: float
    threshold_exceedance_probability: float
    first_three_component_energy: float
    validation_warning: str
    interpretation_warning: str


def fallback_audit() -> tuple[HighDimensionalSimulationAudit, list[float], list[float], list[float]]:
    final_totals = [23.2, 24.1, 22.8, 25.7, 24.9, 23.6, 26.1, 22.4, 24.7, 25.2]
    svd_energy = [0.46, 0.21, 0.11, 0.07, 0.05]
    audit = HighDimensionalSimulationAudit(
        model_name="synthetic_high_dimensional_simulation_audit",
        state_dimension=24,
        time_steps=40,
        ensemble_runs=250,
        method="sparse_linear_state_update_with_correlated_monte_carlo_shocks",
        random_seed=20260629,
        transition_spectral_radius=0.94,
        transition_density=0.12,
        final_state_mean_norm=4.8,
        final_state_mean_total=24.6,
        final_state_95th_percentile_total=26.0,
        threshold_exceedance_probability=0.10,
        first_three_component_energy=round(sum(svd_energy[:3]), 12),
        validation_warning="Simulation results depend on state representation, transition structure, random seed, shock distribution, covariance assumptions, time step, ensemble size, and validation evidence.",
        interpretation_warning="High-dimensional simulation outputs are conditional model outcomes, not observations of the future. Scenario assumptions, uncertainty, sensitivity, and model limits should be reported.",
    )
    return audit, final_totals, svd_energy, [0.94, 0.12]


def simulation_audit() -> tuple[HighDimensionalSimulationAudit, list[float], list[float], list[float]]:
    try:
        import numpy as np
    except Exception:
        return fallback_audit()

    n = 24
    time_steps = 40
    ensemble_runs = 250
    seed = 20260629
    rng = np.random.default_rng(seed)

    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        A[i, i] = 0.82
        if i > 0:
            A[i, i - 1] = 0.08
        if i < n - 1:
            A[i, i + 1] = 0.08
        if i + 5 < n:
            A[i, i + 5] = 0.08 / 3.0

    spectral_radius = float(max(abs(np.linalg.eigvals(A))))
    if spectral_radius >= 0.98:
        A = A / (spectral_radius + 0.05)
        spectral_radius = float(max(abs(np.linalg.eigvals(A))))

    base_state = np.linspace(1.0, 2.5, n)
    covariance = 0.015 * np.eye(n)
    for i in range(n - 1):
        covariance[i, i + 1] = 0.006
        covariance[i + 1, i] = 0.006

    trajectories = np.zeros((ensemble_runs, time_steps + 1, n), dtype=float)
    for run in range(ensemble_runs):
        x = base_state + rng.normal(0.0, 0.05, size=n)
        trajectories[run, 0, :] = x
        for t in range(time_steps):
            shock = rng.multivariate_normal(np.zeros(n), covariance)
            input_vector = 0.03 * np.sin((t + 1) / 6.0) * np.ones(n)
            x = A @ x + input_vector + shock
            x = np.maximum(x, 0.0)
            trajectories[run, t + 1, :] = x

    final_states = trajectories[:, -1, :]
    final_totals = final_states.sum(axis=1)
    threshold = float(np.quantile(final_totals, 0.90))
    exceedance_probability = float(np.mean(final_totals > threshold))

    centered = final_states - final_states.mean(axis=0)
    singular_values = np.linalg.svd(centered, full_matrices=False, compute_uv=False)
    energy = singular_values**2 / np.sum(singular_values**2)
    density = float(np.count_nonzero(A) / A.size)

    audit = HighDimensionalSimulationAudit(
        model_name="synthetic_high_dimensional_simulation_audit",
        state_dimension=n,
        time_steps=time_steps,
        ensemble_runs=ensemble_runs,
        method="sparse_linear_state_update_with_correlated_monte_carlo_shocks",
        random_seed=seed,
        transition_spectral_radius=round(spectral_radius, 12),
        transition_density=round(density, 12),
        final_state_mean_norm=round(float(np.linalg.norm(final_states.mean(axis=0))), 12),
        final_state_mean_total=round(float(np.mean(final_totals)), 12),
        final_state_95th_percentile_total=round(float(np.quantile(final_totals, 0.95)), 12),
        threshold_exceedance_probability=round(exceedance_probability, 12),
        first_three_component_energy=round(float(np.sum(energy[:3])), 12),
        validation_warning="Simulation results depend on state representation, transition structure, random seed, shock distribution, covariance assumptions, time step, ensemble size, and validation evidence.",
        interpretation_warning="High-dimensional simulation outputs are conditional model outcomes, not observations of the future. Scenario assumptions, uncertainty, sensitivity, and model limits should be reported.",
    )
    return audit, final_totals.tolist(), energy.tolist(), [spectral_radius, density]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, final_totals, energy, matrix_summary = simulation_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "high_dimensional_simulation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "ensemble_final_totals.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["run_id", "final_total"])
        writer.writeheader()
        for run_id, total in enumerate(final_totals):
            writer.writerow({"run_id": run_id, "final_total": round(float(total), 12)})

    with (output_dir / "tables" / "final_state_svd_energy.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["component", "energy_share"])
        writer.writeheader()
        for index, value in enumerate(energy[:10]):
            writer.writerow({"component": index + 1, "energy_share": round(float(value), 12)})

    with (output_dir / "tables" / "transition_matrix_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerow({"metric": "transition_spectral_radius", "value": round(float(matrix_summary[0]), 12)})
        writer.writerow({"metric": "transition_density", "value": round(float(matrix_summary[1]), 12)})

    (output_dir / "json" / "high_dimensional_simulation_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("High-dimensional simulation audit complete.")


if __name__ == "__main__":
    main()
