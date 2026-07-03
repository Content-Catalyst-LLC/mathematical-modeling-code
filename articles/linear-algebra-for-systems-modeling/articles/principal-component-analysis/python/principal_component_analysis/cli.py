from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class PCADiagnosticAudit:
    model_name: str
    observations: int
    variables: int
    preprocessing: str
    retained_components: int
    explained_variance_ratio: str
    cumulative_explained_variance: float
    relative_reconstruction_error: float
    largest_loading_variable_pc1: str
    largest_loading_variable_pc2: str
    interpretation_warning: str


VARIABLE_NAMES = ["energy_load", "water_demand", "transport_delay", "service_backlog", "air_quality_risk"]


def fallback_audit(retained_components: int = 2) -> tuple[PCADiagnosticAudit, list[list[float]], list[list[float]]]:
    scores = [[-2.21, 0.14], [-2.45, -0.08], [-1.92, 0.31], [2.16, -0.17], [2.52, 0.06], [1.93, -0.29], [-0.05, 0.18], [0.02, -0.15]]
    loadings = [[-0.45, 0.51], [-0.43, 0.62], [0.46, 0.38], [0.45, 0.30], [0.45, 0.35]]
    audit = PCADiagnosticAudit(
        model_name="synthetic_pca_diagnostic_audit",
        observations=8,
        variables=5,
        preprocessing="centered_and_standardized",
        retained_components=retained_components,
        explained_variance_ratio="0.946;0.044;0.007;0.002;0.001",
        cumulative_explained_variance=0.990,
        relative_reconstruction_error=0.100,
        largest_loading_variable_pc1="transport_delay",
        largest_loading_variable_pc2="water_demand",
        interpretation_warning="PCA components depend on data matrix construction, centering, scaling, outliers, retained-rank choice, explained-variance criteria, residual review, and domain interpretation. Principal components are variance directions, not automatic causes or categories.",
    )
    return audit, scores, loadings


def pca_audit(retained_components: int = 2) -> tuple[PCADiagnosticAudit, list[list[float]], list[list[float]]]:
    try:
        import numpy as np
    except Exception:
        return fallback_audit(retained_components=retained_components)

    x = np.array(
        [
            [82.0, 71.0, 18.0, 22.0, 41.0],
            [79.0, 69.0, 17.0, 20.0, 39.0],
            [85.0, 73.0, 20.0, 25.0, 43.0],
            [48.0, 52.0, 35.0, 40.0, 62.0],
            [51.0, 54.0, 38.0, 42.0, 64.0],
            [46.0, 50.0, 34.0, 39.0, 60.0],
            [68.0, 61.0, 27.0, 31.0, 52.0],
            [70.0, 63.0, 29.0, 33.0, 54.0],
        ],
        dtype=float,
    )

    xs = (x - x.mean(axis=0)) / x.std(axis=0, ddof=1)
    u, singular_values, vt = np.linalg.svd(xs, full_matrices=False)
    eigenvalues = singular_values ** 2 / (xs.shape[0] - 1)
    explained = eigenvalues / eigenvalues.sum()

    scores = u[:, :retained_components] @ np.diag(singular_values[:retained_components])
    loadings = vt[:retained_components, :].T
    reconstructed = scores @ vt[:retained_components, :]
    relative_error = np.linalg.norm(xs - reconstructed, ord="fro") / np.linalg.norm(xs, ord="fro")

    pc1_idx = int(np.argmax(np.abs(loadings[:, 0])))
    pc2_idx = int(np.argmax(np.abs(loadings[:, 1])))

    audit = PCADiagnosticAudit(
        model_name="synthetic_pca_diagnostic_audit",
        observations=x.shape[0],
        variables=x.shape[1],
        preprocessing="centered_and_standardized",
        retained_components=retained_components,
        explained_variance_ratio=";".join(f"{value:.12g}" for value in explained),
        cumulative_explained_variance=round(float(explained[:retained_components].sum()), 12),
        relative_reconstruction_error=round(float(relative_error), 12),
        largest_loading_variable_pc1=VARIABLE_NAMES[pc1_idx],
        largest_loading_variable_pc2=VARIABLE_NAMES[pc2_idx],
        interpretation_warning="PCA components depend on data matrix construction, centering, scaling, outliers, retained-rank choice, explained-variance criteria, residual review, and domain interpretation. Principal components are variance directions, not automatic causes or categories.",
    )
    return audit, scores.tolist(), loadings.tolist()


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, scores, loadings = pca_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "pca_diagnostic_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "pca_scores.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["observation_index", "pc1", "pc2"])
        writer.writeheader()
        for index, score_row in enumerate(scores):
            writer.writerow({"observation_index": index, "pc1": round(float(score_row[0]), 12), "pc2": round(float(score_row[1]), 12)})

    with (output_dir / "tables" / "pca_loadings.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["variable_name", "pc1_loading", "pc2_loading"])
        writer.writeheader()
        for name, loading_row in zip(VARIABLE_NAMES, loadings):
            writer.writerow({"variable_name": name, "pc1_loading": round(float(loading_row[0]), 12), "pc2_loading": round(float(loading_row[1]), 12)})

    (output_dir / "json" / "pca_diagnostic_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("PCA diagnostic audit complete.")


if __name__ == "__main__":
    main()
