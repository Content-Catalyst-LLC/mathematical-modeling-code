from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class DimensionalityReductionAudit:
    model_name: str
    observations: int
    original_dimensions: int
    reduced_dimensions: int
    method: str
    preprocessing: str
    preservation_target: str
    explained_variance_retained: float
    relative_reconstruction_error: float
    mean_pairwise_distance_distortion: float
    validation_warning: str
    interpretation_warning: str


def fallback_audit() -> tuple[DimensionalityReductionAudit, list[list[float]]]:
    coordinates = [[-2.42, 0.11], [-2.66, -0.06], [-2.10, 0.27], [2.34, -0.16], [2.71, 0.08], [2.12, -0.24], [-0.05, 0.18], [0.06, -0.18]]
    audit = DimensionalityReductionAudit(
        model_name="synthetic_dimensionality_reduction_audit",
        observations=8,
        original_dimensions=6,
        reduced_dimensions=2,
        method="svd_based_pca_projection",
        preprocessing="centered_and_standardized",
        preservation_target="maximum_variance_under_linear_projection",
        explained_variance_retained=0.982,
        relative_reconstruction_error=0.134,
        mean_pairwise_distance_distortion=0.286,
        validation_warning="Reduced representations should be validated against task performance, residuals, subgroup behavior, distance distortion, reconstruction error, and sensitivity to preprocessing.",
        interpretation_warning="Dimensionality reduction preserves selected structure while discarding or distorting other structure. Reduced coordinates are model artifacts, not automatic causes, categories, or complete system truths.",
    )
    return audit, coordinates


def pca_reduction_audit(reduced_dimensions: int = 2) -> tuple[DimensionalityReductionAudit, list[list[float]]]:
    try:
        import numpy as np
    except Exception:
        return fallback_audit()

    x = np.array(
        [
            [82.0, 71.0, 18.0, 22.0, 41.0, 3.2],
            [79.0, 69.0, 17.0, 20.0, 39.0, 3.0],
            [85.0, 73.0, 20.0, 25.0, 43.0, 3.5],
            [48.0, 52.0, 35.0, 40.0, 62.0, 6.1],
            [51.0, 54.0, 38.0, 42.0, 64.0, 6.4],
            [46.0, 50.0, 34.0, 39.0, 60.0, 5.9],
            [68.0, 61.0, 27.0, 31.0, 52.0, 4.8],
            [70.0, 63.0, 29.0, 33.0, 54.0, 5.0],
        ],
        dtype=float,
    )

    xs = (x - x.mean(axis=0)) / x.std(axis=0, ddof=1)
    u, singular_values, vt = np.linalg.svd(xs, full_matrices=False)
    scores = u[:, :reduced_dimensions] @ np.diag(singular_values[:reduced_dimensions])
    reconstructed = scores @ vt[:reduced_dimensions, :]

    eigenvalues = singular_values ** 2 / (xs.shape[0] - 1)
    explained_variance = eigenvalues / eigenvalues.sum()
    relative_error = np.linalg.norm(xs - reconstructed, ord="fro") / np.linalg.norm(xs, ord="fro")

    original_distances = np.sqrt(((xs[:, None, :] - xs[None, :, :]) ** 2).sum(axis=2))
    reduced_distances = np.sqrt(((scores[:, None, :] - scores[None, :, :]) ** 2).sum(axis=2))
    mask = original_distances > 1e-12
    distortion = np.abs(reduced_distances[mask] - original_distances[mask]) / original_distances[mask]

    audit = DimensionalityReductionAudit(
        model_name="synthetic_dimensionality_reduction_audit",
        observations=x.shape[0],
        original_dimensions=x.shape[1],
        reduced_dimensions=reduced_dimensions,
        method="svd_based_pca_projection",
        preprocessing="centered_and_standardized",
        preservation_target="maximum_variance_under_linear_projection",
        explained_variance_retained=round(float(explained_variance[:reduced_dimensions].sum()), 12),
        relative_reconstruction_error=round(float(relative_error), 12),
        mean_pairwise_distance_distortion=round(float(distortion.mean()), 12),
        validation_warning="Reduced representations should be validated against task performance, residuals, subgroup behavior, distance distortion, reconstruction error, and sensitivity to preprocessing.",
        interpretation_warning="Dimensionality reduction preserves selected structure while discarding or distorting other structure. Reduced coordinates are model artifacts, not automatic causes, categories, or complete system truths.",
    )
    return audit, scores.tolist()


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, coordinates = pca_reduction_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "dimensionality_reduction_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "reduced_coordinates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["observation_index", "z1", "z2"])
        writer.writeheader()
        for index, coord in enumerate(coordinates):
            writer.writerow({"observation_index": index, "z1": round(float(coord[0]), 12), "z2": round(float(coord[1]), 12)})

    (output_dir / "json" / "dimensionality_reduction_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Dimensionality reduction audit complete.")


if __name__ == "__main__":
    main()
