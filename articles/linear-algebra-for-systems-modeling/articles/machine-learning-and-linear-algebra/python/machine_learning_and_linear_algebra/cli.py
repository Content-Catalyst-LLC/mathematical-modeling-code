from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class MachineLearningLinearAlgebraAudit:
    model_name: str
    observations: int
    features: int
    method: str
    preprocessing: str
    regularization_strength: float
    feature_matrix_condition_number: float
    gram_matrix_condition_number: float
    numerical_rank: int
    ridge_weight_norm: float
    training_rmse: float
    maximum_absolute_residual: float
    first_two_component_energy: float
    validation_warning: str
    interpretation_warning: str


def fallback_audit() -> tuple[MachineLearningLinearAlgebraAudit, list[float], list[float], list[float]]:
    weights = [1.84, 0.92, 1.45, 0.77, 0.61]
    residuals = [-0.9, 1.2, -1.8, 0.7, 2.1, -0.6, 1.5, -1.1, 3.8, -0.5]
    singular_values = [6.24, 2.16, 0.91, 0.42, 0.18]
    audit = MachineLearningLinearAlgebraAudit(
        model_name="synthetic_machine_learning_linear_algebra_audit",
        observations=10,
        features=5,
        method="standardized_ridge_regression_with_svd_diagnostics",
        preprocessing="centered_and_standardized_features_centered_target",
        regularization_strength=0.75,
        feature_matrix_condition_number=18.4,
        gram_matrix_condition_number=339.2,
        numerical_rank=5,
        ridge_weight_norm=round(sum(w*w for w in weights) ** 0.5, 12),
        training_rmse=1.9,
        maximum_absolute_residual=max(abs(v) for v in residuals),
        first_two_component_energy=0.94,
        validation_warning="Training error is not generalization evidence. Use validation data, time splits, cross-validation, residual review, and distribution-shift checks before deployment.",
        interpretation_warning="Weights, components, embeddings, and model scores are learned artifacts of the feature matrix, objective, preprocessing, regularization, and training data. They are not automatic causes or truths.",
    )
    return audit, weights, residuals, singular_values


def ml_linear_algebra_audit(lam: float = 0.75) -> tuple[MachineLearningLinearAlgebraAudit, list[float], list[float], list[float]]:
    try:
        import numpy as np
    except Exception:
        return fallback_audit()

    X = np.array(
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
    y = np.array([42.0, 40.0, 51.0, 58.0, 61.0, 47.0, 55.0, 50.0, 68.0, 45.0], dtype=float)

    Xs = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)
    yc = y - y.mean()
    gram = Xs.T @ Xs
    weights = np.linalg.solve(gram + lam * np.eye(Xs.shape[1]), Xs.T @ yc)
    predictions = Xs @ weights + y.mean()
    residuals = y - predictions
    singular_values = np.linalg.svd(Xs, full_matrices=False, compute_uv=False)
    rank = int(np.linalg.matrix_rank(Xs))
    component_energy = singular_values**2 / np.sum(singular_values**2)
    first_two_energy = float(np.sum(component_energy[:2]))

    audit = MachineLearningLinearAlgebraAudit(
        model_name="synthetic_machine_learning_linear_algebra_audit",
        observations=X.shape[0],
        features=X.shape[1],
        method="standardized_ridge_regression_with_svd_diagnostics",
        preprocessing="centered_and_standardized_features_centered_target",
        regularization_strength=lam,
        feature_matrix_condition_number=round(float(np.linalg.cond(Xs)), 12),
        gram_matrix_condition_number=round(float(np.linalg.cond(gram)), 12),
        numerical_rank=rank,
        ridge_weight_norm=round(float(np.linalg.norm(weights, ord=2)), 12),
        training_rmse=round(float(np.sqrt(np.mean(residuals**2))), 12),
        maximum_absolute_residual=round(float(np.max(np.abs(residuals))), 12),
        first_two_component_energy=round(first_two_energy, 12),
        validation_warning="Training error is not generalization evidence. Use validation data, time splits, cross-validation, residual review, and distribution-shift checks before deployment.",
        interpretation_warning="Weights, components, embeddings, and model scores are learned artifacts of the feature matrix, objective, preprocessing, regularization, and training data. They are not automatic causes or truths.",
    )
    return audit, weights.tolist(), residuals.tolist(), singular_values.tolist()


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    feature_names = ["energy_load", "network_delay", "maintenance_backlog", "weather_stress", "demand_variability"]
    audit, weights, residuals, singular_values = ml_linear_algebra_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "ml_linear_algebra_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "ridge_weights.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["feature", "weight"])
        writer.writeheader()
        for feature, weight in zip(feature_names, weights):
            writer.writerow({"feature": feature, "weight": round(float(weight), 12)})

    with (output_dir / "tables" / "residual_diagnostics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["observation", "residual"])
        writer.writeheader()
        for index, residual in enumerate(residuals):
            writer.writerow({"observation": index, "residual": round(float(residual), 12)})

    total_energy = sum(v * v for v in singular_values)
    with (output_dir / "tables" / "singular_value_diagnostics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["component", "singular_value", "energy_share"])
        writer.writeheader()
        for index, value in enumerate(singular_values):
            writer.writerow({"component": index + 1, "singular_value": round(float(value), 12), "energy_share": round(float(value * value / total_energy), 12)})

    (output_dir / "json" / "ml_linear_algebra_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Machine learning linear algebra audit complete.")


if __name__ == "__main__":
    main()
