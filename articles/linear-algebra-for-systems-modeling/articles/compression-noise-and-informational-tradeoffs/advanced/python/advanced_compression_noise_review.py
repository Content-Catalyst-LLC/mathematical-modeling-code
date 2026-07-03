from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedCompressionNoiseReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedCompressionNoiseReview]:
    return [
        AdvancedCompressionNoiseReview("original_representation", "required", "Define the original matrix, signal, feature table, image, field, or state representation."),
        AdvancedCompressionNoiseReview("preprocessing", "required", "Document centering, scaling, normalization, transformations, filtering, and weighting."),
        AdvancedCompressionNoiseReview("compression_method", "required", "State the compression method and what structure it is intended to preserve."),
        AdvancedCompressionNoiseReview("retained_rank", "required", "Report retained rank, threshold choice, retained energy, discarded energy, and sensitivity tests."),
        AdvancedCompressionNoiseReview("noise_definition", "required", "Justify which variation is treated as noise or discardable residual."),
        AdvancedCompressionNoiseReview("reconstruction_error", "required", "Report aggregate reconstruction error and localized residuals."),
        AdvancedCompressionNoiseReview("weak_signal_review", "required", "Examine discarded components, rare cases, localized residuals, and early warning signals."),
        AdvancedCompressionNoiseReview("responsible_simplification", "required", "Validate compressed representation against purpose, consequences, and accountability needs."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_compression_noise_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_compression_noise_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Compression, Noise, and Informational Tradeoffs Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_compression_noise_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced compression and noise review complete.")


if __name__ == "__main__":
    main()
