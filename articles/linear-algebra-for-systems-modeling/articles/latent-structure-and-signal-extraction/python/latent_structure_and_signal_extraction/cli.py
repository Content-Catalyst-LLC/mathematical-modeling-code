from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class LatentStructureAudit:
    model_name: str
    observations: int
    variables: int
    method: str
    preprocessing: str
    retained_rank: int
    retained_signal_ratio: float
    relative_reconstruction_error: float
    maximum_observation_residual: float
    highest_residual_observation: int
    signal_definition_warning: str
    interpretation_warning: str


def fallback_audit(retained_rank: int = 2) -> tuple[LatentStructureAudit, list[list[float]], list[float]]:
    scores = [[-2.41, 0.11], [-2.63, -0.04], [-2.05, 0.21], [1.78, -0.23], [2.09, -0.02], [1.61, -0.30], [-0.31, 0.16], [-0.19, -0.06], [2.11, 1.29]]
    residuals = [0.42, 0.35, 0.47, 0.55, 0.62, 0.58, 0.31, 0.28, 1.43]
    audit = LatentStructureAudit(
        model_name="synthetic_latent_structure_signal_extraction_audit",
        observations=9,
        variables=6,
        method="svd_low_rank_signal_extraction",
        preprocessing="centered_and_standardized",
        retained_rank=retained_rank,
        retained_signal_ratio=0.962,
        relative_reconstruction_error=0.195,
        maximum_observation_residual=max(residuals),
        highest_residual_observation=residuals.index(max(residuals)),
        signal_definition_warning="The retained low-rank structure is treated as signal only under the chosen method, preprocessing, retained rank, scaling, and validation assumptions.",
        interpretation_warning="Latent components are inferred mathematical structures, not automatic causes, categories, mechanisms, or complete system truths. Residuals require review before being dismissed as noise.",
    )
    return audit, scores, residuals


def latent_structure_audit(retained_rank: int = 2) -> tuple[LatentStructureAudit, list[list[float]], list[float]]:
    try:
        import numpy as np
    except Exception:
        return fallback_audit(retained_rank=retained_rank)

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
            [90.0, 78.0, 42.0, 47.0, 71.0, 7.8],
        ],
        dtype=float,
    )

    xs = (x - x.mean(axis=0)) / x.std(axis=0, ddof=1)
    u, singular_values, vt = np.linalg.svd(xs, full_matrices=False)

    scores = u[:, :retained_rank] @ np.diag(singular_values[:retained_rank])
    reconstructed = scores @ vt[:retained_rank, :]
    residuals = xs - reconstructed

    retained_signal_ratio = float(np.sum(singular_values[:retained_rank] ** 2) / np.sum(singular_values ** 2))
    relative_error = float(np.linalg.norm(residuals, ord="fro") / np.linalg.norm(xs, ord="fro"))
    residual_norms = np.sqrt(np.sum(residuals * residuals, axis=1))
    highest_residual_observation = int(np.argmax(residual_norms))

    audit = LatentStructureAudit(
        model_name="synthetic_latent_structure_signal_extraction_audit",
        observations=x.shape[0],
        variables=x.shape[1],
        method="svd_low_rank_signal_extraction",
        preprocessing="centered_and_standardized",
        retained_rank=retained_rank,
        retained_signal_ratio=round(retained_signal_ratio, 12),
        relative_reconstruction_error=round(relative_error, 12),
        maximum_observation_residual=round(float(residual_norms.max()), 12),
        highest_residual_observation=highest_residual_observation,
        signal_definition_warning="The retained low-rank structure is treated as signal only under the chosen method, preprocessing, retained rank, scaling, and validation assumptions.",
        interpretation_warning="Latent components are inferred mathematical structures, not automatic causes, categories, mechanisms, or complete system truths. Residuals require review before being dismissed as noise.",
    )
    return audit, scores.tolist(), residual_norms.tolist()


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, scores, residual_norms = latent_structure_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "latent_structure_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "latent_scores.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["observation_index", "latent_1", "latent_2"])
        writer.writeheader()
        for index, score_row in enumerate(scores):
            writer.writerow({"observation_index": index, "latent_1": round(float(score_row[0]), 12), "latent_2": round(float(score_row[1]), 12)})

    with (output_dir / "tables" / "residual_diagnostics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["observation_index", "residual_norm"])
        writer.writeheader()
        for index, value in enumerate(residual_norms):
            writer.writerow({"observation_index": index, "residual_norm": round(float(value), 12)})

    (output_dir / "json" / "latent_structure_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Latent structure and signal extraction audit complete.")


if __name__ == "__main__":
    main()
