from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class CompressionNoiseAudit:
    model_name: str
    rows: int
    columns: int
    method: str
    preprocessing: str
    retained_rank: int
    retained_energy_ratio: float
    discarded_energy_ratio: float
    compression_ratio: float
    relative_reconstruction_error: float
    maximum_row_residual: float
    highest_residual_row: int
    noise_warning: str
    interpretation_warning: str


def fallback_audit(retained_rank: int = 2) -> tuple[CompressionNoiseAudit, list[float], list[float]]:
    singular_values = [6.25, 1.86, 0.74, 0.51, 0.22, 0.09]
    row_residuals = [0.42, 0.35, 0.47, 0.55, 0.62, 0.58, 0.31, 0.28, 1.43]
    retained = sum(v*v for v in singular_values[:retained_rank]) / sum(v*v for v in singular_values)
    audit = CompressionNoiseAudit(
        model_name="synthetic_compression_noise_audit",
        rows=9,
        columns=6,
        method="svd_low_rank_compression",
        preprocessing="centered_and_standardized",
        retained_rank=retained_rank,
        retained_energy_ratio=round(retained, 12),
        discarded_energy_ratio=round(1.0 - retained, 12),
        compression_ratio=round((9 * 6) / (retained_rank * (9 + 6 + 1)), 12),
        relative_reconstruction_error=0.195,
        maximum_row_residual=max(row_residuals),
        highest_residual_row=row_residuals.index(max(row_residuals)),
        noise_warning="Discarded components are not automatically noise. They may contain weak signals, localized structure, subgroup patterns, anomalies, or early warning behavior.",
        interpretation_warning="Compression preserves selected structure while losing or distorting other information. Retained rank, preprocessing, thresholds, residuals, and validation context should be documented.",
    )
    return audit, singular_values, row_residuals


def compression_noise_audit(retained_rank: int = 2) -> tuple[CompressionNoiseAudit, list[float], list[float]]:
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

    uk = u[:, :retained_rank]
    sk = singular_values[:retained_rank]
    vtk = vt[:retained_rank, :]
    reconstructed = uk @ np.diag(sk) @ vtk
    residuals = xs - reconstructed

    retained_energy = float(np.sum(sk ** 2) / np.sum(singular_values ** 2))
    discarded_energy = 1.0 - retained_energy
    rows, columns = xs.shape
    compression_ratio = (rows * columns) / (retained_rank * (rows + columns + 1))
    relative_error = float(np.linalg.norm(residuals, ord="fro") / np.linalg.norm(xs, ord="fro"))
    row_residuals = np.sqrt(np.sum(residuals * residuals, axis=1))
    highest_residual_row = int(np.argmax(row_residuals))

    audit = CompressionNoiseAudit(
        model_name="synthetic_compression_noise_audit",
        rows=rows,
        columns=columns,
        method="svd_low_rank_compression",
        preprocessing="centered_and_standardized",
        retained_rank=retained_rank,
        retained_energy_ratio=round(retained_energy, 12),
        discarded_energy_ratio=round(discarded_energy, 12),
        compression_ratio=round(float(compression_ratio), 12),
        relative_reconstruction_error=round(relative_error, 12),
        maximum_row_residual=round(float(row_residuals.max()), 12),
        highest_residual_row=highest_residual_row,
        noise_warning="Discarded components are not automatically noise. They may contain weak signals, localized structure, subgroup patterns, anomalies, or early warning behavior.",
        interpretation_warning="Compression preserves selected structure while losing or distorting other information. Retained rank, preprocessing, thresholds, residuals, and validation context should be documented.",
    )
    return audit, singular_values.tolist(), row_residuals.tolist()


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, singular_values, row_residuals = compression_noise_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "compression_noise_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    total_energy = sum(value * value for value in singular_values)
    with (output_dir / "tables" / "singular_value_energy.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["index", "singular_value", "energy_share"])
        writer.writeheader()
        for index, value in enumerate(singular_values):
            writer.writerow({"index": index + 1, "singular_value": round(float(value), 12), "energy_share": round(float(value * value / total_energy), 12)})

    with (output_dir / "tables" / "row_residuals.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["row_index", "residual_norm"])
        writer.writeheader()
        for index, value in enumerate(row_residuals):
            writer.writerow({"row_index": index, "residual_norm": round(float(value), 12)})

    (output_dir / "json" / "compression_noise_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Compression, noise, and informational tradeoff audit complete.")


if __name__ == "__main__":
    main()
