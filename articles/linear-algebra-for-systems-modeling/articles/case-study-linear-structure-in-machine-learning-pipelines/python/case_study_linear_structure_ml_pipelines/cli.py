from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class MachineLearningPipelineAudit:
    workflow_name: str
    scenario_name: str
    observation_count: int
    feature_count: int
    train_count: int
    test_count: int
    model_family: str
    regularization_strength: float
    test_rmse: float
    max_absolute_residual: float
    largest_weight_feature: str
    preprocessing_summary: str
    leakage_warning: str
    interpretation_warning: str


FEATURES = ["asset_age", "load_index", "inspection_gap", "temperature_stress"]

X = [
    [12.0, 0.72, 18.0, 0.41],
    [18.0, 0.81, 24.0, 0.52],
    [7.0, 0.55, 12.0, 0.30],
    [25.0, 0.93, 30.0, 0.68],
    [20.0, 0.88, 28.0, 0.61],
    [9.0, 0.60, 14.0, 0.33],
    [15.0, 0.76, 20.0, 0.48],
    [30.0, 0.98, 35.0, 0.75],
    [11.0, 0.66, 16.0, 0.37],
    [22.0, 0.90, 29.0, 0.64],
]

y = [0.34, 0.48, 0.24, 0.72, 0.63, 0.29, 0.42, 0.82, 0.33, 0.67]


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*matrix)]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def fit_standardizer(matrix: list[list[float]]) -> tuple[list[float], list[float]]:
    columns = transpose(matrix)
    means = [mean(col) for col in columns]
    scales = []
    for col, mu in zip(columns, means):
        variance = sum((value - mu) ** 2 for value in col) / (len(col) - 1)
        scale = math.sqrt(variance)
        scales.append(scale if scale > 0 else 1.0)
    return means, scales


def transform_standardizer(matrix: list[list[float]], means: list[float], scales: list[float]) -> list[list[float]]:
    return [[(row[j] - means[j]) / scales[j] for j in range(len(row))] for row in matrix]


def add_intercept(matrix: list[list[float]]) -> list[list[float]]:
    return [[1.0] + row for row in matrix]


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def transpose_matmul(A: list[list[float]]) -> list[list[float]]:
    p = len(A[0])
    return [[sum(row[i] * row[j] for row in A) for j in range(p)] for i in range(p)]


def transpose_vecmul(A: list[list[float]], vector: list[float]) -> list[float]:
    p = len(A[0])
    return [sum(A[i][j] * vector[i] for i in range(len(A))) for j in range(p)]


def solve_linear_system(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    n = len(rhs)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]

    for pivot in range(n):
        max_row = max(range(pivot, n), key=lambda r: abs(aug[r][pivot]))
        aug[pivot], aug[max_row] = aug[max_row], aug[pivot]

        pivot_value = aug[pivot][pivot]
        if abs(pivot_value) < 1e-12:
            raise ValueError("System is singular or nearly singular.")

        for col in range(pivot, n + 1):
            aug[pivot][col] /= pivot_value

        for row in range(n):
            if row == pivot:
                continue
            factor = aug[row][pivot]
            for col in range(pivot, n + 1):
                aug[row][col] -= factor * aug[pivot][col]

    return [aug[i][n] for i in range(n)]


def fit_ridge(design_matrix: list[list[float]], target: list[float], ridge_lambda: float) -> list[float]:
    xtx = transpose_matmul(design_matrix)
    xty = transpose_vecmul(design_matrix, target)

    for i in range(len(xtx)):
        if i == 0:
            continue
        xtx[i][i] += ridge_lambda

    return solve_linear_system(xtx, xty)


def rmse(errors: list[float]) -> float:
    return math.sqrt(sum(error ** 2 for error in errors) / len(errors))


def build_audit() -> MachineLearningPipelineAudit:
    train_indices = [0, 1, 2, 3, 4, 5, 6]
    test_indices = [7, 8, 9]

    X_train = [X[i] for i in train_indices]
    y_train = [y[i] for i in train_indices]
    X_test = [X[i] for i in test_indices]
    y_test = [y[i] for i in test_indices]

    means, scales = fit_standardizer(X_train)
    X_train_scaled = transform_standardizer(X_train, means, scales)
    X_test_scaled = transform_standardizer(X_test, means, scales)

    train_design = add_intercept(X_train_scaled)
    test_design = add_intercept(X_test_scaled)

    ridge_lambda = 0.25
    beta = fit_ridge(train_design, y_train, ridge_lambda)
    predictions = matvec(test_design, beta)
    residuals = [observed - predicted for observed, predicted in zip(y_test, predictions)]

    feature_weights = beta[1:]
    largest_weight_index = max(range(len(feature_weights)), key=lambda i: abs(feature_weights[i]))

    return MachineLearningPipelineAudit(
        workflow_name="machine_learning_linear_structure_audit",
        scenario_name="synthetic_infrastructure_risk_pipeline",
        observation_count=len(X),
        feature_count=len(FEATURES),
        train_count=len(train_indices),
        test_count=len(test_indices),
        model_family="ridge_regression_linear_baseline",
        regularization_strength=ridge_lambda,
        test_rmse=round(rmse(residuals), 12),
        max_absolute_residual=round(max(abs(error) for error in residuals), 12),
        largest_weight_feature=FEATURES[largest_weight_index],
        preprocessing_summary="Training means and scales were fit on training rows only and then applied to test rows.",
        leakage_warning="Scaling, imputation, feature selection, dimensionality reduction, and threshold tuning must be fit inside the training process. Full-data preprocessing can leak evaluation information into the model.",
        interpretation_warning="Linear pipeline outputs depend on feature definitions, target validity, preprocessing, train-test separation, regularization, residual structure, subgroup performance, drift monitoring, and deployment context. Coefficients and predictions are not automatic causal explanations or decision rules.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "machine_learning_linear_structure_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "machine_learning_linear_structure_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = [
        "# Machine Learning Linear Structure Audit",
        "",
        f"- Workflow: {audit.workflow_name}",
        f"- Scenario: {audit.scenario_name}",
        f"- Observation count: {audit.observation_count}",
        f"- Feature count: {audit.feature_count}",
        f"- Train count: {audit.train_count}",
        f"- Test count: {audit.test_count}",
        f"- Model family: {audit.model_family}",
        f"- Regularization strength: {audit.regularization_strength}",
        f"- Test RMSE: {audit.test_rmse}",
        f"- Max absolute residual: {audit.max_absolute_residual}",
        f"- Largest weight feature: {audit.largest_weight_feature}",
        "",
        audit.preprocessing_summary,
        "",
        audit.leakage_warning,
        "",
        audit.interpretation_warning,
    ]
    (output_dir / "reports" / "machine_learning_linear_structure_audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Machine learning linear structure audit complete.")


if __name__ == "__main__":
    main()
