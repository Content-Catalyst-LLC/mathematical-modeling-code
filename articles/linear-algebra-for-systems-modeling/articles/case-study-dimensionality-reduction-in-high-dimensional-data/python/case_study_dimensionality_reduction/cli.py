from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class DimensionalityReductionAudit:
    workflow_name: str
    scenario_name: str
    observation_count: int
    feature_count: int
    retained_components: int
    cumulative_explained_variance: float
    reconstruction_rmse: float
    dominant_component_feature: str
    preprocessing_summary: str
    validation_warning: str
    interpretation_warning: str


FEATURES = ["load", "temperature", "vibration", "pressure", "latency"]

DATA = [
    [80.0, 31.0, 0.42, 101.0, 14.0],
    [82.0, 32.0, 0.45, 100.0, 15.0],
    [78.0, 30.0, 0.41, 102.0, 13.0],
    [95.0, 37.0, 0.62, 96.0, 22.0],
    [97.0, 38.0, 0.65, 95.0, 24.0],
    [94.0, 36.0, 0.60, 97.0, 21.0],
    [70.0, 28.0, 0.35, 104.0, 11.0],
    [72.0, 29.0, 0.36, 103.0, 12.0],
]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*matrix)]


def standardize(matrix: list[list[float]]) -> tuple[list[list[float]], list[float], list[float]]:
    cols = transpose(matrix)
    means = [mean(col) for col in cols]
    scales = []
    for col, mu in zip(cols, means):
        variance = sum((value - mu) ** 2 for value in col) / (len(col) - 1)
        scales.append(math.sqrt(variance))
    standardized = [[(row[j] - means[j]) / scales[j] for j in range(len(row))] for row in matrix]
    return standardized, means, scales


def covariance(matrix: list[list[float]]) -> list[list[float]]:
    n = len(matrix)
    p = len(matrix[0])
    return [[sum(matrix[i][a] * matrix[i][b] for i in range(n)) / (n - 1) for b in range(p)] for a in range(p)]


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(vector: list[float]) -> float:
    return math.sqrt(dot(vector, vector))


def outer(a: list[float], b: list[float]) -> list[list[float]]:
    return [[x * y for y in b] for x in a]


def subtract_matrix(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def power_iteration(matrix: list[list[float]], iterations: int = 500) -> tuple[float, list[float]]:
    p = len(matrix)
    vector = [1.0 / math.sqrt(p) for _ in range(p)]
    for _ in range(iterations):
        nxt = matvec(matrix, vector)
        length = norm(nxt)
        if length == 0:
            break
        vector = [value / length for value in nxt]
    eigenvalue = dot(vector, matvec(matrix, vector))
    return eigenvalue, vector


def top_eigenpairs_symmetric(matrix: list[list[float]], k: int) -> list[tuple[float, list[float]]]:
    working = [row[:] for row in matrix]
    pairs = []
    for _ in range(k):
        eigenvalue, vector = power_iteration(working)
        pairs.append((eigenvalue, vector))
        working = subtract_matrix(working, [[eigenvalue * cell for cell in row] for row in outer(vector, vector)])
    return pairs


def project(matrix: list[list[float]], components: list[list[float]]) -> list[list[float]]:
    return [[dot(row, component) for component in components] for row in matrix]


def reconstruct(scores: list[list[float]], components: list[list[float]]) -> list[list[float]]:
    p = len(components[0])
    return [[sum(score[j] * components[j][feature] for j in range(len(components))) for feature in range(p)] for score in scores]


def rmse(A: list[list[float]], B: list[list[float]]) -> float:
    count = len(A) * len(A[0])
    return math.sqrt(sum((A[i][j] - B[i][j]) ** 2 for i in range(len(A)) for j in range(len(A[0]))) / count)


def build_audit() -> DimensionalityReductionAudit:
    standardized, _, _ = standardize(DATA)
    cov = covariance(standardized)
    retained = 2
    eigenpairs = top_eigenpairs_symmetric(cov, retained)
    eigenvalues = [pair[0] for pair in eigenpairs]
    components = [pair[1] for pair in eigenpairs]
    total_variance = sum(cov[i][i] for i in range(len(cov)))
    cumulative_explained = sum(eigenvalues) / total_variance

    scores = project(standardized, components)
    reconstructed = reconstruct(scores, components)
    reconstruction_error = rmse(standardized, reconstructed)

    first_component = components[0]
    dominant_index = max(range(len(FEATURES)), key=lambda i: abs(first_component[i]))

    return DimensionalityReductionAudit(
        workflow_name="dimensionality_reduction_audit",
        scenario_name="synthetic_high_dimensional_sensor_feature_matrix",
        observation_count=len(DATA),
        feature_count=len(FEATURES),
        retained_components=retained,
        cumulative_explained_variance=round(cumulative_explained, 12),
        reconstruction_rmse=round(reconstruction_error, 12),
        dominant_component_feature=FEATURES[dominant_index],
        preprocessing_summary="Features were centered and standardized before covariance-based PCA.",
        validation_warning="Component selection should be checked against reconstruction error, stability, subgroup error, rare-pattern preservation, and downstream task performance.",
        interpretation_warning="Principal components are mathematical directions of variation. They are not automatically causal factors, natural categories, or decision-ready explanations. Scaling, feature choice, missing data, leakage controls, and validation evidence must remain attached to the reduced representation.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "dimensionality_reduction_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "dimensionality_reduction_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = [
        "# Dimensionality Reduction Audit",
        "",
        f"- Workflow: {audit.workflow_name}",
        f"- Scenario: {audit.scenario_name}",
        f"- Observation count: {audit.observation_count}",
        f"- Feature count: {audit.feature_count}",
        f"- Retained components: {audit.retained_components}",
        f"- Cumulative explained variance: {audit.cumulative_explained_variance}",
        f"- Reconstruction RMSE: {audit.reconstruction_rmse}",
        f"- Dominant first-component feature: {audit.dominant_component_feature}",
        "",
        audit.preprocessing_summary,
        "",
        audit.validation_warning,
        "",
        audit.interpretation_warning,
    ]
    (output_dir / "reports" / "dimensionality_reduction_audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Dimensionality reduction audit complete.")


if __name__ == "__main__":
    main()
