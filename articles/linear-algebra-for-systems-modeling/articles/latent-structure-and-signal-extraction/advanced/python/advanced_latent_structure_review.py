from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedLatentStructureReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedLatentStructureReview]:
    return [
        AdvancedLatentStructureReview("observed_matrix", "required", "Define observations, variables, measurements, units, weights, and missing-data handling."),
        AdvancedLatentStructureReview("preprocessing", "required", "Document centering, scaling, normalization, transformations, filtering, and weighting."),
        AdvancedLatentStructureReview("method_choice", "required", "State whether extraction uses SVD, PCA, factor models, NMF, ICA, embeddings, or another method."),
        AdvancedLatentStructureReview("rank_or_dimension", "required", "Report retained rank, component count, factor count, latent dimension, and sensitivity tests."),
        AdvancedLatentStructureReview("signal_definition", "required", "Explain why retained components are treated as signal."),
        AdvancedLatentStructureReview("residual_review", "required", "Report reconstruction error, residual norms, anomaly scores, and localized residual patterns."),
        AdvancedLatentStructureReview("stability_validation", "required", "Validate across preprocessing, samples, time windows, subgroups, rank choices, and seeds."),
        AdvancedLatentStructureReview("responsible_interpretation", "required", "Treat latent components as inferred model artifacts, not causes, categories, proxies, or complete truths."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_latent_structure_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_latent_structure_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Latent Structure and Signal Extraction Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_latent_structure_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced latent structure review complete.")


if __name__ == "__main__":
    main()
