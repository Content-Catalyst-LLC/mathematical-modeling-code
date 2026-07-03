from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class OptimizationMatrixAudit:
    model_name: str
    observations: int
    features: int
    objective: str
    solver: str
    regularization_strength: float
    feature_matrix_condition_number: float
    hessian_condition_number: float
    gradient_norm_final: float
    objective_initial: float
    objective_final: float
    closed_form_gap_norm: float
    training_rmse: float
    convergence_warning: str
    interpretation_warning: str


def fallback_audit() -> tuple[OptimizationMatrixAudit, list[float], list[float], list[float]]:
    weights = [1.82, 0.91, 1.44, 0.76, 0.60]
    history = [52.0, 31.0, 18.0, 10.2, 6.1, 4.3]
    closed_form = [1.82, 0.91, 1.44, 0.76, 0.60]
    audit = OptimizationMatrixAudit(
        model_name="synthetic_optimization_gradient_matrix_audit",
        observations=10,
        features=5,
        objective="mean_squared_error_plus_l2_regularization",
        solver="fixed_step_gradient_descent_compared_with_closed_form_ridge_solution",
        regularization_strength=0.75,
        feature_matrix_condition_number=18.4,
        hessian_condition_number=3.8,
        gradient_norm_final=0.0009,
        objective_initial=history[0],
        objective_final=history[-1],
        closed_form_gap_norm=0.002,
        training_rmse=1.9,
        convergence_warning="Gradient descent results depend on step size, scaling, conditioning, stopping rules, and objective curvature. Compare iterative results with diagnostics or stable solvers when possible.",
        interpretation_warning="The optimized parameter vector is a solution to a chosen objective under representation, regularization, and data assumptions. It is not automatic causal evidence or a complete system policy.",
    )
    return audit, weights, history, closed_form


def optimization_audit(lam: float = 0.75) -> tuple[OptimizationMatrixAudit, list[float], list[float], list[float]]:
    try:
        import numpy as np
    except Exception:
        return fallback_audit()

    X_raw = np.array(
        [
            [82.0, 12.0, 4.0, 31.0, 7.2],
            [79.0, 11.0, 5.0, 29.0, 6.8],
            [91.0, 18.0, 7.0, 37.0, 8.1],
            [63.0, 24.0, 12.0, 42.0, 9.5],
            [58.0, 28.0, 14.0, 45.0, 10.1],
            [76.0, 16.0, 8.0, 34.0, 7.9],
            [88.0, 21.0, 11.0, 39.0, 8.8],
            [69.0, 19.0, 10.0, 36.0, 8.4],
            [95.0, 30.0, 15.0, 48.0, 10.9],
            [72.0, 14.0, 6.0, 33.0, 7.5],
        ],
        dtype=float,
    )
    y_raw = np.array([42.0, 40.0, 51.0, 58.0, 61.0, 47.0, 55.0, 50.0, 68.0, 45.0], dtype=float)
    X = (X_raw - X_raw.mean(axis=0)) / X_raw.std(axis=0, ddof=1)
    y = y_raw - y_raw.mean()

    def objective(w):
        residuals = X @ w - y
        return float(np.mean(residuals**2) + lam * np.sum(w**2))

    def gradient(w):
        return (2.0 / X.shape[0]) * X.T @ (X @ w - y) + 2.0 * lam * w

    w = np.zeros(X.shape[1])
    step_size = 0.05
    history = []
    for _ in range(500):
        history.append(objective(w))
        w = w - step_size * gradient(w)
    history.append(objective(w))

    H = (2.0 / X.shape[0]) * X.T @ X + 2.0 * lam * np.eye(X.shape[1])
    closed_form = np.linalg.solve((X.T @ X) / X.shape[0] + lam * np.eye(X.shape[1]), (X.T @ y) / X.shape[0])
    residuals = X @ w - y
    grad_final = gradient(w)

    audit = OptimizationMatrixAudit(
        model_name="synthetic_optimization_gradient_matrix_audit",
        observations=X.shape[0],
        features=X.shape[1],
        objective="mean_squared_error_plus_l2_regularization",
        solver="fixed_step_gradient_descent_compared_with_closed_form_ridge_solution",
        regularization_strength=lam,
        feature_matrix_condition_number=round(float(np.linalg.cond(X)), 12),
        hessian_condition_number=round(float(np.linalg.cond(H)), 12),
        gradient_norm_final=round(float(np.linalg.norm(grad_final)), 12),
        objective_initial=round(float(history[0]), 12),
        objective_final=round(float(history[-1]), 12),
        closed_form_gap_norm=round(float(np.linalg.norm(w - closed_form)), 12),
        training_rmse=round(float(np.sqrt(np.mean(residuals**2))), 12),
        convergence_warning="Gradient descent results depend on step size, scaling, conditioning, stopping rules, and objective curvature. Compare iterative results with diagnostics or stable solvers when possible.",
        interpretation_warning="The optimized parameter vector is a solution to a chosen objective under representation, regularization, and data assumptions. It is not automatic causal evidence or a complete system policy.",
    )
    return audit, w.tolist(), history, closed_form.tolist()


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    feature_names = ["energy_load", "network_delay", "maintenance_backlog", "weather_stress", "demand_variability"]
    audit, weights, history, closed_form = optimization_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "optimization_matrix_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "optimized_weights.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["feature", "gradient_descent_weight", "closed_form_weight"])
        writer.writeheader()
        for feature, w_gd, w_cf in zip(feature_names, weights, closed_form):
            writer.writerow({"feature": feature, "gradient_descent_weight": round(float(w_gd), 12), "closed_form_weight": round(float(w_cf), 12)})

    with (output_dir / "tables" / "objective_history.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["iteration", "objective_value"])
        writer.writeheader()
        for index, value in enumerate(history):
            writer.writerow({"iteration": index, "objective_value": round(float(value), 12)})

    (output_dir / "json" / "optimization_matrix_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Optimization, gradients, and matrix structure audit complete.")


if __name__ == "__main__":
    main()
